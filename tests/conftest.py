"""Pytest configuration and shared fixtures for Project Chimera tests."""

import pytest
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_mcp_client() -> MagicMock:
    """Mock MCP client for unit tests."""
    client = MagicMock()
    client.call_tool = AsyncMock()
    client.list_tools = AsyncMock(return_value=[])
    return client


@pytest.fixture
def mock_redis_client() -> MagicMock:
    """Mock Redis client for unit tests."""
    client = MagicMock()
    client.lpush = MagicMock(return_value=1)
    client.brpop = MagicMock(return_value=(b"queue", b'{"task_id": "test"}'))
    return client


@pytest.fixture
def sample_agent_data() -> dict:
    """Sample agent configuration for testing."""
    return {
        "agent_id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "TestAgent",
        "persona": {
            "backstory": "Test backstory",
            "voice_traits": ["witty", "friendly"],
            "core_beliefs": ["sustainability"]
        },
        "budget_daily_usd": 50.00,
        "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    }


@pytest.fixture
def sample_task() -> dict:
    """Sample task for testing worker execution."""
    return {
        "task_id": "task-123",
        "task_type": "generate_content",
        "agent_id": "550e8400-e29b-41d4-a716-446655440000",
        "priority": "high",
        "context": {
            "goal": "Create post about trending topic",
            "topic": "Ethiopian fashion week"
        },
        "state_version": 42
    }
