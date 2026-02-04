# Project Chimera: Agent Skills

**Purpose:** This directory contains reusable capabilities that Chimera agents can invoke during task execution.

**Note:** Skills are different from MCP Servers:
- **Skills** = Internal Python functions/modules that agents can call
- **MCP Servers** = External services that expose tools/resources via MCP protocol

---

## Skill Architecture

Each skill is a self-contained module with:
- Clear input/output contracts (Pydantic models)
- Error handling and retries
- Comprehensive logging
- Unit tests

---

## Defined Skills (Day 1)

### Skill 1: `skill_trend_discovery`

**Purpose:** Discover trending topics relevant to an agent's niche

**Input Schema:**
```python
from pydantic import BaseModel
from typing import List, Optional

class TrendDiscoveryInput(BaseModel):
    agent_id: str
    niche: str
    region: str
    time_window_hours: int = 24
    min_relevance_score: float = 0.75
```

**Output Schema:**
```python
class TrendDiscoveryOutput(BaseModel):
    trends: List[dict]  # [{title, description, relevance_score, source_url}]
    discovery_timestamp: str
    agent_id: str
```

**Implementation Status:** 🔴 Not Implemented (Spec Only)

**Dependencies:**
- `mcp-server-newsdata` (for news aggregation)
- Weaviate (for semantic filtering)

**Example Usage:**
```python
from skills.trend_discovery import discover_trends

result = await discover_trends(
    agent_id="uuid",
    niche="ethiopian_fashion",
    region="ethiopia"
)

for trend in result.trends:
    print(f"{trend['title']} - Relevance: {trend['relevance_score']}")
```

---

### Skill 2: `skill_content_generation`

**Purpose:** Generate complete social media post (caption + image specifications)

**Input Schema:**
```python
class ContentGenerationInput(BaseModel):
    agent_id: str
    topic: str
    platform: str  # "twitter", "instagram", etc.
    content_type: str  # "post", "story", "reel"
    character_reference_id: Optional[str]  # For image consistency
```

**Output Schema:**
```python
class ContentGenerationOutput(BaseModel):
    caption: str
    image_prompt: str  # For image generation tool
    hashtags: List[str]
    confidence_score: float
    reasoning_trace: str  # Why this content was generated
```

**Implementation Status:** 🔴 Not Implemented (Spec Only)

**Dependencies:**
- Weaviate (retrieve persona + past successful posts)
- LLM (Gemini 3 Flash or Claude Haiku for content generation)

**Quality Criteria:**
- Caption length appropriate for platform (280 chars for Twitter)
- Hashtags relevant to niche (3-5 hashtags)
- Confidence score based on semantic similarity to training data

**Example Usage:**
```python
from skills.content_generation import generate_content

result = await generate_content(
    agent_id="uuid",
    topic="New sustainable fashion trend in Addis Ababa",
    platform="twitter"
)

if result.confidence_score > 0.90:
    # Proceed to image generation and publishing
    pass
```

---

### Skill 3: `skill_engagement_analysis`

**Purpose:** Analyze engagement metrics and recommend optimization strategies

**Input Schema:**
```python
class EngagementAnalysisInput(BaseModel):
    agent_id: str
    post_ids: List[str]
    time_range_days: int = 7
```

**Output Schema:**
```python
class EngagementAnalysisOutput(BaseModel):
    avg_likes: float
    avg_comments: float
    avg_shares: float
    top_performing_topics: List[str]
    best_posting_times: List[str]  # Hours in UTC
    recommendations: List[str]  # Actionable insights
```

**Implementation Status:** 🔴 Not Implemented (Spec Only)

**Dependencies:**
- PostgreSQL (task_log with engagement data)
- Weaviate (semantic analysis of top posts)

**Example Usage:**
```python
from skills.engagement_analysis import analyze_engagement

result = await analyze_engagement(
    agent_id="uuid",
    time_range_days=7
)

print(f"Average engagement: {result.avg_likes} likes")
print(f"Best times to post: {result.best_posting_times}")
```

---

## Skill Development Guidelines

### 1. Structure
Each skill should be in its own subdirectory:
```
skills/
├── trend_discovery/
│   ├── __init__.py
│   ├── main.py          # Core logic
│   ├── schemas.py       # Pydantic models
│   └── tests.py         # Unit tests
├── content_generation/
└── engagement_analysis/
```

### 2. Error Handling
All skills must implement robust error handling:
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def skill_function(input_data):
    try:
        # Implementation
        pass
    except ExternalAPIError as e:
        logger.error(f"API failed: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise
```

### 3. Logging
Use structured logging for traceability:
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "skill_executed",
    skill_name="trend_discovery",
    agent_id=agent_id,
    execution_time_ms=elapsed_ms
)
```

### 4. Testing
Every skill requires:
- Unit tests with mocked dependencies
- Integration tests with real services (marked as `@pytest.mark.integration`)

```python
# tests/test_trend_discovery.py
import pytest
from skills.trend_discovery import discover_trends

@pytest.mark.unit
async def test_trend_discovery_filters_low_relevance(mock_mcp_client):
    # Test that trends below min_relevance_score are filtered
    pass

@pytest.mark.integration
async def test_trend_discovery_real_api():
    # Test with real MCP server
    pass
```

---

## Skill Invocation Pattern (Worker → Skill)

Workers invoke skills as part of task execution:

```python
# In worker service
from skills.content_generation import generate_content

async def execute_content_task(task: dict) -> dict:
    # 1. Validate task
    # 2. Call appropriate skill
    result = await generate_content(
        agent_id=task["agent_id"],
        topic=task["context"]["topic"],
        platform="twitter"
    )
    
    # 3. Return result to Judge
    return {
        "task_id": task["task_id"],
        "result": result.dict(),
        "confidence_score": result.confidence_score
    }
```

---

## Future Skills (Post-MVP)

- `skill_video_generation` - Generate short-form video content
- `skill_comment_response` - Context-aware reply generation
- `skill_collaboration_negotiation` - Agent-to-agent deal making
- `skill_budget_optimization` - Recommend cost-saving strategies
- `skill_persona_evolution` - Update persona based on engagement data

---

## Skill vs MCP Server Decision Matrix

| Use Skill | Use MCP Server |
|-----------|----------------|
| Complex multi-step logic | Simple CRUD operations |
| Requires multiple MCP calls | Single external API call |
| Agent-specific business logic | Platform-generic functionality |
| Needs rich error handling | Stateless request/response |

**Example:**
- ✅ **Skill:** `generate_content()` - Orchestrates persona retrieval, LLM generation, validation
- ✅ **MCP Server:** `post_tweet()` - Wraps Twitter API directly

---

## Development Status

**Day 1:** ✅ Skill contracts defined (this README)  
**Day 2:** 🔴 Implement `skill_trend_discovery`  
**Day 2:** 🔴 Implement `skill_content_generation`  
**Day 3:** 🔴 Implement `skill_engagement_analysis`

---

**Last Updated:** February 4, 2026  
**Status:** Specification Complete - Ready for Implementation
