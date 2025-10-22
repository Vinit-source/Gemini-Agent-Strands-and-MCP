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

### 3. Debate Room Chat Application 🆕🌐
A modern web-based chat application with React UI, WebSocket real-time communication, and SQLite persistence.

**Documentation:**
- [Chat Application Guide](docs/CHAT_APPLICATION.md) - Complete setup and usage guide

**Key Features:**
- 🚀 Real-time chat with WebSocket
- 👥 Multi-client support
- 🤖 AI-powered facilitation
- 💾 Persistent conversation storage (SQLite)
- 🎨 Modern, responsive React UI
- 🔄 Live facilitator feedback

**Quick Start:**
```bash
# Start both backend and frontend
./start_chat_app.sh

# Or manually:
# Terminal 1 - Backend
python3 debate_chat_server.py

# Terminal 2 - Frontend
cd debate-room-ui
npm install
npm run dev
```

**Access:**
- Backend API: http://localhost:8080
- Frontend UI: http://localhost:5173

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
     GEMINI_API_KEY='your_gemini_api_key' // Generate your own Gemini API key from [here](https://aistudio.google.com/api-keys).
     ```
     4. Run mcp_calculator.py:
	 ```bash
	 uv run mcp_calculator.py
	 ```

## Note
You can import `geminiAgent.py` in your own scripts to utilize Strands and MCP functionalities.
```python
from geminiAgent import GeminiAgent  # Use this in place of the Agent class of Strands
```
