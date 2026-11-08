// detect.go — the two refusals that wear a 200.
//
// This file is the port of probe.py's detect_challenge and detect_false_200, plus
// the three shapes METHODOLOGY.md §5.1 adds that probe.py does not classify:
// an undeclared gzip body, a read longer than Content-Length, and a 206 whose
// Content-Range names a span it did not deliver (rule 13).
//
// The record shape is unchanged: the extra shapes are new values of
// false_200.kind, never a new key.
package main

import (
	"encoding/json"
	"strconv"
	"strings"
)

// A challenge is a refusal wearing a status: record it and try the next route (METHODOLOGY.md section 7).
var challengeSignatures = []struct {
	name    string
	needles []string
}{
	{"cloudflare-challenge", []string{
		"just a moment...", "just a moment…", "checking your browser",
		"attention required! | cloudflare", "enable javascript and cookies to continue",
		"cf-challenge", "cf_chl_opt", "cf_chl_prog", "/cdn-cgi/challenge-platform",
	}},
	{"datadome", []string{"datadome", "captcha-delivery.com", "geo.captcha-delivery.com"}},
	{"perimeterx", []string{"px-captcha", "_pxhd", "perimeterx", "px-block"}},
	{"akamai-bot-manager", []string{"_abck", "akamai bot manager", "ak_bmsc"}},
	{"imperva-incapsula", []string{"incapsula", "_incap_ses", "request unsuccessful. incapsula"}},
	{"aws-waf", []string{"awswaf", "aws waf", "aws-waf-token"}},
	{"ddos-guard", []string{"ddos-guard", "ddos guard", "checking your browser before accessing"}},
	{"sucuri", []string{"sucuri_cloudproxy", "sucuri website firewall"}},
	{"generic-captcha", []string{"g-recaptcha", "hcaptcha.com", "recaptcha/api.js", "cf-turnstile"}},
	{"human-verification", []string{
		"verify you are human", "human verification", "prove you are human",
		"are you a robot", "complete the security check",
	}},
	// The corpus learned this population is Chinese-language. probe-alist.sh
	// greps these five and auto-discovery.md names 人机验证 as a required needle.
	{"zh-cn-interstitial", []string{
		"人机验证", "请稍候", "安全验证", "访问验证", "滑动验证", "人机身份验证",
	}},
}

// jsCookieGate detects the gate that is neither a captcha nor a page: a 200 with
// <title>Loading...</title> and a location.replace() carrying a JWT in `ch=` or
// `js=`. Measured on alist.advanced360.top 2026-10-22 (probe-alist.sh:86).
// It is checked before the signature table because its body contains no needle.
func jsCookieGate(bodyText string) (bool, string) {
	low := strings.ToLower(bodyText)
	if len(low) > 8000 {
		low = low[:8000]
	}
	for _, call := range []string{"window.location.replace", "window.location.href",
		"location.replace(", "location.href="} {
		i := strings.Index(low, call)
		if i < 0 {
			continue
		}
		tail := low[i:]
		if len(tail) > 400 {
			tail = tail[:400]
		}
		for _, marker := range []string{"?ch=", "&ch=", "?js=", "&js="} {
			if strings.Contains(tail, marker) {
				return true, "js-cookie-gate:" + call + marker
			}
		}
	}
	return false, ""
}

var loginTitleMarkers = []string{
	"sign in", "log in", "login", "sign-in", "log-in", "authentication required",
}

// titleOf returns the lowercased contents of the first <title> in html.
func titleOf(html string) string {
	if len(html) > 20000 {
		html = html[:20000]
	}
	low := strings.ToLower(html)
	i := strings.Index(low, "<title")
	if i < 0 {
		return ""
	}
	j := strings.Index(low[i:], ">")
	if j < 0 {
		return ""
	}
	j += i
	k := strings.Index(low[j:], "</title>")
	if k < 0 {
		return ""
	}
	return strings.TrimSpace(low[j+1 : j+k])
}

