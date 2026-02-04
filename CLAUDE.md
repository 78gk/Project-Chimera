# Project Chimera: AI Assistant Context File

**Purpose:** This file provides context to AI coding assistants (Claude, Cursor, GitHub Copilot) working on Project Chimera.

---

## PROJECT CONTEXT

**Project Name:** Chimera - Autonomous Influencer Network  
**Architecture:** FastRender Hierarchical Swarm (Planner-Worker-Judge)  
**Integration:** Model Context Protocol (MCP) for all external interactions  
**Development Methodology:** Spec-Driven Development (SDD)

---

## THE PRIME DIRECTIVE

⚠️ **NEVER generate implementation code without first checking the `specs/` directory.**

All code must align with:
1. `specs/_meta.md` - Vision and constraints
2. `specs/functional.md` - User stories and acceptance criteria  
3. `specs/technical.md` - API contracts and database schemas
4. `specs/openclaw_integration.md` - Agent protocols

---

## WORKFLOW FOR AI ASSISTANTS

### When asked to implement a feature:

1. **CHECK SPECS FIRST**
   ```
   Read specs/_meta.md for constraints
   Read specs/functional.md for user stories
   Read specs/technical.md for API contracts
   ```

2. **EXPLAIN YOUR PLAN**
   - Summarize the relevant spec requirements
   - Outline your implementation approach
   - Identify any spec gaps or ambiguities
   - Wait for human confirmation before coding

3. **IMPLEMENT WITH TRACEABILITY**
   - Reference spec requirement IDs in code comments
   - Follow the database schemas exactly as defined
   - Use MCP tools via the defined interfaces
   - Write tests first (TDD approach)

4. **VALIDATE AGAINST SPECS**
   - Ensure your code matches the API contracts
   - Verify database schema compliance
   - Check that error handling matches requirements

---

## ARCHITECTURAL RULES

### Rule 1: FastRender Pattern is Mandatory
- **Planner:** Decomposes goals, creates tasks
- **Worker:** Executes single atomic tasks (stateless)
- **Judge:** Validates outputs, enforces OCC

**Never** merge these roles into a single agent.

### Rule 2: MCP for All External Interactions
- **No direct API calls** to Twitter, Instagram, databases, etc.
- All external calls go through MCP Tools
- Perception uses MCP Resources
- Reasoning templates use MCP Prompts

**Example - WRONG:**
```python
import twitter_api
twitter_api.post_tweet("Hello world")  # ❌ Direct API call
```

**Example - CORRECT:**
```python
mcp_client.call_tool("mcp-server-twitter", "post_tweet", {
    "text": "Hello world"
})  # ✅ Via MCP
```

### Rule 3: Database Schema is Immutable
- The PostgreSQL schema in `specs/technical.md` is the source of truth
- Use SQLAlchemy ORM models that match the schema exactly
- **Never** add columns without updating the spec first

### Rule 4: Test-Driven Development
- Write failing tests before implementation
- Tests encode acceptance criteria from `specs/functional.md`
- Place tests in `tests/` directory
- Run tests with `make test`

---

## CODE STYLE GUIDELINES

### Python
- **Formatter:** Black (line length 88)
- **Linter:** Ruff
- **Type Hints:** Required for all public functions
- **Docstrings:** Google style

```python
from typing import Optional

def example_function(agent_id: str, confidence: float) -> Optional[dict]:
    """Execute a task for the specified agent.
    
    Args:
        agent_id: UUID of the agent
        confidence: Confidence score (0.0-1.0)
        
    Returns:
        Task result dictionary, or None if failed
        
    Raises:
        ValueError: If confidence is out of range
    """
    pass
```

### Async/Await
- Use `async/await` for all I/O operations (database, API calls, MCP)
- Use `asyncio.gather()` for parallel operations

### Error Handling
- Use custom exceptions (defined in `src/exceptions.py`)
- Always log errors with context (agent_id, task_id, etc.)
- Never swallow exceptions silently

