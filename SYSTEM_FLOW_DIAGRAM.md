# System Flow Diagram

## Overall Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interaction (CLI)                    │
│                                                               │
│  1. Configure: room_type, num_participants, NUM_ROUNDS       │
│  2. Enter participant names                                  │
│  3. Participate in rounds                                    │
│  4. Receive feedback after each round                        │
│  5. View final English summary                               │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              DebateRoomFacilitator (Main Class)              │
│                                                               │
│  State:                                                       │
│  • room_type: str                                            │
│  • num_rounds: int          ← NEW                            │
│  • participants: List[str]                                   │
│  • conversation_history: List[Dict]                          │
│  • english_feedback_history: Dict  ← NEW                     │
│                                                               │
│  Methods:                                                     │
│  • setup_room()                                              │
│  • select_topic()                                            │
│  • initialize_agent()       ← ENHANCED                       │
│  • get_agent_feedback()     ← ENHANCED                       │
│  • get_final_english_summary()  ← NEW                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    GeminiAgent (AI Core)                     │
│                                                               │
│  Enhanced System Prompt:                                     │
│  • Facilitate discussion                                     │
│  • Provide fact-checking                                     │
│  • PROVIDE ENGLISH FEEDBACK  ← NEW                           │
│  • Format as bullet points   ← NEW                           │
│  • Track learning progress   ← NEW                           │
│                                                               │
│  Connected to: MCP Tools via MCPClient                       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                MCP Server (Debate Room Tools)                │
│                                                               │
│  Tools:                                                       │
│  • topic_selector()                                          │
│  • initialize_room()                                         │
│  • get_next_speaker()                                        │
│  • validate_turn()                                           │
│  • analyze_discussion_pulse()                                │
└─────────────────────────────────────────────────────────────┘
```

## Session Flow (Enhanced with English Feedback)

```
START
  │
  ▼
┌──────────────────────┐
│  Get Configuration   │
│  • Room Type         │
│  • Participants (1-6)│
│  • NUM_ROUNDS ← NEW  │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Initialize System   │
│  • Start MCP Server  │
│  • Setup Room        │
│  • Select Topic      │
│  • Initialize Agent  │
│    (with English     │
│     feedback prompt) │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│   ROUND LOOP START   │
│   (1 to num_rounds)  │ ← NEW: Fixed rounds
└──────┬───────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│         For Each Participant in Turn          │
│                                               │
│  1. Display current speaker                   │
│  2. Get user input                            │
│  3. Handle commands (skip/exit)               │
│  4. Store statement in history                │
│  5. Store for English tracking  ← NEW         │
│  6. Advance to next speaker                   │
└──────┬────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│          FACILITATOR FEEDBACK                 │
│                                               │
│  Input: Recent conversation (last 5 stmts)   │
│                                               │
│  Agent Generates:                             │
│  ┌────────────────────────────────────────┐  │
│  │ **Discussion Feedback:**               │  │
│  │ • Content observations                 │  │
│  │ • Fact-checking                        │  │
│  │ • Common ground                        │  │
│  │ • Suggestions                          │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │ **English Feedback:**          ← NEW   │  │
│  │ • **Person A**: Grammar tips           │  │
│  │ • **Person B**: Sentence structure     │  │
│  │ • **Person C**: Vocabulary suggestions │  │
│  └────────────────────────────────────────┘  │
│                                               │
│  Extract and store English feedback  ← NEW   │
└──────┬────────────────────────────────────────┘
       │
       ▼
┌──────────────────────┐
│  More Rounds?        │
│  (count < num_rounds)│ ← NEW: Check limit
└──────┬───────────────┘
       │
       │ YES → Loop back to Round Loop
       │
       ▼ NO
┌──────────────────────────────────────────────┐
│      FINAL ENGLISH LEARNING SUMMARY  ← NEW   │
│                                               │
│  Input: All participant statements            │
│                                               │
│  Agent Generates for Each Participant:        │
│  ┌────────────────────────────────────────┐  │
│  │ **[Name] - English Learning Summary:** │  │
│  │                                         │  │
│  │ • Strengths                            │  │
│  │ • Areas for Improvement                │  │
│  │ • Progress Observed                    │  │
│  │ • Tips for Continued Growth            │  │
│  └────────────────────────────────────────┘  │
│                                               │
│  Display formatted summary                    │
└──────┬────────────────────────────────────────┘
       │
       ▼
      END
