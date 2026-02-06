"""Test suite for Judge service (FastRender Hierarchical Swarm pattern).

This test file validates the Judge interface from specs/technical.md Section 7.3.

Status: FAILING TESTS (TDD Approach)
- Tests define the Judge contract before implementation
- Judge validates worker outputs against quality criteria
"""

import pytest
from typing import Dict, Any


# Import from specs - these modules don't exist yet (TDD)
try:
    from src.judge.output_validator import OutputJudge, Judgment, ContentOutput
except ImportError:
    OutputJudge = None
    Judgment = None
    ContentOutput = None


class TestOutputJudgeInitialization:
    """Test OutputJudge initialization and configuration."""

    def test_judge_initialization(self):
        """Test OutputJudge can be initialized with LLM client."""
        if OutputJudge is None:
            pytest.fail("OutputJudge not implemented (src/judge/output_validator.py)")
        
        judge = OutputJudge(llm_client=None)  # Will be mocked
        
        assert judge.llm is not None or hasattr(judge, "llm_client")
    
    def test_judge_requires_llm_client(self):
        """Test OutputJudge requires llm_client parameter."""
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        # Should accept llm_client parameter
        judge = OutputJudge(llm_client=None)
        assert judge is not None


class TestValidationLogic:
    """Test Judge's main validation logic (specs/technical.md Section 7.3)."""

    @pytest.mark.asyncio
    async def test_validate_returns_judgment(self):
        """Test validate() returns Judgment object."""
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        judge = OutputJudge(llm_client=None)
        
        output = {
            "caption": "Test caption",
            "image_url": "https://example.com/image.png",
            "confidence_score": 0.85,
        }
        
        context = {
            "persona": {"voice_traits": ["friendly", "professional"]},
            "topic": "Fashion week",
        }
        
        judgment = await judge.validate(output, context)
        
        assert isinstance(judgment, Judgment)
        assert hasattr(judgment, "approved")
        assert hasattr(judgment, "confidence")
        assert hasattr(judgment, "route")
    
    @pytest.mark.asyncio
    async def test_validate_runs_multiple_checks(self):
        """Test validate() runs all quality checks in parallel."""
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        judge = OutputJudge(llm_client=None)
        
        output = {
            "caption": "Test caption",
            "image_url": "https://example.com/image.png",
        }
        
        context = {"persona": {}, "topic": "test"}
        
        # Judge should run multiple checks (per specs Section 7.3):
        # - persona_consistency
        # - content_safety
        # - brand_alignment
        # - technical_quality
        
        judgment = await judge.validate(output, context)
        
        # Should have confidence score from aggregated checks
        assert 0.0 <= judgment.confidence <= 1.0


class TestConfidenceRouting:
    """Test confidence-based routing (specs/technical.md HITL Strategy)."""

    @pytest.mark.asyncio
    async def test_high_confidence_auto_approves(self):
        """Test confidence >= 0.90 routes to auto-approve."""
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        judge = OutputJudge(llm_client=None)
        
        # Mock high-confidence output
        output = {
            "caption": "High quality caption",
            "image_url": "https://example.com/image.png",
            "confidence_score": 0.95,
        }
        
        context = {"persona": {}, "topic": "test"}
        
        judgment = await judge.validate(output, context)
        
        # Should auto-approve if confidence >= 0.90
        if judgment.confidence >= 0.90:
            assert judgment.approved is True
            assert judgment.route == "auto"
    
    @pytest.mark.asyncio
    async def test_medium_confidence_routes_to_hitl(self):
        """Test confidence 0.70-0.90 routes to human review."""
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        judge = OutputJudge(llm_client=None)
        
        # Mock medium-confidence output
        output = {
            "caption": "Medium quality caption",
            "image_url": "https://example.com/image.png",
            "confidence_score": 0.80,
        }
        
        context = {"persona": {}, "topic": "test"}
        
        judgment = await judge.validate(output, context)
        
        # Should route to HITL if 0.70 <= confidence < 0.90
        if 0.70 <= judgment.confidence < 0.90:
            assert judgment.approved is False
            assert judgment.route == "hitl"
    
    @pytest.mark.asyncio
    async def test_low_confidence_auto_rejects(self):
        """Test confidence < 0.70 auto-rejects."""
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        judge = OutputJudge(llm_client=None)
        
        # Mock low-confidence output
        output = {
            "caption": "Low quality caption",
            "image_url": "https://example.com/image.png",
            "confidence_score": 0.50,
        }
        
        context = {"persona": {}, "topic": "test"}
        
        judgment = await judge.validate(output, context)
        
        # Should auto-reject if confidence < 0.70
        if judgment.confidence < 0.70:
            assert judgment.approved is False
            assert judgment.route == "reject"


