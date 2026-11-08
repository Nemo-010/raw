// util.go — small parsing wrappers, kept in one place so the call sites read as prose.
package main

import (
	"strconv"
	"strings"
)

func parseInt64(s string) (int64, error) {
	return strconv.ParseInt(strings.TrimSpace(s), 10, 64)
}

func parseFloat(s string) (float64, error) {
	return strconv.ParseFloat(strings.TrimSpace(s), 64)
}

func strconvFormatInt(i int64) string {
	return strconv.FormatInt(i, 10)
}
