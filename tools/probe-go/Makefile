# probe-go — build, test, selftest.
#
# One command builds it. There is no dependency fetch: the prober uses only the
# Go standard library, so a machine with Go installed and no network can build
# and test this tool. That is the strongest form of the hermeticity the bar asks
# for, and the reason there is no go.sum here: a module with no requirements has
# no sums to record.

BIN     := dist/probe-go.exe
SRC     := $(wildcard src/*.go)
GOFLAGS := -trimpath
LDFLAGS := -s -w

ifeq ($(OS),Windows_NT)
  BIN := dist/probe-go.exe
else
  BIN := dist/probe-go
endif

.PHONY: all build test selftest vet fmt bench clean size

all: build

build: $(BIN)
	@echo "built $(BIN)"
	@ls -l $(BIN) | awk '{print "size:", $$5, "bytes"}'

$(BIN): $(SRC) go.mod
	@mkdir -p dist
	go build $(GOFLAGS) -ldflags="$(LDFLAGS)" -o $(BIN) ./src/

## test: `go vet` plus the selftest. No network. This is what CI would run.
test: vet selftest
	@echo "test: ok"

selftest: $(BIN)
	./$(BIN) --selftest

vet:
	go vet ./src/

fmt:
	gofmt -l src/

size: $(BIN)
	@ls -l $(BIN)

## bench: the measurement that decides whether this tool should exist at all.
## It is not a micro-benchmark: it compares this tool against the script
## fallback over the same host list, at the same concurrency. See README.md.
bench: $(BIN)
	@echo "run scripts/probe/probe.py's fallback and this binary on one list:"
	@echo "  python bench/compare.py --modeled --hosts 250 --concurrency 8 --rtt 0.10 --rounds 3"
	@echo "the numbers recorded in README.md came from that command."

clean:
	rm -rf dist
