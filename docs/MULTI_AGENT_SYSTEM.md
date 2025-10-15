# Multi-Agent System with Grammar Correction

## Overview

This implementation extends the debate room facilitator with a **multi-agent architecture** featuring:

1. **Facilitator Agent** - Provides discussion facilitation, fact-checking, and convergence navigation
2. **Grammar Correction Agent** - Offers instant feedback on English grammar, sentence structure, and language usage

Both agents work in parallel to provide comprehensive support for debate/discussion participants.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLI Interface                            │
│              (debate_room_facilitator.py)                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ├──────────────┬──────────────────────────┐
                     ▼              ▼                          ▼
          ┌──────────────────┐  ┌──────────────┐  ┌──────────────────┐
          │ GeminiAgent      │  │ GrammarAgent │  │ MCP Servers      │
          │ (Facilitator)    │  │ (Grammar)    │  │                  │
          │                  │  │              │  │ - Debate Tools   │
          │ • Fact-checking  │  │ • Grammar    │  │   (port 8000)    │
          │ • Discussion     │  │   checking   │  │ - Grammar Tools  │
          │   analysis       │  │ • Language   │  │   (port 8001)    │
          │ • Convergence    │  │   feedback   │  │                  │
          └──────────────────┘  └──────────────┘  └──────────────────┘
                     │              │
                     ▼              ▼
          ┌──────────────────────────────────────────────────┐
          │        Gemini Model (gemini-2.5-flash)           │
          └──────────────────────────────────────────────────┘
```

## Components

### 1. Grammar Agent (`grammarAgent.py`)

A specialized agent for English language coaching that:
- Analyzes grammar, punctuation, and sentence structure
- Provides constructive, encouraging feedback
- Uses lower temperature (0.3) for consistent corrections
- Prioritizes the most important issues

**Feedback Format:**
- ✓ = Grammatically correct
- ⚠ = Minor issues with suggestions
- ✗ = Significant issues requiring revision

### 2. Grammar Tools Server (`grammar_tools.py`)

MCP server running on port 8001 providing:
- `check_grammar()` - Analyzes text for grammar errors
- `get_grammar_stats()` - Tracks grammar feedback statistics
- `set_feedback_frequency()` - Configures feedback frequency

### 3. Enhanced Facilitator (`debate_room_facilitator.py`)

Updated to support multi-agent coordination:
- Manages both facilitator and grammar agents
- Provides instant grammar feedback after each statement
- Coordinates feedback timing between agents
- Allows enabling/disabling grammar feedback

### 4. AWS AgentCore Integration (`aws_agentcore_integration.py`)

Deployment module for AWS Bedrock AgentCore SDK:
- Configures both agents for AWS deployment
- Manages agent orchestration
- Provides deployment configuration
- Enables cloud-based agent hosting

## Usage

### Basic Usage

```bash
# Run the multi-agent debate room
uv run debate_room_facilitator.py
```

**Configuration Options:**
1. Room type: `debate` or `discussion`
2. Grammar feedback: `yes` or `no`
3. Number of participants: 1-6
4. Participant names

### Example Session

```
DEBATE/DISCUSSION ROOM FACILITATOR
Multi-Agent System with Grammar Correction
===========================================================

Room type (debate/discussion) [discussion]: discussion
Enable grammar feedback? (yes/no) [yes]: yes
Number of participants (1-6) [3]: 2

Enter names for 2 participant(s):
Participant 1 name: Alice
Participant 2 name: Bob

Starting debate room tools server...
Starting grammar tools server...

Topic: The impact of artificial intelligence on job markets

--- Round 1 ---

[Turn: Alice]
Alice: I thinks AI will replace many jobs.

📝 Grammar Feedback:
⚠ Suggestion: "I thinks" should be "I think" (subject-verb agreement). 
The rest of the sentence is clear and well-structured.

[Turn: Bob]
Bob: But it creates new opportunities for everyone.

📝 Grammar Feedback:
✓ Well said! The grammar and structure are clear.

------------------------------------------------------------
FACILITATOR FEEDBACK
------------------------------------------------------------

