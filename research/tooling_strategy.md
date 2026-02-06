# Project Chimera: Tooling Strategy

**Date:** February 5, 2026  
**Status:** Day 2 - Task 2.3 Sub-Task A Documentation  
**Purpose:** Define MCP (Model Context Protocol) tooling for development and runtime

---

## Overview

Project Chimera uses **Model Context Protocol (MCP)** for all external integrations, following our architecture decision documented in `context.md`. This document outlines our MCP strategy across two categories:

1. **Developer Tools (MCP)** - Tools for development environment
2. **Agent Skills (Runtime)** - Tools for agent operations

---

## 1. Developer Tools (MCP)

These MCP servers enhance the development experience and are configured in `.vscode/mcp.json`.

### 1.1 Configured MCP Servers

#### **Tenx MCP Sense** (Telemetry & Analytics)
- **Purpose:** Track development velocity and feedback
- **Provider:** 10x Engineering Analytics
- **Status:** ✅ Active
- **Configuration:** `.vscode/mcp.json`
- **Usage:** Automatic telemetry during development
- **Why:** Required for 3-Day Challenge submission tracking

**Configuration:**
```json
{
  "mcpServers": {
    "tenxfeedbackanalytics": {
      "command": "npx",
      "args": ["-y", "@upstreamapi/tenx-mcp-sense"],
      "disabled": false,
      "autoApprove": ["provide_feedback"]
    }
  }
}
```

---

### 1.2 Recommended Developer MCP Servers (Future)

#### **Git MCP Server**
- **Purpose:** Git operations via MCP
- **Use Cases:** Commit, branch, merge via AI agent
- **Status:** 🔜 Future consideration
- **Why Not Now:** Standard git commands sufficient for challenge

#### **Filesystem MCP Server**
- **Purpose:** File operations via MCP
- **Use Cases:** Create/read/update/delete files
- **Status:** 🔜 Future consideration
- **Why Not Now:** Direct file operations simpler for setup

#### **GitHub MCP Server**
- **Purpose:** GitHub API operations
- **Use Cases:** PR creation, issue tracking, CI/CD integration
- **Status:** 🔜 Post-challenge
- **Why Not Now:** Focus on core infrastructure first

#### **Docker MCP Server**
- **Purpose:** Container operations via MCP
- **Use Cases:** Build, run, manage containers
- **Status:** 🔜 Post-challenge
- **Why Not Now:** Makefile automation sufficient

---

## 2. Agent Skills (Runtime MCP)

These MCP servers provide runtime capabilities for agents and are documented in `skills/README.md`.

### 2.1 Priority 1: MVP MCP Servers

#### **mcp-server-weaviate** (Memory & Context)
- **Purpose:** Semantic memory search and storage
- **Repository:** To be implemented in `skills/mcp-server-weaviate/`
- **Tools Exposed:**
  - `search_memory` - Retrieve relevant past interactions
  - `store_memory` - Save successful patterns
  - `get_persona` - Fetch agent persona details
- **Status:** 🔴 Spec complete, implementation pending
- **Priority:** CRITICAL - Required for Epic 8 (Agent Memory)

#### **mcp-server-twitter** (Social Media)
- **Purpose:** Twitter/X API integration
- **Repository:** To be implemented in `skills/mcp-server-twitter/`
- **Tools Exposed:**
  - `post_tweet` - Publish tweets
  - `reply_to_tweet` - Respond to mentions
  - `get_trending_topics` - Discover trends
- **Status:** 🔴 Spec complete, implementation pending
- **Priority:** HIGH - Required for Epic 2 (Content Generation)

#### **mcp-server-coinbase** (Financial Autonomy)
- **Purpose:** Coinbase AgentKit integration
- **Repository:** To be implemented in `skills/mcp-server-coinbase/`
- **Tools Exposed:**
  - `transfer_usdc` - Execute payments
  - `get_balance` - Check wallet balance
  - `execute_transaction` - Generic transactions
- **Status:** 🔴 Spec complete, implementation pending
- **Priority:** HIGH - Required for Epic 4 (Financial Autonomy)

---

### 2.2 Priority 2: Enhanced MCP Servers

