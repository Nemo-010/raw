# The free lane: what costs nothing, and what it charges instead

Free storage is not a smaller version of paid storage. It is a
different mechanism with a different failure. A paid box fails on the invoice. A free
tier fails on a clock, a gate, or a decision made by one person in another timezone.
This page states the shape of the free lane, then the four Tier-1
entries whose quotas are real and unreachable, then the ranking by what a reader can
obtain today. The 22 documents beside it carry the providers.

## The argument in one page

No free provider in this corpus gives 20 TiB to one account. The largest single free
allocation found is Cloudflare Pages at 47.68 TiB per account, and it is reachable
only through a constraint: 100 projects x 20,000 files x 25 MiB, so
the mean object must be at least 10.49 MiB. The second largest set is the pooled
education tenant at 100 TB, and it needs an institution.

So the free lane is a composition, and the composition has four jobs.

| job | provider | ceiling | what it costs instead |
|---|---|---|---|
| cold archive | Cloudflare Pages | 47.68 TiB per account | write-once, no ranged reads, mean object at least 10.49 MiB |
| hot working set | ModelScope, HF storage buckets | "no storage limits" (vendor claim), 100 GB private | an undisclosed commit throttle on the write path |
| serving, 500 GB to 1 TiB every day | GitHub Releases behind a Worker | no total cap, no bandwidth cap, 2 GiB per asset | a token cache is mandatory; a 2 GiB asset exceeds the 512 MB CDN cache object cap |
| zero-account replica | BigFile.net | 256 GB per object | 365-day sliding retention, no index, and the manifest is held only by the uploader |

Each row is a different kind of promise. Pages is a published product commitment with
no ratio and no cap. ModelScope's is a vendor sentence with no egress policy and an
enforced write throttle the vendor declines to publish. GitHub's is a contractual
bandwidth statement with a discretionary clause attached. BigFile.net's is a fact with
no account behind it at all, which is why it works and why nothing can be restored if
the manifest is lost.

The failure each one is likely to meet, in the order it is likely to arrive:

- The archive fails on **file size**, not on quota. An archive of 1 MiB objects needs
  10.5 accounts, not 1, and the fix is a `tar` step, not another provider.
- The hot tier fails on the **write path**. A 10 TiB initial upload of 25 MiB shards is
  419,000 files, and one-file-per-commit is precisely the pattern ModelScope's throttle is
  tuned against.
- The serving tier fails at **request one** if the Worker mints a token per client
  request, and at the first asset over 512 MB if it tries to cache the body.
- The replica fails on **recovery**, because there is no account to enumerate.

## Tier 1, ranked by reachability

The column that decides everything is identity, not quota.

| rank | provider | quota | identity | the catch |
|---|---|---|---|---|
| 1 | Cloudflare Pages | 47.68 TiB per account | email | write-once, 25 MiB per file, mean 10.49 MiB, no ranges |
| 2 | Borealis | no quota object on the collection | email, affiliation free text | 2.5 GB per file, terms reserve removal |
| 3 | Zenodo | 50 GB per record, unlimited records, 150 GB pool | email | write-once, 30-day edit window |
| 4 | Internet Archive | 1 TB per item, unlimited items | email | about 145 GB per day per IP |
| 5 | Harvard Dataverse | 1 TiB per collection where an admin set one | email | new collections support-gated |
| 6 | RepOD | "not to exceed 2 TB" per dataset, advisory | email, self-serve | 5 GB per file, ranged reads conditional |
| 7 | `pan.moe` | 1 TB, permanent | email | single operator |
| 8 | Ploud | 1 TB, Nextcloud 31 | any-phone | single operator |
| 9 | 1yunpan | 500 GB | email | 1 TB per month egress |
| 10 | M365 A1 education | 100 TB pooled per tenant | education tenant | quotas falling |
| 11 | HDX | no published quota | email plus a reviewed organisation | editorial gate |

## Four Tier-1 entries that are unreachable

These four appear near the top of any size-ordered table, and a reader cannot
obtain any of them. Their figures are real and worth zero here.

| provider | quota | what blocks it |
|---|---|---|
| CSC Allas | 10 TiB per project, default | Haka or Virtu login, or a home organisation with a CSC contract (`fails-identity`) |
| LUMI-O | 150 TB per LUMI project, default | a LUMI or EuroHPC project allocation (`fails-identity`) |
| Open Storage Network | 1 to 50 TB of S3 per allocation, 10 TB minimum | a US NSF ACCESS allocation |
| CNB | 64 GB per asset | a WeChat identity |

