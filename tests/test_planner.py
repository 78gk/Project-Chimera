"""Test suite for Planner service (FastRender Hierarchical Swarm pattern).

This test file validates the Planner interface from specs/technical.md Section 7.1.

Status: FAILING TESTS (TDD Approach)
- Tests define the Planner contract before implementation
- Planner decomposes goals into executable tasks
"""

import pytest
from datetime import datetime
from typing import List, Dict, Any
from enum import Enum


# Import from specs - these modules don't exist yet (TDD)
try:
    from src.planner.agent_planner import AgentPlanner, Task, TaskPriority, TaskDAG
except ImportError:
    AgentPlanner = None
    Task = None
    TaskPriority = None
    TaskDAG = None


class TestTaskModel:
    """Test Task data model from specs/technical.md Section 7.1."""

    def test_task_model_schema(self):
        """Test Task model has required fields."""
        if Task is None:
            pytest.fail("Task model not implemented (src/planner/agent_planner.py)")
        
        # Required fields per specs
        required_fields = [
            "task_id",
            "task_type",
            "agent_id",
            "priority",
            "context",
            "dependencies",
            "created_at",
        ]
        
        # Create a task
        task = Task(
            task_id="task_123",
            task_type="generate_content",
            agent_id="agent_550e8400",
            priority=TaskPriority.HIGH,
            context={"goal": "Create post about trending topic"},
            dependencies=[],
            created_at=datetime.utcnow(),
        )
        
        for field in required_fields:
            assert hasattr(task, field), f"Task missing field: {field}"
    
    def test_task_priority_enum(self):
        """Test TaskPriority enum has correct values."""
        if TaskPriority is None:
            pytest.skip("TaskPriority enum not implemented")
        
        expected_priorities = {"HIGH", "MEDIUM", "LOW"}
        actual_priorities = {p.name for p in TaskPriority}
        
        assert expected_priorities == actual_priorities


class TestAgentPlannerInitialization:
    """Test AgentPlanner initialization and configuration."""

    def test_planner_initialization(self, mock_redis_client, mock_mcp_client):
        """Test AgentPlanner can be initialized with required dependencies."""
        if AgentPlanner is None:
            pytest.fail("AgentPlanner not implemented (src/planner/agent_planner.py)")
        
        planner = AgentPlanner(
            agent_id="agent_550e8400",
            redis_client=mock_redis_client,
            llm_client=None,  # Will be mocked
        )
        
        assert planner.agent_id == "agent_550e8400"
        assert planner.redis is not None
    
    def test_planner_requires_agent_id(self, mock_redis_client):
        """Test AgentPlanner requires agent_id parameter."""
        if AgentPlanner is None:
            pytest.skip("AgentPlanner not implemented")
        
        with pytest.raises(TypeError):
            AgentPlanner(redis_client=mock_redis_client)


class TestGoalDecomposition:
    """Test Planner's goal decomposition logic (specs/technical.md Section 7.1)."""

    @pytest.mark.asyncio
    async def test_decompose_goal_returns_task_list(self, mock_redis_client):
        """Test decompose_goal() returns list of Task objects."""
        if AgentPlanner is None:
            pytest.skip("AgentPlanner not implemented")
        
        planner = AgentPlanner(
            agent_id="agent_550e8400",
            redis_client=mock_redis_client,
            llm_client=None,
        )
        
        tasks = await planner.decompose_goal("Promote sustainable fashion week")
        
        assert isinstance(tasks, list)
        assert len(tasks) > 0
        
        for task in tasks:
            assert isinstance(task, Task)
    
    @pytest.mark.asyncio
    async def test_decompose_goal_creates_task_dag(self, mock_redis_client):
        """Test decompose_goal() creates task DAG with dependencies."""
        if AgentPlanner is None:
            pytest.skip("AgentPlanner not implemented")
        
        planner = AgentPlanner(
            agent_id="agent_550e8400",
            redis_client=mock_redis_client,
            llm_client=None,
        )
        
        # Goal should decompose into multiple steps
        tasks = await planner.decompose_goal("Promote sustainable fashion week")
        
        # Expected DAG structure (per specs example):
        # 1. research_trends (no dependencies)
        # 2. generate_content (depends on research_trends)
        # 3. publish_content (depends on generate_content)
        
        task_types = [task.task_type for task in tasks]
        
        # Should have research as first step
        assert "research_trends" in task_types or "discover_trends" in task_types
        
        # Later tasks should have dependencies
        dependent_tasks = [t for t in tasks if len(t.dependencies) > 0]
        assert len(dependent_tasks) > 0
    
    @pytest.mark.asyncio
    async def test_decompose_goal_assigns_priorities(self, mock_redis_client):
        """Test decompose_goal() assigns appropriate task priorities."""
        if AgentPlanner is None:
            pytest.skip("AgentPlanner not implemented")
        
        planner = AgentPlanner(
            agent_id="agent_550e8400",
            redis_client=mock_redis_client,
            llm_client=None,
        )
        
        tasks = await planner.decompose_goal("Create urgent post about trending topic")
        
        # At least one task should be HIGH priority
        high_priority_tasks = [t for t in tasks if t.priority == TaskPriority.HIGH]
        assert len(high_priority_tasks) > 0


