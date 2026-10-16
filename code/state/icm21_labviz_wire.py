"""LabvizMoves wire seam that icm21_check.py loads by file path.

LabvizMoves stays outside the approved wire scope, as before this seam,
until the D2 MapBinding parser (plan Step 15) replaces this rejection.
"""


def validate_labviz_moves(value, schema, fixtures, root):
    raise ValueError('wire type outside approved scope')
