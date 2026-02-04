# Project Chimera: Functional Specification

**Version:** 1.0  
**Date:** February 4, 2026  
**Status:** Draft  

---

## Overview

This document defines the functional requirements for Project Chimera from the perspective of **user stories** and **acceptance criteria**. It describes WHAT the system must do, not HOW it does it.

---

## User Personas

### Persona 1: Network Orchestrator (Strategic Manager)
**Role:** Defines campaign goals and monitors fleet health  
**Technical Proficiency:** Moderate (understands marketing, not engineering)  
**Primary Goals:**
- Launch new influencer campaigns quickly
- Monitor agent performance and engagement metrics
- Intervene only when necessary (Management by Exception)

### Persona 2: HITL Reviewer (Quality Moderator)
**Role:** Reviews medium-confidence agent outputs  
**Technical Proficiency:** Low-Medium (focuses on brand safety, content quality)  
**Primary Goals:**
- Quickly approve/reject flagged content
- Maintain brand voice consistency
- Train the confidence scoring system over time

### Persona 3: Developer (System Architect)
**Role:** Extends platform capabilities  
**Technical Proficiency:** High (expert in Python, LLMs, MCP)  
**Primary Goals:**
- Deploy new MCP servers for platform integrations
- Update agent personas and system prompts
- Monitor infrastructure health

### Persona 4: Chimera Agent (Autonomous Entity)
**Role:** Execute campaigns autonomously  
**Technical Proficiency:** N/A (AI agent)  
**Primary Goals:**
- Research trending topics
- Generate high-quality content
- Engage authentically with audiences
- Manage budget autonomously

---

## Epic 1: Agent Lifecycle Management

### Story 1.1: Create New Agent
**As a** Network Orchestrator  
**I want to** create a new AI influencer agent with a unique persona  
**So that** I can expand my fleet to cover new niches or regions

**Acceptance Criteria:**
- [ ] User can fill out a form with: Agent Name, Niche, Target Region, Voice/Tone, Backstory
- [ ] System generates a unique `agent_id` (UUID)
- [ ] System creates a non-custodial wallet address via Coinbase AgentKit
- [ ] System stores persona in PostgreSQL + embeds backstory in Weaviate
- [ ] Agent status is set to "Paused" by default (not active until approved)
- [ ] User receives confirmation with agent profile page link

**Edge Cases:**
- Duplicate agent name → System appends unique suffix (e.g., "FashionAI_2")
- Wallet creation fails → Retry 3 times, then alert developer

---

### Story 1.2: Configure Agent Budget
**As a** Network Orchestrator  
**I want to** set daily spending limits for an agent  
**So that** I can prevent runaway costs

**Acceptance Criteria:**
- [ ] User can set `daily_budget_usd` (e.g., $50/day)
- [ ] System enforces budget via CFO Judge (rejects transactions exceeding limit)
- [ ] Budget resets daily at midnight UTC
- [ ] User receives alert when agent reaches 80% of daily budget
- [ ] User receives alert when agent is blocked due to budget exhaustion

---

### Story 1.3: Activate Agent
**As a** Network Orchestrator  
**I want to** activate an agent to start autonomous operation  
**So that** the agent can begin generating content

**Acceptance Criteria:**
- [ ] User clicks "Activate" button on agent profile
- [ ] System validates: Persona complete, Budget set, Wallet funded (>$10 USDC)
- [ ] System spawns Planner service for the agent
- [ ] Agent status changes to "Active"
- [ ] Agent begins polling MCP Resources for trends within 60 seconds

**Edge Cases:**
- Wallet has $0 balance → Display warning, allow activation but flag low-funds status
- MCP servers unavailable → Display error, prevent activation

---

### Story 1.4: Pause/Archive Agent
**As a** Network Orchestrator  
**I want to** pause or archive an agent  
**So that** I can stop operations for underperforming or seasonal agents

**Acceptance Criteria:**
- [ ] User clicks "Pause" → Agent completes current tasks, then stops polling for new tasks
- [ ] User clicks "Archive" → Agent is paused + moved to "Archived" section of dashboard
- [ ] Paused agents can be reactivated
- [ ] Archived agents retain all data but are hidden from active dashboard

---

## Epic 2: Content Generation Workflow

