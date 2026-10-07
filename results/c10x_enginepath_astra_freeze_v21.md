**FIX-FIRST**

**BLOCKING — Prior blocker 4 remains partial.** The revised [X1-(ii) predicate](docs/C10X_ENGINEPATH_PREREG.md:72) allows relative error ≤1e-4, but [§5](docs/C10X_ENGINEPATH_PREREG.md:188) still names “X1-(ii) non-zero distance” as a halt trigger. The [§8 fold log](docs/C10X_ENGINEPATH_PREREG.md:237) also retains “any resulting distance HALTs.”

Exact replacements:

- In §5, replace the X1-(ii) predicted-halt clause with:

  > X1-(ii) failure of its declared acceptance predicate (returned-z relative error >1e-4 for a nonzero reference, measured floor >1e-5, unequal step counts, or unequal zero-reference outputs; fix: reconcile the reduced path with §2.3’s declared arithmetic and rerun X1-(ii) once). A nonzero distance within the declared tolerance is not itself a halt trigger.

- In §8, Codex #16, replace the parenthetical with:

  > (a position with exactly-zero engine CE takes the constant branch; acceptance follows the X1-(ii) predicate amended in v2.1, not an exact-equality requirement for nonzero references)

Blockers 1, 2, 3 and 5 are fixed equivalently. No other blocking contradiction found in the full v2.1 document.