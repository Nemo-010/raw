# Models and media hubs: which hub accepts one huge blob

A model hub is the only free service class that is built to accept a single object of tens or
hundreds of gigabytes, because a model checkpoint is exactly that. That makes it the most
useful class in this topic for a shard plan, and the least useful for a corpus, because a hub's
storage is a catalogue rather than a filesystem.

This document covers 13 qualifying records: the Hugging Face competitors, the ML
platforms with dataset storage, and the model hubs with a per-object cap in the tens of
gigabytes. 18 were rejected.

## The comparison

Sorted by the per-object cap where one is published, and by repository total where it is not.

| provider | free ceiling | binding constraint | identity | verdict |
|---|---|---|---|---|
| Baidu AI Studio (aistudio.baidu.com)... | Two separate pools, which is the interesting part: (1) Notebook persistent workspace... | per-object-cap: 50 GB per file | national-id | qualifies-with-caveat |
| Modelers (modelers.cn, Huawei/Ascend ecosystem)... | Not published. The community is an explicit Hugging-Face-shaped hub, models, datasets... | - | country-phone | qualifies-with-caveat |
| OpenCSG (CSGHub SaaS, opencsg.com / hub.opencsg.com)... | No published byte quota anywhere in the docs... | pull-count: limit observed | any-phone | qualifies-with-caveat |
| OpenDataLab (opendatalab.com / opendatalab.org.cn) | Not published. What is documented is capability rather than quota: the dataset center... | - | country-phone | qualifies-with-caveat |
| OpenXLab (Shanghai AI Lab)... | Not published, and this is the honest finding... | - | national-id | qualifies-with-caveat |
| DagsHub (DagsHub Storage + DVC remote) | 20 GB of DagsHub Storage on the free Individual plan... | - | - | qualifies-with-caveat |
| Kaggle dataset quota-request program... | Not a fixed number: Kaggle staff grant additional per-dataset storage quota on request... | - | - | qualifies-with-caveat |
| Kaggle Datasets (public) | 200 GB per dataset (hard, public or private), 50 top-level files per dataset... | per-object-cap: 200 GB/dataset | - | qualifies |
| Kaggle Notebook outputs (kaggle/working)... | Up to 20 GB of output per notebook version saved to /kaggle/working... | - | - | qualifies-with-caveat |
| Modal Volumes | 1 TiB of Volume storage free per workspace on the Starter plan... | - | - | qualifies |
| Weights & Biases / CoreWeave Forge... | Free plan: 5 GB/month of storage. Pro: 100 GB/month... | - | - | fails-quota |
| Civitai, model version files... | No published per-account or per-file byte quota... | per-object-cap: >=65 | - | qualifies-with-caveat |
| Ollama registry (registry.ollama.ai)... | No published byte quota, no published per-file cap... | per-object-cap: NOT published, and NOT 2 GiB like GitHub | - | qualifies-with-caveat |

## What the class is

Four shapes.

**A model hub** takes a repository of many shards. Ollama, Civitai and OpenCSG are members, and
their value is that a single blob can be 40 GB or more.

**An ML platform** attaches storage to a compute product. Kaggle, Modal, DagsHub and Weights &
Biases are members, and their quotas are per dataset or per workspace.

**A Chinese hub** is a Hugging Face competitor with a large repository allowance and no
published quota. OpenCSG, Modelers, OpenXLab, OpenDataLab and Baidu AI Studio are members.

**A media hub** takes one large file per version. Civitai is the only true member, at 65.83 GiB
per file.

## OpenCSG: the repository total is not the object cap

The tree API settles this.

`GET https://hub.opencsg.com/api/v1/models/deepseek-ai/DeepSeek-V3/tree` returned 200 with
150,045 bytes on 2026-10-22 (`measured`: 200, 150,045 B): 176 files, 688,603,604,082 bytes in total, of which
163 are shards above 1 GB, and the largest single object is 6,584,784,447 bytes.

So the repository total is 688.6 GB and the object cap is 6.58 GB. A shard plan built on the
first figure is 105 times too coarse and fails on the first upload.

The same platform has a read-path trap:
`GET .../resolve/main/model-00001-of-00005.safetensors` returned 200 with 135 bytes,
which is a git-lfs pointer rather than a file (`measured`, 2026-10-22: 200, 135 B). A client that trusts the
status code downloads 135 bytes and reports success. The bytes require a POST to the LFS batch
endpoint, which returns a presigned OSS URL with `X-Amz-Expires=259200`, or 72 hours.

## Ollama: 39.6 GiB in the namespace a client can use

`GET /v2/` returns 404 with 19 bytes, so the OCI discovery endpoint is absent. A manifest
request for `library/llama3.3` returns 200 with 1,006 bytes and a single model layer of
42,520,398,528 bytes, which is 39.6 GiB (`inferred`, 2026-10-22).

