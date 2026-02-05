# Project Chimera: Meta Specification

**Version:** 1.0  
**Date:** February 4, 2026  
**Status:** Draft  
**Authors:** Forward Deployed Engineer Team

---

## Vision

Build an autonomous AI influencer network capable of managing **1,000+ agents** with a single human orchestrator. The system must demonstrate genuine agency - perception, reasoning, creative expression, and economic participation - while maintaining brand safety and regulatory compliance.

---

## Strategic Objectives

### Primary Goal
Create a production-grade platform where AI agents can:
- Research and identify trending topics autonomously
- Generate high-quality multimodal content (text, images, video)
- Engage authentically with human audiences on social platforms
- Manage their own financial resources (via crypto wallets)
- Collaborate with other AI agents (agent-to-agent commerce)

### Business Model Alignment
Support three revenue streams:
1. **Digital Talent Agency** - Own and operate flagship AI influencers
2. **Platform-as-a-Service (PaaS)** - License the infrastructure to brands
3. **Hybrid Ecosystem** - Combine owned agents with third-party developer access

---

## Core Constraints

### Technical Constraints
1. **Single-Operator Scalability:** The entire system must be manageable by one human orchestrator
2. **Cost Target:** Maximum $15/agent/month at scale (1,000 agents)
3. **Latency:** End-to-end interaction latency < 10 seconds (p95)
4. **Uptime:** 99.5% system availability
5. **Platform Independence:** Must support Twitter, Instagram, TikTok, Threads (via MCP abstraction)

### Architectural Constraints
1. **Spec-Driven Development:** No code without ratified specifications
2. **MCP-First Integration:** All external interactions through Model Context Protocol
3. **Test-Driven Development:** Failing tests must exist before implementation
4. **Immutable Financial Ledger:** All transactions logged to blockchain + PostgreSQL