// detectChallenge returns (detected, signature). It never fires on a large
// healthy document: a title match is trusted, a body match only on a refusal
// status or a small body.
func detectChallenge(status int, contentType, bodyText string) (bool, string) {
	if bodyText == "" {
		return false, ""
	}
	if len(bodyText) > 60000 {
		// Only the head is scanned; a challenge page is short by construction.
	}
	low := strings.ToLower(bodyText)
	title := titleOf(bodyText)
	isHTML := strings.Contains(strings.ToLower(contentType), "html") ||
		strings.Contains(safeHead(low, 2000), "<html")

	// The JS-cookie gate first: its body carries no signature word at all.
	if isHTML && len(bodyText) < 60000 {
		if gate, sig := jsCookieGate(bodyText); gate {
			return true, sig
		}
	}

	if isHTML && title != "" {
		for _, sig := range challengeSignatures {
			for _, n := range sig.needles {
				if strings.Contains(title, n) {
					return true, sig.name + ":title:" + n
				}
			}
		}
	}

	trustedStatus := map[int]bool{401: true, 403: true, 407: true, 429: true,
		503: true, 520: true, 521: true, 522: true, 523: true, 524: true, 530: true}[status]
	small := len(bodyText) < 60000
	if trustedStatus || small {
		for _, sig := range challengeSignatures {
			for _, n := range sig.needles {
				if strings.Contains(low, n) {
					return true, sig.name + ":" + n
				}
			}
		}
	}

	// A login wall is a different refusal: credentials, not a captcha.
	if isHTML && small && (strings.Contains(low, `type="password"`) ||
		strings.Contains(low, `type='password'`) || strings.Contains(low, "type=password")) {
		for _, m := range loginTitleMarkers {
			if strings.Contains(title, m) || strings.Contains(safeHead(low, 4000), m) {
				return true, "login-wall:" + m
			}
		}
	}
	return false, ""
}

func safeHead(s string, n int) string {
	if len(s) < n {
		return s
	}
	return s[:n]
}

var errorJSONKeys = []string{"error", "errors", "message", "detail", "reason"}

// false200Body is the body-side half of the check, split out so --selftest can
// drive it from committed fixtures without a socket.
type false200Body struct {
	hasContentEncoding bool
	declared           *int64
	method             string
}

// detectFalse200 returns (kind, signature) or ("", ""). A 2xx that carries no
// payload is the rule that cost the most waves: 200 is a status, not a result.
func detectFalse200(status int, contentType string, body []byte, bodyText string,
	f false200Body) (string, string) {
	if status < 200 || status > 299 {
		return "", ""
	}
	if status == 204 || status == 205 || f.method == "HEAD" {
		return "", ""
	}
	n := len(body)
	if n == 0 {
		return "empty", "status " + strconv.Itoa(status) + " with a 0-byte body"
	}

	// §5.1: a 200 whose first two bytes are 1f8b is a gzip body with no
	// content-encoding, because an edge can drop a coding the client never
	// declared. Declaring Accept-Encoding: identity is what makes this visible.
	//
	// It is only a defect on a resource that should have been text: a .crate,
	// .tgz or application/gzip body is an archive and legitimately starts 1f8b.
	// Calling that a false-200 is the inverse error, and it buries the real one.
	if !f.hasContentEncoding && n >= 2 && body[0] == 0x1f && body[1] == 0x8b &&
		textualContentType(contentType) {
		return "undeclared-gzip", "status " + strconv.Itoa(status) +
			" with a gzip body and no content-encoding"
	}

	// Rule 10: a resolve/ that returns a pointer instead of the object.
	if strings.HasPrefix(string(safeHeadB(body, 60)), "version https://git-lfs") && n < 1024 {
		return "lfs-pointer", "git-lfs pointer, " + strconv.Itoa(n) + " bytes"
	}

	// §5.1: a length that contradicts Content-Length. Under-delivery is the
	// truncated-body error class (established vocabulary); a body that is
	// LONGER than declared is this one. Byte identity is the point.
	if f.declared != nil && !f.hasContentEncoding && int64(n) > *f.declared {
		return "length-mismatch", "read " + strconv.Itoa(n) + " bytes, declared " +
			strconv.FormatInt(*f.declared, 10)
	}

	ctype := strings.ToLower(contentType)
	low := strings.ToLower(bodyText)
	isJSON := strings.Contains(ctype, "json") || strings.HasPrefix(bodyText, "{") ||
		strings.HasPrefix(bodyText, "[")

	if isJSON {
		var v interface{}
		if err := json.Unmarshal(body, &v); err == nil {
			if obj, ok := v.(map[string]interface{}); ok {
				if code, ok := numAsInt(obj["code"]); ok && code >= 400 {
					return "json-error", "200 with {\"code\": " + strconv.Itoa(code) + "}"
				}
				for _, k := range []string{"success", "ok"} {
					if b, ok := obj[k].(bool); ok && !b {
						return "json-error", "200 with \"" + k + "\": false"
					}
				}
				if s, ok := obj["status"].(string); ok {
					ls := strings.ToLower(s)
					if ls == "error" || ls == "failed" || ls == "fail" {
						return "json-error", "200 with status: \"" + s + "\""
					}
				}
				for _, k := range errorJSONKeys {
					v, present := obj[k]
					if !present || v == nil {
						continue
					}
					switch v.(type) {
					case string, map[string]interface{}, []interface{}:
					default:
						continue
					}
					if isEmptyJSONValue(v) {
						continue
					}
					code, hasCode := numAsInt(obj["code"])
					if k == "error" || (hasCode && code >= 400) {
						return "json-error", "200 with a truthy \"" + k + "\" member"
					}
				}
			}
			if arr, ok := v.([]interface{}); ok && len(arr) == 0 && n < 200 {
				return "json-empty", "200 with an empty JSON array"
			}
		}
	}

	if strings.Contains(ctype, "html") || strings.Contains(safeHead(low, 500), "<html") {
		if n < 30000 {
			for _, pair := range [][2]string{
				{"404 not found", "html-error-page"},
				{"page not found", "html-error-page"},
				{"file not found", "html-error-page"},
				{"this page could not be found", "html-error-page"},
				{"the page you requested could not be found", "html-error-page"},
				{"account suspended", "host-error-page"},
				{"domain is parked", "parked-page"},
				{"site not found", "host-error-page"},
				{"502 bad gateway", "host-error-page"},
				{"service unavailable", "host-error-page"},
			} {
				if strings.Contains(low, pair[0]) {
					return pair[1], "200 with \"" + pair[0] + "\""
				}
			}
		}
		if n < 128 {
			return "tiny-html", "200 with a " + strconv.Itoa(n) + "-byte HTML body"
		}
	}
	return "", ""
}

