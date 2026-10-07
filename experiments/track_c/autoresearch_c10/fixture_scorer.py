"""Inert private scorer; deliberately includes a private output sentinel."""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from v13_common import ARMS, digest, validate_handoff, verify, write_json
verify(Path(__file__).resolve().parent, sys.argv[1])
run = Path(sys.argv[2])
validate_handoff(run)
for arm in ARMS:
    saved = json.loads((run / (arm + '.pt')).read_text())
    if saved != {'model.layers.4.mlp.down_proj.weight': [0.0001]}:
        raise SystemExit('inert tensor fixture rejected')
s = {'heldout_full': 7, 'canon': 7, 'first_token': 40, 'A1': 69, 'A2': 69,
     'L1_flips': 0, 'frame_flips': 1, 'described_as': 90.38, 'L3': 30,
     'ppl_post': 21.506, 'law5_ok': True, 'scope_ok': True, 'dw_total': 88.974,
     'edit_seconds': 0.0, 'score_seconds': 0.0, 'guards': 'ok'}
write_json(run / 'score.json', {'summary': s, 'private_sentinel': 'PRIVATE_SCORER_FIXTURE'})
print('PRIVATE_SCORER_FIXTURE')
