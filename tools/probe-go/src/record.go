// record.go — the JSON record, byte-shape compatible with probe.py's.
//
// Every base key probe.py emits is present with the same name and the same JSON
// type, so a reader (or render.py) cannot tell which program produced a record
// except by `probe_version` and `tool`. Key order follows probe.py's insertion
// order, because records are read by humans as often as by jq.
package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"strconv"
	"time"
)

const probeVersion = "1.0.0-go.1"

type Challenge struct {
	Detected  bool   `json:"detected"`
	Signature string `json:"signature"`
}

type False200 struct {
	Detected  bool    `json:"detected"`
	Kind      *string `json:"kind"`
	Signature *string `json:"signature"`
}

type Redirect struct {
	Status      int    `json:"status"`
	Location    string `json:"location"`
	RawLocation string `json:"raw_location"`
	From        string `json:"from"`
}

type TLSInfo struct {
	Insecure        bool    `json:"insecure"`
	HandshakeOK     *bool   `json:"handshake_ok,omitempty"`
	Version         string  `json:"tls_version,omitempty"`
	Cipher          string  `json:"cipher,omitempty"`
	CertDERSHA256   *string `json:"cert_der_sha256,omitempty"`
	Error           string  `json:"error,omitempty"`
	Detail          string  `json:"detail,omitempty"`
	Verified        *bool   `json:"verified,omitempty"`
	VerifyCode      *int    `json:"verify_code,omitempty"`
	VerifyMessage   *string `json:"verify_message,omitempty"`
	PeerSubject     string  `json:"peer_subject,omitempty"`
	PeerNotAfter    string  `json:"peer_not_after,omitempty"`
	PeerIssuer      string  `json:"peer_issuer,omitempty"`
}

type RangeRec struct {
	Requested    string  `json:"requested"`
	Honoured     *bool   `json:"honoured"`
	ContentRange *string `json:"content_range"`
}

type Check struct {
	Expected interface{} `json:"expected"`
	Actual   interface{} `json:"actual"`
	Match    bool        `json:"match"`
}

// Record is one probe. The first block is probe.py's stable base; the second is
// its documented extras; the third is what this tool adds and labels as its own.
type Record struct {
	URL          string            `json:"url"`
	FinalURL     string            `json:"final_url"`
	Method       string            `json:"method"`
	Status       *int              `json:"status"`
	Bytes        int               `json:"bytes"`
	SHA256       *string           `json:"sha256"`
	ContentType  *string           `json:"content_type"`
	ElapsedMS    *float64          `json:"elapsed_ms"`
	Redirects    []Redirect        `json:"redirects"`
	HeadersSubset map[string]string `json:"headers_subset"`
	Challenge    Challenge         `json:"challenge"`
	Error        *string           `json:"error"`
	ProbedAt     string            `json:"probed_at"`

	ProbeVersion  string    `json:"probe_version"`
	Tool          string    `json:"tool"`
	Usable        bool      `json:"usable"`
	DeclaredBytes *int64    `json:"declared_bytes"`
	Truncated     bool      `json:"truncated"`
	SHA256Scope   string    `json:"sha256_scope"`
	TTFBMS        *float64  `json:"ttfb_ms"`
	Attempts      int       `json:"attempts"`
	URLsTried     []string  `json:"urls_tried"`
	TLS           TLSInfo   `json:"tls"`
	False200      False200  `json:"false_200"`
	Range         *RangeRec `json:"range"`
	Checks        map[string]Check `json:"checks"`

	// This tool's additions. A reader that ignores them sees a probe.py record.
	ErrorDetail string  `json:"error_detail,omitempty"`
	Scheme      string  `json:"scheme"`
	HTTPVersion string  `json:"http_version,omitempty"`
	Compressed  bool    `json:"compressed"`
	// Integrity names the byte-level verdict separately from the status, so a
	// summary can count "answered" and "verifiable" apart.
	Integrity string `json:"integrity"`
}

func newRecord(url, method string, insecure bool) *Record {
	return &Record{
		URL:           url,
		FinalURL:      url,
		Method:        method,
		Bytes:         0,
		Redirects:     []Redirect{},
		HeadersSubset: map[string]string{},
		Challenge:     Challenge{},
		ProbedAt:      isoNow(),
		ProbeVersion:  probeVersion,
		Tool:          "probe-go",
		SHA256Scope:   "none",
		URLsTried:     []string{},
		TLS:           TLSInfo{Insecure: insecure},
		False200:      False200{},
		Checks:        map[string]Check{},
		Integrity:     "none",
	}
}

func isoNow() string {
	t := time.Now().UTC()
	return t.Format("2006-01-02T15:04:05.") + fmt.Sprintf("%03dZ", t.Nanosecond()/1e6)
}

func strptr(s string) *string { return &s }
func intptr(i int) *int       { return &i }
func boolptr(b bool) *bool    { return &b }
func f64ptr(f float64) *float64 { return &f }

func sha256Hex(b []byte) string {
	h := sha256.Sum256(b)
	return hex.EncodeToString(h[:])
}

func itoa(i int) string { return strconv.Itoa(i) }