#### **mcp-server-ideogram** (Image Generation)
- **Purpose:** AI image generation for posts
- **Provider:** Ideogram API
- **Tools Exposed:**
  - `generate_image` - Create images from prompts
  - `apply_character_lora` - Apply consistent character style
- **Status:** 🟡 Planned for post-MVP
- **Cost:** ~$0.08 per image

#### **mcp-server-news** (Trend Discovery)
- **Purpose:** News aggregation for trend discovery
- **Provider:** NewsData.io or similar
- **Tools Exposed:**
  - `get_trending_topics` - Fetch trending news
  - `search_news` - Search by keywords
- **Status:** 🟡 Planned for post-MVP

#### **mcp-server-instagram** (Additional Platform)
- **Purpose:** Instagram API integration
- **Status:** 🟡 Planned for Phase 2
- **Dependency:** Twitter MCP working first

---

## 3. MCP Architecture Principles

### 3.1 Why MCP?

From `context.md`:
> **Integration Layer: Model Context Protocol (MCP)**  
> **Rationale:** Platform independence, maintainability, prevents vendor lock-in

**Benefits:**
1. ✅ **Platform Independence** - Workers don't know Twitter exists
2. ✅ **Maintainability** - API changes isolated to MCP server
3. ✅ **Testability** - Easy to mock MCP servers for tests
4. ✅ **Replaceability** - Swap Twitter for Mastodon without code changes

### 3.2 MCP vs Direct API Calls

**❌ Bad Approach (Tight Coupling):**
```python
import tweepy
auth = tweepy.OAuthHandler(KEY, SECRET)
api = tweepy.API(auth)
api.update_status("Hello world")
```

**✅ Good Approach (MCP Abstraction):**
```python
result = await mcp_client.call_tool("post_content", {
    "platform": "twitter",
    "text": "Hello world"
})
```

---

## 4. MCP Server Deployment Strategy

### 4.1 Development Environment
- **Hosting:** Local processes (via Docker Compose)
- **Configuration:** `.vscode/mcp.json` for IDE integration
- **Communication:** stdio (standard input/output)

### 4.2 Production Environment
- **Hosting:** Kubernetes (self-hosted)
- **Configuration:** K8s ConfigMaps and Secrets
- **Communication:** HTTP/gRPC
- **High Availability:** 3 replicas per MCP server
- **Load Balancing:** Service mesh (Istio)

**Deployment Config Example:**
```yaml
# k8s/mcp-weaviate-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server-weaviate
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-weaviate
  template:
    spec:
      containers:
      - name: mcp-weaviate
        image: chimera/mcp-weaviate:latest
        ports:
        - containerPort: 3000
        env:
        - name: WEAVIATE_URL
          valueFrom:
            configMapKeyRef:
              name: mcp-config
              key: weaviate-url
```

---

## 5. MCP Server Implementation Checklist

For each MCP server, we follow this checklist:

### Development
- [ ] Create directory in `skills/mcp-server-[name]/`
- [ ] Define MCP tool schemas (JSON)
- [ ] Implement tool handlers (Python/Node.js)
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Document in server README

### Deployment
- [ ] Create Dockerfile
- [ ] Create Kubernetes manifests
- [ ] Configure secrets management
- [ ] Setup monitoring (Prometheus metrics)
- [ ] Setup logging (structured logs)
- [ ] Deploy to dev environment
- [ ] Load test
- [ ] Deploy to production

### Documentation
- [ ] Update `skills/README.md`
- [ ] Create API documentation
- [ ] Document error codes
- [ ] Document rate limits
- [ ] Add example usage

---

## 6. Decision Matrix: When to Use MCP vs Skills

From `skills/README.md`:

| Scenario | Use MCP Server | Use Skill Module |
|----------|----------------|------------------|
| External API call (Twitter) | ✅ Yes | ❌ No |
| LLM prompt orchestration | ❌ No | ✅ Yes |
| Database query (Weaviate) | ✅ Yes | ❌ No |
| Complex business logic | ❌ No | ✅ Yes |
| Trend analysis | ❌ No | ✅ Yes |
| Post publishing | ✅ Yes | ❌ No |

