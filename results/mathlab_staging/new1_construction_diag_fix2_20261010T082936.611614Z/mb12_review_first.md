# Fresh same-family read-only review — superseded candidate

Reviewer: `/root/mb12_deadline_review`. Supplemental static evidence; no code/tests were executed, no files edited. GPT-6-Astra remains the binding reviewer.

Verdict: FIX-FIRST at identity SHA `989a40770928596ace3c9ce017f37fd78c9e6bd7cc0edb3b66edf82e940323dd`, construction SHA `1c3f4c71d0c7da3c4151db87ed2d85d65f30d6f1dad1bcaa32ab04d5514cfd60`, identity-test SHA `7a9a6d3b74fe600cb4784c5711cde6fc6c373e11743ab7538d8afc86e155c6b1`. Construction-test initial SHA `2bb0ab862cb0319704098e13f8bf9b177644395e9962977714d2567c5b9a426a` changed concurrently to `81c1b84995b3ae3ef04927f4a2d62232169f0b5972ae32c534685e908a958559`; that later test snapshot was not reviewed.

1. Identity lines 462–478: `alarm_unwinding=True` unconditionally defers further alarms after the one-shot is consumed. Under `seconds=.4`, `try: time.sleep(2); finally: time.sleep(2)` reaches its active callback finally after the work alarm at approximately .2 seconds and overruns the original end by approximately 2 seconds. No caught or suppressed Stop is required.

2. Identity lines 454–478, 557, 587: a direct registered-worker monitor raises an ordinary primary error. Inject SIGALRM at the supervise trace exception event before matching context exit. The generator is suspended; no exit frame is active; a second pulse can report RSS 11 and replace the original error before the outer handler captures it. Ownership still reaches cleanup. The existing clearing=True injection exercises a later window.

3. Identity lines 458–463, 490–492, 550–552: delay launch context entry after arming its timer and before restoring the blocked signal mask. The pending alarm is deferred because the owning generator is executing, consuming the one-shot before yielding into a stalled OwnedWorker.start. Launch and terminal bodies enter blocking operations before their cancellation checks. Removing alarm_unwinding alone does not close this.

Repeated first-error delivery can interrupt ordinary active callback cleanup before the original end. At terminal recording, the first alarm may occur exactly at the absolute end, leaving no remaining budget for another alarm. A fail-stop must prevent an accepted terminal receipt or Python return at that boundary. No numerical changes were suggested.

Dynamic reproductions were subsequently saved in `red_mb12_review_schedules.log/.json` (3 methods, 5 failures) and `red_mb12_terminal_end.log/.json` (1 method, 1 failure). This review does not cover the later explicit-phase candidate.
