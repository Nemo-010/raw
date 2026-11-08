# Which self-hosted runner removes the per-job cap?

Every cap in this topic belongs to a hosted runner and not to the software. Three CI systems are
free to self-host, and attaching one to a free control plane replaces a 6-hour or a 10-minute
clock with the uptime of a machine you rent. Then the VM is the cost and the CI system is only a
scheduler.

⛔ **Self-hosting is the last resort**: a runner the reader installs and runs, also on a rented
or free VM, comes after every hosted lane of this topic and is never the answer while a hosted
lane exists. Buying a machine is out of scope.

## The comparison

Sorted by how much of the vendor's cap the self-hosted path removes.

| system | licence | cap from the software | control plane | verdict |
| --- | --- | --- | --- | --- |
| Woodpecker CI (self-hosted) | Apache-2.0 | none | yours, or Codeberg's hosted instance | qualifies |
| Forgejo Actions (self-hosted) | GPL | none | yours, or Codeberg's alpha instance | qualifies |
| Gitea Actions (self-hosted) | MIT | none | yours | qualifies |
| Drone CI (self-hosted) | Apache-2.0 community edition | none | none: no hosted product remains | paid-only |

## The numbers that change

GitHub's limits page states both limits in adjacent rows: **6 hours** per job on a GitHub-hosted
runner and **5 days** per job on a self-hosted one. That is a 20-fold extension from attaching a
machine, before any other change.

Woodpecker and Forgejo impose no job clock at all. The limit becomes the machine's memory, its
disk and its own uptime.

The one cap that survives is the **256-job matrix per workflow run**, which the GitHub limits page
states applies "to both GitHub-hosted and self-hosted runners". A self-hosted runner does not buy
you a wider matrix.

`Evidence:` `docs.github.com/en/actions/reference/limits` (read 2026-10-22): the 6-hour hosted and
5-day self-hosted job limits, and the 256-job matrix limit applying to both.

`Verdict:` the route that removes every per-job cap in this topic, and the route that makes the
cost a machine.

## Woodpecker CI

Woodpecker is Apache-2.0, has a server and agents, and Codeberg runs a public instance of it in
production. A workflow is a `.woodpecker.yml` and an agent can run on any host with Docker, podman
or a local backend.

The property that matters is that a self-hosted agent attached to Codeberg's hosted server removes
Codeberg's 2, 5 and 10-minute caps, because the cap belongs to the runner and not to the server.
That is documented on Codeberg's own CI page: "Woodpecker enables users and organizations to add
their own agents for running workflows. This is recommended for resource-intensive tasks."

`Evidence:` `woodpecker-ci.org/docs/intro` (read 2026-10-22): the Apache-2.0 engine with a server
and agents. `docs.codeberg.org/ci/` (read 2026-10-22): self-hosted agents are recommended for
resource-intensive tasks and Codeberg's hosted instance is Woodpecker.

`Verdict:` qualifies. The free CI system whose caps are entirely on the machine.

## Forgejo and Gitea Actions

Forgejo is GPL and Gitea is MIT, and both implement a GitHub-Actions-compatible workflow with
documented differences. Codeberg's hosted runners use `ghcr.io/catthehacker/ubuntu:act-latest` "to
provide a certain compatibility level with GitHub Actions", and Docker-in-Docker is not officially
supported on them, though building images with podman is.

The compatibility is the value and the subset is the cost. A workflow that depends on a GitHub-only
action does not move without an edit, and that is the price of removing the clock.

`Evidence:` `forgejo.org/docs/latest/user/actions/` (read 2026-10-22): the compatibility and its
documented differences. `codeberg.org/actions/meta` (read 2026-10-22): the default act image and the
Docker-in-Docker limitation.

`Verdict:` qualifies. Actions syntax without GitHub, on a machine that has no job clock.

## Drone CI

There is no hosted Drone product left. The community edition is self-hostable and Woodpecker is the
maintained fork of the same design. A search for "Drone free tier" should land on Woodpecker.

`Evidence:` `woodpecker-ci.org/docs/intro` (read 2026-10-22): Woodpecker presents itself as the
community continuation of the Drone design.

`Verdict:` paid-only as a service. The self-hosted fork, Woodpecker, is the last resort, after every hosted
lane.

## What it costs

The software is free and the machine is not. That is the whole trade and this topic does not price
the machine, because the compute topic does. What this topic can say is which cap it removes: on
GitHub, 6 hours becomes 5 days; on Codeberg, 10 minutes becomes no clock; on Woodpecker, there was
never a clock once the agent was yours.

The second cost is operational: a self-hosted runner is a machine that must stay up, be patched,
and hold the credentials the builds need. A hosted runner is destroyed after the job and that is a
security property as well as a limit.

## What did not work

- **A self-hosted runner to widen a matrix**: 256 jobs per workflow run applies to both hosted and
  self-hosted runners (`documented`, `docs.github.com/en/actions/reference/limits`).
- **Codeberg's hosted runners as a long-job venue**: 2, 5 and 10 minutes per job, and attaching
  your own agent is the documented fix (`documented`, `docs.codeberg.org/ci/`).
- **Drone as a hosted service**, above: no hosted product remains (`documented`,
  `woodpecker-ci.org/docs/intro`).
- **GitHub Actions syntax on Forgejo without edits**: a documented subset, so a GitHub-only action
  does not run (`documented`, `forgejo.org/docs/latest/user/actions/`).
- **Docker-in-Docker on Codeberg's hosted runners**: not officially supported; podman is the
  documented route for image builds (`documented`, `codeberg.org/actions/meta`).

## Chaining

**A free control plane plus a free machine.** `GitHub Actions` or `Codeberg CI` as the scheduler,
with a self-hosted agent on a free VM. The scarce link is the VM, and that is the compute topic's
question.

**Woodpecker as a private CI on a paid host.** `Woodpecker` on a small always-on machine gives a
private pipeline with no cap and no public repository. The scarce link is the machine's monthly
cost, which is the smallest number in this whole topic once it replaces a minute pool.
