## 1. Purpose and Paradigm

This specification defines a multi-agent development harness that treats a Large Language Model's Feed Forward Network (FFN) as a physically queryable and editable graph database. The system coordinates agent workflows across two parallel state mediums — a Git repository (deterministic syntactic state) and a versioned parametric overlay (the `.vindex` layer, representing semantic state physically encoded in model weights via the MEMIT algorithm).

The paradigm shift is from **in-context learning** (retrieval-augmented generation, transient context windows) to **in-weight learning** (permanent, zero-latency semantic memory physically wired into model pathways). Agent outputs that pass validation are not merely committed to a repository — they are compiled into the model itself, such that subsequent agents natively "know" the project's architectural state without requiring prompt reconstruction.

The harness is a specification framework, not an implementation. It defines:
- What components exist and what each must guarantee.
- How components interface with one another (the Interface Contract catalog in Appendix B).
- What threats the system defends against and what it assumes about its deployment environment (Part II).
- Which questions remain empirical or operational and are deliberately left open (Part V).