```

## Data Flow (English Feedback)

```
┌─────────────────┐
│ User Statement  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Store in conversation_history   │
│  {                               │
│    "speaker": "Alice",           │
│    "content": "AI is change..."  │
│  }                               │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  After Round: Get Feedback       │
│                                  │
│  Prompt includes:                │
│  • Recent statements             │
│  • Request for English feedback  │
│  • Format specifications         │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Agent Response                  │
│                                  │
│  **English Feedback:**           │
│  • **Alice**: Use "is changing"  │
│    not "is change"               │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Extract & Store                 │
│                                  │
│  english_feedback_history = {    │
│    "Alice": [                    │
│      {"round": 1, ...}           │
│    ]                             │
│  }                               │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  At End: Generate Summary        │
│                                  │
│  Analyze all Alice's statements  │
│  Generate comprehensive feedback │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Display Final Summary           │
│                                  │
│  **Alice - English Learning:**   │
│  • Strengths: Clear ideas        │
│  • Improvements: Verb tenses     │
│  • Progress: Good correction     │
│  • Tips: Practice continuous     │
└──────────────────────────────────┘
```

## Key Enhancement Points

### 1. Initialization
```
OLD: DebateRoomFacilitator(room_type="discussion")
NEW: DebateRoomFacilitator(room_type="discussion", num_rounds=3)
     └─ Configurable rounds
```

### 2. System Prompt
```
OLD: "You are a facilitator..."
NEW: "You are a facilitator AND English instructor..."
     └─ English feedback instructions
     └─ Bullet point format requirements
```

### 3. Feedback Loop
```
OLD: General discussion feedback only
NEW: Discussion feedback + English feedback (bullet points per participant)
```

### 4. Session End
```
OLD: End without summary
NEW: End with comprehensive English learning summary for each participant
```

## Component Integration

```
┌────────────────────────────────────────────────────────┐
│                    Main Components                      │
│                                                         │
│  ┌──────────────┐         ┌──────────────┐           │
│  │   CLI Input  │────────▶│ Facilitator  │           │
│  │   • Rounds   │         │   • Tracks   │           │
│  │   • Names    │         │   • Manages  │           │
│  └──────────────┘         └──────┬───────┘           │
│                                   │                    │
│                                   ▼                    │
│  ┌──────────────┐         ┌──────────────┐           │
│  │  MCP Tools   │◀────────│ GeminiAgent  │           │
│  │  • Topic     │         │  • Enhanced  │           │
│  │  • Turns     │         │    Prompt    │           │
│  └──────────────┘         └──────┬───────┘           │
│                                   │                    │
│                                   ▼                    │
│                          ┌──────────────┐             │
│                          │   Feedback   │             │
│                          │  • Discussion│             │
│                          │  • English   │← NEW        │
│                          └──────────────┘             │
│                                   │                    │
│                                   ▼                    │
│                          ┌──────────────┐             │
│                          │   Summary    │             │
│                          │  • Per User  │← NEW        │
│                          │  • English   │             │
│                          └──────────────┘             │
└────────────────────────────────────────────────────────┘
```

## Feature Comparison

```
┌─────────────────────┬──────────────┬──────────────┐
│      Feature        │   Original   │   Enhanced   │
├─────────────────────┼──────────────┼──────────────┤
│ Rounds              │ Infinite     │ Configurable │
│                     │ (until exit) │ (1-N rounds) │
├─────────────────────┼──────────────┼──────────────┤
│ Feedback Type       │ Discussion   │ Discussion + │
│                     │ only         │ English      │
├─────────────────────┼──────────────┼──────────────┤
│ Feedback Format     │ Paragraph    │ Bullet points│
│                     │              │ per person   │
├─────────────────────┼──────────────┼──────────────┤
│ Final Summary       │ None         │ Comprehensive│
│                     │              │ English      │
│                     │              │ learning     │
├─────────────────────┼──────────────┼──────────────┤
│ Progress Tracking   │ No           │ Yes          │
│                     │              │ (per round)  │
├─────────────────────┼──────────────┼──────────────┤
│ Focus              │ Content      │ Content +    │
│                     │              │ Language     │
└─────────────────────┴──────────────┴──────────────┘
```

## Configuration Options

```
User Input
    │
    ├─ room_type: "discussion" | "debate"
    │
    ├─ num_participants: 1-6
    │
    ├─ num_rounds: 1-∞  ← NEW
    │   └─ Default: 3
    │
    └─ participant_names: [str, str, ...]

            ↓

    DebateRoomFacilitator
            │
            ├─ Initialize with num_rounds
            │
            ├─ Setup room (initialize tracking)
            │
            ├─ Initialize agent (English prompt)
            │
            └─ Run session (with limits)

            ↓

    Output
            │
            ├─ Per-round feedback (bullet points)
            │
            └─ Final summary (per participant)
```

## Success Indicators

```
✅ Requirement 1: English Feedback
   ├─ Grammar corrections: ✓
   ├─ Sentence framing: ✓
   ├─ Bullet points: ✓
   └─ Per participant: ✓

✅ Requirement 2: Variable Rounds
   ├─ Configurable: ✓
   ├─ Set at init: ✓
   ├─ Auto-complete: ✓
   └─ Progress shown: ✓

✅ Requirement 3: Final Summary
   ├─ English focused: ✓
   ├─ Per participant: ✓
   ├─ Comprehensive: ✓
   └─ Well-formatted: ✓
```

---

**This diagram shows the complete enhanced system with all new features integrated seamlessly.**