Both Finnish endpoints answer an anonymous bucket-list request, which is the fact that
makes them look open: `GET https://a3s.fi/` returned 200 with
`<ListAllMyBucketsResult><Owner><ID>anonymous</ID>` in 214 bytes on 2026-10-22
(`measured`: 200, 214 B). The endpoint is live and the quota is real. The registration is the
question, and it is closed.

The heuristic that finds this class quickly: read the deposit help page for the phrase
"outside institution". It separates the repositories that take an email address from
the federated ones that take a Shibboleth identity, and it is the only test that
matters on an academic repository.

## Tier 2, usable today

Zero-friction providers, ordered by the size of the object they accept, because the
per-object cap is what sets the shard size.

| provider | ceiling | per object | identity | rung |
|---|---|---|---|---|
| GitHub Releases | no total cap, about 1.95 TiB per release | 2 GiB | email | `documented` |
| BigFile.net | no account, no quota | 256 GB | anonymous | `documented` |
| axfc | no total cap | 128 GiB | anonymous | `documented` |
| Ollama registry | none published | 39.6 GiB in the library namespace | email to push | `documented` |
| `pan.moe` | 1 TB | not published | email | `reported`, no record |
| misskey.gg | 1 TiB per user | 250 MiB | email | `documented` |
| GigaFile | 300 GB per file, unlimited count | 300 GB | anonymous | `reported` |
| 1fichier | 5 TB, temporary | 300 GB | email | `documented` |
| Ctfile | 5 TB | 20 GB | email, form read only | `documented` |

The rung in each row is the `confidence` on that provider's record, not a mark for the
row. None of these is `measured`: no record in this topic carries that rung. What the
pages establish is the offer, and an offer read off a vendor page is `documented`.
`pan.moe` has no record under any spelling, so its row is `reported` and says so.

Two of these are traps that look like finds. misskey.gg reports `maxFileSizeMb` 1024
in one field and `maxFileSize` 262,144,000 bytes in another, and the second is the one
enforced, so a 1 TiB drive takes 4,096 uploads at 250 MiB. Ollama's 455 GiB figure
belongs to a different namespace than the one `library/` exposes; the largest layer
resolved in `library/` was 42,520,398,528 bytes.

## What the free lane is not

It is not durable. Every provider in the four-job composition is one policy change
from being wrong, and three of them are one operator's decision. It is not fast enough
to be a working set without parallel reads: Zenodo's per-connection throttle makes a
single sequential download a 50x underuse of the link.

And it is not a substitute for the cheapest possible storage, which is a disk somebody
already owns. ⛔ That option is out of scope here, because the corpus assumes no local
hardware, so the floor is the cheapest **managed** capacity: EUR 1.69 per TB per month on
a 100 Mbps port, EUR 2.03 on a 20 TB box with unlimited traffic. Those carry an invoice, a
retention policy and a vendor who can close an account, and that is the real price of
not owning anything.

## The documents

| document | the question it answers |
|---|---|
| [`cloud-tenants.md`](cloud-tenants.md) | what a Google, Microsoft, education or nonprofit tenant gives |
| [`academic.md`](academic.md) | which open-science repository accepts a deposit |
| [`academic-identity.md`](academic-identity.md) | why identical software answers differently at two institutions |
| [`research-clouds.md`](research-clouds.md) | which national research cloud a foreign individual can join |
| [`cloudflare-edge.md`](cloudflare-edge.md) | can a CDN be a store |
| [`anonymous-hosts.md`](anonymous-hosts.md) | what accepts bytes with no account |
| [`ephemeral-hosts.md`](ephemeral-hosts.md) | which host holds a large object, and for how long |
| [`registries.md`](registries.md) | which registry accepts an arbitrary blob |
| [`forge-surfaces.md`](forge-surfaces.md) | what a code forge stores besides code |
| [`relays-and-transports.md`](relays-and-transports.md) | which transport moves bytes without a meter |
| [`transfer-services.md`](transfer-services.md) | why a transfer service is not storage |
| [`messaging.md`](messaging.md) | what a chat platform's attachment store holds |
| [`social-and-fediverse.md`](social-and-fediverse.md) | what an instance or a social platform gives a user |
| [`media-and-archives.md`](media-and-archives.md) | what survives ingest byte for byte |
| [`models-and-media.md`](models-and-media.md) | which model hub accepts one huge blob |
| [`odd-substrates.md`](odd-substrates.md) | which non-storage service holds bytes, and what that costs |
| [`government-portals.md`](government-portals.md) | can an individual publish to a government portal |
| [`baselines.md`](baselines.md) | what Hugging Face, ModelScope and GHCR offer |
| [`sharding.md`](sharding.md) | what per-object ceiling sets the shard size |
| [`host-economics.md`](host-economics.md) | how a free host pays for the disk |
