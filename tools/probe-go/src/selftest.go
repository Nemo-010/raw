// selftest.go — offline. A loopback HTTP server plus committed fixtures.
//
// Every case asserts which classifier fired, not merely that something failed.
// A case that passes because a fixture failed to load is the bug this repository
// already paid for once (scripts/README.md, "A --selftest case that passes because
// a fixture failed to copy is not a pass"), so each fixture case asserts the file
// is non-empty before asserting the verdict.
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net"
	"net/http"
	"os"
	"path/filepath"
	"runtime"
	"sort"
	"strings"
	"sync/atomic"
	"time"
)

type testCase struct {
	name   string
	passed bool
	detail string
}

type harness struct {
	cases   []testCase
	verbose bool
	flaky   int32
}

func (h *harness) check(name string, cond bool, detail string) {
	h.cases = append(h.cases, testCase{name, cond, detail})
	if h.verbose || !cond {
		status := "PASS"
		if !cond {
			status = "FAIL"
		}
		fmt.Fprintf(os.Stderr, "%s %s", status, name)
		if detail != "" {
			fmt.Fprintf(os.Stderr, "  %s", detail)
		}
		fmt.Fprint(os.Stderr, "\n")
	}
}

// fixtureDir finds fixtures/ next to the executable, or beside src/ when run by
// `go test`. It never invents a path silently: a missing directory is a failure.
func fixtureDir() (string, error) {
	candidates := []string{}
	if _, file, _, ok := runtime.Caller(0); ok {
		candidates = append(candidates, filepath.Join(filepath.Dir(file), "..", "fixtures"))
	}
	if exe, err := os.Executable(); err == nil {
		candidates = append(candidates, filepath.Join(filepath.Dir(exe), "..", "fixtures"))
		candidates = append(candidates, filepath.Join(filepath.Dir(exe), "fixtures"))
	}
	wd, _ := os.Getwd()
	candidates = append(candidates, filepath.Join(wd, "fixtures"))
	for _, c := range candidates {
		if st, err := os.Stat(c); err == nil && st.IsDir() {
			return filepath.Clean(c), nil
		}
	}
	return "", fmt.Errorf("fixtures/ not found (looked in %d places)", len(candidates))
}

func readFixture(dir, name string) ([]byte, error) {
	p := filepath.Join(dir, name)
	b, err := os.ReadFile(p)
	if err != nil {
		return nil, err
	}
	return b, nil
}

func selftestOpts() fetchOpts {
	return fetchOpts{
		method: "GET", timeout: 5 * time.Second, userAgent: "probe-go-selftest",
		bytesLimit: -1, maxRedirects: 10,
	}
}

