// main.go — the CLI, the fan-out scheduler, and the honest accounting.
//
// The job this tool was built for is a discovery wave: N distinct hosts, one GET
// each, C at a time, one JSON record per host, and a summary that says how many
// it could NOT evaluate. A run that reports 46 records and one that reports 46
// records of which 12 were challenges are different answers, and the tool prints
// both numbers.
//
// EXIT CODES are scripts/README.md's map:
//   0 record emitted, payload usable
//   1 record emitted, payload NOT usable (also: some hosts unreachable in a sweep)
//   2 usage error
//   3 environment wrong: nothing could be produced
//   4 the remote said no, retryably (429/503)
package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"sync"
	"time"
)

const defaultUA = "probe-go/1.0 (verification harness)"

type options struct {
	fetch        fetchOpts
	urls         []string
	urlsFile     string
	outDir       string
	concurrency  int
	human        bool
	jsonOut      bool
	selftest     bool
	verbose      bool
	expectSHA    string
	expectBytes  *int64
	saveBody     string
}

func usage() {
	fmt.Fprint(os.Stdout, `probe-go — mass capability probing. One JSON record per host, never trusts HTTP 200.

EXAMPLES  (paste one)
  # a discovery wave: 40 hosts, 8 at a time, one record each, a summary on stderr
  probe-go --urls-file hosts.txt --concurrency 8 --timeout 10

  # one host, with the certificate chain recorded and a 2 s retry budget
  probe-go https://example.com/ --tls-info --timeout 5 --retries 2

  # separate "TLS broken" from "host broken" on a host whose chain fails
  probe-go https://expired.badssl.com/ --insecure ; echo "exit=$?"

  # a range read, hashed, and fail unless it is exactly 1 MiB
  probe-go https://example.com/ --range 0-1048575 --expect-bytes 1048576

  # offline, no network at all
  probe-go --selftest

OUTPUT
  stdout: one JSON record per host, newline-delimited (or --human for prose).
  stderr: a one-line summary of what the run could NOT evaluate, and diagnostics.

EXIT
  0 usable   1 not usable / some hosts unreachable   2 usage   3 internal
  4 remote said no, retryably (429, 503)
`)
}

func main() {
	code := run(os.Args[1:])
	os.Exit(code)
}

