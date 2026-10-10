/* Browser measurements only: this module assigns no review verdict. */
(function (scope) {
  'use strict';

  const multiply = (left, right) => [
    left[0] * right[0] + left[2] * right[1],
    left[1] * right[0] + left[3] * right[1],
    left[0] * right[2] + left[2] * right[3],
    left[1] * right[2] + left[3] * right[3]
  ];

  function minimumScale(matrix) {
    const [a, b, c, d] = matrix;
    const sum = a * a + b * b + c * c + d * d;
    const determinant = a * d - b * c;
    return Math.sqrt(Math.max(0, (sum - Math.sqrt(Math.max(0, sum * sum - 4 * determinant * determinant))) / 2));
  }

  function transformMatrix(value) {
    if (!value || value === 'none') return [1, 0, 0, 1];
    const values = value.slice(value.indexOf('(') + 1, -1).split(',').map(Number);
    if (value.startsWith('matrix3d(') && values.length === 16) return [values[0], values[1], values[4], values[5]];
    if (value.startsWith('matrix(') && values.length === 6) return values.slice(0, 4);
    throw new Error('Unmeasured CSS transform: ' + value);
  }

  function zoomValue(value) {
    if (!value || value === 'normal') return 1;
    return value.endsWith('%') ? parseFloat(value) / 100 : parseFloat(value);
  }

  function renderedFontSize(element, style = getComputedStyle, pageZoom = 1) {
    const font = parseFloat(style(element).fontSize);
    if (element.namespaceURI === 'http://www.w3.org/2000/svg' && element.getScreenCTM) {
      const ctm = element.getScreenCTM();
      if (!ctm) return null;
      return font * minimumScale([ctm.a, ctm.b, ctm.c, ctm.d]) * pageZoom;
    }
    let matrix = [1, 0, 0, 1];
    let zoom = pageZoom;
    for (let ancestor = element; ancestor; ancestor = ancestor.parentElement) {
      const computed = style(ancestor);
      // CSS transforms do not act on ordinary non-replaced inline boxes.
      if (computed.display !== 'inline' && computed.display !== 'contents') matrix = multiply(transformMatrix(computed.transform), matrix);
      zoom *= zoomValue(computed.zoom);
    }
    return font * minimumScale(matrix) * zoom;
  }

  function parseColor(value) {
    if (!value || value === 'transparent' || value === 'none') return [0, 0, 0, 0];
    if (value[0] === '#') {
      let hex = value.slice(1);
      if (hex.length === 3 || hex.length === 4) hex = Array.from(hex, part => part + part).join('');
      if (hex.length === 6) hex += 'ff';
      return [0, 2, 4, 6].map((start, index) => parseInt(hex.slice(start, start + 2), 16) / (index === 3 ? 255 : 1));
    }
    if (value.startsWith('color(srgb ')) {
      const parts = value.slice(11, -1).replace('/', ' ').trim().split(/\s+/).map(Number);
      return [parts[0] * 255, parts[1] * 255, parts[2] * 255, parts[3] ?? 1];
    }
    const match = value.match(/^rgba?\((.+)\)$/);
    if (!match) throw new Error('Unmeasured CSS colour: ' + value);
    const parts = match[1].replace('/', ' ').split(/[\s,]+/).filter(Boolean);
    return parts.map((part, index) => part.endsWith('%') ? parseFloat(part) * (index === 3 ? 0.01 : 2.55) : Number(part)).concat(parts.length === 3 ? [1] : []);
  }

  function composite(front, back) {
    const alpha = front[3] + back[3] * (1 - front[3]);
    if (!alpha) return [0, 0, 0, 0];
    return front.slice(0, 3).map((value, index) => (value * front[3] + back[index] * back[3] * (1 - front[3])) / alpha).concat(alpha);
  }

  function effectivePixel(element, start, style = getComputedStyle) {
    let pixel = start;
    for (let ancestor = element; ancestor; ancestor = ancestor.parentElement) {
      const computed = style(ancestor);
      pixel = composite(pixel, parseColor(computed.backgroundColor));
      pixel[3] *= computed.opacity === undefined ? 1 : Number(computed.opacity);
    }
    return composite(pixel, [255, 255, 255, 1]);
  }

  function effectiveBackground(element, style = getComputedStyle) {
    return effectivePixel(element, [0, 0, 0, 0], style);
  }

  function luminance(color) {
    const linear = color.slice(0, 3).map(value => {
      const channel = value / 255;
      return channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4;
    });
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
  }

  function contrast(left, right) {
    const values = [luminance(left), luminance(right)].sort((a, b) => b - a);
    return (values[0] + 0.05) / (values[1] + 0.05);
  }

  function focusRing(element, style = getComputedStyle) {
    const computed = style(element);
    const width = parseFloat(computed.outlineWidth);
    const color = parseColor(computed.outlineColor);
    if (!width || computed.outlineStyle === 'none' || !color[3]) return null;
    const offset = parseFloat(computed.outlineOffset) || 0;
    const rect = element.getBoundingClientRect();
    const distance = offset + width / 2;
    const points = [0.25, 0.5, 0.75].flatMap(fraction => [
      [rect.left + rect.width * fraction, rect.top - distance],
      [rect.right + distance, rect.top + rect.height * fraction],
      [rect.left + rect.width * fraction, rect.bottom + distance],
      [rect.left - distance, rect.top + rect.height * fraction]
    ]);
    const limitations = [];
    const shadows = (computed.boxShadow === 'none' ? [] : (computed.boxShadow || '').match(/(?:rgba?\([^)]*\)|color\([^)]*\)|[^,])+/g) || []).flatMap(shadow => {
      if (/\binset\b/.test(shadow)) return [];
      const paint = shadow.match(/rgba?\([^)]*\)|color\(srgb [^)]*\)|#[\da-f]+/i)?.[0];
      if (!paint) { limitations.push('Unmeasured focus shadow: ' + shadow); return []; }
      const lengths = shadow.replace(paint, '').trim().split(/\s+/).map(parseFloat);
      if (lengths.length < 2 || lengths.some(value => !Number.isFinite(value)) || (lengths[2] || 0) !== 0) {
        limitations.push('Blurred or unsupported focus shadow requires pixel inspection: ' + shadow);
        return [];
      }
      return [{ color: parseColor(paint), x: lengths[0], y: lengths[1], spread: lengths[3] || 0 }];
    });
    let opacity = 1;
    for (let node = element; node; node = node.parentElement) opacity *= Number(style(node).opacity ?? 1);
    const samples = [];
    for (const [x, y] of points) {
      if (x < 0 || y < 0 || x >= innerWidth || y >= innerHeight) {
        limitations.push('Offset focus ring sample is outside the viewport');
        continue;
      }
      const outside = x < rect.left || x > rect.right || y < rect.top || y > rect.bottom;
      const stack = document.elementsFromPoint(x, y);
      const backdrop = stack.find(node => !(outside && (node === element || element.contains?.(node)))) || element.parentElement || document.documentElement;
      for (let node = backdrop; node; node = node.parentElement) if (style(node).backgroundImage !== 'none') limitations.push('Focus backdrop image requires pixel inspection: ' + address(node));
      let matte = [0, 0, 0, 0];
      for (const shadow of shadows.slice().reverse()) {
        if (outside && x >= rect.left + shadow.x - shadow.spread && x <= rect.right + shadow.x + shadow.spread && y >= rect.top + shadow.y - shadow.spread && y <= rect.bottom + shadow.y + shadow.spread) matte = composite(shadow.color, matte);
      }
      matte[3] *= opacity;
      const background = composite(matte, effectiveBackground(backdrop, style));
      const foreground = composite([color[0], color[1], color[2], color[3] * opacity], background);
      samples.push({ x, y, backdrop: address(backdrop), foreground, background, contrast: contrast(foreground, background) });
    }
    const lowest = samples.reduce((minimum, sample) => !minimum || sample.contrast < minimum.contrast ? sample : minimum, null);
    return { method: '12 side samples on the offset outline; composited DOM backdrop and zero-blur exterior shadows', offset_px: offset, width_px: width, contrast: lowest?.contrast ?? null, foreground: lowest?.foreground ?? null, background: lowest?.background ?? null, samples, limitations: Array.from(new Set(limitations)) };
  }

  function address(element) {
    if (element.id) return '#' + element.id;
    const path = [];
    for (let node = element; node && path.length < 5; node = node.parentElement) {
      const siblings = node.parentElement ? Array.from(node.parentElement.children).filter(sibling => sibling.tagName === node.tagName) : [];
      path.unshift(node.tagName.toLowerCase() + (siblings.length > 1 ? ':nth-of-type(' + (siblings.indexOf(node) + 1) + ')' : ''));
      if (node.id) { path[0] = '#' + node.id; break; }
    }
    return path.join(' > ');
  }

  function visible(element) {
    for (let node = element; node; node = node.parentElement) {
      const style = getComputedStyle(node);
      if (style.display === 'none' || style.visibility !== 'visible' || Number(style.opacity) === 0) return false;
    }
    const rect = element.getBoundingClientRect();
    if (rect.width > 0 && rect.height > 0) return true;
    const computed = getComputedStyle(element);
    return element.namespaceURI === 'http://www.w3.org/2000/svg' && (rect.width > 0 || rect.height > 0) && computed.stroke !== 'none' && parseFloat(computed.strokeWidth) > 0;
  }

  const rectangle = rect => ({ x: rect.x, y: rect.y, width: rect.width, height: rect.height, left: rect.left, right: rect.right, top: rect.top, bottom: rect.bottom });

  function clipping(element, rect) {
    const by = [];
    for (let ancestor = element; ancestor; ancestor = ancestor.parentElement) {
      const style = getComputedStyle(ancestor);
      const box = ancestor.getBoundingClientRect();
      if (/(hidden|clip|scroll|auto)/.test(style.overflowX) && (rect.left < box.left - 1 || rect.right > box.right + 1)) by.push({ element: address(ancestor), axis: 'x' });
      if (/(hidden|clip|scroll|auto)/.test(style.overflowY) && (rect.top < box.top - 1 || rect.bottom > box.bottom + 1)) by.push({ element: address(ancestor), axis: 'y' });
    }
    return by;
  }

  function scrollingDescendants() {
    return Array.from(document.querySelectorAll('*')).filter(element => visible(element) && element.scrollWidth > element.clientWidth + 1).map(element => {
      const computed = getComputedStyle(element);
      let container = null;
      for (let node = element; node; node = node.parentElement) if (/(hidden|clip|scroll|auto)/.test(getComputedStyle(node).overflowX)) { container = node; break; }
      const box = container?.getBoundingClientRect();
      const contained = box && box.left >= -1 && box.right <= innerWidth + 1;
      const expectedTable = Boolean(contained && container.matches('.table-wrap') && /(auto|scroll)/.test(getComputedStyle(container).overflowX));
      return { element: address(element), scroll_width: element.scrollWidth, client_width: element.clientWidth, overflow_x: computed.overflowX, rect: rectangle(element.getBoundingClientRect()), contained_by: container ? address(container) : null, expected_table_scroll: expectedTable, contributes_to_root_overflow: !contained };
    });
  }

  function measure(pageZoom = 1) {
    const limitations = new Set();
    const text = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      const element = node.parentElement;
      if (!node.textContent.trim() || !element || element.closest('script, style, template') || !visible(element)) continue;
      const range = document.createRange();
      range.selectNodeContents(node);
      const rect = range.getBoundingClientRect();
      if (!rect.width || !rect.height) continue;
      const style = getComputedStyle(element);
      for (let ancestor = element; ancestor; ancestor = ancestor.parentElement) {
        const computed = getComputedStyle(ancestor);
        if (computed.backgroundImage !== 'none') limitations.add('Background images/gradients require pixel inspection: ' + address(ancestor));
        if (computed.transform.startsWith('matrix3d(')) limitations.add('3D perspective text is measured from the projected x/y matrix: ' + address(ancestor));
      }
      const background = effectiveBackground(element);
      const rawColor = parseColor(element.namespaceURI === 'http://www.w3.org/2000/svg' ? style.fill : style.color);
      if (element.namespaceURI === 'http://www.w3.org/2000/svg') rawColor[3] *= Number(style.fillOpacity);
      const foreground = effectivePixel(element, rawColor);
      text.push({ element: address(element), text: node.textContent.trim(), computed_font_px: parseFloat(style.fontSize), rendered_font_px: renderedFontSize(element, getComputedStyle, pageZoom), foreground, background, contrast: contrast(foreground, background), rect: rectangle(rect), in_viewport: rect.bottom > 0 && rect.top < innerHeight && rect.right > 0 && rect.left < innerWidth, clipped_by: clipping(element, rect) });
    }

    const targets = Array.from(document.querySelectorAll('a[href], button, input, select, textarea, summary, [role="button"], [tabindex]')).filter(visible).map(element => ({ element: address(element), name: element.getAttribute('aria-label') || element.textContent.trim().slice(0, 150) || element.id, tag: element.tagName.toLowerCase(), tab_index: element.tabIndex, disabled: Boolean(element.disabled), rect: rectangle(element.getBoundingClientRect()) }));

    const paint = [];
    const marks = '[data-mark], .fact-cell, .gauge-mark, .gauge-reference, .write-mark, .write-track, .g-cell, .margin-mark';
    const elements = Array.from(document.querySelectorAll('svg rect, svg path, svg line, svg circle, svg polygon, svg polyline, ' + marks + ', a[href], button, input, select, textarea, summary, [tabindex]')).filter(visible);
    for (const element of elements) {
      const style = getComputedStyle(element);
      const innerBackground = effectiveBackground(element);
      const outerBackground = effectiveBackground(element.parentElement || element);
      const colors = element.namespaceURI === 'http://www.w3.org/2000/svg' ? [['fill', style.fill], ['stroke', style.stroke]] : ['Top', 'Right', 'Bottom', 'Left'].filter(side => parseFloat(style['border' + side + 'Width']) > 0 && style['border' + side + 'Style'] !== 'none').map(side => ['border-' + side.toLowerCase(), style['border' + side + 'Color']]);
      if (element.matches(marks)) colors.push(['mark-background', style.backgroundColor]);
      for (const [kind, color] of colors) {
        const raw = parseColor(color);
        if (kind === 'fill') raw[3] *= Number(style.fillOpacity);
        if (kind === 'stroke') raw[3] *= Number(style.strokeOpacity);
        if (!raw[3]) continue;
        const background = kind === 'mark-background' ? outerBackground : innerBackground;
        const foreground = kind === 'mark-background' ? innerBackground : effectivePixel(element, raw);
        const sameAsFill = kind.startsWith('border-') && raw.every((value, index) => value === parseColor(style.backgroundColor)[index]);
        if (!sameAsFill) paint.push({ element: address(element), class: element.getAttribute('class') || '', kind, color, foreground, background, contrast: contrast(foreground, background) });
        if (kind.startsWith('border-')) {
          paint.push({ element: address(element), class: element.getAttribute('class') || '', kind: kind + '-outside', color, foreground, background: outerBackground, contrast: contrast(foreground, outerBackground) });
        }
      }
      if (element.matches(':focus')) {
        const ring = focusRing(element);
        if (ring) {
          ring.limitations.forEach(value => limitations.add(value));
          if (ring.contrast !== null) paint.push({ element: address(element), class: element.getAttribute('class') || '', kind: 'focus-ring', color: style.outlineColor, ...ring });
        }
      }
    }

    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    const prose = Array.from(new Set(document.querySelectorAll('p, blockquote, [data-prose], .prose'))).filter(visible).map(element => {
      const style = getComputedStyle(element);
      context.font = style.font || [style.fontStyle, style.fontWeight, style.fontSize, style.fontFamily].join(' ');
      const fontScale = renderedFontSize(element, getComputedStyle, pageZoom) / parseFloat(style.fontSize);
      const zeroWidth = (context.measureText('0').width + (parseFloat(style.letterSpacing) || 0)) * fontScale;
      const width = element.getBoundingClientRect().width * pageZoom;
      return { element: address(element), text: element.textContent.trim().slice(0, 150), width_px: width, zero_width_px: zeroWidth, characters: zeroWidth ? width / zeroWidth : null };
    });
    const charts = Array.from(document.querySelectorAll('[data-chart]')).filter(visible).map(element => ({ element: address(element), caption: Array.from(element.querySelectorAll('.caption, [data-caption]')).filter(visible).map(node => node.textContent.trim()), caveat: Array.from(element.querySelectorAll('.caveat, [data-caveat], p')).filter(node => visible(node) && /does not mean/i.test(node.textContent)).map(node => node.textContent.trim()) }));
    const body = getComputedStyle(document.body);
    const content = document.querySelector('[data-region="content"]');
    const nav = Array.from(document.querySelectorAll('.top-nav [data-view]')).filter(visible);
    const badge = document.querySelector('#evidence-badge, .evidence-tier');
    const summary = {
      rendered_text_nodes: text.length,
      minimum_rendered_font_px: text.length ? Math.min(...text.map(node => node.rendered_font_px ?? Infinity)) : null,
      body_font_px: parseFloat(body.fontSize),
      body_rendered_font_px: renderedFontSize(document.body, getComputedStyle, pageZoom),
      minimum_text_contrast: text.length ? Math.min(...text.map(node => node.contrast)) : null,
      minimum_mark_border_focus_contrast: paint.length ? Math.min(...paint.map(mark => mark.contrast)) : null,
      minimum_target_width_px: targets.length ? Math.min(...targets.map(target => target.rect.width)) : null,
      minimum_target_height_px: targets.length ? Math.min(...targets.map(target => target.rect.height)) : null,
      maximum_prose_characters: prose.length ? Math.max(...prose.map(block => block.characters ?? 0)) : null,
      clipped_text_nodes: text.filter(node => node.clipped_by.length).length
    };
    return { url: location.href, page_zoom: pageZoom, viewport: { width: innerWidth, height: innerHeight, device_pixel_ratio: devicePixelRatio }, layout: { scroll_width: document.documentElement.scrollWidth, client_width: document.documentElement.clientWidth, scroll_height: document.documentElement.scrollHeight, horizontally_outside_viewport: targets.filter(target => target.rect.left < -1 || target.rect.right > innerWidth + 1).map(target => target.element), scrolling_descendants: scrollingDescendants(), canvases: Array.from(document.querySelectorAll('canvas')).filter(visible).map(element => ({ element: address(element), rect: rectangle(element.getBoundingClientRect()), height_fraction: element.getBoundingClientRect().height / innerHeight })) }, frame: { navigation: nav.map(element => ({ view: element.dataset.view, label: element.textContent.trim() })), breadcrumb: document.querySelector('#breadcrumb, .breadcrumb')?.textContent.trim() ?? null, context: document.querySelector('#context-chip, .context-chip')?.textContent.trim() ?? null, evidence_tier: badge && visible(badge) ? badge.textContent.trim() : null }, content_text: content?.textContent.trim() ?? null, summary, text, targets, paint, prose, charts, limitations: Array.from(limitations) };
  }

  const api = { renderedFontSize, parseColor, composite, effectiveBackground, effectivePixel, contrast, focusRing, address, visible, measure };
  scope.LabMeasure = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(globalThis);