func runSelftest(verbose bool) int {
	h := &harness{verbose: verbose}

	// ---- fixtures, body-side, no socket -----------------------------------
	dir, err := fixtureDir()
	if err != nil {
		fmt.Fprintf(os.Stderr, "selftest: %v\n", err)
		return 1
	}
	h.check("fixtures directory exists", err == nil, dir)

	type fixtureCase struct {
		file    string
		ctype   string
		status  int
		wantKind string
	}
	for _, fc := range []fixtureCase{
		{"empty-200.txt", "text/plain", 200, "empty"},
		{"undeclared-gzip.dat", "text/html", 200, "undeclared-gzip"},
		{"json-error-200.json", "application/json", 200, "json-error"},
		{"html-404-in-200.html", "text/html", 200, "html-error-page"},
		{"lfs-pointer.txt", "text/plain", 200, "lfs-pointer"},
		{"tiny-html.html", "text/html", 200, "tiny-html"},
		{"json-empty-200.json", "application/json", 200, "json-empty"},
		{"parked-page.html", "text/html", 200, "parked-page"},
		{"clean-body.html", "text/html", 200, ""},
		{"clean-body.json", "application/json", 200, ""},
		// A gzip payload declared as an archive is the payload, not a defect.
		// Calling it a false-200 is the inverse error and buries the real one.
		{"archive-declared-gzip.dat", "application/gzip", 200, ""},
	} {
		body, rerr := readFixture(dir, fc.file)
		h.check("fixture present: "+fc.file, rerr == nil && len(body) >= 0,
			fmt.Sprintf("%d bytes, err=%v", len(body), rerr))
		if rerr != nil {
			continue
		}
		kind, sig := detectFalse200(fc.status, fc.ctype, body, string(body),
			false200Body{method: "GET"})
		h.check("classify "+fc.file+" -> "+orEmpty(fc.wantKind), kind == fc.wantKind,
			"got kind="+orEmpty(kind)+" sig="+sig)
	}

	// ---- challenge fixtures ------------------------------------------------
	for _, cf := range []struct {
		file string
		want string
	}{
		{"challenge-cloudflare.html", "cloudflare-challenge:"},
		{"challenge-turnstile.html", "generic-captcha:"},
		{"challenge-login-wall.html", "login-wall:"},
		{"challenge-js-cookie-gate.html", "js-cookie-gate:"},
		{"challenge-zh-cn.html", "zh-cn-interstitial:"},
	} {
		body, rerr := readFixture(dir, cf.file)
		h.check("fixture present: "+cf.file, rerr == nil, fmt.Sprint(rerr))
		if rerr != nil {
			continue
		}
		det, sig := detectChallenge(200, "text/html", string(body))
		h.check("challenge "+cf.file, det && strings.HasPrefix(sig, cf.want),
			"detected="+fmt.Sprint(det)+" sig="+sig)
	}

	// A clean page must NOT be called a challenge. The false-positive direction
	// matters as much as the catch direction.
	clean, _ := readFixture(dir, "clean-body.html")
	det, sig := detectChallenge(200, "text/html", string(clean))
	h.check("clean page is not a challenge", !det, sig)

	// ---- range honesty, no socket -----------------------------------------
	h.check("range mismatch caught",
		rangeMismatch("0-1023", "bytes 1024-2047/4096") == true, "")
	h.check("range match accepted",
		rangeMismatch("1024-2047", "bytes 1024-2047/4096") == false, "")
	h.check("missing content-range is a mismatch",
		rangeMismatch("0-99", "") == true, "")

	// ---- no invented pause, and no location in a cf-ray ---------------------
	h.check("retry waits only the server's Retry-After", retryAfter("") == 0 && retryAfter("90") == 90*time.Second, "")
	h.check("cf-ray keeps the ray id, not the location",
		cfRay("8f1c2a3b4c5d6e7f-KTM") == "8f1c2a3b4c5d6e7f" && cfRay("abc") == "abc", cfRay("8f1c2a3b4c5d6e7f-KTM"))

	// ---- live cases against loopback --------------------------------------
	srv, base := startLoopback(h)
	defer srv.Close()

	o := selftestOpts()
	client := newClient(o)

	r := probeOnce(base+"/ok", o, client)
	h.check("200 usable", r.Usable && r.Status != nil && *r.Status == 200,
		"status="+derefStr(intToStrPtr(r.Status))+" err="+orEmpty(derefStr(r.Error)))

	r = probeOnce(base+"/empty", o, client)
	h.check("empty-200 caught", r.False200.Detected && derefStr(r.False200.Kind) == "empty",
		derefStr(r.False200.Kind))

	r = probeOnce(base+"/redirect", o, client)
	h.check("redirect hop recorded", len(r.Redirects) == 1 &&
		r.Redirects[0].Status == 302 && strings.HasSuffix(r.FinalURL, "/ok"),
		fmt.Sprint(r.Redirects))

	r = probeOnce(base+"/chain", o, client)
	h.check("redirect chain length", len(r.Redirects) == 2, fmt.Sprint(len(r.Redirects)))

	// Range honesty needs the range option set, or the server has nothing to honour.
	ro0 := o
	ro0.rangeSpec = "0-15"
	r = probeOnce(base+"/range", ro0, client)
	h.check("range honoured", r.Status != nil && *r.Status == 206 &&
		r.Bytes == 16 && r.Range != nil && r.Range.Honoured != nil && *r.Range.Honoured,
		fmt.Sprintf("status=%v bytes=%d", derefIntPtr(r.Status), r.Bytes))

	r = probeOnce(base+"/norange", ro0, client)
	h.check("range ignored -> honoured false", r.Status != nil && *r.Status == 200 &&
		r.Range != nil && r.Range.Honoured != nil && !*r.Range.Honoured, "")

	// Rule 13: a 206 that names a different span than requested.
	r = probeOnce(base+"/lying-range", ro0, client)
	h.check("lying 206 caught", r.False200.Detected &&
		derefStr(r.False200.Kind) == "range-mismatch", derefStr(r.False200.Kind))

	// §5.1: a gzip body with no content-encoding, over the wire.
	r = probeOnce(base+"/undeclared-gzip", o, client)
	h.check("undeclared gzip caught", r.False200.Detected &&
		derefStr(r.False200.Kind) == "undeclared-gzip", derefStr(r.False200.Kind))

	// --bytes truncates the read but keeps the truth.
	bo := o
	bo.bytesLimit = 10
	r = probeOnce(base+"/big", bo, client)
	h.check("--bytes truncation", r.Bytes == 10 && r.DeclaredBytes != nil &&
		*r.DeclaredBytes == 10240 && r.Truncated && r.SHA256Scope == "prefix",
		fmt.Sprintf("bytes=%d declared=%v scope=%s", r.Bytes,
			derefInt64Ptr(r.DeclaredBytes), r.SHA256Scope))

	// Retries.
	atomic.StoreInt32(&h.flaky, 0)
	ro := o
	ro.retries = 2
	r = probeOnce(base+"/flaky", ro, client)
	h.check("retry recovers 503", r.Status != nil && *r.Status == 200 && r.Attempts == 2,
		fmt.Sprintf("status=%v attempts=%d", derefIntPtr(r.Status), r.Attempts))

	atomic.StoreInt32(&h.flaky, 0)
	r = probeOnce(base+"/flaky", o, client)
	h.check("no retry without --retries", r.Status != nil && *r.Status == 503 &&
		derefStr(r.Error) == "http-503", fmt.Sprintf("status=%v err=%s",
		derefIntPtr(r.Status), derefStr(r.Error)))

	// Timeout classified, not reported as a dead host. The client's timeout is
	// fixed at construction, so this needs its own client.
	to := o
	to.timeout = 200 * time.Millisecond
	r = probeOnce(base+"/slow", to, newClient(to))
	h.check("timeout classified", derefStr(r.Error) == "timeout",
		"err="+orEmpty(derefStr(r.Error))+" detail="+truncate(r.ErrorDetail, 60))

	// 404 is a finding about the target.
	r = probeOnce(base+"/missing", o, client)
	h.check("404 is an error", r.Status != nil && *r.Status == 404 &&
		derefStr(r.Error) == "http-404" && !r.Usable, derefStr(r.Error))

	// Peer truncation.
	r = probeOnce(base+"/truncated", o, client)
	h.check("peer truncation caught", derefStr(r.Error) == "truncated-body", derefStr(r.Error))

	// HEAD is bodyless by contract.
	ho := o
	ho.method = "HEAD"
	r = probeOnce(base+"/ok", ho, client)
	h.check("HEAD", r.Status != nil && *r.Status == 200 && r.Bytes == 0 &&
		r.DeclaredBytes != nil && *r.DeclaredBytes == 11, "")

	// TLS broken is not host broken. The loopback TLS server has a self-signed
	// certificate, so the verifying handshake must fail with tls_untrusted and
	// --insecure must then return the body. That pair is the whole distinction.
	tlsSrv, tlsBase := startTLSLoopback()
	defer tlsSrv.Close()
	tc := newClient(o)
	r = probeOnce(tlsBase+"/ok", o, tc)
	tlsBrokenClass := derefStr(r.Error) == "tls_untrusted"
	h.check("self-signed chain -> tls_untrusted", tlsBrokenClass,
		"error="+orEmpty(derefStr(r.Error))+" detail="+truncate(r.ErrorDetail, 60))
	h.check("untrusted record is not usable", !r.Usable, "")
	io := o
	io.insecure = true
	ti := newClient(io)
	r = probeOnce(tlsBase+"/ok", io, ti)
	h.check("--insecure then reads the body", r.Usable && r.Bytes == 11,
		fmt.Sprintf("bytes=%d err=%s", r.Bytes, orEmpty(derefStr(r.Error))))

	// --tls-info records the chain even when it is untrusted.
	iio := io
	iio.tlsInfo = true
	r = probeOnce(tlsBase+"/ok", iio, newClient(iio))
	h.check("--tls-info records a handshake", r.TLS.HandshakeOK != nil && *r.TLS.HandshakeOK &&
		r.TLS.CertDERSHA256 != nil, fmt.Sprint(derefPtrBool(r.TLS.HandshakeOK)))

	// ---- classification table, no socket ----------------------------------
	h.check("classify dns",
		classifyError(&net.DNSError{Err: "no such host", Name: "x"}) == "dns", "")
	h.check("classify refused",
		classifyError(&net.OpError{Op: "dial", Err: errRefused{}}) == "connect_refused", "")

	// ---- the JSON shape a consumer depends on -----------------------------
	r = probeOnce(base+"/ok", o, client)
	blob, jerr := json.Marshal(r)
	h.check("record marshals", jerr == nil, fmt.Sprint(jerr))
	if jerr == nil {
		var m map[string]interface{}
		json.Unmarshal(blob, &m)
		required := []string{
			"url", "final_url", "method", "status", "bytes", "sha256",
			"content_type", "elapsed_ms", "redirects", "headers_subset",
			"challenge", "error", "probed_at", "usable", "declared_bytes",
			"truncated", "sha256_scope", "attempts", "urls_tried", "tls",
			"false_200", "range", "checks", "probe_version",
		}
		missing := []string{}
		for _, k := range required {
			if _, ok := m[k]; !ok {
				missing = append(missing, k)
			}
		}
		sort.Strings(missing)
		h.check("record carries probe.py's keys", len(missing) == 0,
			"missing="+strings.Join(missing, ","))
		if ch, ok := m["challenge"].(map[string]interface{}); ok {
			_, hasDet := ch["detected"]
			_, hasSig := ch["signature"]
			h.check("challenge sub-shape", hasDet && hasSig, "")
		} else {
			h.check("challenge sub-shape", false, "challenge is not an object")
		}
		if tl, ok := m["tls"].(map[string]interface{}); ok {
			_, hasIns := tl["insecure"]
			h.check("tls sub-shape", hasIns, "")
		} else {
			h.check("tls sub-shape", false, "tls is not an object")
		}
	}

	// Caller-supplied expectations must set checks{} and gate usable. A parameter
	// that is parsed and unused is the §5.1 failure this case exists to prevent.
	xo := o
	xo.expectBytes = func() *int64 { v := int64(999); return &v }()
	r = probeOnce(base+"/ok", xo, client)
	h.check("--expect-bytes mismatch fails", len(r.Checks) == 1 && !r.Usable &&
		r.Checks["bytes"].Match == false, fmt.Sprintf("checks=%v usable=%v", r.Checks, r.Usable))

	xo2 := o
	xo2.expectBytes = func() *int64 { v := int64(11); return &v }()
	r = probeOnce(base+"/ok", xo2, client)
	h.check("--expect-bytes match passes", r.Checks["bytes"].Match == true && r.Usable, "")

	xo3 := o
	xo3.expectSHA = strings.Repeat("0", 64)
	r = probeOnce(base+"/ok", xo3, client)
	h.check("--expect-sha256 mismatch fails", r.Checks["sha256"].Match == false && !r.Usable, "")

	// ---- the summary arithmetic -------------------------------------------
	okRec := probeOnce(base+"/ok", o, client)
	badRec := probeOnce(base+"/empty", o, client)
	deadRec := probeOnce(base+"/missing", o, client)
	s := summarize([]*Record{okRec, badRec, deadRec}, time.Second)
	h.check("summary counts the not-evaluable",
		s.total == 3 && s.usable == 1 && s.notEval == 2, fmt.Sprintf("%+v", s))

	failed := 0
	for _, c := range h.cases {
		if !c.passed {
			failed++
		}
	}
	fmt.Fprintf(os.Stderr, "selftest: %d passed, %d failed, %d total\n",
		len(h.cases)-failed, failed, len(h.cases))
	if failed > 0 {
		return 1
	}
	return 0
}

