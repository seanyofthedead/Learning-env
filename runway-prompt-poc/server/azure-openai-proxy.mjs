// Minimal server for running Runway against the client's own Azure OpenAI deployment.
// No dependencies (Node 18+). It serves runway.html and forwards prompts to Azure OpenAI,
// so the API key stays on the server and never reaches the browser.
//
//   AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com   (Azure Government: https://<resource>.openai.azure.us)
//   AZURE_OPENAI_DEPLOYMENT=<deployment name>
//   AZURE_OPENAI_API_KEY=<key>          (production: use Entra ID / managed identity instead of a key)
//   AZURE_OPENAI_API_VERSION=2024-10-21 (optional)
//   PORT=8080                            (optional)
//
//   node server/azure-openai-proxy.mjs
//
// The page validates every proposed change against its own whitelist before anything is applied,
// so a bad model reply can only produce a refused proposal, never a changed number.

import http from 'node:http';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const PAGE = path.join(here, '..', 'runway.html');
const { AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_API_KEY } = process.env;
const API_VERSION = process.env.AZURE_OPENAI_API_VERSION || '2024-10-21';
const PORT = Number(process.env.PORT || 8080);
const MAX_BODY = 200_000;

async function askModel(prompt) {
  const url = `${AZURE_OPENAI_ENDPOINT.replace(/\/$/, '')}/openai/deployments/${encodeURIComponent(AZURE_OPENAI_DEPLOYMENT)}/chat/completions?api-version=${API_VERSION}`;
  const r = await fetch(url, {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'api-key': AZURE_OPENAI_API_KEY },
    body: JSON.stringify({
      messages: [
        { role: 'system', content: 'You reply with a single JSON object and nothing else.' },
        { role: 'user', content: prompt },
      ],
      temperature: 0,
      response_format: { type: 'json_object' },
    }),
  });
  if (!r.ok) throw new Error(`Azure OpenAI returned ${r.status}: ${(await r.text()).slice(0, 300)}`);
  const data = await r.json();
  const text = data.choices?.[0]?.message?.content || '{}';
  const parsed = JSON.parse(text);
  // Pass through only the fields the page reads.
  return {
    summary: typeof parsed.summary === 'string' ? parsed.summary : '',
    ops: Array.isArray(parsed.ops) ? parsed.ops : [],
    unsupported: typeof parsed.unsupported === 'string' ? parsed.unsupported : null,
    question: typeof parsed.question === 'string' ? parsed.question : null,
  };
}

const server = http.createServer(async (req, res) => {
  try {
    if (req.method === 'GET' && (req.url === '/' || req.url.startsWith('/runway'))) {
      const html = (await readFile(PAGE, 'utf8')).replace('<script id="demo-data">',
        '<script>window.RUNWAY_LLM = { endpoint: "/api/runway-prompt" };</script>\n<script id="demo-data">');
      res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
      return res.end(html);
    }
    if (req.method === 'POST' && req.url === '/api/runway-prompt') {
      let body = '';
      for await (const chunk of req) { body += chunk; if (body.length > MAX_BODY) throw new Error('Request too large'); }
      const { prompt } = JSON.parse(body);
      if (typeof prompt !== 'string' || !prompt) throw new Error('Missing prompt');
      const out = await askModel(prompt);
      res.writeHead(200, { 'content-type': 'application/json' });
      return res.end(JSON.stringify(out));
    }
    res.writeHead(404).end('Not found');
  } catch (e) {
    console.error(e);
    res.writeHead(502, { 'content-type': 'application/json' }).end(JSON.stringify({ error: String(e.message || e) }));
  }
});

if (!AZURE_OPENAI_ENDPOINT || !AZURE_OPENAI_DEPLOYMENT || !AZURE_OPENAI_API_KEY) {
  console.error('Set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT and AZURE_OPENAI_API_KEY.');
  process.exit(1);
}
server.listen(PORT, () => console.log(`Runway on http://localhost:${PORT}`));
