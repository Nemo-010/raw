# Serving your own weights on a free machine, and the boundary with the compute topic

Self-hosting is the last resort, after every hosted endpoint of this topic.

Self-hosting moves the cost from tokens to time. A model on a free GPU costs nothing
per request and costs a session clock, a cold start and an idle reap. For a workload
that runs continuously that is a worse trade than any paid endpoint. For a workload
that runs in bursts with a fixed model it gives an OpenAI-compatible endpoint with no
quota of its own, at the cost of running the server yourself.

This document owns one thing only: **how to turn a free machine into an endpoint, and
what the endpoint looks like from a client.** The machine itself, its hours and the
clock that reaps it belong to [`../../compute/`](../../compute/README.md), and the
numbers below link there rather than restating them.

If self-hosting is used at all: Kaggle's 30 GPU hours a week is the largest recurring
free GPU that survives being scripted, and it is a notebook rather than a server, so the
endpoint exists only while the notebook runs (`documented` by the compute topic; the serving
shim below is not measured here).

## The comparison

Sorted by how long the endpoint stays up once started. `Serves from` names the
process, not the host, because the host's numbers are the compute topic's.

| Host | Free GPU | Endpoint lifetime | Serves from | Identity | Verdict |
| --- | --- | --- | --- | --- | --- |
| Kaggle Notebooks | 30 GPU hours a week | one session, 60-minute idle timeout | llama.cpp or vLLM in the notebook | any-phone | qualifies-with-caveat |
| Google Colab | unpublished | 12 hours maximum, conditional | llama.cpp or vLLM in the notebook | email | trial-only |
| Lightning AI | 80 GPU hours to start, then a free CPU Studio | 24/7 on CPU, restarted every 4 hours | any server in the Studio | email | qualifies-with-caveat |
| Hugging Face Spaces | ZeroGPU, a daily quota | while the Space runs | any server in a Docker Space | email | qualifies-with-caveat |
| Oracle Cloud Always Free | no GPU | 24/7 on 2 OCPU and 12 GB | llama.cpp on CPU | card | qualifies-with-caveat |

## What the endpoint looks like

Every engine in this class ships an OpenAI-compatible route, so a caller sees the
same shape as a hosted endpoint and the code that calls a paid API does not change:

```bash
# llama.cpp, on whatever machine the notebook or VM is
llama-server -m model.gguf --host 0.0.0.0 --port 8080 -c 8192
curl -sS http://HOST:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"local","messages":[{"role":"user","content":"Reply with the token NEEDLE-7Q4Z and nothing else."}],"max_tokens":256}'
```

The `model` field is ignored by most single-model servers, so a client that compares
the echoed model against the requested one will see a mismatch and must be told that
this endpoint has one model. That is the same check that catches a relay in
[`proxy-of-a-quota.md`](proxy-of-a-quota.md), and here the mismatch is expected rather
than a finding.

## Kaggle

Kaggle gives 30 GPU hours a week on a single P100 with a 60-minute idle timeout, and
the identity it wants is a phone number (`documented` in the compute topic,
[`../../compute/free/gpu-notebooks.md`](../../compute/free/gpu-notebooks.md)).

For serving, the constraint is the idle timeout rather than the weekly hours. A
notebook that nobody touches is stopped after an hour, so the endpoint's real
lifetime is bounded by interactive activity and not by the 30 hours. A scheduled job
that wakes the notebook costs a session start and a model load, which for a 7B model
is minutes rather than seconds.

The 30 hours a week is 4.3 hours a day, which at one session a day is a single
four-hour window. That is enough to serve a batch and not enough to serve a service.

## Colab

Colab publishes no limits, states that the card types vary, and gives a 12-hour
maximum session that is described as conditional (`documented` in the compute topic).
The compute topic's own conclusion applies here without change: a documented absence
of limits is a discretionary throttle, and there is no number to plan against.

For serving that means the endpoint's lifetime is unknown before it starts, which is
worse than a short known one.

## Lightning AI

Lightning gives a free CPU Studio that stays up, restarted every four hours, and 80
GPU hours to start with no card (`documented` in the compute topic,
[`../../compute/free/always-on-free.md`](../../compute/free/always-on-free.md)).

For a small model on CPU it is the only host here whose endpoint is up without
interactive activity, and the four-hour restart is the clock to design around: a
caller needs to retry through a restart, and a long generation that crosses one is
lost.

## Oracle Cloud Always Free

Oracle's Always Free tier gives 2 OCPU, 12 GB of memory and 200 GB of block storage,
with no GPU and a card and phone at signup (`documented` in the compute topic). It is
not an inference host in the sense the others are, and it is listed because it is the
only 24/7 machine in this corpus that a reader can obtain.

A 7B model at four-bit quantization fits in 12 GB and runs on 2 cores at a few tokens
a second, which is slower than any free hosted endpoint in
[`keyless-anonymous.md`](keyless-anonymous.md) and faster than nothing. The
seven-day idle reclaim is the constraint that binds, not the CPU.

## What did not work

- **A free GPU as a server.** Every GPU host in this class either reaps an idle
  session or restarts on a clock. None of them gives a free GPU that stays up for a
  month.
- **Serving from a notebook without a keep-alive.** The 60-minute Kaggle timeout and
  Colab's 12-hour maximum both arrive while the caller is not watching.
- **Counting the GPU hours as request capacity.** 30 hours a week is a machine-time
  allowance; what it serves depends on the model, the quantization and the batch,
  none of which the host meters.

## Chaining

Self-hosting is the bottom of the stack: it never dies the way a keyless endpoint
does, it needs no vendor's permission, and it is slower and less available than
anything else here. It comes after every endpoint in this topic: use the hosted
endpoints first, and serve your own weights on a free or rented machine only for what
no hosted endpoint gives.
