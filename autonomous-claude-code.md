# Letting Claude Code Work Autonomously

## Quick Decision Tree

```
Need human approval?        -> Interactive mode (default)
Running in CI/CD?           -> dontAsk mode + --allowedTools
Want smart auto-approval?   -> auto mode
Fire-and-forget to cloud?   -> --remote
Custom application?         -> Agent SDK (Python/TypeScript)
```

---

## 1. Headless Mode (`-p`)

The foundation of all autonomous work. Claude runs without waiting for user input.

```bash
# Simple task
claude -p "Find all TODO comments in the codebase"

# JSON output for scripting
claude -p "List all API endpoints" --output-format json

# Limit turns to prevent runaway sessions
claude -p "Fix lint errors" --max-turns 10

# Resume a previous session
claude -p "Now fix the remaining tests" --resume "$SESSION_ID"

# Bare mode: skip auto-discovery for CI consistency
claude --bare -p "Run tests" --allowedTools "Bash(npm test *),Read"
```

---

## 2. Permission Modes

Control what Claude can do without asking.

| Mode | Auto-Approves | Best For |
|------|---------------|----------|
| `default` | Reads only | Interactive development |
| `acceptEdits` | File edits + reads | Quick iteration |
| `plan` | Reads only | Exploration before execution |
| `auto` | Safe ops via classifier | Cloud tasks, background jobs |
| `dontAsk` | Pre-approved rules only | CI/CD pipelines |
| `bypassPermissions` | Everything | Isolated containers only |

### Auto Mode (Smart Autonomous)

Uses a classifier to allow safe operations while blocking dangerous ones.

```bash
claude --enable-auto-mode -p "Fix all lint errors"
```

**Blocks**: `curl | bash`, force push to main, production deploys, mass deletion
**Allows**: Local file ops, installing from lock files, pushing to your branch

### DontAsk Mode (Locked-Down CI)

Only runs pre-approved tools. Zero prompts.

```bash
claude --permission-mode dontAsk -p "Run tests and fix failures" \
  --allowedTools "Bash(npm test *),Bash(npm lint *),Read,Edit"
```

### Configure in settings.json

```json
{
  "permissions": {
    "defaultMode": "dontAsk",
    "allow": [
      "Bash(npm test *)",
      "Bash(npm lint *)",
      "Read",
      "Edit"
    ],
    "deny": [
      "Bash(rm *)",
      "Bash(git push origin main)"
    ]
  }
}
```

---

## 3. Writing Effective CLAUDE.md

The most important file for autonomous work. Claude reads it every session.

```markdown
# CLAUDE.md

## Build & Test
- Build: `npm run build`
- Test: `npm test` (Jest)
- Lint: `npm run lint` (auto-fix: `npm run lint:fix`)
- Type check: `npm run type-check`

## Code Style
- ES modules (import/export), not CommonJS
- 2-space indentation, PascalCase components, camelCase utils
- No console.log in production (use logger)

## Architecture
- API handlers: `src/api/handlers/`
- Tests: `__tests__/` adjacent to source files
- Migrations: `db/migrations/` with timestamp prefixes

## Git Workflow
- Reference issues in commits: "fix: #123 - description"
- Run tests before committing

## Common Gotchas
- Database must be running for integration tests
- Auth tokens expire after 1 hour
```

### Path-Specific Rules

Create `.claude/rules/` for targeted instructions:

```markdown
---
paths:
  - "src/api/**/*.ts"
---
# API Rules
- Input validation required on all handlers
- Use standard error response format
```

---

## 4. Hooks for Deterministic Guarantees

Unlike CLAUDE.md (advisory), hooks **always execute**.

### Auto-Format After Edits

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
      }]
    }]
  }
}
```

### Block Dangerous Commands

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "echo 'Blocked' >&2 && exit 2"
      }]
    }]
  }
}
```

### Run Tests After Changes

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "cd \"$CLAUDE_PROJECT_DIR\" && npm test -- --bail",
        "timeout": 300
      }]
    }]
  }
}
```

### Verify Completion Before Stopping

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "agent",
        "prompt": "Verify all unit tests pass. Run the test suite and check results.",
        "timeout": 120
      }]
    }]
  }
}
```

---

## 5. Remote / Cloud Execution

Fire-and-forget tasks that run on Anthropic's cloud.

```bash
# Start a remote task (returns immediately)
claude --remote "Fix the flaky test in auth.spec.ts"

# Start multiple parallel tasks
claude --remote "Fix database query in reports.ts"
claude --remote "Add caching to user service"
claude --remote "Update API documentation"

# Monitor all sessions
/tasks

# Pull a session back to your terminal
claude --teleport
```

### Plan Locally, Execute Remotely

```bash
# Step 1: Explore in plan mode
claude --permission-mode plan

# Step 2: Send execution to cloud
claude --remote "Execute the migration plan in PLAN.md"
```

---

## 6. GitHub Actions Integration

### Claude Code Action

```yaml
name: Claude PR Fix
permissions:
  contents: write
  pull-requests: write

on:
  issue_comment:
    types: [created]

jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Fix the issue mentioned in the comment"
          claude_args: "--max-turns 10"
```

### Scheduled Maintenance

```yaml
name: Weekly Dependency Updates
on:
  schedule:
    - cron: "0 9 * * MON"

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Update dependencies, run tests.
            Create a PR if all tests pass.
```

---

## 7. Auto-Fix for Pull Requests

Claude watches PRs and automatically fixes CI failures and review comments.

**From the web**: Open claude.ai/code -> Create task -> Click "Auto-fix"

**How it works**:
1. Claude monitors PR for CI failures and review comments
2. Investigates the issue autonomously
3. Commits a fix
4. Posts reply on review threads

---

## 8. Agent SDK

Build custom autonomous agents programmatically.

### Python

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Find and fix the auth bug in auth.py",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Edit", "Bash", "Grep"],
        permission_mode="acceptEdits"
    ),
):
    if hasattr(message, 'result'):
        print(message.result)
```

### TypeScript

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Review this codebase for performance issues",
  options: {
    allowedTools: ["Read", "Glob", "Grep"],
    permissionMode: "auto"
  }
})) {
  if ("result" in message) console.log(message.result);
}
```

---

## 9. Best Practices

### Task Scoping

| Good | Bad |
|------|-----|
| "Fix the failing test in auth.test.ts" | "Improve the codebase" |
| "Update all npm packages and run tests" | "Make it work" |
| "Add types to the API handler" | "Refactor everything" |

### Safety Guardrails

```bash
# Safe CI default
claude -p "Fix lint errors" \
  --permission-mode dontAsk \
  --max-turns 5 \
  --allowedTools "Bash(npm lint *),Edit,Read"
```

1. **Start with tight permissions** -- expand as you build trust
2. **Set `--max-turns`** -- prevent infinite loops
3. **Use hooks for hard limits** -- block dangerous operations deterministically
4. **Don't auto-deploy** -- validate before production
5. **Monitor token usage** -- autonomous work consumes tokens quickly

### Make Tasks Idempotent

```bash
# Good: safe to run multiple times
claude -p "Install dependencies if not present. Check node_modules first."

# Risky: side effects on re-run
claude -p "Send deployment notification to Slack"
```

---

## 10. Troubleshooting

| Issue | Solution |
|-------|----------|
| "Permission denied" | Add required tools to `--allowedTools` |
| Infinite loop | Set `--max-turns`, add Stop hook |
| Token exhaustion | Use `--bare` mode, reduce context |
| Unexpected changes | Use plan mode first to review |
| Session disconnects | Use `--remote` for cloud reliability |
| API rate limited | Reduce parallel tasks |
