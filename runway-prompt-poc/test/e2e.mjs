// End-to-end check of the prompt bar in offline-rules mode (no model needed).
// Run: node test/e2e.mjs   (uses the pre-installed Playwright + Chromium)
import { createRequire } from 'module';
import path from 'path';
import { fileURLToPath } from 'url';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const page_url = 'file://' + path.join(here, '..', 'runway.html');
const shots = process.env.SHOTS || '';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
await page.goto(page_url);
let fails = 0;
const check = (ok, msg) => { console.log((ok ? 'PASS ' : 'FAIL ') + msg); if (!ok) fails++; };
const snap = async (n) => { if (shots) await page.screenshot({ path: path.join(shots, n + '.png') }); };

async function prompt(text) {
  await page.fill('#askInput', text);
  await page.click('#askGo');
  await page.waitForTimeout(150);
}
const cardText = () => page.$eval('#askCard', (e) => (e.hidden ? '' : e.innerText));
const apply = async () => { await page.click('#cApply'); await page.waitForTimeout(1600); };
const model = (js) => page.evaluate(js);
const anomalyTotal = (key, rate = 1) => model(`(() => { const R = analyze(DATA, '${key}', ${rate}); return R.recs.filter(k => k.kind === 'anomaly').reduce((t, k) => t + k.r.run.shortfall, 0); })()`);

// Model the scenarios first, like a user would.
await page.click('#runBtn'); await page.waitForTimeout(4500);
check((await model('RunwayUI.state().step')) === 1, 'pipeline lands on Scenarios');
await snap('01-scenarios');
const base = await anomalyTotal('dec11');

await prompt('Add a CR through Feb 28 at 95% of the FY26 rate');
let t = await cardText();
check(/New scenario/.test(t) && /Feb 28, 2027/.test(t) && /95% rate/.test(t), 'add scenario: diff shows the new scenario');
check(/Requests/.test(t) && /Anomaly total/.test(t), 'add scenario: impact computed by engine');
await snap('02-proposal');
await apply();
check((await model('DATA.scenarios.length')) === 6, 'add scenario: six scenarios after apply');
check((await model('RunwayUI.state().scen')) === 'cr270228_95', 'add scenario: navigates to it');
check((await model('RunwayUI.state().rate')) === 0.95, 'add scenario: uses its own rate');
check(JSON.stringify(await model('RUNWAY.cfg.rates')) === '[0.9,0.95,1,1.1]', 'add scenario: rate added to the switch');
await snap('03-new-scenario');

await prompt('Overlay balance is now $900M');
t = await cardText();
check(/\$1,240\.0M/.test(t) && /\$900\.0M/.test(t), 'overlay: before and after shown');
await apply();
check((await model('DATA.overlay.balance')) === 900, 'overlay: applied to the model');

await prompt('Assume a 12-week lapse');
await apply();
check((await model('DATA.overlay.lapseWeeksAssumed')) === 12, 'lapse weeks: applied');

await prompt('Only show CBP, sorted by shortfall');
t = await cardText();
check(/CBP/.test(t) && /Largest shortfall first/.test(t), 'filter + sort: both in one proposal');
await apply();
const rowsShown = await model(`analyze(DATA, 'dec11').rows.map(r => r.x.p.component)`);
check(rowsShown.every((c) => c === 'CBP') && rowsShown.length === 4, 'filter: only CBP rows');
const sf = await model(`analyze(DATA, 'dec11').rows.map(r => r.run.shortfall)`);
check(sf.every((v, i) => i === 0 || sf[i - 1] >= v), 'sort: descending shortfall');
await snap('04-cbp-only');

// Filtering must never change another account's numbers.
const cbpOnly = await model(`analyze(DATA, 'lapse').rows.map(r => r.x.p.id + ':' + r.o.coveredWk.toFixed(3) + ':' + r.run.shortfall.toFixed(3))`);
await prompt('Show all components'); await apply();
const all = await model(`analyze(DATA, 'lapse').rows.map(r => r.x.p.id + ':' + r.o.coveredWk.toFixed(3) + ':' + r.run.shortfall.toFixed(3))`);
check(cbpOnly.every((s) => all.includes(s)), 'filter: hidden components do not change shown numbers');

await prompt('Add a pie chart by component');
t = await cardText();
check(/No settings changed/.test(t) && /code changes/.test(t), 'unsupported request: refused with explanation');
await page.click('#cDone');

// Guardrails on direct operations, as a model might send them.
const g = await model(`(() => {
  const r = RUNWAY.applyOps(RUNWAY.cfg, [
    { op: 'set', path: 'meta.crEnd', value: '2026-12-18' },
    { op: 'set', path: 'overlay.balance', value: -5 },
    { op: 'addScenario', value: { end: '2027-11-01' } },
    { op: 'removeScenario', key: 'jan30' },
    { op: 'set', path: 'scenarios.dec11.end', value: '2026-12-20' },
    { op: 'set', path: 'scoring.weights.margin', value: 0.5 },
  ]);
  return { errors: r.errors, weights: r.cfg.scoring.weights, sum: Object.values(r.cfg.scoring.weights).reduce((a, b) => a + b, 0) };
})()`);
check(g.errors.length === 5, 'guardrails: five bad operations refused (' + g.errors.length + ')');
check(g.weights.margin === 0.5 && Math.abs(g.sum - 1) < 0.002, 'weights: others rescale to keep 100%');

await prompt('Open the anomaly package');
check((await model('RunwayUI.state().step')) >= 5, 'navigation: opens the package');
await page.waitForTimeout(2500);
await snap('05-package');

// Undo everything back to the original numbers.
const n = await model('RUNWAY.history.length');
for (let i = 0; i < n; i++) await model('RUNWAY.undo()');
await model('RunwayUI.refresh()');
check(Math.abs((await anomalyTotal('dec11')) - base) < 1e-9 && (await model('DATA.scenarios.length')) === 5, 'undo: back to the original model');

await page.click('#histBtn'); await page.waitForTimeout(200);
check(/No changes yet/.test(await cardText()), 'change log empty after undo');

// Phone width
await page.setViewportSize({ width: 390, height: 844 });
await page.waitForTimeout(400);
const overflow = await model('document.documentElement.scrollWidth > window.innerWidth');
check(!overflow, 'phone: no horizontal scroll');
await page.click('#histBtn');
await prompt('Add a CR through Mar 15');
await snap('06-phone');

check(errors.length === 0, 'no console errors' + (errors.length ? ': ' + errors.join(' | ') : ''));
await browser.close();
console.log(fails ? fails + ' failed' : 'all passed');
process.exit(fails ? 1 : 0);
