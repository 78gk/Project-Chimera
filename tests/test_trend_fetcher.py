"""Test suite for trend discovery and fetching functionality.

This test file validates that trend data structures match the API contracts
defined in specs/technical.md and skills/README.md.

Status: FAILING TESTS (TDD Approach)
- Tests define the contract that implementation must satisfy
- Tests should fail until src/planner/trend_fetcher.py is implemented
"""

import pytest
from datetime import datetime
from typing import List, Dict, Any
from pydantic import ValidationError


# Import from specs - these modules don't exist yet (TDD)
# This will cause ImportError - which is expected for TDD
try:
    from src.planner.trend_fetcher import TrendFetcher, Trend, TrendSource
except ImportError:
    # Create placeholder classes for type hints
    TrendFetcher = None
    Trend = None
    TrendSource = None


class TestTrendDataStructure:
    """Test that trend data structures match API contract from specs/technical.md."""

    def test_trend_model_schema(self):
        """Test that Trend model has required fields per specs."""
        # This test will fail until Trend model is implemented
        if Trend is None:
            pytest.fail("Trend model not implemented yet (src/planner/trend_fetcher.py)")
        
        # Expected schema from skills/README.md (TrendDiscoveryOutput)
        required_fields = {
            "trend_id": str,
            "topic": str,
            "relevance_score": float,
            "volume": int,
            "source": str,
            "discovered_at": datetime,
        }
        
        # Validate Trend model has all required fields
        for field_name, field_type in required_fields.items():
            assert hasattr(Trend, field_name), f"Trend model missing field: {field_name}"
        
    def test_trend_relevance_score_range(self):
        """Test that relevance_score is constrained between 0.0 and 1.0."""
        if Trend is None:
            pytest.skip("Trend model not implemented yet")
        
        # Valid trend
        valid_trend_data = {
            "trend_id": "trend_123",
            "topic": "sustainable fashion",
            "relevance_score": 0.85,
            "volume": 10000,
            "source": "twitter",
            "discovered_at": datetime.utcnow(),
        }
        
        trend = Trend(**valid_trend_data)
        assert 0.0 <= trend.relevance_score <= 1.0
        
        # Invalid trend - score too high
        invalid_trend_data = valid_trend_data.copy()
        invalid_trend_data["relevance_score"] = 1.5
        
        with pytest.raises(ValidationError):
            Trend(**invalid_trend_data)
    
    def test_trend_volume_positive(self):
        """Test that volume is always a positive integer."""
        if Trend is None:
            pytest.skip("Trend model not implemented yet")
        
        # Invalid trend - negative volume
        with pytest.raises(ValidationError):
            Trend(
                trend_id="trend_123",
                topic="test",
                relevance_score=0.5,
                volume=-100,
                source="twitter",
                discovered_at=datetime.utcnow(),
            )


class TestTrendFetcherInterface:
    """Test TrendFetcher API contract from specs/technical.md Section 7.1."""

    @pytest.fixture
    def mock_mcp_client(self):
        """Mock MCP client for testing."""
        from unittest.mock import AsyncMock, MagicMock
        
        client = MagicMock()
        client.call_tool = AsyncMock(return_value={
            "trends": [
                {
                    "topic": "Ethiopian Fashion Week",
                    "volume": 15000,
                    "relevance_score": 0.92,
                }
            ]
        })
        return client

    @pytest.mark.asyncio
    async def test_trend_fetcher_initialization(self, mock_mcp_client):
        """Test that TrendFetcher can be initialized with MCP client."""
        if TrendFetcher is None:
            pytest.fail("TrendFetcher not implemented yet (src/planner/trend_fetcher.py)")
        
        fetcher = TrendFetcher(mcp_client=mock_mcp_client)
        assert fetcher.mcp_client is not None
    
    @pytest.mark.asyncio
    async def test_fetch_trends_returns_list(self, mock_mcp_client):
        """Test that fetch_trends() returns a list of Trend objects."""
        if TrendFetcher is None:
            pytest.skip("TrendFetcher not implemented yet")
        
        fetcher = TrendFetcher(mcp_client=mock_mcp_client)
        
        trends = await fetcher.fetch_trends(
            niche="fashion",
            region="ET",  # Ethiopia
            time_window_hours=24,
        )
        
        assert isinstance(trends, list)
        assert len(trends) > 0
        
        # Each item should be a Trend object
        for trend in trends:
            assert isinstance(trend, Trend)
    
    @pytest.mark.asyncio
    async def test_fetch_trends_filters_by_relevance(self, mock_mcp_client):
        """Test that fetch_trends() filters by min_relevance_score."""
        if TrendFetcher is None:
            pytest.skip("TrendFetcher not implemented yet")
        
        fetcher = TrendFetcher(mcp_client=mock_mcp_client)
        
        # Fetch with high relevance threshold
        trends = await fetcher.fetch_trends(
            niche="fashion",
            region="ET",
            min_relevance_score=0.8,
        )
        
        # All returned trends should meet threshold
        for trend in trends:
            assert trend.relevance_score >= 0.8
    
    @pytest.mark.asyncio
    async def test_fetch_trends_handles_empty_results(self, mock_mcp_client):
        """Test that fetch_trends() handles case when no trends found."""
        # Mock returns empty list
        mock_mcp_client.call_tool.return_value = {"trends": []}
        
        if TrendFetcher is None:
            pytest.skip("TrendFetcher not implemented yet")
        
        fetcher = TrendFetcher(mcp_client=mock_mcp_client)
        trends = await fetcher.fetch_trends(niche="obscure_topic")
        
        assert isinstance(trends, list)
        assert len(trends) == 0


