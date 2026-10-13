# Astra review packet — D-HW-2 amendments 18–19 (Intel package manager; Intel auto-login)

You are the cross-family reviewer. Read-only. Work from the files below in this repository; cite `path:line` for every claim.

## Question
Amendment 18 replaces Homebrew with MacPorts as the Intel Mac's package manager, after Homebrew's installer refused the machine. `design.md:242` says: re-pin Intel/Sonoma dependencies "through actual compatibility/identity checks… If the chosen native packages are unavailable/incompatible, stop for a reviewed hosting change; do not silently switch to a cloud database, Linux VM, different version or different edition." This is that review.

Decide:
1. Is the evidence sufficient that Homebrew is unavailable/unsuitable for this host (x86_64, macOS 14.8.9)? Note `install.sh` behaviour on macOS 14 as well as the pkg.
2. Is MacPorts-2.12.6-14-Sonoma.pkg an acceptable, correctly identified installer to install now (identity: hash, signer, notarization, Distribution constraints)?
3. Does amendment 18 preserve every design.md:242 obligation (re-pin through real checks; stop-for-review on unavailability; no silent version/edition/VM/cloud switch) and avoid granting research-engine provisioning? Name any wording that weakens them.
4. Is amendment 19 (auto-login with FileVault off) recorded accurately, with its consequence carried to the Drive-credential question?
5. Anything in design.md / integration_plan.md that still names Homebrew for the Intel host and is now inconsistent.

Out of scope: R2–R5 discharge, the research-engine spec, Drive activation itself.

## Verdict format
First line: `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`. Then numbered findings `F<n>. [severity: blocker|condition|note] <claim>. Evidence: path:line. Consequence: …`, then required changes `R<n>`, then "What I checked and did not check".

## Subject files (SHA-256 at packet time)
- `results/compute_storage_brainstorm_20261011T054507Z/decisions_log.md` d4a86db838d576cb38d19a7a16f96e6731d29888a348d356b423ff75224d0757
- `results/compute_storage_brainstorm_20261011T054507Z/design.md` bd22f5d2c9d53bf043f71de31082947af41d680b18b9bebee48f7c90797753cc
- `results/compute_storage_brainstorm_20261011T054507Z/integration_plan.md` b650e88071e987b84006e2467c4a8c8a42deee0bdc35504ac6f652f4a870d8a7
- `results/intel_setup_20261011/setup_log.md` dfeb9a21a418343fb7f417df3c75b2d3dea10cb385293c1b5a07aec39cea9e31
- `results/intel_setup_20261011/pkg_evidence/Homebrew_install.sh_fetched_20261011` 5f333bbe53bc490e51e7ccb1df8779b3dd6ee73a1a7379efda216edb08ccb148
- `results/intel_setup_20261011/pkg_evidence/Homebrew_Support-Tiers_fetched_20261011.md` 5905e1b47de98283e20edf31697922fb82d6f9dced20dc6e929cf587a49ee23c
- `results/intel_setup_20261011/pkg_evidence/Homebrew-7.0.9.pkg.Distribution.xml` 4728392a2e2b1cebd069db9e87eb6af5d89ac9aa1d4f695f3229e514bdf8b027
- `results/intel_setup_20261011/pkg_evidence/MacPorts-2.12.6-14-Sonoma.pkg.asc` 031a3cd3710400456b9641c542edc50a65462d208f2ed4c1f278da9945e5a7fe
- `results/intel_setup_20261011/pkg_evidence/MacPorts-2.12.6-14-Sonoma.pkg.Distribution.xml` ed7177157b0baf78ea168eb197430551adaf8261232e0349fe96e9feaaf1ad45
- `results/intel_setup_20261011/pkg_evidence/signature_checks.txt` 6c14377009aeb5712542788776497d0a6a233f23bab1fb5281c29c30b15f2d2b

Notes: `pkg_evidence/signature_checks.txt` is MAESTRO's local `pkgutil --check-signature` / `spctl` / `shasum` output for both pkgs; the Distribution XMLs were extracted with `xar` from those exact pkgs; Support-Tiers.md and install.sh were fetched from GitHub (Homebrew/brew, Homebrew/install default branches) on 2026-10-11. Amendment text: the last two sections of decisions_log.md and the final paragraph of design.md. Machine facts: setup_log.md and `results/intel_setup_20261011/inventory_20261011T0740Z.txt`.