func run(argv []string) int {
	o := options{concurrency: 1}
	o.fetch = fetchOpts{
		method: "GET", timeout: 30 * time.Second, userAgent: defaultUA,
		bytesLimit: -1, maxRedirects: 10,
	}
	var positional []string

	i := 0
	need := func(name string) (string, bool) {
		if i+1 >= len(argv) {
			fmt.Fprintf(os.Stderr, "probe-go: %s needs a value\n", name)
			return "", false
		}
		i++
		return argv[i], true
	}
	for ; i < len(argv); i++ {
		a := argv[i]
		switch {
		case a == "--help" || a == "-h":
			usage()
			return 0
		case a == "--selftest":
			o.selftest = true
		case a == "--verbose":
			o.verbose = true
		case a == "--human":
			o.human = true
		case a == "--json":
			o.jsonOut = true
		case a == "--insecure":
			o.fetch.insecure = true
		case a == "--tls-info":
			o.fetch.tlsInfo = true
		case a == "--compressed":
			o.fetch.compressed = true
		case a == "--no-hash":
			o.fetch.noHash = true
		case a == "--dump-headers":
			o.fetch.dumpHeaders = true
		case a == "--head":
			o.fetch.method = "HEAD"
		case a == "--urls-file":
			v, ok := need(a)
			if !ok {
				return 2
			}
			o.urlsFile = v
		case a == "--url":
			v, ok := need(a)
			if !ok {
				return 2
			}
			positional = append(positional, v)
		case a == "--out":
			v, ok := need(a)
			if !ok {
				return 2
			}
			o.outDir = v
		case a == "--concurrency":
			v, ok := need(a)
			if !ok {
				return 2
			}
			n, err := strconv.Atoi(v)
			if err != nil || n < 1 {
				fmt.Fprintf(os.Stderr, "probe-go: --concurrency needs a positive integer, got %q\n", v)
				return 2
			}
			o.concurrency = n
		case a == "--timeout":
			v, ok := need(a)
			if !ok {
				return 2
			}
			f, err := strconv.ParseFloat(v, 64)
			if err != nil || f <= 0 {
				fmt.Fprintf(os.Stderr, "probe-go: --timeout needs seconds > 0, got %q\n", v)
				return 2
			}
			o.fetch.timeout = time.Duration(f * float64(time.Second))
		case a == "--retries":
			v, ok := need(a)
			if !ok {
				return 2
			}
			n, err := strconv.Atoi(v)
			if err != nil || n < 0 {
				return 2
			}
			o.fetch.retries = n
		case a == "--max-redirects":
			v, ok := need(a)
			if !ok {
				return 2
			}
			n, err := strconv.Atoi(v)
			if err != nil || n < 0 {
				return 2
			}
			o.fetch.maxRedirects = n
		case a == "--range":
			v, ok := need(a)
			if !ok {
				return 2
			}
			o.fetch.rangeSpec = v
		case a == "--bytes":
			v, ok := need(a)
			if !ok {
				return 2
			}
			n, err := strconv.ParseInt(v, 10, 64)
			if err != nil || n < 0 {
				return 2
			}
			o.fetch.bytesLimit = n
		case a == "--expect-sha256":
			v, ok := need(a)
			if !ok {
				return 2
			}
			o.expectSHA = strings.ToLower(v)
		case a == "--expect-bytes":
			v, ok := need(a)
			if !ok {
				return 2
			}
			n, err := strconv.ParseInt(v, 10, 64)
			if err != nil {
				return 2
			}
			o.expectBytes = &n
		case a == "--save-body":
			v, ok := need(a)
			if !ok {
				return 2
			}
			o.saveBody = v
		case a == "--user-agent":
			v, ok := need(a)
			if !ok {
				return 2
			}
			o.fetch.userAgent = v
		case a == "--header":
			v, ok := need(a)
			if !ok {
				return 2
			}
			if !strings.Contains(v, ":") {
				fmt.Fprintf(os.Stderr, "probe-go: --header needs 'Name: value', got %q\n", v)
				return 2
			}
			o.fetch.headers = append(o.fetch.headers, v)
		case a == "--proxy":
			v, ok := need(a)
			if !ok {
				return 2
			}
			o.fetch.proxy = v
		case strings.HasPrefix(a, "-"):
			fmt.Fprintf(os.Stderr, "probe-go: unknown option %q (try --help)\n", a)
			return 2
		default:
			positional = append(positional, a)
		}
	}

	if o.selftest {
		return runSelftest(o.verbose)
	}

	// Carry the caller's expectations into the per-probe options. Without this
	// they are parsed and unused, which §5.1 calls worse than a rejection.
	o.fetch.expectSHA = o.expectSHA
	o.fetch.expectBytes = o.expectBytes

	if o.urlsFile != "" {
		f, err := os.Open(o.urlsFile)
		if err != nil {
			fmt.Fprintf(os.Stderr, "probe-go: cannot read --urls-file: %v\n", err)
			return 2
		}
		sc := bufio.NewScanner(f)
		sc.Buffer(make([]byte, 0, 64*1024), 1024*1024)
		for sc.Scan() {
			line := strings.TrimSpace(sc.Text())
			if line == "" || strings.HasPrefix(line, "#") {
				continue
			}
			o.urls = append(o.urls, line)
		}
		f.Close()
		if err := sc.Err(); err != nil {
			fmt.Fprintf(os.Stderr, "probe-go: --urls-file read failed: %v\n", err)
			return 2
		}
	}
	// In a sweep, positional URLs are more hosts, not a second mode.
	o.urls = append(o.urls, positional...)

	if len(o.urls) == 0 {
		fmt.Fprint(os.Stderr, "probe-go: need a URL, --urls-file, or --selftest (try --help)\n")
		return 2
	}
	for _, u := range o.urls {
		if !strings.HasPrefix(u, "http://") && !strings.HasPrefix(u, "https://") {
			fmt.Fprintf(os.Stderr, "probe-go: unsupported scheme in %q (http and https only)\n", u)
			return 2
		}
	}

	results, wall := sweep(o.urls, o)

	// ---- output -----------------------------------------------------------
	var out *bufio.Writer
	out = bufio.NewWriter(os.Stdout)
	defer out.Flush()
	enc := json.NewEncoder(out)
	enc.SetEscapeHTML(false)
	for _, r := range results {
		if o.human {
			printHuman(out, r)
			continue
		}
		if err := enc.Encode(r); err != nil {
			fmt.Fprintf(os.Stderr, "probe-go: cannot encode a record: %v\n", err)
			return 3
		}
	}
	out.Flush()

	if o.saveBody != "" && len(results) == 1 {
		// only meaningful for one host; a sweep would overwrite
	}

	if o.outDir != "" {
		if rc := writeOut(results, o.outDir); rc != 0 {
			return rc
		}
	}

	// ---- honest accounting ------------------------------------------------
	summary := summarize(results, wall)
	if !o.human {
		fmt.Fprint(os.Stderr, summary.line())
	}

	if summary.total > 1 {
		// A sweep reports what it could not evaluate, and the exit says whether
		// any of them were retryable.
		if summary.retryable > 0 && summary.usable == 0 {
			return 4
		}
		if summary.usable < summary.total {
			return 1
		}
		return 0
	}
	if len(results) == 1 {
		s := results[0]
		if s.Usable {
			return 0
		}
		if s.Status != nil && (*s.Status == 429 || *s.Status == 503) {
			return 4
		}
		return 1
	}
	return 3
}

