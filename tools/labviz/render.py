"""Saved evidence pictures and a static, accessible HTML notebook."""
import html
import json
from pathlib import Path
import textwrap
from PIL import Image, ImageDraw, ImageFont

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
from jinja2 import Environment, FileSystemLoader, select_autoescape

PACKAGE = Path(__file__).resolve().parent
MISSING = 'not recorded for this run'
COLORS = {'write': '#47e6b1', 'injection': '#ab9fff', 'candidate': '#ffd16a',
          'stopped': '#ff858d', 'inconclusive': '#67cfff'}
plt.rcParams.update({'font.size': 9, 'text.color': '#f3f6fc', 'axes.labelcolor': '#f3f6fc',
                     'xtick.color': '#f3f6fc', 'ytick.color': '#f3f6fc', 'axes.edgecolor': '#64728e',
                     'axes.facecolor': '#101b30', 'figure.facecolor': '#101b30',
                     'svg.fonttype': 'none', 'svg.hashsalt': 'labviz', 'font.family': 'DejaVu Sans'})


def wrap(text, width=48):
    return '\n'.join(textwrap.wrap(str(text), width, break_long_words=True))


def score_text(r):
    if r.get('score_label'):
        return r['score_label']
    if r['score'] is not None:
        unit = 'reworded answers' if r.get('source','').startswith('results/c10') else 'recorded observations'
        return f'{r["score"]} of {r["out_of"]} {unit}' if r['out_of'] is not None else f'{r["score"]} right (total not recorded)'
    if r['percent'] is not None:
        unit='reworded answers' if r.get('source','').startswith('results/c10') else 'recorded measure'
        return f'{r["percent"]}% {unit} (counts {MISSING})'
    return f'Answer score: {MISSING}'


def side_text(r):
    s = r['side']
    lines = []
    for label, key, total in [('Real facts flipped', 'L1_flipped_to_edited_value','L1_n'),
                              ('Unrelated facts kept','L3_top1_agree','L3_n')]:
        lines.append(f'{label}: {s[key]}/{s[total]}' if s[key] is not None and s[total] is not None else f'{label}: {MISSING}')
    a,b = s['generic_ppl_pre'],s['generic_ppl_post']
    lines.append(f'Writing difficulty: {a} → {b} (lower is easier)' if a is not None and b is not None else f'Writing quality: {MISSING}')
    if s.get('relation_flips'):
        lines.append('Other relation flips: ' + ', '.join(f'{k} {v}' for k,v in s['relation_flips'].items()))
    if s.get('same_frame_flips') is not None:
        lines.append(f'Same wording, other subjects flipped: {s["same_frame_flips"]}')
    return lines


