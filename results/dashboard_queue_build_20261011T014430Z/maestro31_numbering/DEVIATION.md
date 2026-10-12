# MAESTRO31 numbering fix (operator report, 2026-10-11 ~02:45Z)

Operator saw item numbers 1, 3, 8, 2, 4, 5, 6, 7, 9 in the queue tab: Q3's height-limited view moves
running / needs-you / in-review items to the top but kept each item's stored queue position as its number.
Operator wants numbers to follow the order on screen.

One-line change by MAESTRO (not a builder): after the priority sort in `render`, items are renumbered in display
order (tools/dashboard_queue.py, the line after `ordered.sort(...)`). Test-first: test_q3_03 now expects
`1. Active priority … 4. [READY] Low priority first`; RED = 1 error (substring not found, red_detail.log),
GREEN = 40/40 (green.log). Before copies + hashes: this dir.