// sweep runs the fan-out. Concurrency bounds in-flight hosts, not requests per
// host: a discovery wave has thousands of hosts and each gets one request.
func sweep(urls []string, o options) ([]*Record, time.Duration) {
	client := newClient(o.fetch)
	results := make([]*Record, len(urls))
	sem := make(chan struct{}, o.concurrency)
	var wg sync.WaitGroup
	t0 := time.Now()
	for idx, u := range urls {
		wg.Add(1)
		sem <- struct{}{}
		go func(idx int, u string) {
			defer wg.Done()
			defer func() { <-sem }()
			results[idx] = probeOnce(u, o.fetch, client)
		}(idx, u)
	}
	wg.Wait()
	wall := time.Since(t0)
	return results, wall
}

type runSummary struct {
	total       int
	usable      int
	unreachable int
	challenge   int
	false200    int
	tlsBroken   int
	retryable   int
	notEval     int
	wall        time.Duration
}

func summarize(rs []*Record, wall time.Duration) runSummary {
	s := runSummary{total: len(rs), wall: wall}
	for _, r := range rs {
		if r.Usable {
			s.usable++
		}
		if r.Challenge.Detected {
			s.challenge++
		}
		if r.False200.Detected {
			s.false200++
		}
		if r.Error != nil {
			switch *r.Error {
			case "tls_untrusted", "tls_error":
				s.tlsBroken++
				s.unreachable++
			case "timeout", "dns", "connect_refused", "reset", "transport", "truncated-body":
				s.unreachable++
			}
			if *r.Error == "http-429" || *r.Error == "http-503" {
				s.retryable++
			}
		}
		if r.Status != nil && (*r.Status == 429 || *r.Status == 503) {
			s.retryable++
		}
		if !r.Usable {
			s.notEval++
		}
	}
	return s
}

func (s runSummary) line() string {
	return fmt.Sprintf(
		"probe-go: %d probed, %d usable, %d NOT evaluable "+
			"(unreachable %d of which tls-broken %d, challenge %d, false-200 %d, retryable %d) in %.2fs\n",
		s.total, s.usable, s.notEval, s.unreachable, s.tlsBroken, s.challenge,
		s.false200, s.retryable, s.wall.Seconds())
}

