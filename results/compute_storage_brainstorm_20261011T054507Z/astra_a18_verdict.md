VERDICT: GO-WITH-CONDITIONS

The supplied evidence supports switching to MacPorts and installing the identified **package manager only**, subject to the corrections and installation checks below. It does not authorize research-engine provisioning.

For citations, `D/` means `results/compute_storage_brainstorm_20261011T054507Z/`; `I/` means `results/intel_setup_20261011/`; `E/` means `I/pkg_evidence/`.

F1. [severity: condition] **Homebrew’s supplied installation routes reject this Intel host, but the macOS wording needs precision.** The host is x86_64 running 14.8.9. The pkg requires arm64 and macOS ≥15. The fetched shell installer independently aborts on non-arm64 Macs; its separate macOS 14 check only prints an unsupported-version warning. Thus the switch has sufficient evidence without claiming every Homebrew installation is impossible. The support document also distinguishes potentially functional Tier 3 installations from configurations where Homebrew cannot run.  
Evidence: `I/inventory_20261011T0740Z.txt:6–8`; `E/Homebrew-7.0.9.pkg.Distribution.xml:6–10`; `E/Homebrew_install.sh_fetched_20261011:9–12,169–173,267,625–654`; `E/Homebrew_Support-Tiers_fetched_20261011.md:86–109,118–126,143–159`; `D/design.md:426`.  
Consequence: qualify “Homebrew 7 refuses Intel and macOS 14” by installer route; no unsupported Homebrew experiment is needed to justify MacPorts.

F2. [severity: note] **The recorded MacPorts identity and Distribution support this installer selection.** The receipt identifies SHA-256 `184ac171c201391a502958951867e77062010c781ade302b70b1f176e42d23d6`, Developer ID Installer **Joshua Root (QTA3A3B7F3)**, trusted notarization, and `spctl` acceptance. Distribution permits `arm64,x86_64` and macOS ≥14, <15, matching this host. It additionally rejects an ancient DarwinPorts installation and checks for `/usr/bin/xcodebuild`; CLT installation is recorded.  
Evidence: `E/signature_checks.txt:27–54`; `E/MacPorts-2.12.6-14-Sonoma.pkg.Distribution.xml:4–27,43`; `I/inventory_20261011T0740Z.txt:6–8`; `I/setup_log.md:22`.  
Consequence: acceptable for the bounded package-manager installation. These receipts do not establish compatibility of Neo4j, Java, Python, DuckDB, or other ports.

F3. [severity: condition] **The setup log contains an incorrect abbreviated MacPorts hash.** It gives `184ac171…e5a7fe`, whereas the receipt and amendment give a digest ending `e42d23d6`.  
Evidence: `I/setup_log.md:25`; `E/signature_checks.txt:54`; `D/decisions_log.md:208`.  
Consequence: correct this before it becomes a copied installation identity or handoff pin.

F4. [severity: note] **Amendment 18 preserves every obligation in design.md:242 by explicitly retaining that paragraph.** Real compatibility/identity checks remain mandatory; unavailable or incompatible native dependencies require reviewed change; silent cloud, Linux VM, version, and edition substitutions remain prohibited; alternatives still require separate budgets. Research-engine provisioning explicitly remains gated on the Intel specification and Astra review.  
Evidence: `D/decisions_log.md:210`; `D/design.md:239–245`; `D/integration_plan.md:23`.  
Consequence: no substantive waiver is granted. However, “whichever channel supplies them” must remain subordinate to the original review requirements. The amendment’s abbreviated fallback list omits **incompatibility, edition changes, and separate budgeting**; it is safe through incorporation of §242, not as a standalone replacement for it.

F5. [severity: condition] **One operative Homebrew reference is stale, and the blanket replacement instruction reaches a historical reference incorrectly.** The first sentence of design.md:242 still names Homebrew dependencies for Intel. Conversely, design.md:32 and the second sentence of :242 describe the **old M3 ARM provisioning evidence** and should continue to identify Homebrew accurately. Amendment 18 explicitly includes :32 in “every Homebrew reference … now means MacPorts ports,” which is too broad. Integration row I1 contains no literal Homebrew reference and retains the Intel repinning/review requirement.  
Evidence: `D/design.md:32,242`; `D/decisions_log.md:208`; `D/integration_plan.md:23`.  
Consequence: update prospective Intel instructions; preserve historical M3 facts and frozen-source descriptions.

F6. [severity: note] **Amendment 19 accurately records configured automatic login and carries the physical-access consequence into the future Drive-credential decision.** It records the operator’s choice, `autoLoginUser`, and `/etc/kcpassword` presence, consistent with the setup log. FileVault-off status has inventory evidence. The amendment explicitly requires the Drive question to restate both FileVault-off and automatic login; Drive authentication remains separately authorized. This establishes recorded configuration, not a demonstrated reboot/login test.  
Evidence: `D/decisions_log.md:197,216`; `I/setup_log.md:25`; `I/inventory_20261011T0740Z.txt:25–26`; `D/design.md:263,426`.  
Consequence: no further approval of automatic login is needed for this review. The eventual Drive-credential question must retain that disclosure; this review does not discharge it.

Required changes:

R1. Correct the Homebrew summary to distinguish **pkg architecture/OS rejection**, **shell-installer architecture rejection**, and **shell-installer OS warning**. Add the shell-source evidence to amendment 18. Addresses F1.

R2. Replace the incorrect setup-log abbreviation with the full MacPorts SHA-256 from `signature_checks.txt:54`. Addresses F3.

R3. Replace only the prospective Intel package-manager wording in design.md:242 and narrow amendment 18’s blanket replacement sentence. Preserve historical M3 Homebrew references and every remaining §242 obligation. Addresses F4–F5.

R4. Before installation, verify the **actual package copied to Intel** against that full digest and confirm the Distribution prerequisites. Installation remains limited to MacPorts itself; stop on a mismatch or failed prerequisite. The packet records that copying/installing had not yet occurred. Evidence: `I/setup_log.md:25`; `E/MacPorts-2.12.6-14-Sonoma.pkg.Distribution.xml:10–27`.

What I checked and did not check

- Recomputed all ten supplied subject-file hashes: **all match** the packet.
- Checked the local installer source, support-tier snapshot, Distribution XMLs, signature/notarization/hash receipt, amendments, hosting constraints, credential boundary, and Homebrew references in both design documents.
- Relied on the supplied provenance and MAESTRO receipts. I did not independently hash the actual pkg binary, repeat Apple signature assessment, verify the detached PGP signature, or independently retrieve GitHub’s asset digest.
- No files changed, installations, SSH sessions, reboot tests, dependency commissioning, or Drive activation occurred. R2–R5 discharge and the research-engine specification were outside this review.

🌱 graft reported ~9,687 tokens saved this turn, 1 successful call.