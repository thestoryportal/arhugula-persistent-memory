"""LabvizMoves wire seam that icm21_check.py loads by file path.

LabvizMoves stays outside the approved wire scope, as before this seam,
until the D2 MapBinding parser (plan Step 15) replaces this rejection.
The rejection is a TypeError, not a ValueError: wire() catches ValueError per
example as an observed FAIL, which would match an expected FAIL. A TypeError
fails the whole run, as the scope check did before this seam.
"""


def validate_labviz_moves(value, schema, fixtures, root):
    raise TypeError('wire type outside approved scope')
