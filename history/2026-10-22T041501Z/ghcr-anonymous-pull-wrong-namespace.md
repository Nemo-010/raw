# A `measured` claim that GHCR issues no anonymous pull tokens was a probe of a repository that does not exist

- **When:** 2026-10-22T04:15:01Z
- **Status:** corrected
- **Supersedes:** `dossier/ci-cd-runners/ghcr.json` (`evidence`, `confidence`, `confidence_note`, `reliability_note`), `docs/ci-cd-runners/free/registries-and-cache.md` §GitHub Packages and GHCR, §Docker Hub, the comparison table and §What did not work
- **Superseded by:** `dossier/ci-cd-runners/ghcr.json` as corrected, and `docs/ci-cd-runners/free/registries-and-cache.md`
- **Evidence:** three GHCR anonymous token requests and manifest fetches run from this machine on 2026-10-22, saved under `.tmp/work/fx-db-dns-ci/probe-ghcr/`
- **Confidence:** measured

## What we believed

"GHCR does not issue anonymous pull tokens. A request to
`https://ghcr.io/token?scope=repository:library/hello-world:pull` returned **403**" with
`{"errors":[{"code":"DENIED","message":"requested access to the resource is denied"}]}`. The record
carried the `measured` rung on the strength of that 403, and the document built an asymmetry on it:
Docker Hub base images are free to pull and GHCR ones are not, so the build chain's scarce link was
"pulled anonymously".

## What we found

GHCR issues anonymous pull tokens for any public package. `library/` is Docker Hub's namespace and
does not exist on `ghcr.io`, so the 403 was a 404-shaped answer about the path and not a statement
about anonymity.

Re-run on 2026-10-22, three public packages:

```bash
curl -s "https://ghcr.io/token?scope=repository:catthehacker/ubuntu:pull&service=ghcr.io"
# 200, 69 bytes: a token JSON body
curl -s -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.oci.image.index.v1+json" \
  "https://ghcr.io/v2/catthehacker/ubuntu/manifests/act-latest"
# 200, 754 bytes, schemaVersion 2, application/vnd.oci.image.index.v1+json
```

`actions/actions-runner` returned 200 with a 73-byte token and a 1,609-byte manifest.
`homebrew/core/hello` returned 200 with a 69-byte token and a 9,610-byte manifest at tag `2.12.3`.
The control, `library/hello-world`, returned 403 with 86 bytes every time, which is why the error
was invisible: the writer's own control was the thing under test and it was the wrong resource.

Digests of the saved responses, so the next session can check this claim rather than trust it:
token `e26b35c1dc64bf51b6e02f5a20f7d7fbf436a944d445155e8fc313a42ec3a808`, manifest
`62d572b92f9f32d3427b6d220ad1f9dca9c7b6ffad37d295425037dbff78abaf`.

## How we found it

An adversarial review named the namespace error. Re-running the probe from this machine reproduced
the reviewer's result exactly: three for three on public packages, and the control still 403.

## What it cost us

A fabricated constraint, and it was in the one place the corpus treats as unimpeachable. A `measured`
label ends the argument: a reader does not check a measurement, they act on it. The asymmetry it
produced said that Docker Hub base images are free and GHCR ones are not, which is false; it also
made the build chain's "scarce link" the wrong link, because a public GHCR image costs the puller
nothing and needs no identity either.

The storage claim the record exists for was never in doubt and is unchanged: 500 MB of private
storage shared with Packages and Actions artifacts.

## What a future session should do differently

**A control proves the instrument, not the subject.** `library/hello-world` is a Docker Hub
namespace; using it as a GHCR control tests that GHCR does not have Docker Hub's namespace, which
nobody doubted. The probe needed one real public package in the scope and one nonexistent one, and
it had only the nonexistent one.

**Record the request, not just the answer.** The saved token and manifest files under
`.tmp/work/fx-db-dns-ci/probe-ghcr/` are what let this entry be checked. The original record kept a
status code and a byte count, which a wrong path produces just as readily as a right one.

**A `measured` negative needs a positive control in the same scope.** "X does not happen" is the
easiest claim to get wrong from a misaddressed request, and it is the claim a reader is least able
to falsify.