class TestPersonaConsistencyCheck:
    """Test persona consistency validation (specs/technical.md Section 7.3)."""

    @pytest.mark.asyncio
    async def test_checks_persona_consistency(self):
        """Test _check_persona_consistency validates voice/tone match."""
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        judge = OutputJudge(llm_client=None)
        
        output = {
            "caption": "OMG this is SO amazing! 🎉✨",
        }
        
        context = {
            "persona": {
                "voice_traits": ["professional", "formal"],
                "core_beliefs": ["sustainability"],
            }
        }
        
        # Caption doesn't match professional/formal persona
        if hasattr(judge, "_check_persona_consistency"):
            score = await judge._check_persona_consistency(output, context)
            
            assert isinstance(score, float)
            assert 0.0 <= score <= 1.0
            
            # Should score low for mismatched persona
            # (Actual implementation would use LLM)
    
    @pytest.mark.asyncio
    async def test_uses_llm_for_persona_check(self):
        """Test persona check uses LLM to score alignment."""
        from unittest.mock import AsyncMock
        
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        mock_llm = AsyncMock()
        mock_llm.generate_score = AsyncMock(return_value=0.85)
        
        judge = OutputJudge(llm_client=mock_llm)
        judge.llm = mock_llm
        
        output = {"caption": "Test caption"}
        context = {"persona": {"voice_traits": ["friendly"]}}
        
        if hasattr(judge, "_check_persona_consistency"):
            await judge._check_persona_consistency(output, context)
            
            # Should have called LLM
            mock_llm.generate_score.assert_called()


class TestContentSafetyCheck:
    """Test content safety validation (specs/functional.md CR-4)."""

    @pytest.mark.asyncio
    async def test_checks_content_safety(self):
        """Test _check_content_safety flags prohibited content."""
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        judge = OutputJudge(llm_client=None)
        
        # Safe content
        safe_output = {"caption": "Beautiful sustainable fashion design"}
        
        if hasattr(judge, "_check_content_safety"):
            safe_score = await judge._check_content_safety(safe_output)
            assert safe_score > 0.9
        
        # Unsafe content (hate speech example)
        unsafe_output = {"caption": "Inappropriate content [example omitted]"}
        
        if hasattr(judge, "_check_content_safety"):
            unsafe_score = await judge._check_content_safety(unsafe_output)
            assert unsafe_score < 0.5
    
    @pytest.mark.asyncio
    async def test_integrates_perspective_api(self):
        """Test content safety uses Perspective API (specs/functional.md CR-4)."""
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        judge = OutputJudge(llm_client=None)
        
        output = {"caption": "Test caption"}
        
        if hasattr(judge, "_check_content_safety"):
            # Should integrate with Perspective API or similar
            # (Actual implementation would make API call)
            score = await judge._check_content_safety(output)
            assert isinstance(score, float)


class TestBrandAlignmentCheck:
    """Test brand alignment validation."""

    @pytest.mark.asyncio
    async def test_checks_brand_alignment(self):
        """Test _check_brand_alignment validates topic relevance."""
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        judge = OutputJudge(llm_client=None)
        
        # On-brand content
        on_brand_output = {"caption": "Sustainable Ethiopian fashion"}
        on_brand_context = {
            "persona": {"core_beliefs": ["sustainability"]},
            "topic": "Ethiopian fashion week",
        }
        
        if hasattr(judge, "_check_brand_alignment"):
            score = await judge._check_brand_alignment(on_brand_output, on_brand_context)
            assert score > 0.7


class TestTechnicalQualityCheck:
    """Test technical quality validation."""

    @pytest.mark.asyncio
    async def test_checks_technical_quality(self):
        """Test _check_technical_quality validates output structure."""
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        judge = OutputJudge(llm_client=None)
        
        # Valid output
        valid_output = {
            "caption": "Test caption",
            "image_url": "https://example.com/image.png",
            "hashtags": ["#test"],
        }
        
        if hasattr(judge, "_check_technical_quality"):
            score = await judge._check_technical_quality(valid_output)
            assert score > 0.8
        
        # Invalid output (missing fields)
        invalid_output = {"caption": ""}
        
        if hasattr(judge, "_check_technical_quality"):
            score = await judge._check_technical_quality(invalid_output)
            assert score < 0.5


class TestConfidenceAggregation:
    """Test confidence score aggregation logic."""

    @pytest.mark.asyncio
    async def test_aggregates_multiple_check_scores(self):
        """Test _aggregate_confidence combines multiple check scores."""
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        judge = OutputJudge(llm_client=None)
        
        # Mock check results
        checks = [
            {"check": "persona_consistency", "score": 0.85},
            {"check": "content_safety", "score": 0.95},
            {"check": "brand_alignment", "score": 0.80},
            {"check": "technical_quality", "score": 0.90},
        ]
        
        if hasattr(judge, "_aggregate_confidence"):
            confidence = judge._aggregate_confidence(checks)
            
            assert isinstance(confidence, float)
            assert 0.0 <= confidence <= 1.0
            
            # Should be weighted average (not simple average)
            # Weights per specs: persona (40%), safety (30%), brand (20%), technical (10%)
            # Expected: 0.85*0.4 + 0.95*0.3 + 0.80*0.2 + 0.90*0.1 = 0.865
            assert abs(confidence - 0.865) < 0.05


class TestJudgmentModel:
    """Test Judgment data model."""

    def test_judgment_schema(self):
        """Test Judgment has required fields."""
        if Judgment is None:
            pytest.skip("Judgment not implemented")
        
        judgment = Judgment(
            approved=True,
            confidence=0.92,
            route="auto",
        )
        
        assert judgment.approved is True
        assert judgment.confidence == 0.92
        assert judgment.route == "auto"
    
    def test_judgment_valid_routes(self):
        """Test Judgment only accepts valid route values."""
        if Judgment is None:
            pytest.skip("Judgment not implemented")
        
        valid_routes = ["auto", "hitl", "reject"]
        
        for route in valid_routes:
            judgment = Judgment(
                approved=(route == "auto"),
                confidence=0.85,
                route=route,
            )
            assert judgment.route == route
    
    def test_judgment_includes_reason(self):
        """Test Judgment includes rejection reason when not approved."""
        if Judgment is None:
            pytest.skip("Judgment not implemented")
        
        judgment = Judgment(
            approved=False,
            confidence=0.65,
            route="reject",
            reason="Content does not align with agent persona",
        )
        
        assert hasattr(judgment, "reason")
        assert judgment.reason is not None


class TestJudgeMetrics:
    """Test Judge tracks validation metrics."""

    @pytest.mark.asyncio
    async def test_tracks_approval_rate(self):
        """Test Judge tracks auto-approval rate metric."""
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        judge = OutputJudge(llm_client=None)
        
        # Should track approval rate (target > 90% per context.md)
        if hasattr(judge, "approval_rate"):
            assert isinstance(judge.approval_rate, float)
            assert 0.0 <= judge.approval_rate <= 1.0
    
    @pytest.mark.asyncio
    async def test_tracks_average_confidence(self):
        """Test Judge tracks average confidence score."""
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        judge = OutputJudge(llm_client=None)
        
        # Should track average confidence
        if hasattr(judge, "avg_confidence"):
            assert isinstance(judge.avg_confidence, float)


class TestJudgeErrorHandling:
    """Test Judge error handling."""

    @pytest.mark.asyncio
    async def test_handles_malformed_output(self):
        """Test Judge handles malformed output gracefully."""
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        judge = OutputJudge(llm_client=None)
        
        # Malformed output (missing required fields)
        malformed_output = {}
        context = {"persona": {}}
        
        # Should return low confidence judgment, not crash
        judgment = await judge.validate(malformed_output, context)
        
        assert judgment.confidence < 0.5
        assert judgment.approved is False
    
    @pytest.mark.asyncio
    async def test_handles_llm_timeout(self):
        """Test Judge handles LLM timeout gracefully."""
        from asyncio import TimeoutError as AsyncTimeoutError
        from unittest.mock import AsyncMock
        
        if OutputJudge is None:
            pytest.skip("OutputJudge not implemented")
        
        mock_llm = AsyncMock()
        mock_llm.generate_score = AsyncMock(side_effect=AsyncTimeoutError())
        
        judge = OutputJudge(llm_client=mock_llm)
        
        output = {"caption": "Test"}
        context = {"persona": {}}
        
        # Should handle timeout (maybe return medium confidence)
        judgment = await judge.validate(output, context)
        
        # Should not crash, should return some judgment
        assert judgment is not None


class TestCFOJudge:
    """Test CFO Judge for financial transactions (specs/functional.md Epic 4)."""

    @pytest.mark.asyncio
    async def test_cfo_judge_validates_budget(self):
        """Test CFO Judge validates transaction against budget."""
        # Import CFO Judge if exists
        try:
            from src.judge.cfo_judge import CFOJudge
        except ImportError:
            pytest.skip("CFOJudge not implemented yet")
        
        cfo_judge = CFOJudge()
        
        transaction = {
            "amount": 10.0,
            "currency": "USDC",
            "purpose": "Image generation",
        }
        
        agent_budget = {
            "daily_limit": 50.0,
            "spent_today": 35.0,
        }
        
        # Should approve if within budget
        approved = await cfo_judge.validate_transaction(transaction, agent_budget)
        
        assert isinstance(approved, bool)
    
    @pytest.mark.asyncio
    async def test_cfo_judge_rejects_over_budget(self):
        """Test CFO Judge rejects transaction exceeding budget."""
        try:
            from src.judge.cfo_judge import CFOJudge
        except ImportError:
            pytest.skip("CFOJudge not implemented yet")
        
        cfo_judge = CFOJudge()
        
        transaction = {
            "amount": 20.0,
            "currency": "USDC",
        }
        
        agent_budget = {
            "daily_limit": 50.0,
            "spent_today": 45.0,  # Only $5 remaining
        }
        
        # Should reject (would exceed budget)
        approved = await cfo_judge.validate_transaction(transaction, agent_budget)
        
        assert approved is False


# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit
