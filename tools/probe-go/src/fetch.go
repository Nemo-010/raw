// fetch.go — one URL, one record. Redirects followed by hand so every hop is kept,
// TLS failure separated from host failure, and the byte-level verdict recorded
// even when the status line claims success.
package main

import (
	"bytes"
	"context"
	"crypto/tls"
	"crypto/x509"
	"errors"
	"io"
	"net"
	"net/http"
	"net/url"
	"strings"
	"time"
)

// interestingHeaders are the ones a reviewer actually needs.
var interestingHeaders = map[string]bool{
	"content-type": true, "content-length": true, "content-encoding": true,
	"content-range": true, "accept-ranges": true, "location": true, "server": true,
	"etag": true, "last-modified": true, "cache-control": true, "retry-after": true,
	"www-authenticate": true, "x-amz-expires": true, "x-archive-keep-old-version": true,
	"x-web-egress": true, "x-web-provider": true, "x-reader-source": true,
	"cf-ray": true, "cf-cache-status": true,
}

var interestingPrefixes = []string{"x-web-", "x-reader-", "x-archive-", "x-proxy-", "x-amz-", "x-goog-"}

func headerSubset(h http.Header, dumpAll bool) map[string]string {
	out := map[string]string{}
	for k, vs := range h {
		lk := strings.ToLower(k)
		keep := dumpAll || interestingHeaders[lk]
		if !keep {
			for _, p := range interestingPrefixes {
				if strings.HasPrefix(lk, p) {
					keep = true
					break
				}
			}
		}
		if !keep {
			continue
		}
		v := strings.Join(vs, ", ")
		if lk == "cf-ray" {
			v = cfRay(v)
		}
		out[lk] = v
	}
	return out
}

// cfRay drops the location suffix of a cf-ray value ("8f1c2a3b4c5d6e7f-KTM" -> "8f1c2a3b4c5d6e7f"): it names the
// Cloudflare location that served the probing machine, which is that machine's network identity.
func cfRay(v string) string {
	parts := strings.Split(v, ",")
	for i, p := range parts {
		p = strings.TrimSpace(p)
		if j := strings.LastIndex(p, "-"); j > 0 && len(p)-j-1 == 3 && isUpper3(p[j+1:]) && isHex(p[:j]) {
			p = p[:j]
		}
		parts[i] = p
	}
	return strings.Join(parts, ", ")
}

func isUpper3(s string) bool {
	for _, c := range s {
		if c < 'A' || c > 'Z' {
			return false
		}
	}
	return true
}

