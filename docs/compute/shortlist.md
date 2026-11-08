# The compute shortlist: three ranked tens, and what the cart actually charges

This page answers five questions: ten free tiers a reader can sign up for, ten paid
machines under USD 5, ten micro machines under USD 1, the NAT and IPv6-only sellers, and
the old seasonal sale pages that still sell.

⛔ **Read the last two columns before any other.** A page price is what the vendor
advertises. A cart price is what the vendor charges. The two disagree on **nine hosts** in this
page, and on three of those the cart charges a *monthly* rate where the page quotes an
*annual* one. The link is only worth clicking if the cart prices the plan.

⚠ **Nothing here was bought and no account was created.** Every row is `documented`: a
first-party page read on 2026-10-24. A handful were read in a real browser after a
Cloudflare challenge was cleared, and those say so. None is `measured`.

## ⛔ A stateless fetch makes a healthy store look dead

VolpaByte returned
"Could not load any product groups" on every URL, through the broker and through a pinned
rendering provider. It is not dead. Warm a cookie jar from `volpabyte.net/` first and the
identical URL redirects to `cart.php?a=confproduct&i=0` and prints all four billing cycles.

The same is true of AlphaVPS: `cart.php?a=add&pid=509` bounces to the store list without a
jar and lands on the config page with one. A cookieless read published a "dead" verdict for
both hosts, and both were wrong.

**The rule:** before calling a WHMCS or Blesta cart dead, re-run it with
`curl -c jar -b jar` warmed from the vendor's homepage. A store that answers
"Could not load any product groups" is a store that has not seen a session, not a store
that has stopped selling.

## The rate this page converts at

Every non-USD price below is converted at the **ECB reference rate of 2026-10-23**, the last
one published before the reads:

| currency | units per USD | 1 unit in USD |
| --- | --- | --- |
| EUR | 0.89341 | **1.1193** |
| CHF | 0.82435 | 1.21307 |
| PLN | 3.92611 | 0.25470 |
| CNY | 6.67024 | 0.14992 |
| IDR | 18,107.80 | 0.0000552 |
| TRY | 49.73778 | 0.020105 |
| RUB | 81.2967 | 0.012300 |

⚠ **RUB is not an ECB rate** — the ECB publishes no rouble reference. It is
`open.er-api.com`, read 2026-10-24, and is labelled as such wherever it is used.

⛔ **`USD/mo` and `USD/yr` both appear on every row because one alone is a half-truth.** A
vendor that quotes only a year has no monthly price; a vendor that quotes only a month has no
annual one. Where the vendor publishes **both**, both are given. Where it publishes **one**,
that one is converted and the other is derived, and the derivation is marked in the row as
`÷12` or `×12`.

---

## 1. Ten free tiers — ranked by what the machine can do

`USD/mo` and `USD/yr` are both **0** because these are free at the point of use. What ends them
is the column that matters.

