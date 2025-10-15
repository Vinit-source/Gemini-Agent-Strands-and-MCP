# Gemini-Agent-Strands-and-MCP

Learnings from the different repositories within the [Strands Agents](https://github.com/strands-agents).

## Features

### 1. Calculator Agent (Example)
A basic example demonstrating MCP server integration with calculation tools.

### 2. Debate Room Facilitator Agent 🆕
A fully functional debate/discussion room facilitator that manages conversations for 1-6 participants.

**Documentation:**
- [Quick Start Guide](docs/QUICKSTART.md) - Get started in 5 minutes
- [Full Documentation](docs/DEBATE_ROOM_README.md) - Detailed features and architecture
- [Example Session](docs/EXAMPLE_SESSION.md) - See it in action
- [Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md) - Technical implementation details
- [Requirements Verification](docs/REQUIREMENTS_VERIFICATION.md) - Proof all requirements met

**Key Capabilities:**
- Topic selection from curated list
- Turn management and sequencing
- Intelligent feedback with fact-checking
- Discussion pulse sensing
- Navigation toward convergence/exploration of viewpoints

**Quick Start:**
```bash
uv run debate_room_facilitator.py
```

**Test Components:**
```bash
python3 test_debate_room.py
```

### 3. Multi-Agent System with Grammar Correction 🆕✨

An advanced **multi-agent architecture** featuring parallel agent coordination:

- **Facilitator Agent**: Provides discussion facilitation, fact-checking, and convergence navigation
- **Grammar Correction Agent**: Offers instant feedback on English grammar, sentence structure, and language usage

**Documentation:**
- [Multi-Agent System Guide](docs/MULTI_AGENT_SYSTEM.md) - Complete architecture and usage guide

**Key Features:**
- ✨ **Dual-agent coordination** - Facilitator + Grammar agents working in parallel
- 📝 **Instant grammar feedback** - Real-time language coaching for participants
- 🌐 **AWS AgentCore integration** - Deploy agents to AWS Bedrock
- 🎯 **Specialized expertise** - Each agent focuses on its domain
- ⚙️ **Flexible configuration** - Enable/disable agents as needed

**Quick Start:**
```bash
uv run debate_room_facilitator.py
# Choose "yes" for grammar feedback when prompted
```

**Test Grammar Agent:**
```bash
python3 grammarAgent.py
```

**AWS Deployment:**
```bash
python3 aws_agentcore_integration.py
```

## Setup Instructions
1. Clone the repository:
	 ```bash
	 git clone https://github.com/Vinit-source/Gemini-Agent-Strands-and-MCP.git
	 cd Gemini-Agent-Strands-and-MCP
	 ```
	 2. Run the setup script:
	 ```bash
	 chmod +x setup.sh
	 ./setup.sh
	 ```
	 3. Create .env:
     ```
     GEMINI_API_KEY='your_gemini_api_key' // Generate your own Gemini API key from https://aistudio.google.com/api-keys
     
     # Optional: For AWS AgentCore deployment
     AWS_ACCESS_KEY_ID='your_aws_access_key_id'
     AWS_SECRET_ACCESS_KEY='your_aws_secret_access_key'
     AWS_DEFAULT_REGION='us-east-1'
     ```
     4. Run examples:
	 ```bash
	 # Calculator example
	 uv run mcp_calculator.py
	 
	 # Multi-agent debate room with grammar correction
	 uv run debate_room_facilitator.py
	 ```

## Architecture

The project demonstrates:
- **Single-agent systems** (calculator, basic facilitator)
- **Multi-agent systems** (facilitator + grammar correction)
- **MCP tool servers** (debate tools, grammar tools)
- **AWS AgentCore deployment** (cloud-based agent hosting)

## Note
You can import agent classes in your own scripts:
```python
from geminiAgent import GeminiAgent  # Main facilitator agent
from grammarAgent import GrammarAgent  # Grammar correction agent
```

## Components

- `geminiAgent.py` - Main agent using Gemini model
- `grammarAgent.py` - Specialized grammar correction agent
- `debate_room_facilitator.py` - Multi-agent debate room coordinator
- `debate_room_tools.py` - MCP server for debate tools (port 8000)
- `grammar_tools.py` - MCP server for grammar tools (port 8001)
- `aws_agentcore_integration.py` - AWS Bedrock AgentCore deployment
- `mcp_calculator.py` - Simple calculator example

## License

Apache License 2.0 - See [LICENSE](LICENSE) file for details.