def image(r, path):
    grid = r.get('grid')
    heading = r['model'] + '\n' + wrap(r['title'], 54)
    header_height = max(1.35, .23 * len(heading.splitlines()) + .9)
    heights = [header_height, max(1.4, .18 * len(grid)) if grid else .65, 1.65 if r['curves'] else .65,
               1.65 if r['losses'] else .65, 1.4]
    if r.get('outcomes') or r['measurements'] and r['score'] is None and r['percent'] is None:
        heights.append(max(1.5, .17 * len(r['measurements'])))
    fig, axes = plt.subplots(len(heights), 1, figsize=(5.1, sum(heights)), gridspec_kw={'height_ratios': heights})
    for ax in axes:
        ax.set_axis_off()
    axes[0].text(-.32, .96, heading, va='top', weight='bold', fontsize=10)
    axes[0].text(-.32, .08, wrap(score_text(r), 60), color='#47e6b1')
    if grid:
        ncols = max((len(row) for row in grid), default=0)
        if ncols:
            values = np.full((len(grid), ncols), 2)
            for i,row in enumerate(grid):
                for j,v in enumerate(row):
                    values[i,j] = 1 if v is True else 0 if v is False else 2
            ax = axes[1]; ax.set_axis_on()
            ax.imshow(values, aspect='auto', interpolation='none', cmap=ListedColormap(['#ff858d','#47e6b1','#53617b']), vmin=0, vmax=2)
            ax.set_title(wrap(r['grid_label'], 48), color='#f3f6fc', fontsize=9, loc='left')
            ax.set_xticks(range(ncols), [f'Q{j+1}' for j in range(ncols)])
            ax.set_yticks(range(len(grid)), r['fact_labels'] or [str(i+1) for i in range(len(grid))], fontsize=9)
            ax.set_xlabel('Green ✓ right · red × wrong · grey ? unrecorded', fontsize=9)
    else:
        axes[1].text(-.32,.6, wrap('Fact × rewording grid: ' + MISSING,60), va='center')
    if r['curves']:
        ax = axes[2]; ax.set_axis_on()
        for c in r['curves']:
            ax.scatter(range(1,len(c['probs'])+1), c['probs'], s=12, alpha=.65)
        ax.set_ylim(-.03,1.03); ax.set_ylabel('Probability'); ax.set_xlabel('Answer piece (token)')
        ax.set_title('Recorded word-by-word confidence; dots only', loc='left', fontsize=9)
    else:
        axes[2].text(-.32,.6, wrap('Word-by-word confidence: ' + MISSING,60), va='center')
    if r['losses']:
        ax = axes[3]; ax.set_axis_on(); x,y=zip(*r['losses']); ax.scatter(x,y,color='#67cfff',s=10)
        ax.set_xlabel('Training step'); ax.set_ylabel('Loss'); ax.set_title('Training mistakes (loss); lower is better', loc='left', fontsize=9)
    else:
        axes[3].text(-.32,.6, wrap('Training loss: ' + MISSING,60), va='center')
    axes[4].text(-.32,1, '\n'.join(wrap(x, 58) for x in side_text(r)), va='top', fontsize=9)
    if len(axes)>5:
        ax = axes[5]
        if r.get('outcomes'):
            lines=[]
            for i,label in enumerate(r['outcomes']['columns']):
                values=[row[i] for row in r['outcomes']['values']]
                lines.append(f'{label}: {values.count(True)} true / {values.count(False)} false / {values.count(None)} unrecorded')
            ax.text(-.32,1,wrap('All saved per-fact outcomes\n'+'\n'.join(lines),58),va='top',fontsize=9)
        elif r['measurements']:
            ax.set_axis_on(); labels,values=zip(*r['measurements']); positions=range(len(values))
            ax.scatter(values,positions,color='#67cfff',s=12);ax.set_yticks(list(positions),[wrap(x,25) for x in labels],fontsize=9)
            ax.invert_yaxis();ax.set_title('Recorded fields (first 16; original units)',loc='left',fontsize=9)
    fig.subplots_adjust(left=.29,right=.96,top=.98,bottom=.04,hspace=.85)
    fig.savefig(path.with_suffix('.svg'), metadata={'Date': None})
    fig.savefig(path.with_suffix('.png'), dpi=110, metadata={'Software': 'Lab View'})
    metadata={'width_px':561,'text_px':[t.get_fontsize()*110/72 for t in fig.findobj(matplotlib.text.Text) if t.get_text()]}
    plt.close(fig)
    return metadata


def picture_readable(metadata, display_width):
    return bool(metadata.get('text_px')) and min(metadata['text_px'])*display_width/metadata['width_px'] >= 13


