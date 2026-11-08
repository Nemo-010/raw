#!/usr/bin/env python3
"""compute-price.py -- every paid compute figure in docs/compute/, from a rate.

PURPOSE
    Turn a published rate and a billing model into the two numbers a reader
    compares, `10h` (300 hours) and `24/7` (730 hours), at one named shape.
    A price here is a triple: a shape, a horizon, and what the meter counts.

WHY IT EXISTS
    The topic quotes one number more often than any other, Modal's Sandbox rate,
    and that number was a hardcoded literal that no published rate produced. It
    was 3.2 times the page's own arithmetic and it propagated into a headline.
    A constant is not a derivation. Every rate below therefore carries the page
    sentence or the record field it comes from, in the line that uses it.

WHY IT IS IN scripts/
    It used to live under `.tmp/work/`, and `.tmp/` is never committed. Every
    paid figure in the topic cited a path that a clean tree deletes, so the
    provenance of the whole paid lane would have gone with it.

DEPENDENCIES
    Python standard library only. No network. The rates are the inputs and each
    one states where it was read.

OUTPUT
    One table on stdout. `--modal` prints the Modal arithmetic alone, which is
    the check a reader re-derives by hand.

EXIT CODES  (repository map, scripts/README.md)
    0  the table was printed
    2  usage error
"""
import argparse
import sys

H300 = 300.0     # 10 h/day x 30
H730 = 730.0     # 24/7 for a month
CREDIT = 30.0    # Modal Starter's monthly credit, USD


def allocated(rate_h, h=H300):
    """Wall-clock: the box bills while it runs and does not bill while stopped."""
    return rate_h * h


def allocated_with_keep(compute_h, disk_month, h=H300):
    """Compute bills while running; disk bills for every month it is kept."""
    return compute_h * (h / H730) + disk_month


# --- Modal: the shape conversion is the whole error -------------------------
# modal.com/pricing, raw HTML (read 2026-10-22), the Sandbox and Notebooks
# table: "CPU (non-preemptible) Physical core (2 vCPU equivalent)
# $ 0.00003942 / core / sec", "Memory (non-preemptible) $ 0.00000667 / GiB /
# sec", and "Sandboxes are billed at non-preemptible rates of 3x list price".
# The rate card's own FAQ: "each physical core is equivalent to 2 vCPUs as
# offered by AWS or GCP".
#
# So a 2 vCPU shape is ONE physical core, and the shape every table in this
# topic labels "2 vCPU / 4 GiB" is 1 core plus 4 GiB of memory. Charging 2
# cores for 2 vCPU is the 2x that turned USD 0.238 into USD 0.476, and the
# literal that stood here before was USD 0.76, which is the 8 vCPU / 8 GiB
# shape at this same rate card.
MODAL_CORE_USD_S = 0.00003942     # non-preemptible, per physical core per second
MODAL_GIB_USD_S = 0.00000667      # non-preemptible, per GiB per second
MODAL_VCPU_PER_CORE = 2           # stated on the page, quoted above
MODAL_PREEMPT_USD_S = 0.0000131   # preemptible, per physical core per second
MODAL_PREEMPT_GIB_USD_S = 0.00000222


def modal_rate(vcpu=2, gib=4, preemptible=False):
    cores = vcpu / MODAL_VCPU_PER_CORE
    if preemptible:
        return cores * MODAL_PREEMPT_USD_S * 3600 + gib * MODAL_PREEMPT_GIB_USD_S * 3600
    return cores * MODAL_CORE_USD_S * 3600 + gib * MODAL_GIB_USD_S * 3600