The 455.5 GiB figure belongs to a different namespace and does not appear in
`library/`. That is not a refutation: the registry does hold a blob that large
somewhere, and the namespace an uploader would write to does not expose it.

The pull path is open: a blob request returned 307 to `*.r2.cloudflarestorage.com` with
`X-Amz-Expires=86400`, then 206 with `Content-Range: bytes 0-1023/42520398528`. The push path is
gated, with 401 and `www-authenticate: Bearer` on an unauthenticated push, and the practical
write ceiling is an undocumented 413.

The measure of this provider is that there is no paid storage tier to upsell to. Ollama's paid
product is a hosted service rather than bytes, which is why the registry can be generous and
why it is the strongest finding in this class.

## Civitai: 65.83 GiB per file

Civitai publishes no per-account or per-file quota, and its own Data Storage Policy describes
what happens to uploaded content by default. A 65.83 GiB zip was verified in production and a
307 to 206 ranged read worked on a 43.0 GiB file with a SHA-256 match (`documented`, 2026-10-21).

It is a media hub with a model hub's per-object cap and a catalogue's search interface, which
makes it the only place in the corpus where a 65 GB object is addressable by name rather than by
identifier.

## The ML platforms

Kaggle is the most usable and the most constrained. 200 GB per dataset, 50 top-level files per
dataset, and no published aggregate cap on public datasets: one account was measured holding
1,197.7 GB across 23 public datasets. A quota-request programme exists for datasets above 200
GB and grants storage on a short form.

Modal gives 1 TiB per workspace on the Starter plan, which is the largest free disk allocation
in the corpus. Its Volumes outlive a container, which is what separates it from a notebook disk.

DagsHub gives 20 GB on the free Individual plan, and the commonly cited 10 GB is stale. Weights
& Biases gives 5 GB per month on the free plan and 200 GB on an academic tier.

## The Chinese hubs and the absence of a number

Four records here publish no quota, and the absence is the finding. OpenCSG states explicitly that upload limits depend on the site, the proxy and the
storage configuration, and warns against reading a site limit as a protocol ceiling.

That is a vendor stating that the number does not exist. A plan cannot size against it, and
the record carries `discretionary` rather than a figure.

### Baidu AI Studio (aistudio.baidu.com), dataset + notebook storage