func isEmptyJSONValue(v interface{}) bool {
	switch t := v.(type) {
	case string:
		return t == ""
	case []interface{}:
		return len(t) == 0
	case map[string]interface{}:
		return len(t) == 0
	}
	return false
}

func numAsInt(v interface{}) (int, bool) {
	switch t := v.(type) {
	case float64:
		return int(t), true
	case json.Number:
		i, err := t.Int64()
		return int(i), err == nil
	}
	return 0, false
}

func safeHeadB(b []byte, n int) []byte {
	if len(b) < n {
		return b
	}
	return b[:n]
}

// textualContentType is the set of types where a gzip body is a defect rather
// than the payload. An absent Content-Type is treated as textual, because the
// corpus's failure shape is an HTML error page with no type header at all.
func textualContentType(ct string) bool {
	c := strings.ToLower(ct)
	if c == "" {
		return true
	}
	for _, archive := range []string{"gzip", "x-gzip", "x-tar", "x-compressed",
		"x-7z-compressed", "zip", "x-bzip", "zstd", "x-xz", "octet-stream"} {
		if strings.Contains(c, archive) {
			return false
		}
	}
	return true
}

// rangeMismatch reports whether a 206's Content-Range names a span other than
// the one requested. Rule 13: a 206 can name a range it does not deliver.
func rangeMismatch(requested, contentRange string) bool {
	if contentRange == "" {
		return true
	}
	a, _, ok := strings.Cut(requested, "-")
	if !ok {
		return false
	}
	start, err := strconv.ParseInt(strings.TrimSpace(a), 10, 64)
	if err != nil {
		return false
	}
	// Content-Range: bytes <start>-<end>/<size>
	rest := strings.TrimSpace(contentRange)
	if !strings.HasPrefix(strings.ToLower(rest), "bytes ") {
		return true
	}
	rest = strings.TrimSpace(rest[len("bytes "):])
	span, _, ok := strings.Cut(rest, "/")
	if !ok {
		return true
	}
	gotStart, _, ok := strings.Cut(span, "-")
	if !ok {
		return true
	}
	gs, err := strconv.ParseInt(strings.TrimSpace(gotStart), 10, 64)
	if err != nil {
		return true
	}
	return gs != start
}
