# Mobile Claude Code Features Guide

## Accessing Claude Code on Mobile

### Web App (Primary Method)
Visit **claude.ai/code** from any mobile browser. No installation required.

### Native Mobile Apps
- **iOS**: Claude app on Apple App Store
- **Android**: Claude app on Google Play Store

Both let you kick off tasks, monitor progress, and get notifications.

### Quick Setup from Terminal
```bash
/web-setup
```
This syncs your GitHub credentials, creates a cloud environment, and opens claude.ai/code.

---

## Key Mobile Features

### Session Management
- Start new coding tasks from your phone
- Monitor running sessions in real-time
- Resume past sessions from session history
- Get notified when Claude needs input or finishes

### Code Review & Iteration
- Review changes in **diff view** before creating PRs
- Comment on specific lines to request modifications
- Iterate multiple times before opening a PR
- Create pull requests when satisfied

### Auto-fix for Pull Requests
- Enable auto-fix to watch PRs automatically
- Claude responds to CI failures and reviewer comments
- Monitor status in real-time from mobile

### Cloud Execution
- Tasks run on Anthropic-managed cloud infrastructure
- Sessions continue even if you close the browser
- No impact on your local machine

---

## Mobile vs Desktop Feature Comparison

| Feature | Mobile (Web) | Desktop/CLI |
|---------|:---:|:---:|
| Start tasks | Yes | Yes |
| Diff review | Yes | Yes |
| Real-time steering | Yes | Yes |
| PR creation | Yes | Yes |
| Auto-fix | Yes | Yes |
| Cloud execution | Yes | No |
| Computer use | No | Yes |
| Agent SDK | No | Yes |
| Third-party providers | No | Yes |
| Local MCP servers | No | Yes |

---

## Practical Workflows

### 1. Delegate Work While Traveling
1. Start a task from your phone
2. Let Claude run autonomously while offline
3. Check progress when you have connectivity
4. Review diffs and comment on changes
5. Create PR when satisfied

### 2. Parallel Issue Fixes
From terminal, start multiple remote tasks:
```bash
claude --remote "Fix issue #234 in auth service"
claude --remote "Fix issue #235 in payment service"
claude --remote "Update dependencies in docs"
```
Monitor all from `/tasks` or mobile. Review each independently.

### 3. CI Failure Response
1. Enable **Auto-fix** on a PR from the web interface
2. Claude automatically investigates and pushes fixes
3. Get notified on mobile and review the fix

### 4. On-Call Rapid Response
1. Get alerted to a production issue
2. Open claude.ai/code on your phone
3. Describe the bug and target files
4. Review Claude's fix in diff view
5. Create a PR to deploy the fix

---

## Moving Between Mobile and Desktop

### Terminal to Web
```bash
claude --remote "Fix the authentication bug in src/auth/login.ts"
```
Creates a cloud session you can monitor from any device.

### Web to Terminal (Teleport)
```bash
# Interactive picker
claude --teleport

# Specific session
claude --teleport <session-id>

# From tasks view (press 't' to teleport)
/tasks
```

**Requirements**: Clean git state, correct repository, branch pushed remotely.

---

## Tips for Mobile Success

### Task Scoping
- **Good**: "Fix the failing auth test in src/auth.test.ts"
- **Good**: "Update API docs for the new rate limit response"
- **Avoid**: "Refactor the entire authentication system"

### Before Going Mobile
- Set up your cloud environment with all dependencies
- Document project conventions in `CLAUDE.md`
- Test that setup scripts work correctly
- Enable browser/app notifications

### During Mobile Work
- Keep tasks focused and well-scoped
- Use the diff viewer before approving changes
- Comment on specific changes rather than giving vague feedback
- Let Claude work autonomously -- don't micromanage

### Security
- Don't hardcode secrets in prompts (use environment variables)
- Review shared sessions for sensitive code before sharing
- Verify network access settings match your security needs

---

## Limitations on Mobile

- **GitHub only** (no GitLab or self-hosted repos; Team/Enterprise supports GitHub Enterprise Server)
- **No computer use** (screen control is desktop-only)
- **No Agent SDK** or third-party provider support
- **Cloud-only execution** (can't access local files or databases)
- **Smaller screen** makes diff review require more scrolling
- **No keyboard shortcuts** from the CLI

---

## When Mobile Shines

| Great for Mobile | Better on Desktop |
|---|---|
| Monitoring task progress | Complex real-time steering |
| Reviewing changes async | Large-scale refactoring |
| Starting well-defined tasks | Building new projects from scratch |
| Commenting on code | Interactive debugging |
| Creating PRs | Computer use tasks |
| Enabling auto-fix | Custom MCP server workflows |
