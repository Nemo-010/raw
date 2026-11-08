# Western consumer drives: the 5 to 20 GB tier, and why it fails the floor

The Western consumer drives are the easiest in this topic to register for and the
least useful. Every one of them sits between 5 and 20 GB, which is two to three
orders of magnitude below the working set, and the enterprise-backed ones that do
offer terabytes are tenant products and not drive products.

This document records the tier, states the arithmetic that closes it, and points at
where the real capacity is instead.

## The comparison

Sorted by free quota, because the identity cost is `email` across the set and the
quota is what separates them.

| service | free tier | per-file cap | identity | fails on |
| --- | --- | --- | --- | --- |
| Google Drive | 15 GB | 5 TB per file (not the binding limit) | `email` | quota |
| Microsoft OneDrive | 5 GB | 250 GB | `email` | quota |
| Dropbox | 2 GB base, more by referral | 2 GB on the basic tier | `email` | quota |
| iCloud Drive | 5 GB | - | `email` | quota |

⚠ **None of these four reaches the 500 GiB floor and none is a candidate.** They are
listed because a reader will look for them and because the table is shorter than the
sentence explaining why they are absent.

## The arithmetic that closes the tier

The hot working set is 10 TiB. The largest free tier here is 15 GB.

```
10 TiB / 15 GB = 10,995,116,277,760 / 15,000,000,000 = 733 accounts
```

733 accounts, each needing an identity and each needing to be kept alive, to hold
one working set. That is not a chaining strategy; it is a job.

⛔ **Do not count this tier as capacity.** A table that lists Google Drive's 15 GB
beside Ctfile's 5 TB implies they are comparable. They differ by a factor of 333.

## Where the real Western capacity is, and why it is not here

The Western offers that do clear the floor are not consumer drives:

- **pooled tenants**, which is what the public instances in this topic are actually
  serving: a Microsoft 365 A1 or a Google Workspace account, with 25 TB per
  SharePoint site. That is a tenant product and its quota belongs to the storage
  topic.
- **paid consumer tiers**, which are in [`../paid/README.md`](../paid/README.md).
- **object storage**, which is the storage topic entirely.

⚠ **A tenant is not a drive and the distinction decides the answer.** A drive holds
one person's files under one person's agreement. A tenant holds an organisation's
sites under an organisation's agreement, which is why a public instance can serve
7.43 TiB and why it dies when the tenant is revoked.

## What the Western tier is good for

One thing, and it is not storage: **an always-available small mount for the state of
a bridge.** A 5 GB OneDrive or a 15 GB Google Drive is enough for a config file, a
database dump and a lock file, and both have first-class rclone backends. A bridge
whose state lives on the same disk as its cache loses both at once.

⚠ **This is a redundancy argument and not a capacity argument.** A 5 GB tier does
not become capacity by being reliable.

## Chaining

```
Google Drive or OneDrive (5 to 15 GB) -> rclone -> the bridge's state and config
```

That is the whole role. It does not touch the 10 TiB working set, the 1 TiB per day
serving path or 20 TiB of archive.