class TestTaskEnqueuing:
    """Test Planner's task enqueuing to Redis (specs/technical.md)."""

    @pytest.mark.asyncio
    async def test_enqueue_task_pushes_to_redis(self, mock_redis_client):
        """Test enqueue_task() pushes task to Redis queue."""
        if AgentPlanner is None:
            pytest.skip("AgentPlanner not implemented")
        
        planner = AgentPlanner(
            agent_id="agent_550e8400",
            redis_client=mock_redis_client,
            llm_client=None,
        )
        
        task = Task(
            task_id="task_123",
            task_type="generate_content",
            agent_id="agent_550e8400",
            priority=TaskPriority.HIGH,
            context={"goal": "test"},
            dependencies=[],
            created_at=datetime.utcnow(),
        )
        
        await planner.enqueue_task(task)
        
        # Verify Redis lpush was called
        mock_redis_client.lpush.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_enqueue_respects_dependencies(self, mock_redis_client):
        """Test tasks with dependencies are not enqueued until deps complete."""
        if AgentPlanner is None:
            pytest.skip("AgentPlanner not implemented")
        
        planner = AgentPlanner(
            agent_id="agent_550e8400",
            redis_client=mock_redis_client,
            llm_client=None,
        )
        
        # Task with unmet dependency
        dependent_task = Task(
            task_id="task_456",
            task_type="publish_content",
            agent_id="agent_550e8400",
            priority=TaskPriority.MEDIUM,
            context={"goal": "test"},
            dependencies=["task_123"],  # Depends on another task
            created_at=datetime.utcnow(),
        )
        
        # Should not enqueue immediately
        result = await planner.enqueue_task(dependent_task)
        
        # Implementation should track pending dependencies
        assert result is False or mock_redis_client.lpush.call_count == 0


class TestResourcePolling:
    """Test Planner's resource polling from specs/technical.md Section 7.1."""

    @pytest.mark.asyncio
    async def test_poll_resources_calls_mcp_tools(self, mock_redis_client, mock_mcp_client):
        """Test poll_resources() calls MCP tools to discover trends."""
        if AgentPlanner is None:
            pytest.skip("AgentPlanner not implemented")
        
        # Mock MCP response
        mock_mcp_client.call_tool.return_value = {
            "trends": [
                {"topic": "Ethiopian fashion week", "volume": 15000, "relevance": 0.92}
            ]
        }
        
        planner = AgentPlanner(
            agent_id="agent_550e8400",
            redis_client=mock_redis_client,
            llm_client=None,
        )
        planner.mcp_client = mock_mcp_client
        planner.agent_status = "active"
        
        # Poll should call MCP
        await planner.poll_resources()
        
        # Verify MCP tool was called
        mock_mcp_client.call_tool.assert_called()
    
    @pytest.mark.asyncio
    async def test_poll_creates_tasks_for_relevant_trends(self, mock_redis_client, mock_mcp_client):
        """Test poll_resources() creates tasks for relevant trends."""
        if AgentPlanner is None:
            pytest.skip("AgentPlanner not implemented")
        
        # Mock relevant trend
        mock_mcp_client.call_tool.return_value = {
            "trends": [
                {"topic": "sustainable fashion", "relevance": 0.95}
            ]
        }
        
        planner = AgentPlanner(
            agent_id="agent_550e8400",
            redis_client=mock_redis_client,
            llm_client=None,
        )
        planner.mcp_client = mock_mcp_client
        planner.agent_status = "active"
        
        await planner.poll_resources()
        
        # Should have enqueued at least one task
        assert mock_redis_client.lpush.call_count > 0


