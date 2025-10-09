# Debate Room Facilitator - Example Interaction

This document demonstrates what an actual session with the debate room facilitator looks like.

## Example Session: Discussion on AI and Job Markets

```
============================================================
DEBATE/DISCUSSION ROOM FACILITATOR
============================================================

Room type (debate/discussion) [discussion]: discussion
Number of participants (1-6) [3]: 3

Enter names for 3 participant(s):
Participant 1 name: Alice
Participant 2 name: Bob
Participant 3 name: Carol

Starting debate room tools server...
Waiting for MCP server to start...

============================================================
Room Type: DISCUSSION
Participants: Alice, Bob, Carol
============================================================

Selecting topic...

Topic: The impact of artificial intelligence on job markets

============================================================
DISCUSSION STARTED
============================================================

Instructions:
- Each participant will be prompted to speak in turn
- Type your statement when it's your turn
- The agent will provide feedback periodically
- Type 'exit' to end the discussion
- Type 'skip' to skip your turn
============================================================


--- Round 1 ---

[Turn: Alice]
Alice: I think AI will definitely replace many jobs, especially in manufacturing and routine tasks. We're already seeing this with automation.

[Turn: Bob]
Bob: That's a valid concern, Alice. But I believe AI will also create new types of jobs that we can't even imagine yet - just like the internet did in the 1990s.

[Turn: Carol]
Carol: I agree with both of you to some extent. The key issue is the transition period. We need strong retraining programs to help workers adapt.

------------------------------------------------------------
FACILITATOR FEEDBACK
------------------------------------------------------------

Thank you all for these thoughtful opening statements. I notice we're converging on an important recognition - that AI's impact on employment is complex and multifaceted.

Alice raises a crucial point about job displacement, particularly in sectors vulnerable to automation. Bob adds an optimistic perspective about job creation, drawing on historical parallels. Carol wisely identifies the transition challenge as a key concern.

It seems we're finding common ground on the idea that AI will transform rather than simply eliminate employment. Perhaps we could explore Carol's point further - what specific types of retraining programs might be most effective? And how quickly would they need to be implemented?

------------------------------------------------------------


--- Round 2 ---

[Turn: Alice]
Alice: Good question. I think we need programs focused on digital literacy and skills that complement AI, like creative problem-solving and emotional intelligence.

[Turn: Bob]
Bob: Absolutely. And these programs should be government-subsidized. Companies benefit from AI adoption, so they should contribute to workforce transition costs.

[Turn: Carol]
Carol: I'd add that we should start this training much earlier - even in K-12 education. We can't wait until people lose their jobs to start preparing them.

------------------------------------------------------------
FACILITATOR FEEDBACK
------------------------------------------------------------

Excellent progression in your discussion. I'm observing a clear convergence toward solutions, which is wonderful for a group discussion.

All three of you are building on each other's ideas constructively. Alice identifies the types of skills needed - and I'd note that research supports her emphasis on uniquely human capabilities that AI currently struggles with. Bob introduces the important question of funding and corporate responsibility, which is gaining traction in policy circles. Carol expands the timeframe to include preventive education.

Your discussion is moving from problem identification to solution design. You might also consider: What role should individuals play in their own reskilling? And how do we address workers in industries facing immediate disruption?

------------------------------------------------------------


--- Round 3 ---

[Turn: Alice]
Alice: Individuals definitely need to take some responsibility, but let's be realistic - not everyone has the time or resources while working full-time jobs.

[Turn: Bob]
Bob: That's why I think paid training leave could be part of the solution. Like paid parental leave, but for career transitions.

[Turn: Carol]
Carol: I love that idea, Bob! And maybe we could pilot this in industries where AI adoption is happening fastest, to test what works.

------------------------------------------------------------
FACILITATOR FEEDBACK
------------------------------------------------------------

This is a remarkably productive discussion. I'm impressed by how you're balancing idealism with pragmatism.

Alice brings important nuance by acknowledging barriers to individual action - a fact check here: studies show that workers in lower-income brackets spend 50+ hours per week on work and basic life maintenance, leaving little room for extensive retraining. Bob's "paid training leave" concept is innovative and addresses Alice's concern directly. Carol's suggestion of pilot programs demonstrates systems thinking.

You've moved from identifying a problem (AI's impact on jobs) to proposing concrete, interconnected solutions (education reform, corporate funding, paid training leave, and pilot programs). This represents excellent convergence toward actionable ideas. The common thread is shared responsibility across government, corporations, and individuals.

Are there any concerns or potential drawbacks to the solutions you've proposed that we should consider?

------------------------------------------------------------


--- Round 4 ---

[Turn: Alice]
Alice: One concern - how do we pay for all this? The programs we're discussing would be expensive.

[Turn: Bob]
Bob: Fair point. Maybe a small tax on AI-driven productivity gains? Companies using AI to replace workers could contribute proportionally.

[Turn: Carol]
Carol: That could work. And it creates an incentive structure - companies would balance AI adoption with the social costs.

------------------------------------------------------------
FACILITATOR FEEDBACK
------------------------------------------------------------

You're now tackling implementation challenges, which shows mature thinking about your proposed solutions.

Alice raises the practical question of funding - a necessary reality check. Bob proposes an "AI tax" or productivity tax, which has been discussed in policy circles (notably by Bill Gates and others). Carol identifies an additional benefit - the incentive structure that such a tax would create.

I notice you've maintained respectful, constructive dialogue throughout, building on rather than opposing each other's ideas. This discussion has evolved from concern about job displacement to a comprehensive framework: early education, corporate responsibility, funded training programs, pilot projects, and innovative funding mechanisms.

Your conversation exemplifies how group discussion can lead to synthesis of diverse perspectives into actionable proposals. Well done!

------------------------------------------------------------

[Turn: Alice]
Alice: exit

Ending discussion...

============================================================
FACILITATOR'S CLOSING REMARKS
============================================================

Thank you all for this excellent discussion on AI's impact on job markets. 

You began with legitimate concerns about job displacement and evolved the conversation into a nuanced exploration of solutions. Key themes that emerged:

**Common Ground:**
- AI will transform employment, creating both challenges and opportunities
- The transition period requires active management and support
- Shared responsibility across multiple stakeholders is essential

**Proposed Solutions:**
- Education system reform starting at K-12 level
- Retraining programs focused on uniquely human skills
- Corporate contribution to workforce transition costs
- Paid training leave for career transitions
- Pilot programs in high-impact industries
- Potential AI productivity tax to fund initiatives

Your discussion demonstrated:
- Respectful listening and building on others' ideas
- Balance between optimism and realism
- Movement from problem identification to solution design
- Consideration of practical implementation challenges

This is exactly the kind of thoughtful, convergent dialogue that can lead to meaningful action. Thank you for your engaged participation!

============================================================
```

