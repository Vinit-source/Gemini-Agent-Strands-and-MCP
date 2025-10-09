# Debate Room Facilitator - Quick Start Guide

## What is it?

A fully functional AI-powered facilitator for debate and discussion rooms that:
- Manages turn-taking for 1-6 participants
- Provides intelligent feedback and guidance
- Facilitates productive conversations on various topics

## Quick Start

### 1. Setup (One Time)
```bash
./setup.sh
source ~/.venv/bin/activate
```

### 2. Configure API Key
Create `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key_here
```
Get your key from: https://aistudio.google.com/api-keys

### 3. Run
```bash
uv run debate_room_facilitator.py
```

## Basic Usage

### Choose Room Type
- **Discussion**: Aims for convergence and consensus
- **Debate**: Explores different viewpoints and arguments

### Set Participants
- Enter number of participants (1-6)
- Provide names for each participant

### During the Session
- **Your turn**: Type your statement and press Enter
- **Skip turn**: Type `skip`
- **End session**: Type `exit`

### Facilitator Feedback
After each round, the AI facilitator will:
- Fact-check claims
- Sense the pulse of the discussion
- Highlight common ground
- Suggest productive directions

## Example Commands

```bash
# Start the facilitator
uv run debate_room_facilitator.py

# Test the tools (without running full simulation)
python3 test_debate_room.py
```

## Customization

### Add New Topics
Edit `debate_room_tools.py`:
```python
TOPICS = [
    "Your new topic here",
    # ... existing topics
]
```

### Adjust Facilitator Behavior
Edit system prompt in `debate_room_facilitator.py` → `initialize_agent()` method

### Change Participant Limits
Edit `initialize_room()` function in `debate_room_tools.py`

## Architecture

```
User Input → CLI Interface → DebateRoomFacilitator → GeminiAgent → MCP Tools
                                    ↓
                            Manages State & Turns
                                    ↓
                            Provides AI Feedback
```

## Files

- `debate_room_facilitator.py` - Main application (CLI simulation)
- `debate_room_tools.py` - MCP server with debate tools
- `test_debate_room.py` - Component tests
- `DEBATE_ROOM_README.md` - Full documentation
- `EXAMPLE_SESSION.md` - Sample interaction

## Troubleshooting

**"Port already in use"**
```bash
lsof -ti:8000 | xargs kill -9
```

**"No module named 'strands'"**
- Run `./setup.sh` again
- Activate venv: `source ~/.venv/bin/activate`

**"GEMINI_API_KEY not set"**
- Create `.env` file with your API key
- Ensure it's in the project root directory

## Tips

1. **Better Discussions**: Encourage participants to build on each other's points
2. **Fact Claims**: The agent will fact-check, so cite sources when possible
3. **Skip Strategically**: Use skip if you need time to think
4. **Multiple Rounds**: Best insights often come after 3-4 rounds

## See Also

- Full documentation: `DEBATE_ROOM_README.md`
- Example session: `EXAMPLE_SESSION.md`
- Component tests: `test_debate_room.py`