def card_picture(card, path):
    """Save a compact SVG/PNG directly from typed leaves; no browser is needed."""
    width=561; size=14; lines=[]
    def val(x): return x.get('value') if isinstance(x,dict) else x
    def text(s): lines.extend(textwrap.wrap(str(s),66,break_long_words=True) or [''])
    text(val(card['context'].get('question')) or 'Recorded observation')
    text(val(card['identity'].get('model')) or 'model not recorded')
    text('RECORDED · '+card['identity']['field'])
    for name,quantity in card.get('headline',{}).items():
        if val(quantity) is not None: text(name.replace('_',' ')+': '+str(val(quantity)))
    if val(card.get('label')) is not None: text('Recorded label: '+str(val(card['label'])))
    text(val(card.get('oracle_class')) or '')
    strip=[]
    for f in card.get('per_fact',[]):
        hits=val(f['rewordings_hit']); strip.append(hits if isinstance(hits,list) else [None])
    if strip: text('Teacher-forced complete answer positions' if card['per_fact'][0]['hit_kind']=='teacher-forced' else 'Recorded complete-answer outcomes')
    heights=22*len(lines)+40; gridheight=22*len(strip)
    layers=card.get('per_layer',[]); height=heights+gridheight+22*len(layers)+70
    png=Image.new('RGB',(width,height),'#101b30'); draw=ImageDraw.Draw(png); font=ImageFont.load_default(size=size)
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>Recorded card {card["card_id"]}</title><rect width="100%" height="100%" fill="#101b30"/>']
    text_sizes=[]
    def write(s,x,y):
        draw.text((x,y),s,font=font,fill='#f3f6fc')
        svg.append(f'<text x="{x}" y="{y+size}" font-family="sans-serif" font-size="{size}" fill="#f3f6fc">{html.escape(s)}</text>'); text_sizes.append(size)
    y=16
    for s in lines: write(s,16,y); y+=22
    for i,row in enumerate(strip):
        write(str(val(card['per_fact'][i]['subject']) or i+1),16,y)
        for j,hit in enumerate(row):
            colour='#47e6b1' if hit is True else '#ff858d' if hit is False else '#53617b'; x=210+40*j
            draw.rectangle((x,y,x+32,y+18),fill=colour); svg.append(f'<rect x="{x}" y="{y}" width="32" height="18" fill="{colour}"/>')
            write('+' if hit is True else 'x' if hit is False else '?',x+10,y)
        y+=22
    peak=val(card.get('scale',{}).get('max')) or 1
    for layer in layers:
        amount=val(layer['write_size']); written=val(layer['written']); bar=250*amount/peak if written else 0
        write('Layer '+str(layer['layer']),16,y)
        if val(layer['configured']):
            draw.rectangle((110,y,360,y+18),outline='#f3f6fc'); svg.append(f'<rect x="110" y="{y}" width="250" height="18" fill="none" stroke="#f3f6fc"/>')
        if written:
            draw.rectangle((110,y,110+bar,y+18),fill='#47e6b1'); svg.append(f'<rect x="110" y="{y}" width="{bar}" height="18" fill="#47e6b1"/>')
        write(f'{amount:.6g}' if written else 'not written',372,y); y+=22
    write('Full precision and sources: '+card['card_id']+'.json',16,y+20)
    path.with_suffix('.svg').write_text(''.join(svg)+'</svg>\n')
    png.save(path.with_suffix('.png'),optimize=False)
    return {'width_px':width,'text_px':text_sizes,'renderer':'SVG/Pillow'}


def history_svg(inv):
    rows=inv['history']; width=900; rowheight=83; height=100+len(rows)*rowheight
    x0,x1=390,850
    def x(score):return x0+(x1-x0)*score/72
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
         '<title id="title">Every scoreboard result, in date order</title><desc id="desc">Scores are separate recorded observations. No line estimates values between runs. Unscored rows remain visible.</desc>',
         f'<rect width="{width}" height="{height}" fill="#101b30"/>',
         '<g fill="#f3f6fc" font-family="system-ui" font-size="16">']
    for score,label,color in [(0,'0','#c5d2e9'),(14,'Usual method ≈14','#ffd16a'),(61,'Goal 61','#47e6b1'),(72,'72','#c5d2e9')]:
        xx=x(score);out.append(f'<path d="M{xx},50 V{height-20}" stroke="{color}" stroke-dasharray="5 5"/><text x="{xx}" y="25" text-anchor="middle">{label}</text>')
    for i,r in enumerate(rows):
        y=80+i*rowheight;color=COLORS.get(r.get('kind'),'#67cfff'); name=html.escape(r['title']);model=html.escape(r['model'])
        out.append(f'<a href="#'+r['id']+f'"><text x="12" y="{y}">{r["date"]} · {name[:42]}</text><text x="12" y="{y+23}" font-size="13">{model} · {html.escape(r["score_label"])}</text>')
        if r['score'] is not None:
            out.append(f'<circle cx="{x(r["score"])}" cy="{y}" r="9" fill="{color}"/><text x="{x(r["score"])+15}" y="{y+5}">{r["score"]}</text>')
        else:
            out.append(f'<text x="{x0}" y="{y}" fill="{color}">not scored</text>')
        out.append('</a>')
    return ''.join(out)+ '</g></svg>'


def render_page(inv, evaluations):
    env=Environment(loader=FileSystemLoader(PACKAGE),autoescape=select_autoescape(['html']))
    env.filters['score']=score_text;env.filters['side']=side_text
    env.filters['source_url']=lambda s:'evidence/'+s.split(':',1)[0]
    return env.get_template('index.html').render(**inv,evaluations=evaluations['entries'],missing=MISSING)