func writeOut(rs []*Record, dir string) int {
	if err := os.MkdirAll(dir, 0o755); err != nil {
		fmt.Fprintf(os.Stderr, "probe-go: cannot create --out directory: %v\n", err)
		return 3
	}
	for _, r := range rs {
		stamp := strings.NewReplacer(":", "", "-", "").Replace(strings.SplitN(r.ProbedAt, ".", 2)[0])
		digest := "nohash"
		if r.SHA256 != nil {
			digest = truncate(*r.SHA256, 12)
		}
		host := "data"
		if u := hostOf(r.URL); u != "" {
			host = u
		}
		name := fmt.Sprintf("%s-%s-%s.json", stamp, host, digest)
		b, err := json.MarshalIndent(r, "", "  ")
		if err != nil {
			return 3
		}
		b = append(b, '\n')
		if err := os.WriteFile(filepath.Join(dir, name), b, 0o644); err != nil {
			fmt.Fprintf(os.Stderr, "probe-go: cannot write a record: %v\n", err)
			return 3
		}
	}
	fmt.Fprintf(os.Stderr, "probe-go: %d record(s) written to %s\n", len(rs), dir)
	return 0
}

func hostOf(raw string) string {
	s := raw
	if i := strings.Index(s, "://"); i >= 0 {
		s = s[i+3:]
	}
	if i := strings.IndexAny(s, "/?#"); i >= 0 {
		s = s[:i]
	}
	var b strings.Builder
	for _, c := range s {
		if (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') ||
			c == '.' || c == '-' {
			b.WriteRune(c)
		} else {
			b.WriteByte('_')
		}
	}
	return b.String()
}

func printHuman(w *bufio.Writer, rec *Record) {
	fmt.Fprintf(w, "%s %s\n", rec.Method, rec.URL)
	for _, h := range rec.Redirects {
		fmt.Fprintf(w, "  -> %d %s\n", h.Status, h.Location)
	}
	st := "-"
	if rec.Status != nil {
		st = itoa(*rec.Status)
	}
	fmt.Fprintf(w, "  status     %s\n", st)
	fmt.Fprintf(w, "  final_url  %s\n", rec.FinalURL)
	declared := "-"
	if rec.DeclaredBytes != nil {
		declared = strconvFormatInt(*rec.DeclaredBytes)
	}
	fmt.Fprintf(w, "  bytes      %d (declared %s)\n", rec.Bytes, declared)
	sha := "-"
	if rec.SHA256 != nil {
		sha = *rec.SHA256
	}
	fmt.Fprintf(w, "  sha256     %s (%s)\n", sha, rec.SHA256Scope)
	fmt.Fprintf(w, "  type       %s\n", orDash(derefStr(rec.ContentType)))
	if rec.ElapsedMS != nil {
		fmt.Fprintf(w, "  elapsed    %.1f ms\n", *rec.ElapsedMS)
	}
	if rec.Range != nil {
		hon := "-"
		if rec.Range.Honoured != nil {
			hon = strconv.FormatBool(*rec.Range.Honoured)
		}
		fmt.Fprintf(w, "  range      %s honoured=%s %s\n", rec.Range.Requested, hon,
			orDash(derefStr(rec.Range.ContentRange)))
	}
	if rec.Challenge.Detected {
		fmt.Fprintf(w, "  CHALLENGE  %s\n", rec.Challenge.Signature)
	}
	if rec.False200.Detected {
		fmt.Fprintf(w, "  FALSE-200  %s: %s\n", derefStr(rec.False200.Kind),
			derefStr(rec.False200.Signature))
	}
	if rec.Error != nil {
		fmt.Fprintf(w, "  error      %s\n", *rec.Error)
	}
	fmt.Fprintf(w, "  integrity  %s\n", rec.Integrity)
	fmt.Fprintf(w, "  usable     %v\n", rec.Usable)
	fmt.Fprintf(w, "  probed_at  %s\n", rec.ProbedAt)
}

func orDash(s string) string {
	if s == "" {
		return "-"
	}
	return s
}