I notice both of you are touching on important aspects of AI's 
impact on employment. Alice raises the concern about job 
displacement, which is a valid consideration backed by various 
studies. Bob's point about new opportunities is equally 
important - research shows AI is creating roles in data science, 
AI ethics, and human-AI collaboration...
```

## Multi-Agent Benefits

### 1. Specialized Expertise
- **Facilitator**: Focus on discussion dynamics and fact-checking
- **Grammar Agent**: Dedicated to language quality improvement

### 2. Parallel Processing
- Both agents analyze statements simultaneously
- Grammar feedback is instant (per statement)
- Facilitator feedback is strategic (per round)

### 3. Comprehensive Support
- Participants improve both **content** (via facilitator) and **expression** (via grammar agent)
- Real-time language coaching during discussions
- Balanced feedback on substance and form

### 4. Flexible Configuration
- Grammar feedback can be enabled/disabled
- Each agent operates independently
- Easy to add more specialized agents

## AWS AgentCore Deployment

### Prerequisites

1. AWS Account with Bedrock access
2. AWS credentials configured
3. bedrock-agentcore SDK installed

### Deployment Steps

```python
from aws_agentcore_integration import MultiAgentDeployment

# Create deployment
deployment = MultiAgentDeployment(region="us-east-1")

# Configure agents
deployment.configure_facilitator_agent()
deployment.configure_grammar_agent()

# Deploy to AWS
result = deployment.deploy_agents()
print(f"Deployment status: {result['status']}")
```

### Configuration

Set environment variables:
```bash
export AWS_ACCESS_KEY_ID="your_key"
export AWS_SECRET_ACCESS_KEY="your_secret"
export AWS_DEFAULT_REGION="us-east-1"
```

Or add to `.env`:
```
AWS_ACCESS_KEY_ID="your_key"
AWS_SECRET_ACCESS_KEY="your_secret"
AWS_DEFAULT_REGION="us-east-1"
```

## Testing Grammar Agent

```bash
# Test grammar agent standalone
python3 grammarAgent.py
```

This runs test cases with various grammar issues and shows feedback.

## Customization

### Adjusting Grammar Agent Behavior

Edit `grammarAgent.py` system prompt:
```python
system_prompt = """
Your custom instructions for grammar checking...
"""
```

### Changing Feedback Frequency

Options in facilitator:
- `every_statement` - Immediate feedback (default)
- `every_round` - Batch feedback per round
- `on_request` - Only when requested

### Adding More Agents

To add additional specialized agents:

1. Create new agent class (e.g., `factCheckAgent.py`)
2. Create corresponding MCP tools server
3. Update facilitator to coordinate new agent
4. Add agent configuration to AWS deployment

## Architecture Benefits

### Scalability
- Each agent can be scaled independently
- MCP servers can run on different ports/machines
- Easy to distribute load across services

### Maintainability
- Clear separation of concerns
- Each agent has single responsibility
- Modular tool servers

### Extensibility
- Add new agents without modifying existing ones
- New tools can be added to MCP servers
- Deployment configurations are composable

## Technical Details

### Agent Communication

Agents communicate through:
1. **MCP Client** - For tool interactions
2. **Direct invocation** - For agent-to-agent coordination
3. **Shared state** - Via facilitator class

### State Management

The facilitator maintains:
- Conversation history (shared context)
- Participant order and state
- Agent instances and configurations
- Feedback timing and coordination

### Error Handling

Graceful degradation:
- Grammar agent failure doesn't stop facilitation
- MCP server connection issues are caught
- Users are informed of disabled features

## Performance Considerations

### Grammar Agent
- Uses temperature 0.3 for consistency
- Analyzes statements in real-time
- Minimal latency for short statements

### Facilitator Agent
- Uses temperature 0.7 for creativity
- Processes last 5 statements for context
- Provides feedback after each round

### MCP Servers
- Lightweight tool servers
- Run in background threads
- Minimal resource overhead

## Future Enhancements

Potential additions to the multi-agent system:

1. **Fact-Checking Agent** - Dedicated to verifying claims
2. **Sentiment Analysis Agent** - Monitors discussion tone
3. **Summary Agent** - Generates discussion summaries
4. **Research Agent** - Finds relevant sources and data
5. **Mediator Agent** - Resolves conflicts and disagreements

Each can be added following the same pattern used for the grammar agent.

## Troubleshooting

### Grammar Agent Not Starting

Check:
1. Port 8001 is available: `lsof -i :8001`
2. grammar_tools.py is present
3. MCP dependencies installed

### AWS Deployment Issues

Check:
1. AWS credentials are configured
2. Bedrock access is enabled
3. Region supports required models
4. IAM permissions are sufficient

### Performance Issues

Solutions:
1. Disable grammar feedback for faster rounds
2. Reduce context window (fewer statements)
3. Use lighter models for grammar checking
4. Batch grammar feedback per round instead of per statement

## References

- [AWS Bedrock AgentCore SDK](https://github.com/aws/bedrock-agentcore-sdk-python)
- [Strands Agents Documentation](https://github.com/strands-agents/docs)
- [MCP Protocol](https://github.com/strands-agents/sdk-python)
- [Gemini API](https://ai.google.dev/docs)
