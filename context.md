# PROJECT CONTEXT
Last Updated: 2026-02-05 13:33 UTC | Version: v1.0.0

## 🎯 PRIMARY GOAL
Build an autonomous AI influencer system managing 1,000+ agents with a single human orchestrator using FastRender Hierarchical Swarm architecture and Model Context Protocol.

## 📋 ACTIVE OBJECTIVES
- [x] Day 1: Research & Foundation - Complete (priority: HIGH)
- [ ] Day 2: Specifications & Context Engineering - In Progress (priority: HIGH)
- [ ] Day 3: Infrastructure & Governance - Pending (priority: HIGH)
- [ ] Implement core agent patterns (Planner-Worker-Judge) (priority: HIGH)
- [ ] Integrate MCP for platform independence (priority: HIGH)

## 🏗️ ARCHITECTURE DECISIONS

### Agent Pattern: FastRender Hierarchical Swarm
```
Planner (Strategy) → Task Queue → Worker Pool (Execution) → Review Queue → Judge (Quality Control)
```
**Rationale**: Specialization + parallelism + built-in QA for scale

### Integration Layer: Model Context Protocol (MCP)
**Rationale**: Platform independence, maintainability, prevents vendor lock-in

### Database: Polyglot Persistence
- **PostgreSQL**: Transactional data (users, campaigns, financial ledger)
- **Weaviate**: Semantic memory (agent personas, interaction history)
- **Redis**: Ephemeral queues (task coordination, caching)
**Rationale**: Each database optimized for its specific workload

### Development Methodology: Spec-Driven Development (SDD)
**Rationale**: Prevents AI hallucination at scale, maintains architectural discipline

### HITL Strategy: Confidence-Based Routing
- **> 0.90 confidence** → Auto-approve (95% of actions)
- **0.70-0.90 confidence** → Async human review (5% of actions)
- **< 0.70 confidence** → Auto-reject & retry
**Rationale**: 90%+ autonomy with safety guardrails

## 🚫 CONSTRAINTS & NON-NEGOTIABLES
1. **Single Human Orchestrator**: System must operate with minimal human intervention
2. **Cost Target**: < $15/agent/month at 1,000 agent scale
3. **Auto-Approval Rate**: > 90% to maintain autonomy
4. **Worker Task Latency**: < 10 seconds (p95)
5. **System Uptime**: 99.5%
6. **Spec-First Development**: No implementation without specifications
7. **MCP Integration**: All external tools must use MCP standard

## 📁 PROJECT STRUCTURE
```
project-chimera/
├── docs/                          # Project documentation & SRS
├── research/                      # Strategic research & architecture decisions
├── specs/                         # GitHub Spec Kit specifications
├── skills/                        # Agent runtime capabilities
├── tests/                         # Test-Driven Development
├── src/                           # Implementation
│   ├── planner/                  # Strategy layer
│   ├── worker/                   # Execution layer
│   └── judge/                    # Quality control layer
├── pyproject.toml                 # Python project definition
├── Dockerfile                     # Containerization
└── Makefile                       # Automation commands
```

## 🛠️ TECHNOLOGY STACK
- **Language**: Python 3.11+
- **Package Manager**: uv
- **Databases**: PostgreSQL, Weaviate, Redis
- **Integration**: Model Context Protocol (MCP)
- **Commerce**: Coinbase AgentKit
- **Containerization**: Docker
- **CI/CD**: GitHub Actions

## 📊 SUCCESS METRICS

### Technical KPIs
- Worker Task Latency: < 10 seconds (p95)
- Auto-Approval Rate: > 90%
- System Uptime: 99.5%

### Business KPIs
- Cost per Agent: < $15/month
- Human Review Time: < 30 min/day per 100 agents
- Content Quality Score: > 4.0/5.0

## 💰 COST MODEL (1,000 agents at scale)
- Infrastructure: $1,500/month
- LLM APIs: $8,000/month
- Data storage: $500/month
- **Total: ~$10/agent/month**

## ✅ COMPLETED MILESTONES
- [x] Research synthesis (Agent Social Networks, MCP, SDD)
- [x] Architecture strategy document
- [x] Day 1 submission report
- [x] Git repository initialization
- [x] Specs directory structure with GitHub Spec Kit

## 🔄 CURRENT STATUS
**Phase**: Day 1 Complete → Day 2 In Progress  
**Focus**: Specifications & Context Engineering  
**Role**: Forward Deployed Engineer (FDE) Trainee

### Next Immediate Actions
1. Complete technical specifications in specs/
2. Define agent skills and MCP tooling strategy
3. Write failing tests (TDD approach)
4. Setup Python environment with uv
5. Configure MCP Sense connection

## 📚 KEY DOCUMENTS
- `README.md` - Project overview and quick start
- `docs/Project_Chimera_SRS.md` - Software Requirements Specification
- `docs/Project_Chimera_3Day_Challenge.md` - Challenge requirements
- `research/research_notes.md` - Deep dive: Agent Networks, MCP, SDD
- `research/architecture_strategy.md` - Technical decisions & justifications
- `specs/_meta.md` - Specification metadata and governance
- `DAY1_SUBMISSION_REPORT.md` - Day 1 deliverable

## 🔐 SECURITY & GOVERNANCE
- All code changes require specification alignment
- HITL approval required for confidence < 0.90
- Financial transactions require explicit human approval
- Agent behavior must be auditable and traceable

## 🎓 LESSONS LEARNED
- Spec-Driven Development prevents scope creep
- MCP provides clean abstraction for integrations
- Confidence-based routing balances autonomy with safety
- Polyglot persistence optimizes for workload characteristics

---

## 📝 CHANGELOG

### v1.0.0 - 2026-02-05 13:33 UTC
**Initial Context Creation**
- Synthesized project context from README, SRS, and 3-Day Challenge docs
- Established primary goal: 1,000+ agent autonomous influencer system
- Documented architecture decisions (FastRender Swarm, MCP, Polyglot DB)
- Defined constraints (< $15/agent/month, > 90% auto-approval)
- Set success metrics (technical and business KPIs)
- Captured Day 1 completion status
- Identified Day 2 objectives (specs, skills, TDD)