| # | provider | what the plan gives | native price | USD/mo | USD/yr | card / gate | sign up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | molab | 4 CPU / **32 GiB** + attachable RTX Pro 6000, 96 GB VRAM | free | **0** | **0** | **no card**; 12 h session, 90 min idle | [docs.marimo.io](https://docs.marimo.io/guides/molab/) |
| 2 | GitHub Actions | 4 vCPU / **16 GiB**, 20 concurrent jobs | free | **0** | **0** | **no card**; 6 h job, no inbound port | [github.com/signup](https://github.com/signup) |
| 3 | Kaggle | 4 cores / **30 GiB**, or P100 16 GB, 20 GB disk | free | **0** | **0** | **no card**; phone for GPU; 12 h session | [kaggle.com](https://www.kaggle.com/account/login) |
| 4 | AWS Free plan | `t4g.small` 2 vCPU / 2 GiB Graviton, **750 h/mo**, + $100–200 credits | free | **0** | **0** | **none for most**; $1 hold 3–5 days if asked; **6 months then self-closes** | [signin.aws.amazon.com](https://signin.aws.amazon.com/signup) |
| 5 | Daytona | $200 credit = **31.2 days** of 4 vCPU / 4 GiB / 10 GB at 24/7 | $200 credit | **0** | **0** | **no card**; credit ends, 15 min idle | [app.daytona.io](https://app.daytona.io/) |
| 6 | Opus Host | 1 vCPU / 1 GiB / 20 GB **KVM root, 1 IPv4 + 1 IPv6** | free | **0** | **0** | **no card**; unverified `runtime_days: 30` | [opus-host.de](https://opus-host.de/register) |
| 7 | Oracle Cloud | 2 OCPU / **12 GiB ARM**, 200 GB, 10 TB/mo, routable | free | **0** | **0** | ⚠ **card; hold not published**; idle reclaim <20% p95 | [signup.cloud.oracle.com](https://signup.cloud.oracle.com/) |
| 8 | EUserv | 1 GHz / 1 GiB / 10 GB / 1 TB, permanent root | free | **0** | **0** | **no card**; **IPv6 only** | [euserv.com](https://www.euserv.com/en/virtual-private-server/root-vserver/v2/vs2-free.php) |
| 9 | Silly Development | 0.25 core / 256 MB / 512 MB, **does not sleep** | free | **0** | **0** | **no card**; no expiry in terms | [sillydev.co.uk](https://sillydev.co.uk/panel/auth/register) |
| 10 | freeshell.de | Ubuntu 24.04 shell, **42 GB**, IPv4+IPv6, **private TCP/UDP port**, cron, podman | free | **0** | **0** | **no card**; **postcard to Germany** | [freeshell.de](https://freeshell.de/get-started/) |

⚠ **Nothing in this corpus holds USD 50.** Largest found: Infomaniak **CHF 20**, Koyeb **$29**,
AWS / Alibaba / Huawei **$1**.

⛔ **GitHub's "unlimited"** forbids "any activity unrelated to the production, testing,
deployment, or publication of the software project associated with the repository". The meter
is unlimited; the permitted use is not.

⭐ **AWS does not require a card for most new accounts.** AWS's own signup
page: *"With Sign up for AWS (new), most new customers will not be required to
provide a payment method to get started."* When a card **is** asked for, the
hold is **$1 for 3–5 days** and *"your card will not be charged"*. ⚠ The
account **closes itself six months** after it opens, or when credits run out.

### Free tiers found and rejected

| site | what it offers | why it is not in the ten | record |
| --- | --- | --- | --- |
| [Waifly](https://docs.waifly.com/compte) | 300 MB / 1 GB / 1 MySQL, no card, reaper published | **eleventh** — honest and card-free, but 300 MB runs nothing that matters | `waifly-free` |
| [ASCS Cloud](https://cloud.ascsonoway.com/vps-micro/) | free container, 1 vCPU / 512 MB / 16 GB, public IPv6 | **out of stock until 2026-10-29**; 30-day renewal | `ascs-cloud` |
| [Openworld](https://openworld.eu.org/login) | free container, root SSH, IPv6 + NAT IPv4 | a **7-day renewal only a human can perform** | `openworld` |
| [Red Hat Developer Sandbox](https://developers.redhat.com/developer-sandbox) | 14 GiB across namespaces, OpenShift | **phone**, and a 30-day inactivity purge | `red-hat-developer-sandbox` |
| [Paperspace Gradient](https://console.paperspace.com/signup) | 30 GiB / 8 vCPU notebook, free GPU hours | **notebook-only**, GPU hours metered | `paperspace-gradient-free-tier` |
| [Azure for Students](https://azure.microsoft.com/en-us/free/students/) | $100 credit, **no card** | **full-time university enrolment** | `azure-for-students` |
| [Segfault](https://thc.org/segfault/) | root SSH, **no account at all** | **1.5-day idle reap**; `/sec` wiped at 30 days | `segfault-net` |
| [Huawei Cloud intl](https://www.huaweicloud.com/intl/) | trial VMs | **card, $1 authorisation**, plus real-name verification | `huawei-cloud-intl-free-trial` |
| [Infomaniak](https://www.infomaniak.com/en/hosting/public-cloud) | CHF 300 credit, 3 months | **card, CHF 20 preauth**, 35-country allowlist | `infomaniak-public-cloud` |
| [IONOS Cloud trial](https://cloud.ionos.com/) | 8 cores / 20 GiB / 1.2 TB | **card + company name + sales phone call** | `ionos-cloud-trial` |
| [Volcengine](https://www.volcengine.com/) | trial VMs | **mainland national ID + mainland phone** | `volcengine-free-trial` |
| [VDS.guru](https://vds.guru/trial/) | 1 GiB / 15 GB KVM | **phone**, 24-hour hard stop | `vds-guru-trial` |
| [LinuxZoo](https://linuxzoo.net/) | free Linux VM | **no outbound network at all** | `linuxzoo` |
| [Killercoda](https://killercoda.com/) | interactive Linux scenarios | **90-minute playground**, no persistent disk | `killercoda-free` |
| [Mikrus](https://mikr.us/) | 384 MB / 5 GB, UDP stated | free rung is a **queue and lottery** | `mikrus-10-ipv6-mostly` |
| [CoalByte](https://coalbyte.com/de) | 3 GiB / 1 vCPU / 8 GB | imprint says the company is **not registered yet** | `coalbyte-free` |
| [Psifactor](https://psifactor.pl/?go=newaccount) | root LXC, 2 GiB, public IPv6 with PTR | a human grants it; **IRC required** | `psifactor-free` |
| [HOKAS](https://hokas.net/sign-up) | 0.3 vCPU / 256 MB | markets "never expires" while requiring a **12–24 h ad watch** | `hokas-free` |
| [ElypseCloud](https://elypsecloud.com/vps-linux-gratuit) | 4 GB / 50 GB / 2 vCPU | store returns **"Rupture de stock"** | `elypsecloud-free` |
| [FreeMach](https://freemach.rowe.sh/) | 2 vCPU / 2 GiB / 25 GB | **0 of 10 slots free** | `freemach-free` |
| [IBM LinuxONE](https://community.ibm.com/zsystems/linuxone-community-cloud/) | s390x VM | **hard 120-day stop** | `ibm-linuxone-community` |
| [Google Cloud](https://cloud.google.com/free) | e2-micro | **card at signup** | `google-cloud-free-tier` |
| [Run.cloud](https://run.cloud/) | 4 GiB container | **card** | `run-cloud` |
| [Cloudflare Containers](https://developers.cloudflare.com/containers/) | 4 GiB instance | **card**, metered past allowance | `cloudflare-containers` |
| [VPSWala](https://vpswala.com/) | free 2 GiB VPS | **institutional / student gate** | `vpswala` |
| [Alavps](https://alavps.com/) | 8 GiB | free claim not reachable from any page read | `alavps` |
| [Hex](https://hex.tech/) | 4 GiB notebook | notebook-only, no shell | `hex-community` |
| [Deepnote](https://deepnote.com/) | 5 GiB notebook | notebook-only | `deepnote-free` |
| [Leapcell](https://leapcell.io/) | 4 GiB / 3 vCPU runtime | serverless functions, **no machine** | `leapcell` |
| [MyBinder](https://mybinder.org/) | 2 GiB notebook | anonymous but **ephemeral, rate-limited** | `mybinder` |
| [Vercel](https://vercel.com/signup) | 2 GiB function runtime | serverless, **no persistent machine** | `vercel` |
| [Hugging Face Spaces](https://huggingface.co/) | 16 GiB ZeroGPU | **no shell**, GPU queue | `huggingface-spaces-zerogpu` |
| [Google Cloud Shell](https://shell.cloud.google.com/) | free shell VM | **5 GB home**, reaped weekly | `google-cloud-shell` |
| [GitHub Codespaces](https://github.com/features/codespaces) | 2 vCPU / 8 GiB | 60 free hours a month, then stops | `github-codespaces` |
| [Deno Deploy](https://dash.deno.com/) | 0.75 GiB isolate | serverless, no machine | `deno-deploy` |
| [Ctrl-C Club](https://ctrl-c.club/) | pubnix shell | no root, no ports, manual | `ctrl-c-club` |
| [Envs.net](https://envs.net/) | pubnix shell | no root, manual approval | `envs-net` |
| [Hashbang](https://hashbang.sh/) | pubnix shell | no root | `hashbang` |
| [Hax.co.id](https://hax.co.id/) | free container | recurring renewal clock | `hax-co-id` |
| [Azure Container Apps](https://azure.microsoft.com/en-us/products/container-apps) | 0.5 GiB / 0.25 vCPU | **card**, scale-to-zero | `azure-container-apps` |
| [Google Cloud Run](https://cloud.google.com/run) | 0.5 GiB request-scoped | **card**, no persistent process | `google-cloud-run` |
| [Cloudflare Workers](https://workers.cloudflare.com/) | isolate | **no machine at all** | `cloudflare-workers` |
| [Railway](https://railway.com/) | $5 trial credit | card after trial | `railway` |
| [Microlxc](https://microlxc.net/) | 64 MiB container | too small to run anything | `microlxc-tiny` |
| [OnWorks](https://www.onworks.net/) | browser workstation | a **session**, not a machine | `onworks-workstation` |
| [FreeVPS.trial](https://freevpstrial.net/) | — | **dead** | `freevpstrial-net` |

---

## 2. Ten paid beefy — $1.00–5.00/mo

Ranked by **what the machine is**, then by price. Where a vendor publishes both cycles, both
appear in `native price`, and `USD/mo` gives the monthly-billed figure first.

| # | provider / plan | what the plan gives | native price | USD/mo | USD/yr | renewal | buy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | VolpaByte Ryzen KVM 8 GB | 6 AMD Ryzen vCores / **8 GiB ECC** / 100 GB / **unlimited** / 1 IPv4 + /64 | €4,99/mo · €14,22/qtr · €26,95/6mo · **€50,90/yr** | **5.59** monthly · **4.75** annual | **56.97** (€50,90) | not stated; €4.99/mo is the only evidence | [cart](https://volpabyte.net/dashboard/cart.php?a=configure&productid=1) |
| 2 | 24fire KVM Börse Xeon #1 | 2 vCore / **8 GiB** / 50 GB NVMe / unlimited fair use | €4,11/mo prepaid | **4.60** | **55.20** (×12) | **$4.60**, "permanente Preisgarantie" — 1.80× | [register](https://24fire.de/register) |
| 3 | HostBrr ECO 8 GB | **2 vCore** / 8 GiB / 80 GB / 5 TB | $5.50/mo · **$55.00/yr** | **5.50** monthly · **4.58** annual | **55.00** | **$4.58** — cart prints "Total When Renewing: 1 Year @ $55.00" — **1.00×** | [group page](https://my.hostbrr.com/order/main/packages/largeram/?group_id=67) |
| 4 | AlphaVPS C6G | 3 vCPU / 6 GiB / 55 GB / **6 TB** | €4,99/mo · €27,54/6mo · **€50,90/yr** | **5.59** monthly · **4.75** annual | **56.97** (€50,90) | **$4.75**, "LOCKED AT RENEWAL, FOREVER" ×3 — **1.00×** | [cart](https://alphavps.com/clients/cart.php?a=add&pid=509) |
| 5 | Bulutova VPS Sunucu 8 | 2 vCore / **8 GiB ECC** / 60 GB / 1 Gbps | 194,21 TL/mo · **168,87 TL/ay** (2.026,44 TL/yr) | **4.68** monthly · **4.07** annual, KDV incl. | **48.84** (2.026,44 TL) | **$6.79** if the 40% discount lapses — 1.67× | [cart](https://www.bulutova.com/panel/cart/product/236/annually) |
| 6 | Contabo Cloud VPS 4 | 4 vCPU / **8 GiB** / 100 GB / unlimited | €4,40/mo on 24-mo · €5,50/mo monthly | **4.92** on 24-mo · **6.16** monthly | **59.04** (24-mo term) | **$6.16** — 1.25×. ⚠ JSON-LD implies EUR/USD 1.20 → **$5.28, over the line** | [product](https://contabo.com/en-us/vps/cloud-vps-core-4) |
| 7 | C-Servers ExtraVPS-6144 | 4 vCPU / 6 GiB / 6 TB | $4.29/mo | **4.29** | **51.48** (×12) | not published | [cart](https://web.c-servers.co.uk/order-steps/server/468) |
| 8 | C-Servers ExtraVPS-6144 DDR5 NJ | 3 vCPU / 6 GiB / 20 TB | $4.49/mo | **4.49** | **53.88** (×12) | not published ⚠ **"Out of Stock!"** | [cart](https://web.c-servers.co.uk/order-steps/server/349) |
| 9 | GreenCloudVPS BudgetKVM-3 | 4 cores / **8 GiB** / 60 GB NVMe / 8 TB | **$45.00/yr** | **3.75** (÷12) | **45.00** | ⛔ **not published** in 320,626 bytes — month 13 unknown | [store](https://greencloudvps.com/billing/store/budget-kvm-sale/budgetkvmro-3) |
| 10 | HostBrr ECO 4 GB | 1 vCore / 4 GiB / 40 GB / 2500 GB | $3.25/mo · **$32.50/yr** | **3.25** monthly · **2.71** annual | **32.50** | $2.71 — **1.00×** | [group page](https://my.hostbrr.com/order/main/packages/largeram/?group_id=67) |

⭐ **Best machine for the money: VolpaByte at €50,90 a year** — 6 vCores and 8 GiB for the same
out-of-pocket as AlphaVPS's 3 vCores and 6 GiB. ⚠ Renewal unstated.
⭐ **If a written renewal matters: AlphaVPS C6G**, "LOCKED AT RENEWAL, FOREVER" three ways. ⚠ Only
**Sofia and Los Angeles** in stock of seven.
⭐ **Best value per gigabyte: HostBrr ECO 4 GB at $32.50/yr** — the only 1.00× renewal in the band
whose annual figure the cart prints itself.
⛔ **Do not trust a "dead" verdict in this band without a cookie jar** — see the method note above.

---

## 3. Ten micro machines — under $1.00/mo, ranked for the job

Ranked by what the machine does for a **WireGuard node** or a **health monitor**: RAM, then
whether a port is reachable, then whether it can be ordered today. Price breaks ties.

| # | provider / plan | what the plan gives | native price | USD/mo | USD/yr | address / ports | stock | buy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DediRock Promo Special NY | **2 GiB** / 1 vCPU / 30 GB / 2 TB | **$9.88/yr** | **0.82** (÷12) | **9.88** | **dedicated IPv4**, all ports | ✅ in stock | [cart](https://billing.dedirock.com/index.php/store/promo-vp/promo-vps-special-ny) |
| 2 | VDS6 V6-1 | **2 GiB** / 1 vCPU / 20 GB | **$5.88/yr** | **0.49** (÷12) | **5.88** | **IPv6 only**, all ports | ⛔ **0 available** | [store](https://my.vds6.net/store/v6-ipv6-vps-vds) |
| 3 | ServerMikro NAT LXC 1 GB | **1 GB** / 10 GB / 300 Mbps unmetered | IDR 10.000/mo | **0.55** | **6.63** (×12) | NAT, ⚠ **only 4 TCP** | ✅ in stock | [checkout](https://my.servermikro.com/products/vps-nat-lxc/vps-nat-lxc-1gb-ram/checkout) |
| 4 | host2play LXC Lite | 768 MB / 10 GB LXC | **PLN 34,90/yr** | **0.74** (÷12) | **8.89** | NAT + IPv6, **10 ports** | in stock | [cart](https://host2play.pl/product/159?c=yearly) |
| 5 | ReconV vps-nat512mb | 512 MB / 6 GB LXC | **PLN 45,12/yr** | **0.96** (÷12) | **11.49** | NAT + /128 IPv6, **10 ports, UDP stated** | in stock | [order](https://dash.reconv.pl/en/order/vps/vps-nat512mb) |
| 6 | NATVPS NAT512 KVM NL | 512 MiB / 1 vCPU / 5 GB | **$7.50/yr** | **0.63** (÷12) | **7.50** | NAT + /80 IPv6, **20 ports + SSH** | ✅ **all 8 locations** | [cart](https://clients.natvps.net/?/cart/kvm-netherlands/) |
| 7 | WuyouCloud DE NAT-LXC | 512 MiB / 1 GB / 1 Gbps unmetered | CNY 1,99/mo + CNY 1 setup | **0.30** | **3.58** (×12) | NAT, ports not published | ✅ **5 units** | [register](https://wuyoucloud.de/register.php) |
| 8 | C-Servers NanoVPS-384 US | 384 MiB / 1 vCPU / 12 GB / 2 TB | $2.39/6mo · $3.89/12mo · $6.99/24mo | **0.40** (6-mo) · **0.32** (12-mo) | **3.89** (12-mo) · **4.78** (6-mo) | NAT, UDP with a condition | ✅ in stock | [cart](https://web.c-servers.co.uk/order-steps/server/458) |
| 9 | 56IDC Toy NL NAT2 | 512 MiB / 1 vCPU | **CNY 10,00/yr** | **0.12** (÷12) | **1.50** | NAT, ports not stated | unmarked | [register](https://56idc.net/register.php) |
| 10 | JJFLY 荷兰 NAT | 256 MB / 1.5 GB LXC | CNY 1,00/mo | **0.15** | **1.80** (×12) | NAT + **1 dedicated IPv6**, **10 IPv4 ports** | unmarked | [cart](https://idc.jjfly.cloud/cart?action=configureproduct&pid=6) |

⭐ **WireGuard node: DediRock at $0.82.** Only row in the band with a **dedicated IPv4**, and 2 GiB
is four times the next machine that can actually be ordered. Cart read in a browser: **$9.88 Total Due
Today**. ⚠ Renewal not published.
⭐ **Monitor: NATVPS at $0.63.** 20 forwarded ports plus SSH, **in stock at all eight locations**,
cart prices it.
⚠ **The two cheapest are the two least usable.** JJFLY is a "toy" by the vendor's own words and
blocks outbound 25 and 80/443 to China. TierHive at $0.10 **has no cart at all**.

### The rest of the band, by price

| provider / plan | what the plan gives | native price | USD/mo | USD/yr | note | buy |
| --- | --- | --- | --- | --- | --- | --- |
| TierHive Micro | 128 MiB / 1 GB NVMe | $0.10/mo hourly | **0.10** | **1.20** (×12) | ⚠ **no cart exists**; AUP says "Alpha status" | [register](https://control.tierhive.com/register) |
| 56IDC Toy VPS NAT-384 | 384 MiB / 1 GB / 1 TB | CNY 10,00/yr | **0.12** | **1.50** | **20 TCP** ports | [register](https://56idc.net/register.php) |
| VirNAT US-256 KVM | 256 MiB / 1 vCPU | $0.80/qtr · $2.80/yr | **0.23** | **2.80** | ports **chosen** | [cart](https://virnat.com/client/store/configure/us-256-kvm) |
| luo_cloud DE-2 | 128 MiB / 1 vCPU | CNY 1,50/mo | **0.22** | **2.69** (×12) | ⛔ **cart sells another product, 16.7×** | [page](https://idc.888644.xyz/index.php?rp=/store/lxc-de/de-2) |
| Gullo's NAT-128 | 128 MiB | **$3.50/yr** | **0.29** (÷12) | **3.50** | ⛔ **no UDP stated** — not a VPN node | [cart](https://hosting.gullo.me/order/config/index/nat-vps/?group_id=43&pricing_id=352&coupon=LEB-NAT-128MB) |
| IDreg Net NAT-1 | 128 MB / 2 GB OpenVZ | Rp 8.500/mo | **0.47** | **5.64** (×12) | NAT + **/80 IPv6**, **19 + SSH** | [cart](https://ca.idreg.net/store/vps-nat/nat-1) |
| Axivora MCI-N-C | 512 MiB | €1,25/mo | **1.40** | **16.79** | **IPv6 only**; AXIVORA CONNECT LTD 16780591 | [store](https://store.axivora.net/) |
| KhanWebHost FR 256MB | 256 MB / 5 GB | **$5.99/yr** | **0.50** (÷12) | **5.99** | ⛔ **company dissolved 2023-12-26** | [store still sells](https://khanwebhost.com/register.php) |
| WHPlus IIX NAT 512 | 512 MB | Rp 12.500/mo | **0.69** | **8.28** (×12) | no entity named | [cart](https://my.whplus.com/cart.php?gid=20&language=indonesia) |
| Mikrus 10 | 384 MB / 5 GB | **PLN 35/yr** | **0.74** (÷12) | **8.91** | **UDP stated**, IPv6-mostly | [product](https://mikr.us/product/mikrus-1-0/) |
| Privex VNano SE | 256 MB / 5 GB | $0.99/mo | **0.99** | **11.88** (×12) | **crypto only, no card**; AS210083 | [order](https://pay.privex.io/order/package/vnano-se-ssd) |
| MiaoMiao HGC Nano | nano NAT | CNY 6,60/mo | **0.99** | **11.88** (×12) | no entity named | [store](https://miaomiao.moe/index.php?rp=/store/hgc-nat) |

⚠ **A dash is not a zero.** Where a vendor publishes no figure the row is absent, not blank.

---

## 4. IPv6-only — under $2.00/mo

| # | provider | what the plan gives | native price | USD/mo | USD/yr | IPv6 delivery | IPv4 add-on | buy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DeluxHost X-0 NL | 1 vCore / 512 MB / 10 GB | €4,50–6,00/yr *(cart range)* | **0.50** | **5.40** | IPv6-only, 1× /64, all ports | priced in cart | [deals](https://deluxhost.net/en/deals/x) |
| 2 | SKRIME EPYC 1G | 1 GiB / 10 GB KVM | €0,99/mo | **1.11** | **13.29** (×12) | IPv6-only /64, **all ports** | none | [order](https://skrime.eu/order/server/eyJjIjoyLCJtIjoxLCJkIjoxMCwiNCI6MSwiNiI6MSwiY29uIjoxMH0=) |
| 3 | ST-Hosting Type 9 | 512 MB / 20 GB LXC | €0,99/mo | **1.11** | **13.29** (×12) | IPv6 only, open | not offered | [cart](https://cp.st-hosting.com/en/cart/addToCart/772) |
| 4 | Hop179 OÜ Frankfurt | 1 vCPU / 1 GB / 10 GB / 1 TB | **€11,99/yr** | **1.12** (÷12) | **13.42** | 1 addr "up to /52", **open, no NAT** | €2/mo | [cart](https://my.hop179.net/order/cart/index/v6-vps) |
| 5 | v6Node entry | not published at €1 | €1,00/mo · €3,00 setup | **1.12** | **13.42** (×12) | /64, **DNS64/NAT64** | NAT64 only | [deploy](https://cloud.v6node.com/deploy) |
| 6 | iFog GmbH Amsterdam | 512 MB / 10 GB / 500 GB | **CHF 12,99/yr** (CHF 5,00/3mo) | **1.31** (÷12) | **15.76** | "IPv6", no prefix stated | not offered | [order](https://my.ifog.ch/order/main/index/BGP-Basic) |
| 7 | Axivora MCI-N-B | 1024 MiB / 20 GB | €1,25/mo | **1.40** | **16.79** (×12) | **single /128**, open | none | [store](https://store.axivora.net/products/MCI-IPv6-Only/mci-n-b) |
| 8 | Cloudnium LLC Dallas | 512 MB / 10 GB / 1 TB | $1.50/mo | **1.50** | **18.00** (×12) | 1 addr | none on v6 line | [cart](https://portal.cloudnium.net/cart/dallas-ipv6-vps/) |
| 9 | Skhron Stockholm | 512 MiB / 6 GiB / 1 TiB | €1,69/mo | **1.89** | **22.70** (×12) | **routed /64, free /56** | **€0.65/mo** | [store](https://skhron.eu/services/sweden) |
| 10 | BERO HOST XS DE | 1 core / 1 GB / 10 GB / 25 TB | €12,00/yr | **1.12** (÷12) | **13.42** | /64, open | none | ⛔ **withdrawn** — [page still up](https://bero-host.de/server/prepaid-ipv6-rootserver-mieten) |

⭐ **IPv6 answer: DeluxHost at $0.50/mo** — a /64, all ports open, and the cart prices an optional
IPv4 add-on. ⚠ `reported`, not `documented`.
⭐ **If IPv4 matters: Skhron** — €0.65/mo add-on on a €1,69 box, with a **routed /64 and a free /56**,
more address space than anything else in the band.
⛔ **Dead in this band:** `cinfu-ex2de-ipv6`. **No price published:** `wapac-tw-512-lxc`,
`wapac-tw-512-lxc-ipv6` — in the dossier, not ranked here.

---

## 5. NAT sellers — under $1.50/mo

| # | provider | what the plan gives | native price | USD/mo | USD/yr | TCP / UDP ports | buy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 56IDC Toy NL NAT2 | 512 MiB / 1 vCPU | **CNY 10,00/yr** | **0.12** (÷12) | **1.50** | not stated | [register](https://56idc.net/register.php) |
| 2 | 56IDC Toy VPS NAT-384 | 384 MiB / 1 GB / 1 TB | **CNY 10,00/yr** | **0.12** (÷12) | **1.50** | **20 TCP** / not stated | [register](https://56idc.net/register.php) |
| 3 | JJFLY 荷兰 NAT | 256 MB / 1.5 GB LXC | CNY 1,00/mo | **0.15** | **1.80** (×12) | 10 IPv4 / not stated | [cart](https://idc.jjfly.cloud/cart?action=configureproduct&pid=6) |
| 4 | luo_cloud DE-2 | 128 MiB / 1 vCPU | CNY 1,50/mo | **0.22** | **2.69** (×12) | stated / not stated | ⛔ **cart sells another product, 16.7×** — [page](https://idc.888644.xyz/index.php?rp=/store/lxc-de/de-2) |
| 5 | VirNAT US-256 KVM | 256 MiB / 1 vCPU | $0.80/qtr · **$2.80/yr** | **0.23** | **2.80** | stated / stated, **chosen** | [cart](https://virnat.com/client/store/configure/us-256-kvm) |
| 6 | Gullo's NAT-128 | 128 MiB | **$3.50/yr** | **0.29** (÷12) | **3.50** | stated / ⛔ **no UDP** | [cart](https://hosting.gullo.me/order/config/index/nat-vps/?group_id=43&pricing_id=352&coupon=LEB-NAT-128MB) |
| 7 | WuyouCloud DE NAT-LXC | 512 MiB / 1 GB / 1 Gbps | CNY 1,99/mo + CNY 1 setup | **0.30** | **3.58** (×12) | not published | [register](https://wuyoucloud.de/register.php) |
| 8 | C-Servers NanoVPS-384 | 384 MiB / 12 GB / 2 TB | $2.39/6mo · **$3.89/yr** | **0.40** (6-mo) · **0.32** (12-mo) | **3.89** | stated / stated, conditional | [cart](https://web.c-servers.co.uk/order-steps/server/458) |
| 9 | IDreg Net NAT-1 | 128 MB / 2 GB OpenVZ | Rp 8.500/mo | **0.47** | **5.64** (×12) | **19 + SSH** / not stated | [cart](https://ca.idreg.net/store/vps-nat/nat-1) |
| 10 | KhanWebHost FR 256MB | 256 MB / 5 GB | **$5.99/yr** | **0.50** (÷12) | **5.99** | stated / **TCP+UDP** | ⛔ **company dissolved 2023-12-26** — [store still sells](https://khanwebhost.com/register.php) |
| 11 | ServerMikro NAT LXC 1 GB | 1 GB / 10 GB / 300 Mbps | IDR 10.000/mo | **0.55** | **6.63** (×12) | ⚠ **4 TCP** / not stated | [checkout](https://my.servermikro.com/products/vps-nat-lxc/vps-nat-lxc-1gb-ram/checkout) |
| 12 | NATVPS NAT512 KVM NL | 512 MiB / 5 GB | **$7.50/yr** | **0.63** (÷12) | **7.50** | **20 + SSH** / not stated | [cart](https://clients.natvps.net/?/cart/kvm-netherlands/) |
| 13 | WHPlus IIX NAT 512 | 512 MB | Rp 12.500/mo | **0.69** | **8.28** (×12) | stated / stated | [cart](https://my.whplus.com/cart.php?gid=20&language=indonesia) |
| 14 | Mikrus 10 | 384 MB / 5 GB | **PLN 35/yr** | **0.74** (÷12) | **8.91** | stated / **UDP stated** | [product](https://mikr.us/product/mikrus-1-0/) |
| 15 | host2play LXC Lite | 768 MB / 10 GB LXC | **PLN 34,90/yr** | **0.74** (÷12) | **8.89** | **10** / not stated | [cart](https://host2play.pl/product/159?c=yearly) |
| 16 | DediRock Special NY | **2 GiB** / 30 GB / 2 TB | **$9.88/yr** | **0.82** (÷12) | **9.88** | all / all, **dedicated IPv4** | [cart](https://billing.dedirock.com/index.php/store/promo-vp/promo-vps-special-ny) |
| 17 | ReconV 512 MB | 512 MB / 6 GB LXC | **PLN 45,12/yr** | **0.96** (÷12) | **11.49** | **10** / **yes, ≥1 UDP** | [order](https://dash.reconv.pl/en/order/vps/vps-nat512mb) |
| 18 | Privex VNano SE | 256 MB / 5 GB | $0.99/mo | **0.99** | **11.88** (×12) | IPv6 /64 + NAT64 | [order](https://pay.privex.io/order/package/vnano-se-ssd) |
| 19 | MiaoMiao HGC Nano | nano NAT | CNY 6,60/mo | **0.99** | **11.88** (×12) | stated / stated | [store](https://miaomiao.moe/index.php?rp=/store/hgc-nat) |
| 20 | Axivora MCI-N-C | 512 MiB | €1,25/mo | **1.40** | **16.79** (×12) | **IPv6 only**, open | [store](https://store.axivora.net/) |

**Dead:** `asiavm-nat-eu-hetzner-1gb`, `flapjacks-hk-t1ion-ipv6-mini`, `topcloud-vn-cuc-re-1`,
`ihostart-nat64-1g`, `narwhal-cloud-nat`, `freevpstrial-net`.
**fails-identity:** `hostdata-id-nat-sg-ssd-1gb`. **fails-quota:** `onworks-workstation`.
**No price published:** `pasyun-nat4-dc1-1`, `bytevirt-nat-512-lxc`, `arenastreaming-lxc-nat-basic`,
`host-hong-kong-nat-vps`, `upyun-sg-nat-2`.

### The ladder that changes this band — Cheap-Host

All four rungs: unlimited traffic, 100 Mbit/s, Germany, shared IPv4 with **no IPv6**,
**999 TCP/UDP + SSH**, **port 25 blocked**.

| rung | RUB/mo | USD/mo | USD/yr | vCPU | RAM | NVMe |
| --- | --- | --- | --- | --- | --- | --- |
| NAT Start | 59 | **0.73** | **8.71** (×12) | 1 | 1 GB | 10 GB |
| NAT Base | 99 | **1.22** | **14.61** (×12) | 1 | **2 GB** | 15 GB |
| NAT Pro | 199 | **2.45** | **29.37** (×12) | 2 | **4 GB** | 25 GB |
| NAT Plus | 349 | **4.29** | **51.51** (×12) | 4 | **8 GB** | 50 GB |

**NAT Pro is the biggest NAT machine in the corpus under $3.** Two things keep it out of the
ranked list: every "Choose plan" routes to a login so no price renders before an account, and its
rails are SBP, SberPay, YooMoney, MIR and crypto — **no card network**.

## Old seasonal sale pages: one survives, and it is not the one advertised

**Eleven sale pages and 41 order links were tested. One sells.** Low-end hosts do leave
Black Friday pages up, but none of the tested pages still orders at the old price: the one
seller is a standing promo SKU that the Black Friday page never links to.

### What still sells

| host | page | advertised | what the cart charges | cart | record |
| --- | --- | --- | --- | --- | --- |
| **DediRock** | `store/promo-vp/promo-vps-special-ny` (**standing promo**, not the BF page) | USD 9.88/yr | **USD 9.88 Total Due Today** — 2 GiB / 1 vCPU / 30 GB / 2 TB / 1 IPv4 | ✅ **yes, browser-verified** | `dedirock-promo-vps-special-ny` |
| **RackNerd** | `racknerd.com/specials/` (**live, current**) | USD 21.99 / 35.99 / 59.99 / 89.99 / 119.99 a year | **each pid prices its own plan exactly** | ✅ **all five yes** | `racknerd-1gb-special` |

RackNerd's specials page is the one long-lived seasonal page that works end to end. All
five `cart.php?a=add&pid=` links were followed and each rendered a product configurator
with a matching total:

| pid | product | page | cart |
| --- | --- | --- | --- |
| 952 | 1 GB KVM VPS Special | USD 21.99/yr | **USD 21.99 Total Due Today** |
| 953 | 2 GB KVM VPS Special | USD 35.99/yr | **USD 35.99** |
| 954 | 4 GB KVM VPS Special | USD 59.99/yr | **USD 59.99** |
| 955 | 6 GB KVM VPS Special | USD 89.99/yr | **USD 89.99** |
| 956 | 8 GB KVM VPS Special | USD 119.99/yr | **USD 119.99** |

Its FAQ states the specials are "lifetime recurring" and renew "at the same rate". That is
the vendor's claim about renewal, not a printed renewal invoice. The record for the ladder
as a whole is `racknerd-specials`; the 8 GB rung is `racknerd-8gb-annual-special` at
USD 10.00 a month equivalent (USD 119.99 a year), which is over this page's line and is
recorded `paid-only` rather than recommended.

⚠ **Datalix is recorded but not ranked.** Its Xeon 2026-sale Starter is USD
6.71 a month (`datalix-xeon-2026-sale-starter`), over the USD 5 line — and its
**page and its cart disagree**: the page reads EUR 3.95 with 10 TB of traffic,
the cart reads **EUR 5.99 with 1 TB**, both claiming "dauerhaft".
Unreconciled, and it is the difference between qualifying and not. Its cart
page also arrived **logged in as another user** — the body carried a session
banner naming an account — so its `cart_works` is weaker evidence than any
other row here. The price matches the vendor's own card text, so the
plan-to-URL mapping holds; an anonymous render was never observed.

⚠ **HostBrr ECO 4 GB is the best value per gigabyte in the corpus but sits below this
page's beefy bar.** At USD 32.50 a year (USD 2.71/mo) for 1 vCore / 4 GiB / 40 GB NVMe /
2500 GB it is half the memory of the ten above, so it is recorded as `hostbrr-value-4gb` and
appears in the table as row 9 rather than as a pick. It is the cheapest **renewal-stable**
machine found: 1.00×, with the cart printing the annual figure itself.

### The fossils: live page, nothing to buy

Every row below returns HTTP 200, quotes a price, and sells nothing at that price.

| host | page | advertised | what actually happens | record |
| --- | --- | --- | --- | --- |
| **DediRock** | `dedirock.com/black-friday/` | USD 9.88/yr Saver | the Order href `…/promo-vps-saver-ny-bf` lands on a **category listing, cheapest USD 5.99/month**, a different shape. Six of nine links explicitly **"Out of Stock"** | `dedirock-black-friday` |
| **DediRock** | `dedirock.com/cyber-monday/` | USD 8.88/yr | **9 of 9 links "Out of Stock"**; the page says "All Prices are Yearly Plans" | `dedirock-cyber-monday` |
| **RackNerd** | `store/blackfriday2025/1-gb-kvm-vps-black-friday-2025` | **USD 10.60/yr** | the **product page itself** renders **"Oops, there's a problem… Out of Stock — The plan you selected is out of stock and not available for ordering at this time."** The store also shows `JUST $10.60/YEAR` beside `0 Available` | `racknerd-black-friday-2025` |
| **ColoCrossing** | `colocrossing.com/cyber-monday/` | USD 12.00/yr, and USD 2.37/mo with coupon | 3 of 4 yearly carts **Out of Stock**; the 4th repoints to **USD 3.95/mo** and the coupon is not applied | `colocrossing-cyber-monday` |
| **VirMach** | `virmach.com/black-friday-cyber-monday/` | USD 18.88 / 2 yr | three of four pids repoint to the **account support-level** store (**USD 60–9600/yr**); the fourth is Out of Stock | `virmach-black-friday-cyber-monday` |
| **CloudCone** | `cloudcone.com/black-friday/` | — | a **2021 blog post** titled "Black Friday 2021 CloudCone buyer's guide"; years 2015–2021 only | `cloudcone-black-friday` |
| **Scaleway** | `scaleway.com/en/black-friday/` | — | honest: **"No Black Friday deals available. See you in 2026."** | `scaleway-black-friday` |
| **Contabo** | `contabo.com/en/black-friday/` | — | a forward-looking newsletter stub: **"Coming Soon!"** | `contabo-black-friday` |
| **Hostodo** | `hostodo.com/black-friday-2025` | USD 12/yr, USD 22/yr | ⚠ **unknown**: the deploy console loads but renders no price line, and a control request with a **bogus plan code returned byte-identical output**, so the 200 proves nothing. Reading the price needs a signed-in session | `hostodo-black-friday-2025` |

⛔ **The most dangerous row in this whole page is RackNerd's Black Friday 2025 store.** It
renders `JUST $10.60/YEAR` in the same viewport as `0 Available`. A reader who screenshots
the price and not the stock line believes a USD 0.88/month 1 GB box exists. It does not.

⛔ **The second most dangerous is DediRock's Black Friday page**: it is live, dated this
year, renders properly, and its own "Order Now" button charges a **monthly** rate for a
different machine. There is no error and no sold-out marker.

### Swept and empty

`/black-friday`, `/bf`, `/deals`, `/specials`, `/sale`, `/promo` and `/cyber-monday` were
tried on 35 hosts. All 404 or redirect to the homepage on: AlphaVPS, HostBrr, HostDare,
HostNamaste, ServerCheap, Time4VPS, HostCram, GreenCloudVPS, LetBox, BuyVM, HostHatch,
VPSBG, 24fire, Prometeus, Cloudzy, Hetzner, IONOS, Namecheap, Linode, DigitalOcean,
Vultr. HostNamaste redirects **all ten** paths to its homepage.

⚠ **`buyvm.net/black-friday/` is the textbook HTTP-200 trap**: 12,391 bytes, status 200,
rendering "the page you're looking for is currently not available".

## The four rules this page establishes

1. ⛔ **A page price is not a cart price.** Nine hosts disagreed. Read the cart.
2. ⛔ **A live sale page is not an offer.** Eleven pages, one seller.
3. ⛔ **A price without a renewal is half a price.** DediRock's USD 9.88 has no published
   year two; GreenCloudVPS's USD 3.75 becomes USD 40.00.
4. ⛔ **A marketing button can be broken while the product is fine.** VolpaByte's is dead
   outright; HostBrr's renders `$0.00` and needs the group page instead.

## Where the detail lives

- [`free/no-card.md`](free/no-card.md) — the free tiers, the card gate, what a debit buys
- [`free/always-on-free.md`](free/always-on-free.md) — the ones that do not sleep
- [`paid/under-five.md`](paid/under-five.md) — every machine under USD 5, with renewals
- [`paid/under-one.md`](paid/under-one.md) — every machine under USD 1, split by use case
- [`paid/micro.md`](paid/micro.md) — the sub-dollar band in full
- [`paid/niche-non-english.md`](paid/niche-non-english.md) — the non-English sellers
- [`dead-ends.md`](dead-ends.md) — what is gone, and the evidence of its death