func isHex(s string) bool {
	if s == "" {
		return false
	}
	for _, c := range s {
		if !((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f')) {
			return false
		}
	}
	return true
}

// classifyError maps a transport error onto the stable class vocabulary in
// probe.py. TLS broken is not host broken: the two classes are different
// findings and the corpus records broken chains as a finding, not a death.
func classifyError(err error) string {
	if err == nil {
		return ""
	}
	var certErr *tls.CertificateVerificationError
	if errors.As(err, &certErr) {
		return "tls_untrusted"
	}
	var cve x509.CertificateInvalidError
	if errors.As(err, &cve) {
		return "tls_untrusted"
	}
	var hostErr x509.HostnameError
	if errors.As(err, &hostErr) {
		return "tls_untrusted"
	}
	var uaErr x509.UnknownAuthorityError
	if errors.As(err, &uaErr) {
		return "tls_untrusted"
	}
	var dnsErr *net.DNSError
	if errors.As(err, &dnsErr) {
		if dnsErr.IsTimeout {
			return "timeout"
		}
		return "dns"
	}
	var opErr *net.OpError
	if errors.As(err, &opErr) {
		if opErr.Timeout() {
			return "timeout"
		}
		if opErr.Op == "dial" {
			if strings.Contains(opErr.Err.Error(), "refused") {
				return "connect_refused"
			}
			return "transport"
		}
		return "reset"
	}
	var netErr net.Error
	if errors.As(err, &netErr) && netErr.Timeout() {
		return "timeout"
	}
	if errors.Is(err, context.DeadlineExceeded) {
		return "timeout"
	}
	if errors.Is(err, io.ErrUnexpectedEOF) {
		return "truncated-body"
	}
	var recordErr tls.RecordHeaderError
	if errors.As(err, &recordErr) {
		return "tls_error"
	}
	if strings.Contains(err.Error(), "certificate") {
		return "tls_untrusted"
	}
	if strings.Contains(err.Error(), "tls:") {
		return "tls_error"
	}
	if strings.Contains(err.Error(), "connection refused") {
		return "connect_refused"
	}
	if strings.Contains(err.Error(), "reset by peer") ||
		strings.Contains(err.Error(), "EOF") {
		return "reset"
	}
	return "transport"
}

type fetchOpts struct {
	method      string
	timeout     time.Duration
	insecure    bool
	compressed  bool
	userAgent   string
	headers     []string
	rangeSpec   string
	bytesLimit  int64 // -1 = read all
	noHash      bool
	maxRedirects int
	retries    int
	tlsInfo    bool
	proxy      string
	dumpHeaders bool
	// Caller-supplied expectations. A parsed-but-unused parameter is the failure
	// §5.1 names, so these are carried here and consumed in probeOnce.
	expectSHA   string
	expectBytes *int64
}

func newClient(o fetchOpts) *http.Client {
	tlsCfg := &tls.Config{InsecureSkipVerify: o.insecure} //nolint:gosec // --insecure is the point
	tr := &http.Transport{
		TLSClientConfig:       tlsCfg,
		DisableCompression:    true, // we declare Accept-Encoding ourselves
		MaxIdleConns:          256,
		MaxIdleConnsPerHost:   4,
		IdleConnTimeout:       30 * time.Second,
		TLSHandshakeTimeout:   o.timeout,
		ExpectContinueTimeout: time.Second,
	}
	if o.proxy != "" {
		if pu, err := url.Parse(o.proxy); err == nil {
			tr.Proxy = http.ProxyURL(pu)
		}
	} else {
		tr.Proxy = nil // hermetic by default, like probe.py
	}
	return &http.Client{
		Transport: tr,
		Timeout:   o.timeout,
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse // hops are recorded by hand
		},
	}
}

func requestHeaders(o fetchOpts) map[string]string {
	h := map[string]string{
		"User-Agent":      o.userAgent,
		"Accept":          "*/*",
		"Accept-Encoding": "identity",
	}
	if o.compressed {
		h["Accept-Encoding"] = "gzip"
	}
	if o.rangeSpec != "" {
		h["Range"] = "bytes=" + o.rangeSpec
	}
	for _, raw := range o.headers {
		name, value, ok := strings.Cut(raw, ":")
		if ok {
			h[strings.TrimSpace(name)] = strings.TrimSpace(value)
		}
	}
	return h
}

// tlsProbe is a second, independent handshake. It proves the host speaks TLS when
// the verifying handshake failed, which is what separates tls_untrusted (a
// finding about the certificate) from a dead host.
func tlsProbe(rawURL string, timeout time.Duration) *TLSInfo {
	u, err := url.Parse(rawURL)
	if err != nil || u.Scheme != "https" || u.Hostname() == "" {
		return nil
	}
	port := u.Port()
	if port == "" {
		port = "443"
	}
	info := &TLSInfo{Insecure: true}
	d := &net.Dialer{Timeout: timeout}
	conn, err := tls.DialWithDialer(d, "tcp", net.JoinHostPort(u.Hostname(), port), &tls.Config{
		InsecureSkipVerify: true, //nolint:gosec // the point is to record the chain as served
		ServerName:         u.Hostname(),
	})
	if err != nil {
		info.HandshakeOK = boolptr(false)
		info.Error = classifyError(err)
		info.Detail = truncate(err.Error(), 200)
		return info
	}
	defer conn.Close()
	info.HandshakeOK = boolptr(true)
	st := conn.ConnectionState()
	info.Version = tlsVersionName(st.Version)
	if st.CipherSuite != 0 {
		info.Cipher = tls.CipherSuiteName(st.CipherSuite)
	}
	if len(st.PeerCertificates) > 0 {
		leaf := st.PeerCertificates[0]
		info.CertDERSHA256 = strptr(sha256Hex(leaf.Raw))
		info.PeerSubject = leaf.Subject.String()
		info.PeerIssuer = leaf.Issuer.String()
		info.PeerNotAfter = leaf.NotAfter.UTC().Format(time.RFC3339)
	}
	return info
}