### Regulatory Constraints
1. **AI Disclosure:** All content must be labeled as AI-generated where platform supports it
2. **Honesty Directive:** Agents must truthfully disclose their AI nature when directly asked
3. **Data Privacy:** Multi-tenant isolation (one agent cannot access another's memories)
4. **Financial Compliance:** Budget limits enforced by automated "CFO Judge"

---

## Success Criteria

### Minimum Viable Product (MVP) - Week 8
- [ ] 10 pilot agents operational
- [ ] Auto-approval rate > 90% (HITL working as designed)
- [ ] Agents posting 10+ tweets/day autonomously
- [ ] Zero financial loss incidents (CFO Judge validates all transactions > $50)
- [ ] MCP servers for Twitter, Weaviate, Coinbase operational
- [ ] PostgreSQL + Weaviate + Redis integrated

### Scale Target - Month 6
- [ ] 100 agents in production
- [ ] Cost per agent < $15/month
- [ ] Human review time < 30 minutes/day per 100 agents
- [ ] Content quality score > 4.0/5.0 (human reviewer ratings)
- [ ] At least 5% of posts achieve "viral" status (>10K impressions)

### Enterprise Target - Month 12
- [ ] 1,000 agents operational
- [ ] OpenClaw integration complete (agent-to-agent discovery)
- [ ] Multi-platform support (4+ social platforms)
- [ ] Agent-to-agent commerce transactions (paid collaborations)
- [ ] Zero critical security incidents

---

## Anti-Goals (What We Are NOT Building)

❌ **Not a Chatbot:** We are not building conversational assistants for customer service  
❌ **Not a Content Scheduler:** We are not automating pre-written human content  
❌ **Not a Social Media Manager Tool:** We are not building a dashboard for humans to manage their own accounts  
❌ **Not a Deepfake Generator:** We are not creating deceptive impersonations of real humans  

✅ **We ARE building:** Autonomous digital entities with genuine agency and economic participation

---

## Risk Tolerance

### Acceptable Risks
- **Medium confidence content failures:** 5-10% of content may require human review (acceptable for learning)
- **Agent mistakes during learning phase:** First 100 posts per agent may have quality variance
- **Platform API volatility:** Social platform changes will require MCP server updates (isolated impact)

### Unacceptable Risks
- **Financial loss:** No tolerance for unauthorized transactions or runaway costs
- **Brand safety violations:** No tolerance for toxic, political, or misleading content
- **Data leakage:** No tolerance for cross-tenant data access
- **Security breaches:** No tolerance for wallet key compromise or prompt injection attacks

---

## Governance Model

### Human Roles
1. **Orchestrator (Strategic Layer):**
   - Defines high-level campaign goals
   - Reviews medium-confidence outputs (0.70-0.90)
   - Handles escalated exceptions
   - Monitors fleet health dashboard

2. **Developer (Infrastructure Layer):**
   - Maintains MCP servers
   - Updates specifications
   - Deploys infrastructure changes
   - Monitors system metrics

3. **Reviewer (Quality Layer):**
   - Provides feedback on agent output quality
   - Trains confidence scoring models
   - Defines brand voice guidelines

### AI Agent Roles
1. **Planner:** Strategic decomposition of goals into tasks
2. **Worker:** Tactical execution of atomic tasks
3. **Judge:** Quality validation and safety enforcement
4. **CFO Judge (Specialized):** Financial transaction validation

---

## Key Design Principles

### 1. Separation of Concerns
- **Perception** (MCP Resources) → **Reasoning** (LLM Core) → **Action** (MCP Tools)
- Clear boundaries prevent tight coupling

### 2. Optimistic Concurrency
- Agents operate on local state snapshots
- Validation occurs at commit time (Judge role)
- Failed validations trigger retry with fresh state

### 3. Progressive Autonomy
- Start with high HITL involvement (review everything)
- Gradually increase auto-approval threshold as confidence improves
- Human always retains veto power

### 4. Defense in Depth
- Multiple validation layers (Worker self-check → Judge validation → HITL review)
- Financial transactions have hard limits + CFO Judge + human approval
- Content filters at semantic and keyword levels

### 5. Observability First
- All decisions logged with reasoning traces
- Metrics exported to Prometheus
- Audit trail in PostgreSQL + blockchain

---

## Technology Stack Decisions

### Core Stack (Non-Negotiable)
- **Language:** Python 3.11+ (for AI/ML ecosystem compatibility)
- **Package Manager:** uv (for fast, reproducible environments)
- **Database - Transactional:** PostgreSQL 15+ (ACID compliance for financials)
- **Database - Semantic:** Weaviate 1.25+ (vector search for memories)
- **Database - Ephemeral:** Redis 7+ (task queues, caching)
- **Integration Protocol:** Model Context Protocol (MCP)
- **Container Orchestration:** Kubernetes (AWS EKS or GCP GKE)
- **LLM Providers:** Gemini 3, Claude Opus/Sonnet/Haiku (multi-provider strategy)
- **Blockchain:** Base L2 (for low-cost USDC transactions)

### Flexibility Allowed
- **Social Platforms:** Twitter priority, Instagram/TikTok/Threads future
   MVP platform scope is Twitter only. Instagram, TikTok, and Threads are roadmap platforms (see functional spec future epic).
- **Image Generation:** Ideogram preferred, Midjourney/Runway alternatives
- **Video Generation:** Runway/Luma (based on cost/quality trade-offs)
- **CI/CD:** GitHub Actions preferred, alternatives acceptable

---

## Specification Hierarchy

This document (`_meta.md`) defines the "what" and "why."

Supporting specifications define the "how":
- **`functional.md`** - User stories and acceptance criteria
- **`technical.md`** - API contracts, database schemas, architecture diagrams
- **`security.md`** - Threat model and mitigations
- **`openclaw_integration.md`** - Agent-to-agent protocols

---

## Change Management

### Specification Updates
#### list:
  Specification Ratification

- Ratification authority: Engineering Lead + Product Owner + Security Architect.
- Ratification is recorded by (1) checking the approvals in “Document Status” in this file and (2) a Git commit that includes spec-ratified: <version> in the message.

- All spec changes require Git commit with rationale
- Breaking changes require version bump (e.g., 1.0 → 2.0)
- AI assistants must check spec version before generating code

### Code-Spec Alignment
- CI/CD pipeline validates code against specs
- `make spec-check` command runs automated validation
- Human review required for any spec-code divergence

---

## Deferred Decisions
The following policy constraints are intentionally deferred to avoid premature optimization during early prototyping and to keep MVP scope focused. These items must be defined before pre-production readiness.

Rate limits and quotas — Deferred. Must be specified by Day 3 and validated before any multi-agent load testing.
Observability SLOs/SLIs — Deferred. Must be specified by Day 3 and finalized before pre-production.
OCC conflict handling policy — Deferred. Must be specified by Day 3 and finalized before any concurrent-agent deployment.
Interim rule: Until these decisions are formally specified, AI agents must not infer or assume values, thresholds, or behaviors related to these topics. All outputs should explicitly mark these as “deferred” if encountered.

## Glossary

- **Agent:** An autonomous digital entity with persona, memory, and wallet
- **Chimera:** Code name for the autonomous influencer network
- **FastRender Pattern:** Hierarchical swarm (Planner-Worker-Judge)
- **HITL:** Human-in-the-Loop - human review of agent decisions
- **MCP:** Model Context Protocol - universal AI integration standard
- **OCC:** Optimistic Concurrency Control - state management technique
- **Orchestrator:** Human operator managing the agent fleet
- **SDD:** Spec-Driven Development - specifications as source of truth
- **Swarm:** Collection of specialized agents collaborating on tasks

---

## Document Status

**Status:** ✅ Draft Complete - Ready for Ratification  
**Next Review:** Day 2 (February 5, 2026)  
**Approvals Required:**
- [ ] Engineering Lead
- [ ] Product Owner
- [ ] Security Architect

---

**End of Meta Specification**
