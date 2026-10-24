#!/usr/bin/env node
/* Run both demos headlessly with the app's own render code (app/app.js) against a
 * cache file, and print what each key press would put on screen as JSON.
 * Used by scripts/preflight.py.   Usage: node scripts/headless_run.js [cache.json]
 */
'use strict';
const fs = require('fs');
const path = require('path');
const app = require(path.join(__dirname, '..', 'app', 'app.js'));

const cachePath = process.argv[2] || path.join(__dirname, '..', 'app', 'cache.json');
const cache = JSON.parse(fs.readFileSync(cachePath, 'utf8'));
const out = {};
for (const demo of ['demo1', 'demo2']) {
  const steps = [];
  for (let s = 0; s <= app.LAST_STEP[demo]; s++) {
    steps.push({
      step: s,
      stage_text: app.stageText(cache, demo, s),
      html: app.renderView(cache, demo, s, {}),
      presenter: app.presenterHTML(cache, { view: demo, step: s, version: 'full', timerStart: null }, 0),
    });
  }
  out[demo] = { key_presses: app.LAST_STEP[demo], steps };
}
process.stdout.write(JSON.stringify(out));