def modal_arithmetic():
    cores = 2 / MODAL_VCPU_PER_CORE
    cpu = cores * MODAL_CORE_USD_S * 3600
    mem = 4 * MODAL_GIB_USD_S * 3600
    rate = cpu + mem
    pre = modal_rate(preemptible=True)
    return [
        "Modal Sandbox at 2 vCPU / 4 GiB, non-preemptible (modal.com/pricing, read 2026-10-22)",
        "",
        "  2 vCPU / 2 vCPU-per-core = %.1f physical core" % cores,
        "  %.1f core  x %.8f USD/core/s x 3600 s = USD %.4f/h" % (cores, MODAL_CORE_USD_S, cpu),
        "  4 GiB      x %.8f USD/GiB/s  x 3600 s = USD %.4f/h" % (MODAL_GIB_USD_S, mem),
        "                                          = USD %.4f/h" % rate,
        "",
        "  USD 30 credit / %.4f = %.1f sandbox hours" % (rate, CREDIT / rate),
        "  300 h = USD %.2f    730 h = USD %.2f" % (rate * H300, rate * H730),
        "",
        "  the same shape at the preemptible Function rate = USD %.4f/h, %.1f hours for USD 30"
        % (pre, CREDIT / pre),
        "  ratio non-preemptible / preemptible = %.3f (the page states 3x)"
        % (rate / pre),
        "",
        "  what USD 0.76 would have been: the 8 vCPU / 8 GiB shape at this card =",
        "  %.4f core x %.8f x 3600 + 8 x %.8f x 3600 = USD %.4f/h"
        % (8 / MODAL_VCPU_PER_CORE, MODAL_CORE_USD_S, MODAL_GIB_USD_S,
           modal_rate(vcpu=8, gib=8)),
    ]


def rows():
    out = []

    # --- allocated, one rate per hour, from each provider's page ------------
    # zipbox Small USD 0.0137/h, Lizard Small USD 0.0162/h, boat USD 0.0180/h
    out.append(("zipbox Small", "allocated", 0.0137,
                allocated(0.0137), allocated(0.0137, H730)))
    out.append(("Lizard Small", "allocated", 0.0162,
                allocated(0.0162), allocated(0.0162, H730)))
    out.append(("boat small", "allocated", 0.0180,
                allocated(0.0180), allocated(0.0180, H730)))

    # --- Agent 37: USD 0.80/vCPU + 0.70/GB RAM + 0.09/GB disk per 730 h ----
    a37_compute = 0.80 * 2 + 0.70 * 4
    a37_disk = 0.09 * 4
    out.append(("Agent 37 2v/4GiB/4GiB",
                "compute while run, disk while kept",
                a37_compute / H730,
                allocated_with_keep(a37_compute, a37_disk),
                a37_compute + a37_disk))

    # --- E2B and Daytona: per-second allocated -----------------------------
    e2b = 0.000014 * 2 * 3600 + 0.0000045 * 4 * 3600
    out.append(("E2B 2v/4GiB", "allocated per second", e2b, e2b * H300, e2b * H730))
    day = 0.0504 * 2 + 0.0162 * 4
    out.append(("Daytona 2v/4GiB", "allocated per second", day,
                day * H300, day * H730))

    # --- Freestyle: gross rate, the allowance subtracted by hand -----------
    fsr = 0.04032 * 2 + 0.0129 * 4
    out.append(("Freestyle 2v/4GiB", "allocated per second", fsr,
                fsr * H300, fsr * H730))

    # --- Modal: derived, never typed --------------------------------------
    modal = modal_rate()
    out.append(("Modal Sandbox 2v/4GiB", "allocated per second, non-preemptible",
                modal, modal * H300, modal * H730))

    # --- Upstash: consumed CPU, and the keep-alive flat price --------------
    out.append(("Upstash Small, active CPU at 100%", "consumed CPU", 0.20,
                0.20 * H300, 0.20 * H730))
    out.append(("Upstash Small, keep-alive flat", "flat per box", 8.0 / H730,
                8.0 * (H300 / H730), 8.0))

    # --- Vercel: active CPU plus provisioned memory ------------------------
    vc_full = 0.128 * 2 + 0.0212 * 4
    vc_half = 0.128 * 2 * 0.5 + 0.0212 * 4
    out.append(("Vercel 2v/4GiB at 100% CPU",
                "active CPU + provisioned memory", vc_full,
                vc_full * H300, vc_full * H730))
    out.append(("Vercel 2v/4GiB at 50% CPU",
                "active CPU + provisioned memory", vc_half,
                vc_half * H300, vc_half * H730))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--modal", action="store_true",
                    help="print the Modal derivation alone")
    args = ap.parse_args()

    if args.modal:
        print("\n".join(modal_arithmetic()))
        return 0

    print("%-38s %-38s %9s %9s %9s"
          % ("provider", "model", "USD/h", "300h", "730h"))
    for name, model, per_h, m300, m730 in rows():
        print("%-38s %-38s %9.4f %9.2f %9.2f" % (name, model, per_h, m300, m730))

    print()
    print("\n".join(modal_arithmetic()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
