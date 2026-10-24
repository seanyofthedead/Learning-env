/* AI and the Federal Financial Manager: two live demos.
 * Synthetic demonstration data. Outputs replay from cache.json by default.
 *
 * The render functions below are pure (data in, HTML string out) so that
 * scripts/headless_run.js can run both demos in Node for preflight.
 */
(function () {
  'use strict';

  var PARTS = ['role', 'task', 'context', 'output'];
  var LAST_STEP = { demo1: 6, demo2: 3 };   // step 0 is the title card
  var LIVE_TIMEOUT_MS = 5000;

  // ------------------------------------------------------------ helpers
  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function inline(s) { return esc(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>'); }
  function fmtTime(sec) {
    var neg = sec < 0; sec = Math.abs(Math.round(sec));
    return (neg ? '-' : '') + Math.floor(sec / 60) + ':' + ('0' + (sec % 60)).slice(-2);
  }
  function parseTime(t) { var p = String(t).split(':'); return (+p[0]) * 60 + (+p[1]); }

  // ------------------------------------------------------------ markdown subset
  function splitRow(r) {
    return r.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(function (c) { return c.trim(); });
  }
  function isSeparator(cells) { return cells.every(function (c) { return /^:?-{2,}:?$/.test(c); }); }
  function renderTable(lines) {
    var rows = lines.map(splitRow).filter(function (r) { return !isSeparator(r); });
    var head = rows[0], body = rows.slice(1);
    return '<div class="table-wrap"><table class="md-table"><thead><tr>' +
      head.map(function (c) { return '<th>' + inline(c) + '</th>'; }).join('') +
      '</tr></thead><tbody>' +
      body.map(function (r) {
        return '<tr>' + r.map(function (c) { return '<td>' + inline(c) + '</td>'; }).join('') + '</tr>';
      }).join('') + '</tbody></table></div>';
  }
  function renderMarkdown(md) {
    var lines = String(md || '').replace(/\r/g, '').split('\n'), out = [], i = 0;
    var BLOCK = /^\s*(\||[-*] |\d+[.)] |#{1,6}\s)/;
    while (i < lines.length) {
      var line = lines[i], buf = [];
      if (!line.trim()) { i++; continue; }
      if (/^\s*\|/.test(line)) {
        while (i < lines.length && /^\s*\|/.test(lines[i])) buf.push(lines[i++]);
        out.push(renderTable(buf)); continue;
      }
      if (/^\s*[-*] /.test(line)) {
        while (i < lines.length && /^\s*[-*] /.test(lines[i])) buf.push(lines[i++].replace(/^\s*[-*] /, ''));
        out.push('<ul>' + buf.map(function (t) { return '<li>' + inline(t) + '</li>'; }).join('') + '</ul>'); continue;
      }
      if (/^\s*\d+[.)] /.test(line)) {
        while (i < lines.length && /^\s*\d+[.)] /.test(lines[i])) buf.push(lines[i++].replace(/^\s*\d+[.)] /, ''));
        out.push('<ol>' + buf.map(function (t) { return '<li>' + inline(t) + '</li>'; }).join('') + '</ol>'); continue;
      }
      var h = /^#{1,6}\s+(.*)$/.exec(line);
      if (h) { out.push('<h4 class="md-h">' + inline(h[1]) + '</h4>'); i++; continue; }
      while (i < lines.length && lines[i].trim() && !BLOCK.test(lines[i])) buf.push(lines[i++].trim());
      out.push('<p>' + inline(buf.join(' ')) + '</p>');
    }
    return out.join('\n');
  }

  // ------------------------------------------------------------ outputs (cache or live)
  function outputFor(cache, ctx, demo, key) {
    var live = ctx && ctx.live && ctx.live[demo + '/' + key];
    if (live && live.source === 'live') return live.markdown;
    if (demo === 'demo1') {
      return cache.demo1.stages.filter(function (s) { return s.id === key; })[0].output.markdown;
    }
    return cache.demo2.steps.filter(function (s) { return s.id === key; })[0].output.markdown;
  }
  function sourceBadge(ctx, demo, key) {
    if (!ctx || !ctx.liveMode) return '';
    var l = ctx.live && ctx.live[demo + '/' + key];
    if (!l) return '';
    if (l.source === 'pending') return '<span class="src src-pending">Asking the model…</span>';
    if (l.source === 'live') return '<span class="src src-live">Live: ' + esc(l.model || '') + '</span>';
    return '<span class="src src-cache">Saved output (' + esc(l.reason || 'live unavailable') + ')</span>';
  }
  function outputBody(cache, ctx, demo, key) {
    var l = ctx && ctx.live && ctx.live[demo + '/' + key];
    if (l && l.source === 'pending') {
      return '<p class="pending">Asking the model… the saved output appears if this takes more than 5 seconds.</p>';
    }
    return renderMarkdown(outputFor(cache, ctx, demo, key));
  }

  // Where the on-screen answers came from. Shown on every output panel and in the footer.
  function sourceLine(cache) {
    var g = (cache && cache.generation) || {};
    if (g.mode === 'chat-recorded' || g.mode === 'copilot-recorded') return 'Recorded live in ' + (g.model || 'Microsoft 365 Copilot') + ' on ' + (g.generated_at || '?');
    if (g.mode === 'model-generated') return 'Pre-generated with ' + (g.model || 'a model') + ' on ' + (g.generated_at || '?');
    return 'Representative pre-generated example, not a live AI run';
  }
  function sourceTag(cache) {
    var g = (cache && cache.generation) || {};
    var t = (g.mode === 'chat-recorded' || g.mode === 'copilot-recorded') ? 'Recorded in ' + (g.model || 'Copilot') + ' \u00b7 ' + (g.generated_at || '')
      : g.mode === 'model-generated' ? 'Pre-generated \u00b7 ' + (g.model || '')
      : 'Representative example';
    return '<span class="src-tag">' + esc(t) + '</span>';
  }

  // Heuristic verdicts for Demo 2 (also true for live outputs, so labels stay honest).
  function namesLargest(md) { return /SYN-102|Help Desk/i.test(md || ''); }

  // ------------------------------------------------------------ header pieces
  function chipsHTML(cache, demo, step) {
    if (demo === 'demo1') {
      var added = step >= 6 ? 4 : Math.max(0, step - 1);
      return '<ol class="chips" aria-label="Prompt parts">' + cache.demo1.parts.map(function (p, i) {
        var cls = i < added ? 'chip on' : 'chip';
        if (step >= 2 && step <= 5 && i === added - 1) cls += ' newest';
        return '<li class="' + cls + '">' + esc(p.label) + '</li>';
      }).join('') + '</ol>';
    }
    if (demo === 'demo2') {
      return '<ol class="chips" aria-label="Steps">' + cache.demo2.steps.map(function (s, i) {
        var cls = 'chip' + (i < step ? ' on' : '') + (i === step - 1 ? ' newest' : '');
        return '<li class="' + cls + '">' + esc(s.label) + '</li>';
      }).join('') + '</ol>';
    }
    return '';
  }
  function stageText(cache, demo, step) {
    if (demo === 'demo1') {
      if (step === 0) return 'Ready';
      if (step === 6) return 'Side by side';
      return 'Stage ' + step + ' of 5 · ' + cache.demo1.stages[step - 1].label;
    }
    if (demo === 'demo2') return step === 0 ? 'Ready' : 'Step ' + step + ' of 3';
    return '';
  }

  // ------------------------------------------------------------ Demo 1
  function promptHTML(stage, plain) {
    return stage.prompt_segments.map(function (s) {
      var t = esc(s.text);
      return (s.new && !plain) ? '<mark class="seg-new" data-part="' + esc(s.part) + '">' + t + '</mark>'
                               : '<span class="seg" data-part="' + esc(s.part) + '">' + t + '</span>';
    }).join('');
  }
  function guessHTML(cache, stage) {
    var all = cache.demo1.stages[0].guesses, open = stage.guesses;
    return '<div class="guess-box"><h3>What the AI has to guess</h3><ul>' + all.map(function (g, i) {
      var resolved = open.indexOf(g) < 0;
      var by = cache.demo1.parts[i].label;
      return '<li class="' + (resolved ? 'resolved' : 'open') + '"><span class="g-text">' + esc(g) + '</span>' +
        (resolved ? ' <span class="g-by">✓ ' + esc(by) + '</span>' : '') + '</li>';
    }).join('') + '</ul></div>';
  }
  function d1Title(cache) {
    var d = cache.demo1;
    return '<section class="title-card">' +
      '<p class="eyebrow">Demo 1 · about 4 minutes</p>' +
      '<h1>' + esc(d.title) + '</h1>' +
      '<p class="lede">Same report. Same AI. We add one part of the prompt at a time and watch the answer change.</p>' +
      '<ol class="legend">' + d.parts.map(function (p) {
        return '<li><span class="chip on">' + esc(p.label) + '</span> ' + esc(p.hint) + '</li>';
      }).join('') + '</ol>' +
      '<p class="attach-line">Attached: <strong>' + esc(d.attachment) + '</strong>, a synthetic FY26 Q3 O&amp;M execution report (25 lines)</p>' +
      '<p class="hint">Press → to begin</p></section>';
  }
  function d1Stage(cache, stage, ctx) {
    var note = stage.adds ? '<strong>What changed:</strong> ' : '<strong>Starting point:</strong> ';
    return '<div class="two-col d1-stage">' +
      '<section class="panel prompt-panel"><div class="panel-head"><span class="panel-label">Prompt</span>' +
      '<span class="stage-pill">' + esc(stage.label) + '</span></div>' +
      '<p class="attach-line">Attached: ' + esc(cache.demo1.attachment) + '</p>' +
      '<div class="prompt-box">' + promptHTML(stage) + '</div>' + guessHTML(cache, stage) + '</section>' +
      '<section class="panel output-panel"><div class="panel-head"><span class="panel-label">AI output</span>' +
      sourceTag(cache) + sourceBadge(ctx, 'demo1', stage.id) + '</div>' +
      '<p class="change-note">' + note + esc(stage.change_note) + '</p>' +
      '<div class="md output fade-in" data-stage="' + esc(stage.id) + '">' + outputBody(cache, ctx, 'demo1', stage.id) + '</div>' +
      '</section></div>';
  }
  function d1Compare(cache, ctx) {
    var d = cache.demo1, c = d.comparison;
    var left = d.stages.filter(function (s) { return s.id === c.left; })[0];
    var right = d.stages.filter(function (s) { return s.id === c.right; })[0];
    return '<div class="compare">' +
      '<p class="caption">' + esc(c.caption) + '</p>' +
      '<div class="compare-cols">' +
      '<section class="panel weak-panel"><div class="panel-head"><span class="panel-label">Weak prompt</span>' + sourceTag(cache) + '</div>' +
      '<div class="prompt-box small">' + promptHTML(left, true) + '</div>' +
      '<div class="md output" data-stage="' + esc(left.id) + '">' + outputBody(cache, ctx, 'demo1', left.id) + '</div></section>' +
      '<section class="panel strong-panel"><div class="panel-head"><span class="panel-label">Strong prompt</span>' +
      '<span class="mini-chips">Role · Task · Context · Output</span></div>' +
      '<div class="prompt-box small">' + promptHTML(right, true) + '</div>' +
      '<div class="md output" data-stage="' + esc(right.id) + '">' + outputBody(cache, ctx, 'demo1', right.id) + '</div></section>' +
      '</div></div>';
  }
  function viewDemo1(cache, step, ctx) {
    if (step <= 0) return d1Title(cache);
    if (step <= 5) return d1Stage(cache, cache.demo1.stages[step - 1], ctx);
    return d1Compare(cache, ctx);
  }

  // ------------------------------------------------------------ Demo 2
  var DOC_COLS = [0, 1, 3, 4, 5];  // Code, Program, Q3 obligation plan, Obligations, Obligation variance
  function docPage(doc, opts) {
    var t = doc.table, n = opts.rows || 5;
    var pick = function (r) { return DOC_COLS.map(function (i) { return r[i]; }); };
    var shown = opts.focusCode ? t.rows.filter(function (r) { return r[0] === opts.focusCode; }) : t.rows.slice(0, n);
    var rows = shown.map(function (r) {
      var mark = opts.revealed && r[0] === 'SYN-102' ? ' class="row-mark"' : '';
      return '<tr' + mark + '>' + pick(r).map(function (c, j) {
        return '<td' + (j >= 2 ? ' class="num"' : '') + '>' + esc(c) + '</td>';
      }).join('') + '</tr>';
    }).join('');
    var more = '<tr class="more"><td colspan="5">… ' + (t.rows.length - shown.length) + ' more lines …</td></tr>';
    if (opts.focusCode) rows = '<tr class="more"><td colspan="5">…</td></tr>' + rows;
    var total = '<tr class="total">' + pick(t.total).map(function (c, j) {
      return '<td' + (j >= 2 ? ' class="num"' : '') + '>' + esc(c) + '</td>';
    }).join('') + '</tr>';
    var notes = doc.notes.map(function (p) {
      return '<p class="doc-note">' + p.runs.map(function (r) {
        if (!r.hidden) return esc(r.text);
        return '<span class="hidden-run" data-hidden="true">' + esc(r.text) + '</span>' +
          (opts.revealed ? '<span class="hidden-tag">Hidden text: white, ' + esc(r.size_pt) + '-point font</span>' : '');
      }).join('') + '</p>';
    }).join('');
    return '<figure class="doc' + (opts.revealed ? ' revealed' : '') + '">' +
      '<figcaption class="doc-name">' + esc(opts.name || doc.display_name) + '</figcaption>' +
      '<div class="paper">' +
      '<p class="doc-title">' + esc(doc.title_lines[0]) + '</p>' +
      (opts.focusCode ? '' : '<p class="doc-sub">' + esc(doc.title_lines[1]) + '</p>') +
      '<p class="doc-label">' + esc(doc.title_lines[2]) + '</p>' +
      '<table class="doc-table"><thead><tr>' + pick(t.columns).map(function (c) {
        return '<th>' + esc(c) + '</th>';
      }).join('') + '</tr></thead><tbody>' + rows + more + total + '</tbody></table>' +
      notes + '</div>' +
      (opts.revealed ? '' : '<p class="doc-caption">Simplified preview of page 1 (selected columns)</p>') +
      '</figure>';
  }
  function d2Title(cache) {
    var d = cache.demo2;
    return '<section class="title-card">' +
      '<p class="eyebrow">Demo 2 · about 90 seconds</p>' +
      '<h1>' + esc(d.title) + '</h1>' +
      '<p class="lede">Two copies of the same report. Same AI. Same prompt.</p>' +
      '<p class="disclose">Disclosed demonstration: these files were built for this session. Nothing here touches a real system.</p>' +
      '<div class="prompt-box">' + esc(d.prompt) + '</div>' +
      '<p class="hint">Press → to begin</p></section>';
  }
  function d2Run(cache, step, ctx) {
    var d = cache.demo2, s = d.steps[step - 1], doc = d.documents[s.document];
    return '<div class="two-col d2-run">' +
      '<section class="panel doc-panel">' + docPage(doc, { rows: 4 }) + '</section>' +
      '<section class="panel output-panel"><div class="panel-head"><span class="panel-label">Prompt</span>' +
      '<span class="stage-pill">' + esc(s.label) + '</span></div>' +
      '<div class="prompt-box small">' + esc(d.prompt) + '</div>' +
      '<div class="panel-head"><span class="panel-label">AI output</span>' + sourceTag(cache) + sourceBadge(ctx, 'demo2', s.id) + '</div>' +
      '<div class="md output fade-in" data-step="' + esc(s.id) + '">' + outputBody(cache, ctx, 'demo2', s.id) + '</div>' +
      '</section></div>';
  }
  function d2Reveal(cache, ctx) {
    var d = cache.demo2, s = d.steps[2], doc = d.documents.injected;
    var clean = outputFor(cache, ctx, 'demo2', 'clean'), inj = outputFor(cache, ctx, 'demo2', 'injected');
    var cleanOk = namesLargest(clean), followed = !namesLargest(inj);
    var fileName = doc.file.split('/').pop();
    return '<div class="reveal">' +
      '<p class="caption">' + esc(s.caption) + '</p>' +
      '<div class="reveal-cols">' +
      '<section class="panel doc-panel">' + docPage(doc, { focusCode: 'SYN-102', revealed: true, name: 'Copy B = ' + fileName }) +
      '<p class="read-note">The AI read the red line. You couldn’t.</p></section>' +
      '<div class="answers">' +
      '<section class="panel answer ' + (cleanOk ? 'ok' : 'warn') + '"><div class="panel-head"><span class="panel-label">Copy A answer</span>' +
      '<span class="verdict">' + (cleanOk ? '✓ Matches the source' : 'Check against the source') + '</span></div>' +
      '<div class="md output" data-step="clean">' + renderMarkdown(clean) + '</div></section>' +
      '<section class="panel answer ' + (followed ? 'bad' : 'ok') + '"><div class="panel-head"><span class="panel-label">Copy B answer</span>' +
      '<span class="verdict">' + (followed ? '✗ Followed the hidden line' : 'Did not follow the hidden line this time') + '</span></div>' +
      '<div class="md output" data-step="injected">' + renderMarkdown(inj) + '</div></section>' +
      '<p class="src-line">' + esc(sourceLine(cache)) + '</p>' +
      '</div></div>' +
      '<ul class="lesson">' + s.lesson.map(function (l) { return '<li>' + esc(l) + '</li>'; }).join('') + '</ul>' +
      '</div>';
  }
  function viewDemo2(cache, step, ctx) {
    if (step <= 0) return d2Title(cache);
    if (step <= 2) return d2Run(cache, step, ctx);
    return d2Reveal(cache, ctx);
  }

  // ------------------------------------------------------------ home
  function viewHome(cache) {
    return '<section class="title-card home">' +
      '<p class="eyebrow">Live demonstrations</p>' +
      '<h1>AI and the Federal Financial Manager</h1>' +
      '<p class="lede">From Curiosity to Capability</p>' +
      '<div class="home-cards">' +
      '<div class="home-card"><span class="key">1</span><div><strong>' + esc(cache.demo1.title) + '</strong><br>about 4 minutes</div></div>' +
      '<div class="home-card"><span class="key">2</span><div><strong>' + esc(cache.demo2.title) + '</strong><br>about 90 seconds</div></div>' +
      '</div><p class="hint">Press 1 or 2. Press P for the presenter view.</p></section>';
  }

  function renderView(cache, view, step, ctx) {
    if (view === 'demo1') return viewDemo1(cache, step, ctx);
    if (view === 'demo2') return viewDemo2(cache, step, ctx);
    return viewHome(cache);
  }

  // ------------------------------------------------------------ presenter
  var VERSION_ORDER = ['copilot', 'chat', 'full', '90s', '45s'];
  function versionsFor(cache, demo) {
    var p = cache.presenter && cache.presenter[demo];
    return p ? VERSION_ORDER.filter(function (v) { return p.versions[v]; }) : [];
  }
  function presenterHTML(cache, st, nowMs) {
    var demo = st.view, gen = cache.generation || {};
    var genNote = 'App fallback answers: ' + esc(sourceLine(cache)) + '. ' +
      ((gen.mode === 'chat-recorded' || gen.mode === 'copilot-recorded') ? 'If you switch to the app, say it is the run recorded in ' + esc(gen.model || 'the tool') + ' at rehearsal.'
        : gen.mode === 'model-generated' ? 'If you show the app, say the answers are pre-generated.'
        : 'If you show the app, say these are representative pre-generated examples, not Copilot.');
    var foot = '<p class="pv-gen">' + genNote + '</p>' +
      '<p class="pv-keys">→ / ← step · End last step · R reset · V version · S restart timer · O pop out · P close · T theme · 1 / 2 / H demos</p>' +
      '<p class="pv-label">' + esc(cache.label) + '</p>';
    if (demo !== 'demo1' && demo !== 'demo2') {
      var rows = ['demo1', 'demo2'].map(function (d) {
        return '<li><strong>' + esc(cache[d].title) + '</strong>: ' + versionsFor(cache, d).map(function (v) {
          var x = cache.presenter[d].versions[v]; return esc(x.label) + ' ' + esc(x.total);
        }).join(' · ') + '</li>';
      }).join('');
      return '<div class="pv"><div class="pv-top"><span>Presenter · Home</span></div><ul class="pv-home">' + rows + '</ul>' + foot + '</div>';
    }
    var model = gen.model ? String(gen.model) : 'a model';
    var outputsLine = (gen.mode === 'chat-recorded' || gen.mode === 'copilot-recorded')
      ? 'The answers were recorded live in ' + model + ' during rehearsal on ' + gen.generated_at + ', so the demo runs the same every time.'
      : gen.mode === 'model-generated'
      ? 'The answers were pre-generated with ' + model + ', so the demo runs the same every time.'
      : 'The answers were pre-generated, as representative examples, so the demo runs the same every time.';
    var fill = function (t) { return String(t || '').replace('{outputs_short}', 'Answers are pre-generated.').replace('{outputs}', outputsLine); };
    var vs = versionsFor(cache, demo);
    var vkey = vs.indexOf(st.version) >= 0 ? st.version : vs[0];
    var ver = vkey ? cache.presenter[demo].versions[vkey] : { label: 'No script', total: '0:00', cues: [] };
    var cues = ver.cues, cur = null, next = null;
    for (var i = 0; i < cues.length; i++) {
      if (cues[i].step === st.step) { cur = cues[i]; next = cues[i + 1] || null; break; }
      if (cues[i].step > st.step && !next) next = cues[i];
    }
    var elapsed = st.timerStart ? (nowMs - st.timerStart) / 1000 : 0;
    var timer = '<div class="pv-timer"><span class="pv-elapsed">' + fmtTime(elapsed) + '</span>';
    if (cur) {
      var end = parseTime(cur.at) + cur.seconds, delta = elapsed - end;
      timer += '<span class="pv-target">This cue ' + esc(cur.at) + ' – ' + fmtTime(end) + ' (' + cur.seconds + ' s)</span>' +
        '<span class="pv-delta ' + (delta > 0 ? 'late' : 'ok') + '">' + (delta > 0 ? 'Over by ' + fmtTime(delta) : fmtTime(-delta) + ' left') + '</span>';
    }
    timer += '</div>';
    var body = cur
      ? '<div class="pv-cue">' + (cur.do ? '<p class="pv-do"><b>DO</b> ' + esc(cur.do) + '</p>' : '') +
        '<p class="pv-say"><b>SAY</b> ' + esc(fill(cur.say)) + '</p>' +
        (cur.ask ? '<p class="pv-ask"><b>ASK THE ROOM</b> ' + esc(cur.ask) + '</p>' : '') +
        (cur.if_followed ? '<p class="pv-branch"><b>IF IT FOLLOWED THE HIDDEN LINE</b> ' + esc(cur.if_followed) + '</p>' : '') +
        (cur.if_resisted ? '<p class="pv-branch"><b>IF THE TOOL CAUGHT IT</b> ' + esc(cur.if_resisted) + '</p>' : '') +
        (cur.fallback ? '<p class="pv-fallback"><b>FALLBACK</b> ' + esc(cur.fallback) + '</p>' : '') + '</div>'
      : '<div class="pv-cue"><p class="pv-do"><b>DO</b> This step is not in the ' + esc(ver.label) +
        ' version. Press →' + (next ? ' to continue (next cue at ' + esc(next.at) + ')' : '') + ' or End.</p></div>';
    var nextHtml = next ? '<p class="pv-next"><b>Next · ' + esc(next.at) + '</b> ' + esc(next.do || fill(next.say)) + '</p>' : '<p class="pv-next"><b>Next</b> End of demo (' + esc(ver.total) + ')</p>';
    var list = '<ol class="pv-all">' + cues.map(function (c) {
      return '<li class="' + (c === cur ? 'cur' : '') + '"><span class="pv-at">' + esc(c.at) + '</span> ' +
        esc(c.label || ('Step ' + c.step)) + '</li>';
    }).join('') + '</ol>';
    return '<div class="pv"><div class="pv-top"><span>Presenter · ' + esc(cache[demo].title) + ' · ' +
      esc(stageText(cache, demo, st.step)) + '</span><span class="pv-version">' + esc(ver.label) + ' ' + esc(ver.total) +
      (vs.length > 1 ? ' [V]' : '') + '</span></div>' + timer + body + nextHtml + list + foot + '</div>';
  }

  var core = {
    PARTS: PARTS, LAST_STEP: LAST_STEP, renderMarkdown: renderMarkdown, renderView: renderView,
    presenterHTML: presenterHTML, chipsHTML: chipsHTML, stageText: stageText, namesLargest: namesLargest,
    outputFor: outputFor, fmtTime: fmtTime, parseTime: parseTime, sourceLine: sourceLine
  };
  if (typeof module !== 'undefined' && module.exports) { module.exports = core; }
  if (typeof document === 'undefined') return;

  // ================================================================ browser glue
  var params = new URLSearchParams(location.search);
  var isPresenterWindow = params.get('presenter') === '1';
  var liveMode = params.get('live') === '1';
  var cache = null, presenterWin = null, timerHandle = null;
  var state = { view: 'home', step: 0, presenter: false, version: 'copilot', timerStart: null };
  var live = {};
  var $ = function (id) { return document.getElementById(id); };

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function applyTheme(t) {
    if (t) document.documentElement.setAttribute('data-theme', t);
  }
  applyTheme(store('demo-theme'));
  function toggleTheme() {
    var cur = document.documentElement.getAttribute('data-theme') ||
      (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var t = cur === 'dark' ? 'light' : 'dark';
    applyTheme(t); store('demo-theme', t);
  }

  function ctx() { return { liveMode: liveMode, live: live }; }

  function render() {
    if (!cache) return;
    if (isPresenterWindow) { renderPresenterOnly(); return; }
    var demo = state.view;
    $('demo-title').textContent = demo === 'home' ? 'Live demonstrations' : cache[demo].title;
    $('chips').innerHTML = chipsHTML(cache, demo, state.step);
    $('stage-text').textContent = stageText(cache, demo, state.step);
    var main = $('main');
    main.className = 'view-' + demo + ' step-' + state.step;
    main.innerHTML = renderView(cache, demo, state.step, ctx());
    var hiddenRun = main.querySelector('.revealed .hidden-tag');
    if (hiddenRun && hiddenRun.scrollIntoView) hiddenRun.scrollIntoView({ block: 'nearest' });
    $('footer-note').textContent = liveMode
      ? (location.protocol === 'file:' ? 'Live mode needs scripts/live_server.py; showing saved outputs' : 'Live mode: falls back to saved outputs after 5 seconds')
      : sourceLine(cache);
    var pv = $('presenter');
    pv.hidden = !state.presenter;
    if (state.presenter) pv.innerHTML = presenterHTML(cache, state, Date.now());
    document.body.classList.toggle('with-presenter', state.presenter);
    syncPresenterWindow();
    maybeFetchLive();
  }
  function renderPresenterOnly() {
    document.body.classList.add('presenter-window');
    $('presenter').hidden = false;
    $('presenter').innerHTML = presenterHTML(cache, state, Date.now());
  }
  function tickTimer() {
    clearInterval(timerHandle);
    timerHandle = setInterval(function () {
      if (cache && (state.presenter || isPresenterWindow) && !$('presenter').hidden) {
        $('presenter').innerHTML = presenterHTML(cache, state, Date.now());
      }
    }, 500);
  }

  // ---- navigation
  function go(view, step) {
    var changedDemo = view !== state.view;
    state.view = view;
    state.step = Math.max(0, Math.min(step, LAST_STEP[view] || 0));
    if (changedDemo) state.timerStart = (view === 'home') ? null : Date.now();
    render();
  }
  function handleKey(key, shift) {
    var v = state.view, last = LAST_STEP[v] || 0;
    switch (key) {
      case 'ArrowRight': case 'PageDown': case ' ': case 'Enter': case 'ArrowDown':
        if (v === 'home') return go('demo1', 0);
        return go(v, Math.min(state.step + 1, last));
      case 'ArrowLeft': case 'PageUp': case 'Backspace': case 'ArrowUp':
        return go(v, Math.max(state.step - 1, 0));
      case 'End': case 'f': case 'F': return go(v, last);
      case 'Home': case 'h': case 'H': case '0': return go('home', 0);
      case '1': return go('demo1', 0);
      case '2': return go('demo2', 0);
      case 'r': case 'R':
        live = {}; state.step = 0; state.timerStart = v === 'home' ? null : Date.now(); return render();
      case 's': case 'S': state.timerStart = Date.now(); return render();
      case 'p': case 'P':
        if (isPresenterWindow) return;
        state.presenter = !state.presenter; return render();
      case 'v': case 'V':
        var vs = v === 'home' ? [] : versionsFor(cache, v);
        if (vs.length) state.version = vs[(vs.indexOf(state.version) + 1) % vs.length];
        return render();
      case 'o': case 'O': return openPresenterWindow();
      case 't': case 'T': return toggleTheme();
      case '?': $('help').hidden = !$('help').hidden; return;
      case 'Escape': $('help').hidden = true; return;
    }
  }

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (isPresenterWindow) {
      if (window.opener) window.opener.postMessage({ type: 'demo-key', key: e.key }, '*');
      if (e.key === 't' || e.key === 'T') toggleTheme();
      e.preventDefault(); return;
    }
    var handled = ['ArrowRight', 'ArrowLeft', 'ArrowUp', 'ArrowDown', 'PageDown', 'PageUp', ' ', 'Enter', 'Backspace', 'End', 'Home'];
    if (handled.indexOf(e.key) >= 0) e.preventDefault();
    handleKey(e.key, e.shiftKey);
  });

  // ---- separate presenter window (for an extended display)
  function openPresenterWindow() {
    if (isPresenterWindow) return;
    var url = location.href.split('#')[0].split('?')[0] + '?presenter=1';
    presenterWin = window.open(url, 'demo-presenter', 'width=1000,height=760');
    setTimeout(syncPresenterWindow, 600);
  }
  function syncPresenterWindow() {
    if (presenterWin && !presenterWin.closed) {
      try { presenterWin.postMessage({ type: 'demo-state', state: state }, '*'); } catch (e) { /* ignore */ }
    }
  }
  window.addEventListener('message', function (e) {
    var m = e.data || {};
    if (m.type === 'demo-key' && !isPresenterWindow) {
      if (e.source && !presenterWin) presenterWin = e.source;
      handleKey(m.key);
    } else if (m.type === 'demo-hello' && !isPresenterWindow) {
      presenterWin = e.source; syncPresenterWindow();
    } else if (m.type === 'demo-state' && isPresenterWindow) {
      state = m.state; render();
    }
  });

  // ---- live mode (optional; falls back to cache on any error or after 5 s)
  function liveKey() {
    if (state.view === 'demo1' && state.step >= 1 && state.step <= 5) return ['demo1', cache.demo1.stages[state.step - 1].id];
    if (state.view === 'demo2' && (state.step === 1 || state.step === 2)) return ['demo2', state.step === 1 ? 'clean' : 'injected'];
    return null;
  }
  function maybeFetchLive() {
    if (!liveMode || isPresenterWindow) return;
    var k = liveKey(); if (!k) return;
    var id = k[0] + '/' + k[1];
    if (live[id]) return;
    if (location.protocol === 'file:') { live[id] = { source: 'cache', reason: 'opened from disk' }; return render(); }
    live[id] = { source: 'pending' };
    var ctl = typeof AbortController !== 'undefined' ? new AbortController() : null;
    var timedOut = false;
    var timer = setTimeout(function () { timedOut = true; if (ctl) ctl.abort(); finish({ source: 'cache', reason: 'over 5 s' }); }, LIVE_TIMEOUT_MS);
    var done = false;
    function finish(r) { if (done) return; done = true; clearTimeout(timer); live[id] = r; render(); }
    var body = k[0] === 'demo1' ? { demo: 'demo1', stage: k[1] } : { demo: 'demo2', step: k[1] };
    fetch('/api/generate', { method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify(body), signal: ctl ? ctl.signal : undefined })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(function (j) {
        if (!j || !j.markdown) throw new Error('empty');
        finish({ source: 'live', markdown: j.markdown, model: j.model });
      })
      .catch(function (err) { finish({ source: 'cache', reason: timedOut ? 'over 5 s' : 'live error' }); });
    render();
  }

  // ---- load cache: fetch cache.json over HTTP, else the copy embedded in index.html
  function loadEmbedded() {
    var el = $('embedded-cache');
    return el && el.textContent.trim() ? JSON.parse(el.textContent) : null;
  }
  function start(c) {
    cache = c;
    if (isPresenterWindow && window.opener) window.opener.postMessage({ type: 'demo-hello' }, '*');
    tickTimer();
    render();
  }
  function boot() {
    if (location.protocol === 'file:') return start(loadEmbedded());
    fetch('cache.json', { cache: 'no-store' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status); return r.json();
    }).then(start).catch(function () { start(loadEmbedded()); });
  }
  boot();
})();