func tlsVersionName(v uint16) string {
	switch v {
	case tls.VersionTLS10:
		return "TLSv1.0"
	case tls.VersionTLS11:
		return "TLSv1.1"
	case tls.VersionTLS12:
		return "TLSv1.2"
	case tls.VersionTLS13:
		return "TLSv1.3"
	}
	return "unknown"
}

func truncate(s string, n int) string {
	if len(s) <= n {
		return s
	}
	return s[:n]
}

// errKind gives a short, stable error label for a transport failure.
type bodyResult struct {
	data     []byte
	digest   string
	trunc    bool
	readErr  error
}

// readBody reads up to limit bytes (limit < 0 = all). hashes what it read.
func readBody(r io.Reader, limit int64, wantHash bool) bodyResult {
	var buf bytes.Buffer
	var n int64
	chunk := make([]byte, 64*1024)
	for {
		if limit >= 0 && n >= limit {
			break
		}
		want := int64(len(chunk))
		if limit >= 0 && limit-n < want {
			want = limit - n
		}
		got, err := r.Read(chunk[:want])
		if got > 0 {
			buf.Write(chunk[:got])
			n += int64(got)
		}
		if err != nil {
			if errors.Is(err, io.EOF) {
				break
			}
			res := bodyResult{data: buf.Bytes(), trunc: limit >= 0 && n == limit, readErr: err}
			if wantHash {
				res.digest = sha256Hex(buf.Bytes())
			}
			return res
		}
	}
	res := bodyResult{data: buf.Bytes(), trunc: limit >= 0 && n == limit}
	if wantHash {
		res.digest = sha256Hex(buf.Bytes())
	}
	return res
}