func orEmpty(s string) string {
	if s == "" {
		return "(none)"
	}
	return s
}

func intToStrPtr(i *int) *string {
	if i == nil {
		return nil
	}
	s := fmt.Sprint(*i)
	return &s
}

func derefIntPtr(i *int) interface{} {
	if i == nil {
		return nil
	}
	return *i
}

func derefInt64Ptr(i *int64) interface{} {
	if i == nil {
		return nil
	}
	return *i
}

func derefPtrBool(b *bool) interface{} {
	if b == nil {
		return nil
	}
	return *b
}

type errRefused struct{}

func (errRefused) Error() string { return "dial tcp: connect: connection refused" }

// ---------------------------------------------------------------- loopback --

func startLoopback(h *harness) (*http.Server, string) {
	mux := http.NewServeMux()
	send := func(w http.ResponseWriter, code int, body []byte, ctype string, extra map[string]string) {
		for k, v := range extra {
			w.Header().Set(k, v)
		}
		w.Header().Set("Content-Type", ctype)
		w.Header().Set("Content-Length", fmt.Sprint(len(body)))
		w.WriteHeader(code)
		w.Write(body)
	}

	mux.HandleFunc("/ok", func(w http.ResponseWriter, r *http.Request) {
		send(w, 200, []byte("hello world"), "text/plain", nil)
	})
	mux.HandleFunc("/empty", func(w http.ResponseWriter, r *http.Request) {
		send(w, 200, []byte(""), "text/plain", nil)
	})
	mux.HandleFunc("/redirect", func(w http.ResponseWriter, r *http.Request) {
		send(w, 302, []byte(""), "text/plain", map[string]string{"Location": "/ok"})
	})
	mux.HandleFunc("/chain", func(w http.ResponseWriter, r *http.Request) {
		send(w, 302, []byte(""), "text/plain", map[string]string{"Location": "/redirect"})
	})
	mux.HandleFunc("/range", func(w http.ResponseWriter, r *http.Request) {
		body := make([]byte, 2048)
		for i := range body {
			body[i] = byte(i % 256)
		}
		rng := r.Header.Get("Range")
		if strings.HasPrefix(rng, "bytes=") {
			var a, b int
			fmt.Sscanf(rng, "bytes=%d-%d", &a, &b)
			if b >= len(body) {
				b = len(body) - 1
			}
			chunk := body[a : b+1]
			send(w, 206, chunk, "application/octet-stream", map[string]string{
				"Content-Range":  fmt.Sprintf("bytes %d-%d/%d", a, b, len(body)),
				"Accept-Ranges":  "bytes",
			})
			return
		}
		send(w, 200, body, "application/octet-stream", map[string]string{"Accept-Ranges": "bytes"})
	})
	// Rule 13: says 206, names a span it does not deliver.
	mux.HandleFunc("/lying-range", func(w http.ResponseWriter, r *http.Request) {
		body := []byte("0123456789abcdef")
		send(w, 206, body, "application/octet-stream", map[string]string{
			"Content-Range": "bytes 4096-4111/65536",
		})
	})
	mux.HandleFunc("/norange", func(w http.ResponseWriter, r *http.Request) {
		send(w, 200, []byte(strings.Repeat("x", 2048)), "text/plain", nil)
	})
	mux.HandleFunc("/big", func(w http.ResponseWriter, r *http.Request) {
		send(w, 200, []byte(strings.Repeat("a", 10240)), "text/plain", nil)
	})
	// §5.1: gzip bytes with no content-encoding, as an edge that drops a coding
	// would deliver them.
	mux.HandleFunc("/undeclared-gzip", func(w http.ResponseWriter, r *http.Request) {
		body := []byte{0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00,
			0x00, 0x03, 0x2b, 0x49, 0x2d, 0x2e, 0x01, 0x00,
			0xc6, 0x35, 0xb9, 0x3b, 0x05, 0x00, 0x00, 0x00}
		send(w, 200, body, "text/html", nil)
	})
	mux.HandleFunc("/captcha", func(w http.ResponseWriter, r *http.Request) {
		send(w, 200, []byte(`<html><head><title>Just a moment...</title></head>`+
			`<body>checking your browser</body></html>`), "text/html", nil)
	})
	mux.HandleFunc("/jsonerr", func(w http.ResponseWriter, r *http.Request) {
		send(w, 200, []byte(`{"code":403,"message":"forbidden"}`), "application/json", nil)
	})
	mux.HandleFunc("/flaky", func(w http.ResponseWriter, r *http.Request) {
		n := atomic.AddInt32(&h.flaky, 1)
		if n == 1 {
			send(w, 503, []byte("try later"), "text/plain", nil)
			return
		}
		send(w, 200, []byte("recovered"), "text/plain", nil)
	})
	mux.HandleFunc("/slow", func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(600 * time.Millisecond)
		send(w, 200, []byte("slow"), "text/plain", nil)
	})
	mux.HandleFunc("/truncated", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/plain")
		w.Header().Set("Content-Length", "1000")
		w.WriteHeader(200)
		w.Write([]byte("short"))
		if f, ok := w.(http.Flusher); ok {
			f.Flush()
		}
		// returning without writing the declared bytes; the client sees a short read
	})
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		send(w, 404, []byte("no such route"), "text/plain", nil)
	})

	ln, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		h.check("loopback listener", false, err.Error())
		return &http.Server{}, "http://127.0.0.1:1"
	}
	srv := &http.Server{Handler: mux}
	go srv.Serve(ln)
	return srv, "http://" + ln.Addr().String()
}

func startTLSLoopback() (*http.Server, string) {
	mux := http.NewServeMux()
	mux.HandleFunc("/ok", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/plain")
		w.Header().Set("Content-Length", "11")
		w.WriteHeader(200)
		w.Write([]byte("hello world"))
	})
	ln, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		return &http.Server{}, "https://127.0.0.1:1"
	}
	srv := &http.Server{Handler: mux, TLSConfig: selfSignedTLS(),
		// The verifying handshake is *meant* to fail here; a log line saying so
		// is noise in a summary a reader scans for PASS/FAIL.
		ErrorLog: log.New(io.Discard, "", 0)}
	go srv.ServeTLS(ln, "", "")
	return srv, "https://" + ln.Addr().String()
}