> Two separate pools, which is the interesting part: (1) Notebook persistent workspace, verbatim 'Notebook 100G /home/aistudio/work' (100 GB per user, persisted in real time); (2) Datasets, '50GB50G' (single file under 50 GB, one dataset...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: 50 GB per file. A new account costs national-id. Observed behaviour: Datasets are mutable (versions exist).

Evidence: `https://aistudio.baidu.com` (2026-10-21), record `dossier/storage/baidu-ai-studio-dataset-notebook-storage.json`.
Verdict: `qualifies-with-caveat`.

### Modelers (modelers.cn, Huawei/Ascend ecosystem)

> Not published. The community is an explicit Hugging-Face-shaped hub, models, datasets, and Spaces, plus its own client (openMind Hub Client) and library (openMind) targeting Ascend NPUs. Its contribution guide instructs 'git lfs track' for...

That is the record's own wording (`inferred`, 2026-10-21). A new account costs country-phone. Observed behaviour: API surface is opaque: https://modelers.cn/api/v1/models returns 404, and model detail pages return a 1,638-byte SPA shell regardless of path, so anonymous programmatic access is effectively absent.

Evidence: `https://modelers.cn` (2026-10-21), record `dossier/storage/modelers.json`.
Verdict: `qualifies-with-caveat`.

### OpenCSG (CSGHub SaaS, opencsg.com / hub.opencsg.com)

> No published byte quota anywhere in the docs, and this is deliberate: the upload page states verbatim (upload size and timeout limits are determined by the site, proxy and storage configuration) and explicitly warns ' Git LFS ' (do not...

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `pull-count`: limit observed. A new account costs any-phone. Observed behaviour: Reads depend on Alibaba OSS presigned URLs, so a URL cached for more than 72 h silently dies (301/0-byte), resolve-then-fan-out within the window.

Evidence: `https://opencsg.com` (2026-10-22), record `dossier/storage/opencsg.json`.
Verdict: `qualifies-with-caveat`.

### OpenDataLab (opendatalab.com / opendatalab.org.cn)

> Not published. What is documented is capability rather than quota: the dataset center accepts file, folder, or archive uploads and auto-extracts archives server-side; public datasets require a license field before they can be published (so...

That is the record's own wording (`inferred`, 2026-10-21). A new account costs country-phone. Observed behaviour: API endpoints on opendatalab.com timed out from this network (25 s, then 30 s) while HTML pages served fine, treat the programmatic surface as CN-network-dependent.

Evidence: `https://opendatalab.com` (2026-10-21), record `dossier/storage/opendatalab.json`.
Verdict: `qualifies-with-caveat`.

### OpenXLab (Shanghai AI Lab), model + dataset centers

> Not published, and this is the honest finding. The platform's own intro describes the model center as building an object-storage layer specifically for large files, verbatim: ' AI AI ' (object storage system providing large-file storage...

That is the record's own wording (`inferred`, 2026-10-21). A new account costs national-id. Observed behaviour: The docs site itself was unreliable from an external network (multiple 504s and 25 s timeouts on opendatalab.com and openxlab.org.cn API paths), which is a real signal about operational quality.

Evidence: `https://openxlab.org.cn` (2026-10-21), record `dossier/storage/openxlab-model-dataset-centers.json`.
Verdict: `qualifies-with-caveat`.

### DagsHub (DagsHub Storage + DVC remote)

> 20 GB of DagsHub Storage on the free Individual plan (the commonly cited '10 GB' is stale, the live pricing page says 20 GB), with unlimited public repositories and unlimited collaborators on public repos, and unlimited private repos 'for...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Small company (not hyperscaler-backed).

Evidence: `https://dagshub.com` (2026-10-21), record `dossier/storage/dagshub.json`.
Verdict: `qualifies-with-caveat`.

### Kaggle dataset quota-request program (the >200 GB escape hatch)

> Not a fixed number: Kaggle staff grant additional per-dataset storage quota on request via a short Google Form, explicitly to 'host large, important public datasets'. This is the documented path past the 200 GB per-dataset ceiling

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Grants are discretionary and could in principle be withdrawn, but nothing vanishes on its own.

Evidence: `https://www.kaggle.com/discussions/product-feedback/346049` (2026-10-21), record `dossier/storage/kaggle-dataset-quota-request-program.json`.
Verdict: `qualifies-with-caveat`.

### Kaggle Datasets (public)

> 200 GB per dataset (hard, public or private), 50 top-level files per dataset, 200 GB max total PRIVATE datasets. There is NO documented aggregate cap on public datasets, the docs' 'Technical Specifications' section states only '200GB per...

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `per-object-cap`: 200 GB/dataset. The record states no identity cost. Observed behaviour: Stable, corporate-owned (Google), no history of quota clawback.

Evidence: `https://www.kaggle.com/datasets` (2026-10-21), record `dossier/storage/kaggle-datasets.json`.
Verdict: `qualifies`.

### Kaggle Notebook outputs (kaggle/working), the free side-channel

> Up to 20 GB of output per notebook version saved to /kaggle/working, and every 'Save & Run All' creates a new version. Outputs are themselves addable as dataset inputs to any future notebook. No documented cap on the number of notebook...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Outputs persist indefinitely and are downloadable years later.

Evidence: `https://www.kaggle.com/docs/notebooks` (2026-10-21), record `dossier/storage/kaggle-notebook-outputs-the-free-side-channel.json`.
Verdict: `qualifies-with-caveat`.

### Modal Volumes

> 1 TiB of Volume storage free per workspace on the Starter plan ('Volumes include up to 1 TiB free'; 'Volumes $0.09 / GiB / mo *includes 1 TiB / mo free'), plus 1 TiB/month free network egress. This is the single largest clean free-tier...

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Very stable.

Evidence: `https://modal.com/docs/guide/volumes` (2026-10-21), record `dossier/storage/modal-volumes.json`.
Verdict: `qualifies`.

### Weights & Biases / CoreWeave Forge (academic free tier)

> Free plan: 5 GB/month of storage. Pro: 100 GB/month. 'Free forever for academic research' tier: 200 GB of cloud storage, unlimited tracked hours, up to 25 GB/month Weave ingestion, up to 100 seats, requires an active academic email address

That is the record's own wording (`reported`, 2026-10-21). The record states no identity cost. Observed behaviour: Migrated from wandb.ai branding to CoreWeave Forge (the pricing page 301s to coreweave.com/forge-pricing), product continuity is fine.

Evidence: `https://wandb.ai/site/pricing` (2026-10-21), record `dossier/storage/weights-biases-coreweave-forge.json`.
Verdict: `fails-quota`.

### Civitai, model version files (the 'arbitrary 65 GiB blob' hub)

> No published per-account or per-file byte quota. Its own Data Storage Policy states: 'By default, uploaded content will be stored indefinitely with the exception of input and output files related to model training.' Empirically: a single...

That is the record's own wording (`reported`, 2026-10-21). The constraint that binds is `per-object-cap`: >=65. The record states no identity cost. Observed behaviour: Downloads are reliable and hash-exact when ungated: a full 13,649,928-byte fetch matched the API-advertised SHA-256 exactly (8184D4BA...).

Evidence: `https://civitai.com` (2026-10-21), record `dossier/storage/civitai-model-version-files.json`.
Verdict: `qualifies-with-caveat`.

### Ollama registry (registry.ollama.ai), the strongest finding in this slot

> No published byte quota, no published per-file cap, and no paid storage tier exists to upsell to, the only paid Ollama product is inference compute ('Pricing': Free $0 'Use any cloud model with pay-as-you-go usage credits', Pro $20/mo;...

That is the record's own wording (`documented`, 2026-10-22). The constraint that binds is `per-object-cap`: NOT published, and NOT 2 GiB like GitHub.... The record states no identity cost. Observed behaviour: Pushes to large blobs are flaky: issue #6466 reports 502 Bad Gateway at 40-50% of an 8.5 GB upload, and #13740 reports 413 on 100 GB, resume/retry is required.

Evidence: `https://registry.ollama.ai` (2026-10-22), record `dossier/storage/ollama-registry-the-strongest-finding-in-this-slot.json`.
Verdict: `qualifies-with-caveat`.

## What did not work

| provider | verdict | why it fails |
|---|---|---|
| ClearML (hosted free tier) | fails-quota | Zero free bytes by design. ClearML's free tier is 'Flexible Storage... |
| Comet ML (Comet / Opik), artifact + dataset management | fails-quota | No storage allowance at all on the free tier. The free cloud plan is metered in spans... |
| GitCode (gitcode.com, CSDN), Git/LFS/container quota | fails-quota | No number published. GitCode documents that it meters four resources per user... |
| HyperAI (hyper.ai), free CPU workspace + storage | fails-quota | Free tier storage is 'Free 20 GB + Extra 50 GB, totaling 70 GB'... |
| Lightning AI (Lightning Studios persistent storage) | fails-quota | No GB figure published. The free tier is framed entirely in GPU hours ('Start on the free tier with 80* free GPU hours')... |
| moark (formerly Gitee AI)... | fails-quota | Not published. Gitee's help centre documents the AI-model hosting flow... |
| Neptune.ai | fails-quota | No storage allowance published, and the pricing page fetched contained no GB figure at all... |
| OpenBayes (openbayes.com)... | fails-quota | Free/entry tier attaches 50 GB of workspace storage; the upper tiers attach 200 GB... |
| Oxen.ai (Oxen Hub, dataset versioning for ML) | fails-quota | Explorer (free forever): 50 GB data storage + 50 GB data transfer, unlimited public repos with unlimited collaborators... |
| Pixeltable Cloud | fails-quota | 50 GB Media Store per organization on the free tier, explicitly a HARD limit ('50 GB Media Store per organization... |
| Ultralytics HUB / Ultralytics Platform | fails-quota | Free: 100 GB storage, 10 GB per dataset upload, unlimited number of datasets and models. Pro ($29/seat/mo): 500 GB storage... |
| Common Crawl (the petabyte corpus, read side only) | fails-quota | Not a hosting service: ~300 billion web pages across ~100+ monthly crawls, multi-petabyte... |
| Baseten Delivery Network (BDN) model weight mirrors | fails-egress | No published per-account storage number. BDN 'mirrors model weights to Baseten and caches them near your replicas'... |
| fal.ai persistent /data volume | fails-quota | No published byte quota on the /data volume, the docs state only 'Files written to /data persist between requests... |
| hf-mirror.com / hf-mirror.net (Hugging Face mirror... | fails-quota | None of its own, it is a transparent reverse proxy. Its ToS says so explicitly: it is a... |
| Mage.space uploads | fails-quota | 100 MB per upload, 30-day life. No account-level storage allowance is offered |
| OpenRouter Files API (workspace files) | fails-egress | 10 GiB per workspace, stated verbatim: 'Each workspace can store up to 10 GiB in total. When the workspace is full... |
| Replicate (r8.im + Files API) | fails-quota | Files API is a workspace scratch space with no advertised total... |

Quota and paid are the two large groups. TensorArt's model files are not anonymously retrievable
and its model page is bot-walled at 403. Activeloop pivoted away from storage entirely. Several
hubs publish a quota that is a free trial rather than a tier.

`retention` covers the hubs that garbage-collect unreferenced blobs, which is the model hub's
version of the retention clock: an object that no repository references is deleted, so the
manifest must reference every shard.

## Chaining

A model hub is a shard source with a large per-object cap and a catalogue interface.

The pattern that works is OpenCSG or Civitai for the large shards and a manifest that records
the LFS object identifier rather than the resolve URL, because the resolve path returns a
pointer and the presigned URL expires in 72 hours.

The pattern that fails is a model hub as an archive. A catalogue is organised for retrieval by
name, and an archive of 838,861 shards at 25 MiB has no names worth searching.
