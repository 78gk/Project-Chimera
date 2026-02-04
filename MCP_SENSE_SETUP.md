# MCP Sense Setup Instructions

**Purpose:** Configure Tenx MCP Sense for telemetry tracking during Project Chimera development.

**Why This Matters:** The 3-Day Challenge requires MCP Sense telemetry to verify your development process. They will check that you connected with the same GitHub account you submit with.

---

## What is MCP Sense?

MCP Sense is a telemetry server that tracks:
- Your thinking process and decision-making
- AI assistant interactions
- Code generation patterns
- Development velocity

It acts as a "black box flight recorder" for your development process.

---

## Setup Instructions (VS Code)

### Step 1: Install MCP Sense Server

**Option A: Via npm (Recommended)**
```bash
npm install -g @tenx/mcp-sense
```

**Option B: Via Docker**
```bash
docker pull tenxhq/mcp-sense:latest
```

### Step 2: Configure VS Code Settings

Add to your `.vscode/settings.json`:

```json
{
  "mcp.servers": {
    "tenx-sense": {
      "command": "mcp-sense",
      "args": ["--port", "3001"],
      "env": {
        "TENX_API_KEY": "your_api_key_here",
        "GITHUB_USERNAME": "your_github_username"
      }
    }
  }
}
```

### Step 3: Get Your API Key

1. Visit: https://sense.tenx.com/signup
2. Sign in with your GitHub account (same account you'll submit with)
3. Copy your API key
4. Add to `.env` file:
   ```
   TENX_API_KEY=your_api_key_here
   ```

### Step 4: Verify Connection

1. Restart VS Code
2. Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
3. Type: "MCP: Show Server Status"
4. Verify "tenx-sense" shows as "Connected"

---

## Alternative: Manual Connection Log

If MCP Sense is unavailable or you can't install it, document your process manually:

Create `telemetry/connection_log.md`:

```markdown
# MCP Sense Connection Log

**Date:** February 4, 2026
**GitHub Account:** your_username
**Project:** Project Chimera

## Connection Attempts
- [ ] Attempted installation via npm
- [ ] Configured VS Code settings
- [ ] Verified connection

## Telemetry Events (Manual Tracking)
- 14:30 - Started Day 1 research
- 15:00 - Completed architecture_strategy.md
- 16:30 - Created specs/ directory
- ...
```

---

## Verification for Submission

Before submitting:
1. Check MCP Sense dashboard: https://sense.tenx.com/dashboard
2. Verify you have recorded activity for February 4, 2026
3. Screenshot your connection status (include in submission if requested)

---

## Troubleshooting

**Problem:** "mcp-sense: command not found"  
**Solution:** Ensure npm global bin directory is in your PATH

**Problem:** "Connection refused"  
**Solution:** Check firewall settings, ensure port 3001 is available

**Problem:** "Invalid API key"  
**Solution:** Regenerate key from Tenx dashboard, update .env file

---

## Important Notes

- ⚠️ **Use the same GitHub account** for MCP Sense and final submission
- ⚠️ Don't commit your API key to Git (it's in .gitignore)
- ⚠️ MCP Sense data is used for assessment verification only

---

**Status:** Setup instructions complete  
**Action Required:** Follow steps above to connect MCP Sense
