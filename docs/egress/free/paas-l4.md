# Application platforms with a raw L4 port

An application platform runs a reader's process and fronts it. The question
here is narrower than "can it host my code": **does the free tier expose a raw
TCP or UDP port**, because that is what a WireGuard listener needs.

⭐ **One free tier publishes a raw TCP and UDP port: Zerops, at 100 GB/month, and
its free path is IPv6 while IPv4 costs USD 3 a month.** Every other free tier on
this page is HTTP, TCP only, or a credit too small to matter.

| platform | free tier | L4 transport | volume | verdict |
| --- | --- | --- | --- | --- |
| Zerops | Lightweight Core, free | TCP and UDP on ports 10 to 65435 | 100 GB/month | `fails-quota` |
| Northflank | USD 20/month of resources | TCP and UDP through a team L4 balancer | about 333 GB at USD 0.06/GB | `fails-quota` |
| Railway | USD 1/month of credit | TCP proxy only | about 20 GB | `fails-egress` |
| Koyeb | 100 GB/month outbound | TCP proxy only | 100 GB | `fails-egress` |
| Sevalla | apps from USD 5 | TCP only | none free | `paid-only` |
| Clever Cloud | TCP redirection free in beta | TCP only, a random port above 5000 | none stated | `paid-only` |
| Render | a free service type | HTTP only | 5 GB/month | `fails-egress` |
| Zeabur | a free plan | TCP on the cloud, UDP only on the reader's own server | none published | `fails-egress` |
| Google Cloud Run | 2 million requests a month | HTTP only | 1 GiB/month | `fails-egress` |
| DigitalOcean App Platform | static sites only | HTTP only | 1 GiB per app | `fails-egress` |
| Heroku | none since 2022-11-28 | HTTP only | none | `paid-only` |
| Deno Deploy | 1 million requests a month | HTTP only | 20 GiB/month | `fails-egress` |
| AWS App Runner | closed to new customers | HTTP only | none | `dead` |
| Deta | sunset 2024-10-17 | none | none | `dead` |

## Zerops

The only free tier found with a documented raw `TCP/UDP` port range, from 10 to
65435 (`documented`, read 2026-10-23). The free tier includes 100 GB/month of
transfer, and the free IPv4 is the catch: the free path is IPv6 and a public IPv4
is a USD 3/month add-on.

⚠ **100 GB/month is 0.09 TiB, about one eleventh of the test**, so the row fails
on volume before the IPv4 question matters. It stays recorded because the port
range is the right shape and the add-on is cheap.

## Northflank

USD 20 a month of free resources across two services, with a team-level L4 load
balancer that forwards TCP and UDP to a stable public IP (`documented`, read
2026-10-23). At the platform's egress rate the credit is about 333 GB, and the
balancer itself may not be included in the free Sandbox.

⚠ **Whether a free Sandbox may create an L4 balancer is unstated**, which is the
one question a signup would settle.

## The TCP-only platforms

Railway, Koyeb, Sevalla, Clever Cloud and Zeabur all forward an arbitrary TCP
port and none forwards UDP. A WireGuard datagram cannot cross them without a
wrapper at both ends, which is the host problem described in
[`wireguard-transports.md`](wireguard-transports.md).

⭐ **A TCP proxy is still useful for a different job**: it reaches a service behind
CGNAT and it carries a WebSocket. It is not a WireGuard ingress provider.

## The HTTP-only platforms

Render, Cloud Run, App Platform, Deno Deploy and Heroku front a process with HTTP
and give it no port at all. They are recorded so a reader who finds "free hosting"
in a search does not mistake it for ingress.

## What is dead

- **AWS App Runner**: closed to new customers.
- **Deta Space**: sunset on 2024-10-17.
- **Heroku free dynos**: ended on 2022-11-28.
- **Render's free tier as an L4 path**: HTTP only, one port.

## Chaining

**The free chain.** `Zerops free -> a TCP/UDP port -> wg-quick`. The scarce link
is 100 GB/month and an IPv6-only free path.

**The credit chain.** `Northflank USD 20 -> an L4 balancer -> a UDP listener`. The
scarce link is whether the balancer is inside the free allowance.

## The records

`dossier/egress/zerops.json`, `northflank.json`, `railway.json`, `koyeb.json`,
`sevalla.json`, `clever-cloud.json`, `render.json`, `zeabur.json`,
`google-cloud-run.json`, `digitalocean-app-platform.json`, `heroku.json`,
`deno-deploy.json`, `aws-app-runner.json`, `deta.json`, `fly-io.json`,
`port-buddy.json`.

⚠ **No platform was deployed to.** The two rows that would change with one deploy are
Zerops, whose UDP port would become `measured`, and Northflank, whose balancer
entitlement is unstated.