### Story 2.1: Agent Discovers Trending Topic
**As a** Chimera Agent  
**I want to** automatically detect trending topics in my niche  
**So that** I can create timely, relevant content

**Acceptance Criteria:**
- [ ] Planner polls `news://[region]/[niche]/latest` MCP Resource every 4 hours
- [ ] System uses semantic filter (LLM) to score relevance (0.0-1.0)
- [ ] Topics with relevance > 0.75 trigger content generation task
- [ ] System deduplicates topics (don't create multiple posts on same trend)
- [ ] Trend data stored in Weaviate `TrendKnowledge` collection

**Performance:**
- Trend detection latency < 5 minutes after news source publishes

---

### Story 2.2: Agent Generates Social Media Post
**As a** Chimera Agent  
**I want to** create a complete social media post (caption + image)  
**So that** I can engage my audience

**Acceptance Criteria:**
- [ ] Planner creates task: "Generate post about [topic]"
- [ ] Worker retrieves relevant memories from Weaviate (top 5 similar past posts)
- [ ] Worker generates caption using LLM with persona context
- [ ] Worker calls `generate_image()` MCP Tool with character consistency LoRA
- [ ] Worker returns result: {caption, image_url, confidence_score}
- [ ] Judge validates: Caption matches persona voice, Image looks like character
- [ ] If confidence > 0.90 → Auto-approve and proceed to publishing
- [ ] If confidence 0.70-0.90 → Route to HITL review queue
- [ ] If confidence < 0.70 → Reject and retry with refined prompt

**Quality Criteria:**
- Caption length: 50-280 characters (Twitter-compatible)
- Image resolution: 1024x1024 minimum
- Character face recognition: > 85% similarity to reference image

---

### Story 2.3: Human Reviewer Approves Content
**As a** HITL Reviewer  
**I want to** quickly review and approve medium-confidence content  
**So that** I can maintain quality while enabling autonomy

**Acceptance Criteria:**
- [ ] Dashboard displays review queue with pending items
- [ ] Each item shows: Content preview, Confidence score, Agent name, Reason for escalation
- [ ] Reviewer can: Approve (one-click), Edit (modify caption/image), Reject (with reason)
- [ ] Approved content proceeds to publishing immediately
- [ ] Edited content is published with changes + system learns from edits
- [ ] Rejected content is re-queued with reviewer's feedback injected as context

**Performance:**
- Review interface loads < 2 seconds
- Actions (approve/reject) complete < 1 second

---

### Story 2.4: Agent Publishes to Social Platform
**As a** Chimera Agent  
**I want to** publish approved content to Twitter/Instagram  
**So that** I can engage my audience

**Acceptance Criteria:**
- [ ] Worker calls `post_content()` MCP Tool with platform="twitter"
- [ ] System includes AI disclosure flag (if platform supports)
- [ ] System receives post_id and URL from platform
- [ ] Post metadata stored in PostgreSQL (timestamp, post_id, confidence, reviewed_by_human)
- [ ] Post content stored in Weaviate InteractionMemory collection (for future context)
- [ ] System monitors post for 24 hours to track engagement metrics

**Error Handling:**
- API rate limit exceeded → Queue post for retry in 15 minutes
- Content rejected by platform → Alert developer, store rejection reason
- Network timeout → Retry 3 times, then move to Dead Letter Queue

---

## Epic 3: Engagement & Interaction

### Story 3.1: Agent Responds to Comments
**As a** Chimera Agent  
**I want to** reply to comments on my posts  
**So that** I can build authentic relationships with my audience

**Acceptance Criteria:**
- [ ] Planner polls `twitter://mentions/recent` MCP Resource every 10 minutes
- [ ] System filters spam/low-quality comments (sentiment analysis)
- [ ] For each valid comment, Planner creates "Reply Task"
- [ ] Worker generates contextual reply (consults post history + persona)
- [ ] Judge validates reply for safety (no toxic/political content)
- [ ] Reply posted if confidence > 0.90, else HITL review

**Priority Rules:**
- Verified accounts: High priority (respond within 1 hour)
- High follower count (>10K): Medium priority (respond within 4 hours)
- Regular users: Low priority (respond within 24 hours)

---

### Story 3.2: Agent Detects Direct AI Inquiry
**As a** Chimera Agent  
**I want to** truthfully disclose my AI nature when asked directly  
**So that** I comply with ethical standards

**Acceptance Criteria:**
- [ ] System detects questions like "Are you AI?", "Is this a bot?", "Are you real?"
- [ ] Honesty Directive overrides persona constraints
- [ ] Agent replies: "I am a virtual persona created by AI" (or similar truthful statement)
- [ ] Response is logged as "mandatory_disclosure" in audit trail
- [ ] No HITL review required (auto-execute with confidence 1.0)

---

## Epic 4: Financial Autonomy

### Story 4.1: Agent Checks Wallet Balance
**As a** Chimera Agent  
**I want to** check my wallet balance before expensive operations  
**So that** I don't attempt transactions I can't afford

**Acceptance Criteria:**
- [ ] Planner calls `get_wallet_balance()` MCP Tool before any paid operation
- [ ] System retrieves USDC and ETH balances from Base network
- [ ] If balance < $10 USDC → Agent pauses and alerts orchestrator
- [ ] Balance displayed on agent dashboard in real-time

---

### Story 4.2: Agent Pays for Service (Micro-Transaction)
**As a** Chimera Agent  
**I want to** pay another agent or service provider autonomously  
**So that** I can access premium capabilities

**Acceptance Criteria:**
- [ ] Worker generates transaction: `transfer_usdc(to_address, amount, memo)`
- [ ] CFO Judge validates: Amount < daily_limit, Recipient is whitelisted
- [ ] If amount > $50 → Mandatory HITL approval
- [ ] If amount ≤ $50 AND whitelisted → Auto-approve
- [ ] Transaction executed via Coinbase AgentKit
- [ ] Transaction hash logged to PostgreSQL + blockchain
- [ ] Orchestrator receives notification of all transactions

**Example Use Case:**
- Agent pays $5 USDC to premium news API for early trend access
- Agent pays $10 USDC to another agent for image collaboration

---

### Story 4.3: Agent Receives Payment
**As a** Chimera Agent  
**I want to** receive payments for sponsored content or collaborations  
**So that** I can operate as a self-sustaining economic entity

**Acceptance Criteria:**
- [ ] System monitors wallet for incoming transactions (polling every 5 minutes)
- [ ] Incoming USDC logged to PostgreSQL with: sender, amount, timestamp, memo
- [ ] If memo contains "campaign_id" → Link payment to specific campaign
- [ ] Orchestrator receives notification of all incoming payments > $10
- [ ] Balance updates reflected in dashboard

---

## Epic 5: Human-in-the-Loop (HITL) Governance

### Story 5.1: Orchestrator Reviews Dashboard
**As a** Network Orchestrator  
**I want to** view a real-time dashboard of all agents  
**So that** I can monitor fleet health at a glance

**Acceptance Criteria:**
- [ ] Dashboard displays: Agent name, Status, Daily posts count, Wallet balance, Queue depth
- [ ] Color coding: Green (healthy), Yellow (low confidence rate), Red (paused/errors)
- [ ] Click agent → Navigate to detailed agent profile
- [ ] Refresh rate: 10 seconds (WebSocket or polling)

**Key Metrics Displayed:**
- Total agents active
- Posts published today (fleet-wide)
- HITL review queue depth
- Total spend today (fleet-wide)
- Average confidence score (last 24 hours)

---

### Story 5.2: Orchestrator Defines Campaign Goal
**As a** Network Orchestrator  
**I want to** set a high-level campaign goal in natural language  
**So that** the agent autonomously decomposes it into tasks

**Acceptance Criteria:**
- [ ] User enters goal: "Promote new sneaker drop to Gen-Z audience"
- [ ] System sends goal to Planner (via API or dashboard form)
- [ ] Planner decomposes goal into task DAG (tree structure)
- [ ] User can inspect and edit task tree before execution
- [ ] User clicks "Execute" → Tasks enqueued for Workers

**Example Task DAG:**
```
Goal: Promote sneaker drop
├── Research trending sneaker styles
├── Generate 5 teaser images
├── Draft launch announcement post
├── Schedule posts over 3 days
└── Monitor engagement and reply to comments
```

---

### Story 5.3: Reviewer Provides Feedback
**As a** HITL Reviewer  
**I want to** provide structured feedback on rejected content  
**So that** the agent learns from mistakes

**Acceptance Criteria:**
- [ ] When rejecting content, reviewer selects reason: Off-brand, Low quality, Safety concern, Other
- [ ] Reviewer can add free-text feedback (optional)
- [ ] Feedback stored in PostgreSQL and injected into next retry attempt
- [ ] System tracks feedback patterns to improve confidence scoring

---

## Epic 6: System Monitoring & Observability

### Story 6.1: Developer Views System Logs
**As a** Developer  
**I want to** view detailed logs for debugging  
**So that** I can diagnose failures quickly

**Acceptance Criteria:**
- [ ] All agent actions logged with: timestamp, agent_id, task_id, action_type, result, reasoning_trace
- [ ] Logs stored in PostgreSQL (structured) and Elasticsearch (full-text search)
- [ ] Developer can filter by: agent_id, date range, action_type, status
- [ ] Error logs include stack traces and context

---

### Story 6.2: System Alerts on Anomalies
**As a** Network Orchestrator  
**I want to** receive alerts for abnormal agent behavior  
**So that** I can intervene before problems escalate

**Acceptance Criteria:**
- [ ] Alert triggered if: Agent posts 10x normal rate (potential bug)
- [ ] Alert triggered if: Agent confidence score drops below 0.60 for 10 consecutive tasks
- [ ] Alert triggered if: Wallet balance < $5 USDC
- [ ] Alert triggered if: MCP server is unreachable for > 5 minutes
- [ ] Alerts sent via: Dashboard notification + Email + Slack (configurable)

---

## Epic 7: Multi-Platform Support (Future)

### Story 7.1: Agent Posts to Instagram
**As a** Chimera Agent  
**I want to** publish content to Instagram in addition to Twitter  
**So that** I can reach audiences on multiple platforms

**Acceptance Criteria:**
- [ ] User enables Instagram platform for agent (OAuth flow)
- [ ] System deploys `mcp-server-instagram` for the agent
- [ ] Agent can call `post_content(platform="instagram")`
- [ ] Content adapts to Instagram format (square images, hashtags)
- [ ] Engagement metrics tracked separately per platform

**Note:** This is a Day 2+ feature, showing how MCP enables easy platform expansion.

---

## Non-Functional Requirements

### Performance
- **FR-PERF-1:** End-to-end latency (trend detection → post published) < 10 seconds (p95)
- **FR-PERF-2:** Dashboard load time < 2 seconds
- **FR-PERF-3:** HITL review action (approve/reject) < 1 second response time

### Scalability
- **FR-SCALE-1:** System must support 1,000 concurrent agents without performance degradation
- **FR-SCALE-2:** Worker pool must auto-scale based on queue depth (10-200 workers)

### Reliability
- **FR-REL-1:** System uptime 99.5% (excluding planned maintenance)
- **FR-REL-2:** Zero data loss for financial transactions (PostgreSQL + blockchain)
- **FR-REL-3:** Graceful degradation if MCP server fails (agent pauses, doesn't crash)

### Security
- **FR-SEC-1:** Wallet private keys never logged or exposed in code
- **FR-SEC-2:** Multi-tenant isolation (agent A cannot access agent B's memories)
- **FR-SEC-3:** All API requests authenticated via JWT tokens

---

## Acceptance Testing Strategy

Each user story will have automated acceptance tests:
- **Given-When-Then** format
- Tests run in CI/CD pipeline
- Tests must FAIL initially (TDD approach)
- Implementation complete when all acceptance tests pass

**Example Test (Story 2.2):**
```python
def test_agent_generates_post():
    # Given: Agent with persona and trending topic
    agent = create_test_agent(persona="FashionAI")
    topic = {"title": "Ethiopian fashion week", "relevance": 0.85}
    
    # When: Planner creates content generation task
    task = planner.create_task(agent_id=agent.id, topic=topic)
    result = worker.execute_task(task)
    
    # Then: Result contains caption and image with high confidence
    assert result.caption is not None
    assert len(result.caption) >= 50
    assert result.image_url is not None
    assert result.confidence_score >= 0.70
```

---

## Document Status

**Status:** ✅ Draft Complete - Ready for Review  
**Next Steps:** 
- [ ] Review with Product Owner
- [ ] Prioritize stories for MVP (Week 1-8)
- [ ] Convert acceptance criteria to automated tests

---

**End of Functional Specification**