**Rule of Thumb:**
- **MCP Servers** = External integrations (APIs, databases, services)
- **Skills** = Internal business logic (prompt engineering, analysis, orchestration)

---

## 7. MCP Server Observability

### 7.1 Metrics (Prometheus)

```python
# Common metrics for all MCP servers
mcp_tool_calls_total = Counter('mcp_tool_calls_total', 'Total MCP tool calls', ['server', 'tool'])
mcp_tool_duration_seconds = Histogram('mcp_tool_duration_seconds', 'MCP tool call duration', ['server', 'tool'])
mcp_tool_errors_total = Counter('mcp_tool_errors_total', 'MCP tool errors', ['server', 'tool', 'error_type'])
```

### 7.2 Logging (Structured)

```python
import structlog

logger = structlog.get_logger()

logger.info(
    "mcp_tool_called",
    server="mcp-twitter",
    tool="post_tweet",
    agent_id="agent_550e8400",
    duration_ms=234,
    success=True
)
```

### 7.3 Tracing (OpenTelemetry)

All MCP tool calls instrumented with OpenTelemetry for distributed tracing.

---

## 8. Cost Model (MCP Infrastructure)

From `context.md` cost model:

| MCP Server | Hosting | Monthly Cost (1,000 agents) |
|------------|---------|------------------------------|
| mcp-server-weaviate | Self-hosted (K8s) | $200 (infrastructure) |
| mcp-server-twitter | Self-hosted (K8s) | $100 (infrastructure) |
| mcp-server-coinbase | Self-hosted (K8s) | $100 (infrastructure) |
| mcp-server-ideogram | External API | $8,000 (usage: $0.08/image × 100k images) |
| mcp-server-news | Self-hosted (K8s) | $100 (infrastructure) |
| **Total MCP Infrastructure** | | **~$8,500/month** |

**Cost per agent:** ~$8.50/month (within $15/month target from `context.md`)

---

## 9. Security Considerations

### 9.1 Authentication
- MCP servers authenticate via API keys (stored in K8s secrets)
- Workers authenticate to MCP servers via JWT tokens
- Token rotation every 24 hours

### 9.2 Authorization
- Workers can only call MCP tools their agent owns
- Rate limiting per agent (prevent abuse)
- Audit logging for all financial transactions

### 9.3 Network Security
- MCP servers only accessible within cluster (no public endpoints)
- TLS/mTLS for all internal communication
- Network policies restrict worker → MCP server traffic

---

## 10. Migration Path

### Phase 1: MVP (Current - Day 3)
- ✅ Specs complete
- ✅ Tests define contracts
- 🔴 Implementation pending

### Phase 2: Implementation (Post-Challenge)
- Implement Priority 1 MCP servers
- Deploy to development environment
- Integration testing

### Phase 3: Production (Q2 2026)
- Deploy to Kubernetes
- Setup monitoring and alerting
- Launch with first 10 agents

### Phase 4: Scale (Q3 2026)
- Add Priority 2 MCP servers
- Optimize for 1,000 agents
- OpenClaw integration (Phase 2 feature)

---

## 11. References

- **Main Documentation:** `skills/README.md` - Agent runtime skills
- **Technical Specs:** `specs/technical.md` - MCP deployment architecture
- **Context:** `context.md` - Architecture decisions and rationale
- **OpenClaw Integration:** `specs/openclaw_integration.md` - Agent-to-agent MCP protocols

---

## Document Status

**Status:** ✅ Day 2 Task 2.3 Sub-Task A Complete  
**Last Updated:** February 5, 2026  
**Version:** 1.0

**Summary:**
- Developer MCP: Tenx MCP Sense configured ✅
- Agent MCP: 5 servers specified, implementation pending
- Architecture: MCP-first approach documented
- Deployment: Kubernetes strategy defined
- Cost model: Within $15/agent/month budget
- Security: Authentication, authorization, network policies defined

**Next Steps:**
- Post-Challenge: Implement Priority 1 MCP servers
- Post-Challenge: Deploy to K8s development environment
- Phase 2: Implement Priority 2 MCP servers for scale