// probeOnce is the whole job for one URL.
func probeOnce(rawURL string, o fetchOpts, client *http.Client) *Record {
	rec := newRecord(rawURL, o.method, o.insecure)
	rec.Compressed = o.compressed
	if u, err := url.Parse(rawURL); err == nil {
		rec.Scheme = u.Scheme
	}
	if o.rangeSpec != "" {
		rec.Range = &RangeRec{Requested: o.rangeSpec}
	}

	if o.tlsInfo {
		if info := tlsProbe(rawURL, minDuration(o.timeout, 10*time.Second)); info != nil {
			applyTLS(&rec.TLS, info)
			rec.TLS.Verified = boolptr(!o.insecure)
		}
	}

	hdr := requestHeaders(o)
	cur := rawURL
	start := time.Now()
	var lastStatus *int

	for hop := 0; hop <= o.maxRedirects; hop++ {
		rec.URLsTried = append(rec.URLsTried, cur)
		var resp *http.Response
		var err error
		attempt := 0
		for {
			attempt++
			rec.Attempts++
			req, reqErr := http.NewRequest(o.method, cur, nil)
			if reqErr != nil {
				rec.Error = strptr("bad-arguments")
				rec.ErrorDetail = truncate(reqErr.Error(), 300)
				rec.ElapsedMS = msSince(start)
				rec.Integrity = "invalid-url"
				return rec
			}
			for k, v := range hdr {
				req.Header.Set(k, v)
			}
			resp, err = client.Do(req)
			if err == nil {
				break
			}
			cls := classifyError(err)
			retryable := cls == "timeout" || cls == "reset" || cls == "transport"
			if retryable && attempt <= o.retries {
				// at once: a transport error carries no Retry-After, and no delay is invented
				continue
			}
			rec.Error = strptr(cls)
			rec.ErrorDetail = truncate(err.Error(), 300)
			rec.Integrity = "unreachable"
			if cls == "tls_untrusted" || cls == "tls_error" {
				if info := tlsProbe(cur, minDuration(o.timeout, 10*time.Second)); info != nil {
					applyTLS(&rec.TLS, info)
				}
				rec.TLS.Verified = boolptr(false)
				rec.Integrity = "tls-broken"
			}
			rec.ElapsedMS = msSince(start)
			return rec
		}

		status := resp.StatusCode
		lastStatus = &status
		rec.FinalURL = cur
		rec.Status = intptr(status)
		rec.HTTPVersion = resp.Proto
		rec.HeadersSubset = headerSubset(resp.Header, o.dumpHeaders)
		if ct := resp.Header.Get("Content-Type"); ct != "" {
			first, _, _ := strings.Cut(ct, ";")
			ct = strings.TrimSpace(first)
			if ct != "" {
				rec.ContentType = strptr(ct)
			}
		}
		if cl := resp.Header.Get("Content-Length"); cl != "" {
			if n, perr := parseInt64(cl); perr == nil {
				rec.DeclaredBytes = &n
			}
		}

		loc := resp.Header.Get("Location")
		if (o.method == "GET" || o.method == "HEAD") &&
			(status == 301 || status == 302 || status == 303 || status == 307 || status == 308) &&
			loc != "" {
			newURL := resolveURL(cur, loc)
			rec.Redirects = append(rec.Redirects, Redirect{
				Status: status, Location: newURL, RawLocation: loc, From: cur,
			})
			io.CopyN(io.Discard, resp.Body, 4096)
			resp.Body.Close()
			u, perr := url.Parse(newURL)
			if perr != nil || (u.Scheme != "http" && u.Scheme != "https") {
				rec.Error = strptr("redirect-not-http")
				rec.ErrorDetail = "redirect to " + newURL
				rec.ElapsedMS = msSince(start)
				rec.Integrity = "redirect-refused"
				return rec
			}
			if hop == o.maxRedirects {
				rec.Error = strptr("too-many-redirects")
				rec.ElapsedMS = msSince(start)
				rec.Integrity = "redirect-loop"
				return rec
			}
			cur = newURL
			continue
		}

		// Retry a retryable status before giving up on it.
		if (status == 408 || status == 429 || status == 500 || status == 502 ||
			status == 503 || status == 504) && rec.Attempts <= o.retries {
			io.CopyN(io.Discard, resp.Body, 4096)
			resp.Body.Close()
			time.Sleep(retryAfter(resp.Header.Get("Retry-After")))
			continue
		}

		// Final hop: read the body.
		limit := o.bytesLimit
		if o.method == "HEAD" {
			limit = 0
		}
		wantHash := !o.noHash
		if limit == 0 {
			io.CopyN(io.Discard, resp.Body, 4096)
			resp.Body.Close()
			rec.SHA256Scope = "none"
			rec.Bytes = 0
		} else {
			br := readBody(resp.Body, limit, wantHash)
			resp.Body.Close()
			rec.Bytes = len(br.data)
			rec.Truncated = br.trunc
			if wantHash {
				rec.SHA256 = strptr(br.digest)
				rec.SHA256Scope = "full"
				if br.trunc {
					rec.SHA256Scope = "prefix"
				}
			}
			if br.readErr != nil && rec.Error == nil {
				cls := classifyError(br.readErr)
				rec.Error = strptr(cls)
				rec.ErrorDetail = truncate(br.readErr.Error(), 300)
			}
			rec.ElapsedMS = msSince(start)

			declared := rec.DeclaredBytes
			enc := rec.HeadersSubset["content-encoding"]
			hasEnc := enc != ""
			bodyText := string(br.data)
			if len(br.data) > 2_000_000 {
				bodyText = string(br.data[:2_000_000])
			}

			det, sig := detectChallenge(status, derefStr(rec.ContentType), bodyText)
			if det {
				rec.Challenge = Challenge{Detected: true, Signature: sig}
			}

			kind, ksig := detectFalse200(status, derefStr(rec.ContentType), br.data, bodyText,
				false200Body{hasContentEncoding: hasEnc, declared: declared, method: o.method})
			if kind != "" {
				rec.False200 = False200{Detected: true, Kind: strptr(kind), Signature: strptr(ksig)}
			}

			// A body shorter than Content-Length is the peer cutting the stream:
			// truncation by the peer, not by us. §5.1 and rule 1.
			if rec.Error == nil && declared != nil && !br.trunc && o.method != "HEAD" &&
				!hasEnc && int64(len(br.data)) < *declared {
				rec.Error = strptr("truncated-body")
				rec.ErrorDetail = "read " + itoa(len(br.data)) + " of " +
					strconvFormatInt(*declared) + " declared bytes"
			}

			switch {
			case rec.Error != nil && *rec.Error == "truncated-body":
				rec.Integrity = "length-mismatch"
			case rec.Challenge.Detected:
				rec.Integrity = "challenge"
			case rec.False200.Detected:
				rec.Integrity = "no-payload:" + derefStr(rec.False200.Kind)
			case rec.Error != nil:
				rec.Integrity = "error"
			case len(br.data) > 0 && wantHash && !br.trunc:
				rec.Integrity = "bytes:" + derefStr(rec.SHA256)[:12]
			default:
				rec.Integrity = "unverified"
			}

			// Caller-supplied expectations. §5.1: a parameter that is parsed and
			// unused is worse than a rejected one, because the rejection is
			// visible and this is not. These must set checks{} and must gate usable.
			if o.expectSHA != "" {
				got := strings.ToLower(derefStr(rec.SHA256))
				rec.Checks["sha256"] = Check{Expected: strings.ToLower(o.expectSHA),
					Actual: got, Match: got != "" && got == strings.ToLower(o.expectSHA)}
			}
			if o.expectBytes != nil {
				var actual interface{}
				if rec.DeclaredBytes != nil {
					actual = *rec.DeclaredBytes
				} else {
					actual = int64(rec.Bytes)
				}
				rec.Checks["bytes"] = Check{Expected: *o.expectBytes, Actual: actual,
					Match: actual == *o.expectBytes}
			}
		}
		break
	}

	if rec.Status != nil && *rec.Status >= 400 && *rec.Status < 600 && rec.Error == nil {
		rec.Error = strptr("http-" + itoa(*rec.Status))
		if rec.Integrity == "none" {
			rec.Integrity = "refused"
		}
	}

	// Range honesty: a 206 is the only answer that honoured it.
	if rec.Range != nil {
		if cr, ok := rec.HeadersSubset["content-range"]; ok {
			rec.Range.ContentRange = strptr(cr)
		}
		if rec.Status != nil {
			switch *rec.Status {
			case 206:
				// Rule 13: a 206 can name a range it does not deliver.
				if cr, ok := rec.HeadersSubset["content-range"]; ok &&
					rangeMismatch(rec.Range.Requested, cr) {
					rec.Range.Honoured = boolptr(false)
					rec.False200 = False200{Detected: true, Kind: strptr("range-mismatch"),
						Signature: strptr("206 naming " + cr + " for bytes=" + rec.Range.Requested)}
					rec.Integrity = "no-payload:range-mismatch"
				} else {
					rec.Range.Honoured = boolptr(true)
				}
			case 200, 416:
				rec.Range.Honoured = boolptr(false)
			}
		}
	}

	rec.Usable = rec.Error == nil && rec.Status != nil && *rec.Status >= 200 &&
		*rec.Status < 300 && !rec.Challenge.Detected && !rec.False200.Detected &&
		allChecksPass(rec.Checks)
	if rec.ElapsedMS == nil {
		rec.ElapsedMS = msSince(start)
	}
	if lastStatus == nil && rec.Status != nil {
		rec.Status = lastStatus
	}
	return rec
}

func derefStr(s *string) string {
	if s == nil {
		return ""
	}
	return *s
}

func resolveURL(baseURL, loc string) string {
	b, err := url.Parse(baseURL)
	if err != nil {
		return loc
	}
	l, err := url.Parse(loc)
	if err != nil {
		return loc
	}
	return b.ResolveReference(l).String()
}

func msSince(t time.Time) *float64 {
	v := float64(time.Since(t).Microseconds()) / 1000.0
	return &v
}

func minDuration(a, b time.Duration) time.Duration {
	if a < b {
		return a
	}
	return b
}

func applyTLS(dst *TLSInfo, src *TLSInfo) {
	*dst = *src
}

// retryAfter is the only pause before a retry: the server's own Retry-After in seconds, whatever its size, or none.
// The tool invents no delay and no ceiling (AGENTS.md section 2 rule 15).
func retryAfter(v string) time.Duration {
	if v == "" {
		return 0
	}
	if f, err := parseFloat(v); err == nil && f >= 0 {
		return time.Duration(f * float64(time.Second))
	}
	return 0
}

func allChecksPass(m map[string]Check) bool {
	for _, c := range m {
		if !c.Match {
			return false
		}
	}
	return true
}