class TestPlannerLLMIntegration:
    """Test Planner's LLM integration for goal decomposition."""

    @pytest.mark.asyncio
    async def test_builds_planning_prompt(self, mock_redis_client):
        """Test Planner builds appropriate LLM prompt for goal decomposition."""
        if AgentPlanner is None:
            pytest.skip("AgentPlanner not implemented")
        
        planner = AgentPlanner(
            agent_id="agent_550e8400",
            redis_client=mock_redis_client,
            llm_client=None,
        )
        
        # Should have method to build prompt
        if hasattr(planner, "_build_planning_prompt"):
            prompt = planner._build_planning_prompt("Promote fashion week")
            
            assert isinstance(prompt, str)
            assert "fashion week" in prompt.lower()
            assert "task" in prompt.lower() or "step" in prompt.lower()
    
    @pytest.mark.asyncio
    async def test_validates_task_dag(self, mock_redis_client):
        """Test Planner validates task DAG before enqueuing."""
        if AgentPlanner is None:
            pytest.skip("AgentPlanner not implemented")
        
        planner = AgentPlanner(
            agent_id="agent_550e8400",
            redis_client=mock_redis_client,
            llm_client=None,
        )
        
        # Create circular dependency (invalid DAG)
        task1 = Task(
            task_id="task_1",
            task_type="step1",
            agent_id="agent_550e8400",
            priority=TaskPriority.HIGH,
            context={},
            dependencies=["task_2"],
            created_at=datetime.utcnow(),
        )
        
        task2 = Task(
            task_id="task_2",
            task_type="step2",
            agent_id="agent_550e8400",
            priority=TaskPriority.HIGH,
            context={},
            dependencies=["task_1"],  # Circular!
            created_at=datetime.utcnow(),
        )
        
        # Should detect and reject circular dependency
        if hasattr(planner, "_validate_task_dag"):
            with pytest.raises(ValueError):
                planner._validate_task_dag([task1, task2])


class TestPlannerErrorHandling:
    """Test Planner error handling and edge cases."""

    @pytest.mark.asyncio
    async def test_handles_empty_goal(self, mock_redis_client):
        """Test Planner handles empty goal string gracefully."""
        if AgentPlanner is None:
            pytest.skip("AgentPlanner not implemented")
        
        planner = AgentPlanner(
            agent_id="agent_550e8400",
            redis_client=mock_redis_client,
            llm_client=None,
        )
        
        with pytest.raises((ValueError, Exception)):
            await planner.decompose_goal("")
    
    @pytest.mark.asyncio
    async def test_handles_llm_timeout(self, mock_redis_client):
        """Test Planner handles LLM timeout gracefully."""
        from asyncio import TimeoutError as AsyncTimeoutError
        from unittest.mock import AsyncMock
        
        if AgentPlanner is None:
            pytest.skip("AgentPlanner not implemented")
        
        mock_llm = AsyncMock(side_effect=AsyncTimeoutError())
        
        planner = AgentPlanner(
            agent_id="agent_550e8400",
            redis_client=mock_redis_client,
            llm_client=mock_llm,
        )
        
        with pytest.raises((AsyncTimeoutError, Exception)):
            await planner.decompose_goal("test goal")


class TestPlannerStateManagement:
    """Test Planner maintains agent state correctly."""

    @pytest.mark.asyncio
    async def test_tracks_agent_status(self, mock_redis_client):
        """Test Planner tracks agent status (active/paused/stopped)."""
        if AgentPlanner is None:
            pytest.skip("AgentPlanner not implemented")
        
        planner = AgentPlanner(
            agent_id="agent_550e8400",
            redis_client=mock_redis_client,
            llm_client=None,
        )
        
        # Should have status attribute
        assert hasattr(planner, "agent_status")
        
        # Default should be active or stopped
        assert planner.agent_status in ["active", "stopped", "paused"]
    
    @pytest.mark.asyncio
    async def test_stops_polling_when_inactive(self, mock_redis_client, mock_mcp_client):
        """Test Planner stops resource polling when agent inactive."""
        if AgentPlanner is None:
            pytest.skip("AgentPlanner not implemented")
        
        planner = AgentPlanner(
            agent_id="agent_550e8400",
            redis_client=mock_redis_client,
            llm_client=None,
        )
        planner.mcp_client = mock_mcp_client
        planner.agent_status = "stopped"
        
        # Poll should not call MCP when stopped
        await planner.poll_resources()
        
        # Should not have called MCP
        assert mock_mcp_client.call_tool.call_count == 0


# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit
