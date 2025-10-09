# Debate Room Facilitator

A fully functional debate/discussion room facilitator agent using AWS Strands and Gemini Agent with **English language learning capabilities**.

## Overview

This implementation provides an AI-powered facilitator for debate and discussion rooms that can:

- **Select Topics**: Automatically choose debate/discussion topics from a curated list
- **Manage Turns**: Sequence and coordinate turns for 1-6 participants
- **Configurable Rounds**: Set a specific number of discussion rounds
- **Provide Feedback**: Offer humble, kind feedback including:
  - Fact-checking of claims
  - Sensing the pulse of the discussion
  - Navigating toward convergence (discussions) or exploring viewpoints (debates)
  - Highlighting common ground and diverging points
  - **English language feedback** (grammar, sentence structure, vocabulary)
- **Final Summary**: Comprehensive English learning summary for each participant

## 🆕 New Features

### 1. English Language Feedback
The facilitator now provides detailed feedback on:
- **Sentence structure and framing**
- **Grammar** (verb tenses, subject-verb agreement, articles, prepositions)
- **Vocabulary** usage and word choice
- **Clarity** and coherence

Feedback is formatted as bullet points for each participant after every round.

### 2. Configurable Number of Rounds
- Set the number of rounds during initialization
- Discussion automatically ends after specified rounds
- Provides structure and predictable session duration

### 3. Final English Learning Summary
At the end of discussion, each participant receives:
- **Strengths**: What they did well
- **Areas for Improvement**: Specific patterns to work on
- **Progress Observed**: Improvements during the session
- **Tips for Continued Growth**: Actionable suggestions

📖 **See [ENGLISH_FEEDBACK_FEATURE.md](ENGLISH_FEEDBACK_FEATURE.md) for detailed documentation**

## Components

### 1. `debate_room_tools.py`
MCP server providing tools for:
- `topic_selector`: Select random topics for debate/discussion
- `get_next_speaker`: Manage turn sequencing
- `validate_turn`: Ensure participants speak in correct order
- `initialize_room`: Set up room with participants (1-6 people)
- `analyze_discussion_pulse`: Track discussion progress

### 2. `debate_room_facilitator.py`
Main facilitator agent that:
- Connects to the debate tools MCP server
- Uses GeminiAgent for intelligent facilitation
- Simulates a CLI-based chat environment
- Manages conversation flow and provides periodic feedback

## Usage

### Prerequisites

Ensure you have:
1. Set up the environment using `./setup.sh`
2. Created `.env` file with your `GEMINI_API_KEY`
3. Installed all dependencies

### Running the Debate Room

```bash
uv run debate_room_facilitator.py
```

### Interaction Flow

1. **Configure the Room**:
   - Choose room type: `debate` or `discussion`
   - Set number of participants (1-6)
   - **Set number of rounds** (e.g., 3, 5, 10)
   - Enter participant names

2. **Topic Selection**:
   - The facilitator automatically selects a topic from the predefined list

3. **Discussion**:
   - Participants speak in turn (round-robin)
   - Type your statement when it's your turn
   - Type `skip` to pass your turn
   - Type `exit` to end the discussion early
   - Discussion runs for the specified number of rounds

4. **Facilitator Feedback**:
   - After each round, the agent provides feedback
   - Feedback includes observations, fact-checking, and guidance
   - **English feedback formatted as bullet points for each participant**

5. **Final English Summary**:
   - Comprehensive English learning summary for each participant
   - Includes strengths, improvements, progress, and tips
   - Displayed automatically at the end

## Example Session

```
DEBATE/DISCUSSION ROOM FACILITATOR
==============================================================

Room type (debate/discussion) [discussion]: discussion
Number of participants (1-6) [3]: 3

Enter names for 3 participant(s):
Participant 1 name: Alice
Participant 2 name: Bob
Participant 3 name: Carol

==============================================================
Room Type: DISCUSSION
Participants: Alice, Bob, Carol
==============================================================

Topic: The impact of artificial intelligence on job markets

==============================================================
DISCUSSION STARTED
==============================================================

--- Round 1 ---

[Turn: Alice]
Alice: I think AI will replace many jobs, especially in manufacturing.

[Turn: Bob]
Bob: Yes, but it will also create new jobs in tech and AI development.

[Turn: Carol]
Carol: We need to focus on retraining workers for the AI era.

------------------------------------------------------------
FACILITATOR FEEDBACK
------------------------------------------------------------

I notice some excellent points emerging from all three of you. Alice raises an important concern about job displacement, particularly in sectors like manufacturing where automation is already well-advanced. Bob adds a balanced perspective by highlighting the new opportunities AI creates, which is indeed happening in the tech sector.

Carol's point about retraining is crucial - it seems we're converging on the idea that AI's impact on employment is not simply negative, but transformative. Perhaps we could explore what specific types of training programs might be most effective, or discuss how we balance the pace of AI adoption with workforce preparation?

------------------------------------------------------------
```

## Architecture

```
┌─────────────────────────────────┐
│  CLI Simulation Interface       │
│  (debate_room_facilitator.py)   │
└────────────┬────────────────────┘
             │
             ├─> Manages Participants
             ├─> Sequences Turns
             ├─> Collects Statements
             │
             ▼
┌─────────────────────────────────┐
│  GeminiAgent (Facilitator)      │
│  - System Prompt with Role      │
│  - Connected to MCP Tools       │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Debate Room Tools MCP Server   │
│  (debate_room_tools.py)          │
│  - Topic Selection               │
│  - Turn Management               │
│  - Discussion Analysis           │
└─────────────────────────────────┘
```

## Customization

### Adding Topics

Edit `debate_room_tools.py` and add topics to the `TOPICS` list:

```python
TOPICS = [
    "Your custom topic here",
    # ... existing topics
]
```

### Adjusting Participant Limits

Modify the validation in `initialize_room()` function in `debate_room_tools.py`.

### Changing Facilitator Behavior

Edit the `system_prompt` in `DebateRoomFacilitator.initialize_agent()` to adjust:
- Tone and style
- Feedback frequency
- Focus areas (fact-checking vs. convergence)

## Features

### Turn Management
- Automatic round-robin turn sequencing
- Turn validation to ensure proper order
- Skip functionality for participants

### Intelligent Facilitation
- Context-aware feedback based on recent statements
- Distinction between debate and discussion modes
- Gentle fact-checking and corrections
- Identification of common ground and divergence

### Flexible Configuration
- Support for 1-6 participants (configurable)
- Choice between debate or discussion modes
- Dynamic topic selection

## Technical Details

- **Framework**: AWS Strands Agents
- **AI Model**: Google Gemini (via GeminiAgent)
- **MCP Server**: FastMCP with Streamable HTTP transport
- **Port**: 8000 (debate tools server)
- **Architecture Pattern**: Agent + MCP Tools

## Troubleshooting

**Server won't start**: Ensure port 8000 is available
```bash
lsof -ti:8000 | xargs kill -9  # Kill any process on port 8000
```

**Agent not responding**: Check that `GEMINI_API_KEY` is set in `.env`

**Import errors**: Run the setup script again:
```bash
./setup.sh
source ~/.venv/bin/activate
```