## Key Features Demonstrated

### 1. Turn Management
- Each participant speaks in order (Alice → Bob → Carol)
- Clear indication of whose turn it is
- Support for 'skip' and 'exit' commands

### 2. Topic Selection
- Automatic topic selection from curated list
- Topic: "The impact of artificial intelligence on job markets"

### 3. Facilitator Feedback (After Each Round)
The agent provides:
- **Fact-checking**: References research about worker time constraints
- **Pulse sensing**: Notes progression from problem to solution
- **Convergence navigation**: Identifies common ground and synthesis
- **Humble guidance**: Uses phrases like "I notice", "perhaps we could", "you might consider"

### 4. Discussion Progression
The conversation naturally evolves:
- Round 1: Problem identification
- Round 2: Initial solutions
- Round 3: Refinement and innovation
- Round 4: Implementation challenges

### 5. Closing Remarks
Summary of:
- Common ground achieved
- Solutions proposed
- Quality of dialogue

## Technical Implementation

Behind the scenes, the system:
1. **Runs MCP server** with debate tools (port 8000)
2. **Manages state**:
   - Participant list: `["Alice", "Bob", "Carol"]`
   - Current turn index: rotates 0 → 1 → 2 → 0
   - Conversation history: stores all statements
3. **Uses GeminiAgent** with custom system prompt
4. **Processes feedback** based on recent conversation context (last 5 statements)

## Variable Configuration

All key parameters are configurable:
- Number of participants: 1-6 (variable)
- Room type: debate or discussion
- Participant names: user-defined
- Topics: extensible list in `debate_room_tools.py`
- Feedback frequency: every round (adjustable)

## Tools Used

1. `topic_selector` - Selects discussion topic
2. `initialize_room` - Sets up participant roster
3. `get_next_speaker` - Manages turn sequence
4. `validate_turn` - Ensures proper turn-taking
5. `analyze_discussion_pulse` - Tracks conversation dynamics

## Notes for Testing

To test this yourself with a real API key:

1. Set up environment:
```bash
./setup.sh
source ~/.venv/bin/activate
```

2. Create `.env` with your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

3. Run the facilitator:
```bash
uv run debate_room_facilitator.py
```

4. Follow the prompts to create your discussion room!
