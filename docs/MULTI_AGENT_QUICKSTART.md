# Multi-Agent System Quick Start

Get started with the multi-agent debate room system in 5 minutes!

## What You'll Get

A debate/discussion room with **two AI agents** working together:
1. **Facilitator Agent** - Manages discussions, provides fact-checking
2. **Grammar Agent** - Gives instant English language feedback

## Prerequisites

- Python 3.12+
- GEMINI_API_KEY (get from [Google AI Studio](https://aistudio.google.com/api-keys))
- Dependencies installed (see Setup below)

## Quick Setup

### 1. Clone and Setup

```bash
git clone https://github.com/Vinit-source/Gemini-Agent-Strands-and-MCP.git
cd Gemini-Agent-Strands-and-MCP
chmod +x setup.sh
./setup.sh
```

### 2. Configure Environment

Create `.env` file:
```bash
cat > .env << EOF
GEMINI_API_KEY="your_actual_gemini_api_key"
EOF
```

Get your API key from [Google AI Studio](https://aistudio.google.com/api-keys).

### 3. Install Dependencies

```bash
pip3 install -r requirements.txt
```

## Running the Multi-Agent System

### Basic Usage

```bash
uv run debate_room_facilitator.py
```

### Configuration Options

When you run the system, you'll be prompted:

1. **Room type**: Choose `debate` or `discussion`
   - Discussion: Seeks convergence and consensus
   - Debate: Explores different viewpoints

2. **Grammar feedback**: Choose `yes` or `no`
   - Yes: Enable grammar correction agent
   - No: Facilitator agent only

3. **Number of participants**: Enter 1-6

4. **Participant names**: Enter names for each participant

### Example Session

```
$ uv run debate_room_facilitator.py

DEBATE/DISCUSSION ROOM FACILITATOR
Multi-Agent System with Grammar Correction
===========================================================

Room type (debate/discussion) [discussion]: discussion
Enable grammar feedback? (yes/no) [yes]: yes
Number of participants (1-6) [3]: 2

Participant 1 name: Alice
Participant 2 name: Bob

Starting debate room tools server...
Starting grammar tools server...
✓ Grammar correction agent initialized

Topic: The impact of artificial intelligence on job markets

--- Round 1 ---

[Turn: Alice]
Alice: I thinks AI will replace many jobs.

📝 Grammar Feedback:
⚠ Suggestion: "I thinks" should be "I think"

[Turn: Bob]
Bob: But it creates new opportunities.

📝 Grammar Feedback:
✓ Well said! Clear and grammatically correct.

------------------------------------------------------------
FACILITATOR FEEDBACK
------------------------------------------------------------
Both of you raise important points...
[detailed facilitator feedback]
------------------------------------------------------------
```

## Commands During Discussion

- **Type your statement** - Share your thoughts
- **`skip`** - Skip your turn
- **`exit`** - End the discussion

## Testing

### Test Multi-Agent Components

```bash
python3 test_multi_agent.py
```

Expected output:
```
============================================================
MULTI-AGENT SYSTEM TESTS
============================================================

Test: Import Grammar Agent
------------------------------------------------------------
✓ GrammarAgent imported successfully

[more tests...]

Passed: 5/5
✓ ALL TESTS PASSED!
```

### Test Grammar Agent Alone

```bash
python3 grammarAgent.py
```

This runs test cases showing grammar corrections.

## Understanding the Output

### Grammar Feedback Format

- **✓** = Grammatically correct
- **⚠** = Minor issues with suggestions
- **✗** = Significant issues needing revision

### Facilitator Feedback

Appears after each round and includes:
- Fact-checking of claims
- Observations about discussion flow
- Common ground identification
- Suggestions for direction

## Architecture Overview

```
CLI Input
   │
   ├─→ Facilitator Agent (temp=0.7)
   │   • Fact-checking
   │   • Discussion analysis
   │   • Convergence guidance
   │
   └─→ Grammar Agent (temp=0.3)
       • Grammar checking
       • Instant feedback
       • Language coaching
```

Both agents run in parallel:
- Grammar agent: Instant feedback (per statement)
- Facilitator agent: Strategic feedback (per round)

## Advanced: AWS Deployment

### Prerequisites

- AWS account with Bedrock access
- AWS credentials configured

### Deploy to AWS AgentCore

```bash
# Configure AWS credentials
export AWS_ACCESS_KEY_ID="your_key"
export AWS_SECRET_ACCESS_KEY="your_secret"
export AWS_DEFAULT_REGION="us-east-1"

# Run deployment
python3 aws_agentcore_integration.py
```

This configures both agents for cloud deployment.

### Deployment Configuration

```python
from aws_agentcore_integration import MultiAgentDeployment

deployment = MultiAgentDeployment(region="us-east-1")
deployment.configure_facilitator_agent()
deployment.configure_grammar_agent()
result = deployment.deploy_agents()
```

## Customization

### Disable Grammar Feedback

When prompted, choose `no` for grammar feedback:
```
Enable grammar feedback? (yes/no) [yes]: no
```

### Adjust Number of Participants

Support for 1-6 participants:
```
Number of participants (1-6) [3]: 4
```

### Change Grammar Agent Behavior

Edit `grammarAgent.py` system prompt:
```python
system_prompt = """
Your custom instructions for grammar checking...
"""
```

### Modify Facilitator Style

Edit `debate_room_facilitator.py` system prompt in `initialize_agent()`.

## Troubleshooting

### Port Already in Use

```bash
# Kill processes on ports 8000 and 8001
lsof -ti:8000 | xargs kill -9
lsof -ti:8001 | xargs kill -9
```

### API Key Issues

Check `.env` file:
```bash
cat .env
```

Ensure GEMINI_API_KEY is set correctly (no quotes needed in the value).

### Import Errors

Reinstall dependencies:
```bash
pip3 install -r requirements.txt
```

### Grammar Agent Not Starting

Check if grammar tools server is running:
```bash
# Should show 2 processes (debate tools + grammar tools)
lsof -i :8000
lsof -i :8001
```

## Examples and Documentation

### Run Example Demonstration

```bash
python3 example_multi_agent.py
```

This shows:
- Architecture diagrams
- Workflow explanations
- Example sessions
- Benefits of multi-agent approach
- AWS deployment process

### Read Full Documentation

- [Multi-Agent System Guide](MULTI_AGENT_SYSTEM.md) - Complete architecture
- [Debate Room README](DEBATE_ROOM_README.md) - Original facilitator docs
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - Technical details

## What's Next?

### Try Different Scenarios

1. **Technical Discussion**
   ```
   Topic: Cloud computing architectures
   Participants: 3-4 people
   Grammar: Enabled
   ```

2. **Casual Debate**
   ```
   Topic: Best programming languages
   Participants: 2 people
   Grammar: Disabled for speed
   ```

3. **Formal Debate**
   ```
   Topic: AI ethics and regulation
   Participants: 4-6 people
   Grammar: Enabled for professionalism
   ```

### Explore Features

- Try both debate and discussion modes
- Test with different participant counts
- Compare with/without grammar feedback
- Observe fact-checking in action

### Extend the System

See [Multi-Agent System Guide](MULTI_AGENT_SYSTEM.md) for ideas on:
- Adding more specialized agents
- Customizing agent behaviors
- Integrating additional tools
- Deploying to production

## Getting Help

### Check Logs

The system prints status messages:
- `✓` = Success
- `⚠` = Warning (system continues)
- `✗` = Error (may need attention)

### Common Issues

1. **"No module named 'strands'"**
   - Solution: Run `pip3 install strands-agents`

2. **"GEMINI_API_KEY not set"**
   - Solution: Create `.env` file with your API key

3. **"Port already in use"**
   - Solution: Kill existing processes on ports 8000/8001

4. **Grammar agent not responding**
   - Check: Port 8001 is available
   - Check: grammar_tools.py exists
   - Try: Disable grammar feedback temporarily

### Report Issues

Open an issue on [GitHub](https://github.com/Vinit-source/Gemini-Agent-Strands-and-MCP/issues) with:
- Error message
- Steps to reproduce
- Your setup (OS, Python version)

## Summary

You now have a working multi-agent system with:
- ✅ Facilitator agent for discussion management
- ✅ Grammar agent for language feedback
- ✅ Parallel agent coordination
- ✅ Flexible configuration options
- ✅ AWS deployment capability

**Start discussing:** `uv run debate_room_facilitator.py`

Happy debating! 🎯