---

## COMMON PATTERNS

### Pattern 1: Planner Creates Task
```python
task = {
    "task_id": str(uuid.uuid4()),
    "task_type": "generate_content",
    "agent_id": agent_id,
    "context": {
        "goal": "Promote sneaker drop",
        "persona_constraints": persona.voice_traits
    },
    "state_version": get_current_state_version(agent_id),
    "created_at": datetime.utcnow().isoformat()
}
redis_client.lpush(f"task_queue:{agent_id}", json.dumps(task))
```

### Pattern 2: Worker Executes Task
```python
async def execute_task(task: dict) -> dict:
    # 1. Retrieve context from Weaviate
    memories = await mcp_client.call_tool(
        "mcp-server-weaviate", 
        "search_memory",
        {"agent_id": task["agent_id"], "query": task["context"]["goal"]}
    )
    
    # 2. Generate content using LLM
    result = await llm.generate(prompt=construct_prompt(task, memories))
    
    # 3. Return with confidence score
    return {
        "task_id": task["task_id"],
        "result": result,
        "confidence_score": calculate_confidence(result)
    }
```

### Pattern 3: Judge Validates Output
```python
def validate_output(result: dict, task: dict) -> str:
    # Check confidence threshold
    if result["confidence_score"] < 0.70:
        return "reject"
    
    # Check state version (OCC)
    current_version = get_state_version(task["agent_id"])
    if task["state_version"] != current_version:
        return "reject"  # State changed, retry needed
    
    # Auto-approve or escalate
    if result["confidence_score"] >= 0.90:
        return "approve"
    else:
        return "hitl_review"  # Human review required
```

---

## SECURITY REQUIREMENTS

1. **Never log sensitive data:**
   - Wallet private keys
   - API keys
   - User passwords

2. **Always validate input:**
   - Sanitize user-provided content
   - Validate agent_id ownership (multi-tenancy)
   - Check budget limits before transactions

3. **Use environment variables for secrets:**
   ```python
   import os
   API_KEY = os.getenv("GEMINI_API_KEY")
   if not API_KEY:
       raise ValueError("GEMINI_API_KEY not set")
   ```

---

## TRACEABILITY COMMENTS

Every function should include a traceability comment linking to specs:

```python
def create_agent(persona: dict) -> str:
    """Create a new autonomous agent.
    
    Spec: functional.md - Story 1.1: Create New Agent
    API: technical.md - POST /agents
    """
    pass
```

---

## QUESTIONS TO ASK BEFORE IMPLEMENTING

1. **Does this feature have a spec?** → If no, ask human to write spec first
2. **Does the API contract match technical.md?** → If no, update spec
3. **Are there acceptance tests?** → If no, write tests first
4. **Does this use MCP for external calls?** → If no, refactor to use MCP
5. **Is this testable in isolation?** → If no, refactor for dependency injection

---

## WHEN IN DOUBT

- **Read the specs** in `specs/` directory
- **Ask the human** for clarification
- **Propose a plan** before writing code
- **Write tests first** to encode requirements

**Remember:** Spec-Driven Development prevents architectural drift. The spec is the source of truth.

---

## PROJECT STRUCTURE OVERVIEW

```
project-chimera/
├── specs/                 # Source of truth (READ FIRST)
├── src/
│   ├── planner/          # Planner service
│   ├── worker/           # Worker pool
│   ├── judge/            # Judge service
│   └── mcp_servers/      # Custom MCP server implementations
├── skills/               # Reusable agent capabilities
├── tests/                # TDD tests (write first)
├── docs/                 # SRS and research
└── research/             # Architecture decisions
```

---

## HELPFUL COMMANDS

```bash
# Setup environment
make setup

# Run tests
make test

# Validate code against specs
make spec-check

# Format code
make format

# Start development environment
make dev
```

---

**Last Updated:** February 4, 2026  
**For Questions:** Review `specs/_meta.md` or ask the human orchestrator
