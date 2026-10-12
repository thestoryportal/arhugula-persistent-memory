**DISAGREE.** The record should carry **INVALID-CONTROLS-UNDERFIT**: control failure determines the primary outcome and interpretation; it does not erase the required fit qualifier.

- [CORPUS/58:39](CORPUS/58_C10X_ENGINEPATH.md:39) explicitly concludes “so no -UNDERFIT is recorded on this arm.” That is the disputed error.
- [Prereg:86](docs/C10X_ENGINEPATH_PREREG.md:86) requires the I-2 label to carry **-UNDERFIT** when fewer than 22/24 targets meet the fit threshold. [Prereg:149](docs/C10X_ENGINEPATH_PREREG.md:149) reinforces “every applicable one recorded.” The saved target array confirms **3/24**.
- Crucially, [prereg:157](docs/C10X_ENGINEPATH_PREREG.md:157) says interpretation **“does not change any label.”** Row 2 preceding row 4 therefore selects the control-failure interpretation; it cannot suppress a qualifier.
- The competing reading has some textual support: [prereg:140](docs/C10X_ENGINEPATH_PREREG.md:140) defines the base-class table for control-passing arms, and qualifiers follow that table. But this does not expressly exempt INVALID-CONTROLS from §2.5’s mandatory qualifier. The reader adds that exemption at [reader:445–451](experiments/track_c/c10x_enginepath_read.py:445).

**The frozen prereg binds over its implementation. Yes, record an append-only erratum**, preserving the original reader output as provenance. The earlier review confirmed reader reproduction but missed this compliance issue. No advancement, replication, or mechanism conclusion changes.

Exact wording:

> **Erratum — I-2 qualifier.** The prereg-compliant reported label is **INVALID-CONTROLS-UNDERFIT**. A1 64/72 and A2 65/72 fail the 68/72 control floor, so INVALID-CONTROLS remains the primary outcome and interpretation row 2 applies. Independently, only 3/24 A7 z₄ targets meet fit ≥0.98 against the required 22/24; §2.5 therefore requires -UNDERFIT. Interpretation precedence does not remove qualifiers (§3:157). The pinned reader emitted INVALID-CONTROLS with an empty qualifier list because it suppresses qualifiers on control-failing arms; that historical output is preserved, and this prereg–reader discrepancy is recorded explicitly. I-2 remains not advanced and ineligible for replication; no spreading or method-family conclusion follows.

🌱 graft reported ~167,525 tokens saved (~$0.09), 1 successful call.