class TestTrendFetcherMCPIntegration:
    """Test MCP tool integration for trend discovery."""

    @pytest.mark.asyncio
    async def test_calls_correct_mcp_tool(self, mock_mcp_client):
        """Test that TrendFetcher calls the correct MCP tool."""
        if TrendFetcher is None:
            pytest.skip("TrendFetcher not implemented yet")
        
        fetcher = TrendFetcher(mcp_client=mock_mcp_client)
        
        await fetcher.fetch_trends(
            niche="fashion",
            region="ET",
            time_window_hours=24,
        )
        
        # Verify MCP tool was called with correct name
        mock_mcp_client.call_tool.assert_called_once()
        call_args = mock_mcp_client.call_tool.call_args
        
        # First argument should be tool name
        assert call_args[0][0] in ["get_trending_topics", "discover_trends"]
    
    @pytest.mark.asyncio
    async def test_mcp_tool_receives_correct_parameters(self, mock_mcp_client):
        """Test that MCP tool receives parameters matching skills/README.md schema."""
        if TrendFetcher is None:
            pytest.skip("TrendFetcher not implemented yet")
        
        fetcher = TrendFetcher(mcp_client=mock_mcp_client)
        
        await fetcher.fetch_trends(
            niche="fashion",
            region="ET",
            time_window_hours=24,
            min_relevance_score=0.75,
        )
        
        # Verify parameters match TrendDiscoveryInput schema
        call_args = mock_mcp_client.call_tool.call_args
        params = call_args[0][1]  # Second argument is params dict
        
        assert "niche" in params
        assert "region" in params
        assert params["niche"] == "fashion"
        assert params["region"] == "ET"
    
    @pytest.mark.asyncio
    async def test_handles_mcp_timeout(self, mock_mcp_client):
        """Test graceful handling of MCP server timeout."""
        from asyncio import TimeoutError as AsyncTimeoutError
        
        mock_mcp_client.call_tool.side_effect = AsyncTimeoutError()
        
        if TrendFetcher is None:
            pytest.skip("TrendFetcher not implemented yet")
        
        fetcher = TrendFetcher(mcp_client=mock_mcp_client)
        
        # Should handle timeout gracefully (return empty list or raise custom exception)
        with pytest.raises((AsyncTimeoutError, Exception)):
            await fetcher.fetch_trends(niche="fashion")


class TestTrendCaching:
    """Test trend caching to reduce API calls (from specs/technical.md Section 12.2)."""

    @pytest.mark.asyncio
    async def test_cached_trends_returned_within_ttl(self, mock_mcp_client):
        """Test that cached trends are returned without calling MCP again."""
        if TrendFetcher is None:
            pytest.skip("TrendFetcher not implemented yet")
        
        fetcher = TrendFetcher(mcp_client=mock_mcp_client, cache_ttl_seconds=300)
        
        # First call - should hit MCP
        trends_1 = await fetcher.fetch_trends(niche="fashion", region="ET")
        assert mock_mcp_client.call_tool.call_count == 1
        
        # Second call with same params - should use cache
        trends_2 = await fetcher.fetch_trends(niche="fashion", region="ET")
        assert mock_mcp_client.call_tool.call_count == 1  # Still 1, not 2
        
        # Results should be identical
        assert len(trends_1) == len(trends_2)
    
    @pytest.mark.asyncio
    async def test_cache_expires_after_ttl(self, mock_mcp_client):
        """Test that cache expires after TTL."""
        import asyncio
        
        if TrendFetcher is None:
            pytest.skip("TrendFetcher not implemented yet")
        
        fetcher = TrendFetcher(mcp_client=mock_mcp_client, cache_ttl_seconds=1)
        
        # First call
        await fetcher.fetch_trends(niche="fashion")
        assert mock_mcp_client.call_tool.call_count == 1
        
        # Wait for cache to expire
        await asyncio.sleep(1.5)
        
        # Second call - should hit MCP again
        await fetcher.fetch_trends(niche="fashion")
        assert mock_mcp_client.call_tool.call_count == 2


class TestTrendSourceEnum:
    """Test TrendSource enum for valid source types."""

    def test_trend_source_valid_values(self):
        """Test that TrendSource enum has expected values."""
        if TrendSource is None:
            pytest.skip("TrendSource enum not implemented yet")
        
        # Expected sources from specs
        expected_sources = {"twitter", "google_trends", "news", "reddit"}
        
        actual_sources = {source.value for source in TrendSource}
        
        assert expected_sources.issubset(actual_sources), \
            f"Missing sources: {expected_sources - actual_sources}"


# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit
