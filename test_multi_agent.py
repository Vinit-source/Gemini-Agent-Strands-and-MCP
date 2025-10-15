"""
Tests for Multi-Agent System with Grammar Correction

This script tests the multi-agent functionality including:
- Grammar agent initialization and feedback
- Multi-agent coordination
- AWS AgentCore integration configuration
"""

import sys


def test_grammar_agent_import():
    """Test that grammar agent can be imported."""
    print("\nTest: Import Grammar Agent")
    print("-" * 60)
    try:
        from grammarAgent import GrammarAgent
        print("✓ GrammarAgent imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import GrammarAgent: {e}")
        return False


def test_grammar_tools_import():
    """Test that grammar tools can be imported."""
    print("\nTest: Import Grammar Tools")
    print("-" * 60)
    try:
        from grammar_tools import start_grammar_tools_server
        print("✓ Grammar tools imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import grammar tools: {e}")
        return False


def test_aws_agentcore_integration():
    """Test AWS AgentCore integration module."""
    print("\nTest: AWS AgentCore Integration")
    print("-" * 60)
    try:
        from aws_agentcore_integration import MultiAgentDeployment, create_deployment_config
        
        # Test deployment configuration
        config = create_deployment_config()
        assert config["deployment_name"] == "debate-room-multi-agent-system"
        assert len(config["agents"]) == 2
        assert config["agents"][0]["agent_type"] == "facilitator"
        assert config["agents"][1]["agent_type"] == "grammar"
        print("✓ Deployment configuration created successfully")
        
        # Test deployment class initialization
        deployment = MultiAgentDeployment(region="us-east-1")
        assert deployment.region == "us-east-1"
        print("✓ MultiAgentDeployment initialized successfully")
        
        # Test agent configuration
        facilitator_config = deployment.configure_facilitator_agent()
        assert "agent_name" in facilitator_config
        assert "capabilities" in facilitator_config
        print("✓ Facilitator agent configured")
        
        grammar_config = deployment.configure_grammar_agent()
        assert "agent_name" in grammar_config
        assert "capabilities" in grammar_config
        print("✓ Grammar agent configured")
        
        # Test deployment info
        info = deployment.get_deployment_info()
        assert info["facilitator_config"] is not None
        assert info["grammar_config"] is not None
        print("✓ Deployment info retrieved")
        
        return True
    except Exception as e:
        print(f"✗ AWS AgentCore integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_facilitator_multi_agent_support():
    """Test that facilitator supports multi-agent mode."""
    print("\nTest: Facilitator Multi-Agent Support")
    print("-" * 60)
    try:
        from debate_room_facilitator import DebateRoomFacilitator
        
        # Test initialization with grammar feedback enabled
        facilitator = DebateRoomFacilitator(
            room_type="discussion",
            enable_grammar_feedback=True
        )
        assert facilitator.enable_grammar_feedback == True
        assert hasattr(facilitator, 'grammar_agent')
        assert hasattr(facilitator, 'grammar_mcp_client')
        print("✓ Facilitator initialized with grammar feedback enabled")
        
        # Test initialization with grammar feedback disabled
        facilitator_no_grammar = DebateRoomFacilitator(
            room_type="debate",
            enable_grammar_feedback=False
        )
        assert facilitator_no_grammar.enable_grammar_feedback == False
        print("✓ Facilitator initialized without grammar feedback")
        
        # Test grammar feedback method exists
        assert hasattr(facilitator, 'get_grammar_feedback')
        print("✓ Grammar feedback method exists")
        
        return True
    except Exception as e:
        print(f"✗ Facilitator multi-agent support test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_grammar_agent_analysis():
    """Test grammar agent statement analysis (requires API key)."""
    print("\nTest: Grammar Agent Analysis (Optional)")
    print("-" * 60)
    try:
        from grammarAgent import GrammarAgent
        import os
        
        # Check if API key is available
        if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "test_key_placeholder":
            print("⚠ Skipping - GEMINI_API_KEY not set or is placeholder")
            return True
        
        # Create grammar agent
        agent = GrammarAgent()
        print("✓ Grammar agent created")
        
        # Test analysis method exists and is callable
        assert hasattr(agent, 'analyze_statement')
        assert callable(agent.analyze_statement)
        print("✓ Grammar agent analysis method is available")
        
        print("Note: Actual API calls skipped to avoid costs")
        return True
        
    except ValueError as e:
        if "GEMINI_API_KEY" in str(e):
            print("⚠ Skipping - GEMINI_API_KEY not configured (expected)")
            return True
        raise
    except Exception as e:
        print(f"✗ Grammar agent analysis test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all multi-agent system tests."""
    print("="*60)
    print("MULTI-AGENT SYSTEM TESTS")
    print("="*60)
    
    tests = [
        test_grammar_agent_import,
        test_grammar_tools_import,
        test_aws_agentcore_integration,
        test_facilitator_multi_agent_support,
        test_grammar_agent_analysis,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
