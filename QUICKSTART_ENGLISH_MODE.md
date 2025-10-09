# Quick Start - English Learning Mode

## New Configuration Options

When starting the debate room facilitator, you'll see new prompts:

```
============================================================
DEBATE/DISCUSSION ROOM FACILITATOR
============================================================

Room type (debate/discussion) [discussion]: discussion
Number of participants (1-6) [3]: 2
Number of rounds [3]: 2              ← NEW: Configure rounds
```

## What Changed?

### 1. Before (Original Version)
- Discussion ran indefinitely until 'exit'
- Feedback focused on discussion content only
- No structured English learning

### 2. After (Enhanced Version)
- **Set specific number of rounds** (default: 3)
- **English feedback in every round** (grammar, structure, vocabulary)
- **Final comprehensive English summary** for each participant
- **Formatted bullet points** for clear feedback

## Example Output Comparison

### Original Feedback Format:
```
------------------------------------------------------------
FACILITATOR FEEDBACK
------------------------------------------------------------

Thank you for those points. Alice raises important concerns about 
AI displacement, and Bob provides a balanced view about new 
opportunities. The discussion is moving in a productive direction.

------------------------------------------------------------
```

### New Enhanced Feedback Format:
```
------------------------------------------------------------
FACILITATOR FEEDBACK
------------------------------------------------------------

**Discussion Feedback:**
Thank you for those points. Alice raises important concerns about 
AI displacement, and Bob provides a balanced view about new 
opportunities. The discussion is moving in a productive direction.

**English Feedback:**
• **Alice**: Great sentence structure! Minor note: Consider using 
  "many jobs" instead of "much jobs" (countable noun). Your use of 
  "especially" as a transition is excellent.
• **Bob**: Well-constructed sentence! Small grammar point: "AI will 
  create" (future) is better than "AI creates" in this context. 
  Good vocabulary choice with "opportunities."

------------------------------------------------------------
```

### New: Final Summary
```
============================================================
FINAL ENGLISH LEARNING SUMMARY
============================================================

**Alice - English Learning Summary:**
• **Strengths:** Strong vocabulary, clear expression of complex ideas, 
  good use of transition words
• **Areas for Improvement:** Watch for countable vs uncountable nouns 
  (much/many), occasional article usage
• **Progress Observed:** Improved clarity from Round 1 to Round 2
• **Tips for Continued Growth:**
  - Practice with countable/uncountable noun exercises
  - Read business articles to see articles in context
  - Continue expressing complex ideas - you do this well!

**Bob - English Learning Summary:**
• **Strengths:** Excellent sentence structure, appropriate formality, 
  good logical flow
• **Areas for Improvement:** Verb tenses (future vs present), 
  occasional preposition choices
• **Progress Observed:** Better use of future tense in Round 2
• **Tips for Continued Growth:**
  - Practice future tense in prediction contexts
  - Review common preposition combinations
  - Keep building on your strong foundation

============================================================
Thank you for participating! Keep practicing your English!
============================================================
```

## Key Benefits

### For English Learners:
✅ Real-time feedback on mistakes
✅ Personalized learning for each participant
✅ Clear, actionable improvement tips
✅ Track progress within a single session
✅ Practice English in meaningful conversation

### For Facilitators:
✅ Structured sessions with defined rounds
✅ Predictable duration
✅ Better time management
✅ Comprehensive assessment at the end

## Usage Tips

### 1. Choose Appropriate Number of Rounds

**For beginners:** 2-3 rounds
- Less overwhelming
- Focus on basic corrections
- Build confidence gradually

**For intermediate:** 3-5 rounds
- More opportunities for improvement
- Can track progress better
- Balanced practice time

**For advanced:** 5-10 rounds
- Comprehensive practice
- Detailed feedback accumulation
- Greater depth of discussion

### 2. Setting Up for Best Learning Experience

1. **Start with fewer participants** (2-3) for more detailed feedback
2. **Choose familiar topics** initially to focus on English, not content
3. **Review feedback carefully** after each round before continuing
4. **Take notes** on common errors for personal reference
5. **Save the final summary** for future review

### 3. Progression Path

**Week 1-2:**
```
Participants: 2
Rounds: 2
Focus: Basic grammar corrections
```

**Week 3-4:**
```
Participants: 2-3
Rounds: 3
Focus: Sentence structure + grammar
```

**Week 5+:**
```
Participants: 3-4
Rounds: 4-5
Focus: Advanced vocabulary + style
```

## Command Reference

During the session:

| Command | Action |
|---------|--------|
| Type your message | Speak in your turn |
| `skip` | Skip your turn (no English feedback) |
| `exit` | End early (still get final summary) |
| Just press Enter | Wait for next prompt |

## Feature Highlights

### ✨ Automatic Round Management
No need to manually count rounds - the system tracks it for you:
```
--- Round 1 of 3 ---
--- Round 2 of 3 ---
--- Round 3 of 3 ---
```

### 📊 Progress Tracking
The system notes improvements:
```
**Progress Observed:** Corrected verb tenses in Round 2, 
better vocabulary choices in Round 3
```

### 🎯 Actionable Tips
Specific, practical suggestions:
```
**Tips for Continued Growth:**
- Practice with online grammar exercises focused on articles
- Read 2-3 news articles daily
- Record yourself speaking and review
```

### 💪 Encouraging Tone
Always constructive and supportive:
```
"Great improvement!"
"Your vocabulary is expanding nicely"
"Keep up the excellent work with transitions"
```

## Technical Notes

### Implementation Details

**Added to `DebateRoomFacilitator` class:**
```python
def __init__(self, room_type: str = "discussion", num_rounds: int = 3)
def get_final_english_summary(self) -> str
self.english_feedback_history = {}  # Track feedback per participant
```

**System Prompt Enhancement:**
```python
- **ENGLISH FEEDBACK**: Provide specific feedback on:
  * Sentence structure and framing
  * Grammar corrections
  * Vocabulary usage
  * Clarity and coherence
```

**Session Flow:**
```
Initialize → Setup Room → Select Topic → Initialize Agent → 
Run Rounds (with English feedback) → Final Summary → End
```

## Common Questions

**Q: Can I still use the old version without English feedback?**
A: The English feedback is integrated into all responses. However, you can modify the system prompt to reduce emphasis on English if needed.

**Q: What if I want more/fewer rounds than default?**
A: Simply enter your desired number when prompted, or modify the default in the code.

**Q: Does the final summary show if I exit early?**
A: Yes! The final summary is displayed whenever the session ends, whether naturally or via 'exit'.

**Q: Can I get feedback for specific grammar topics?**
A: The AI provides comprehensive feedback. You can modify the system prompt to emphasize specific areas.

**Q: Is the feedback suitable for all levels?**
A: Yes, the AI adapts its feedback to the complexity of language used by participants.

## Troubleshooting

**Issue:** Feedback not showing English section
- **Solution:** Ensure you're using the updated version with English feedback in system prompt

**Issue:** Rounds not ending automatically
- **Solution:** Check that you entered a valid number for rounds (not text or negative)

**Issue:** Summary not detailed enough
- **Solution:** Participate in more rounds for more comprehensive analysis

## Next Steps

1. Try a 2-round session with a friend
2. Review your English feedback carefully
3. Note down common corrections
4. Apply learnings in next session
5. Gradually increase rounds as you improve

---

**Ready to start improving your English?**

```bash
uv run debate_room_facilitator.py
```

Happy learning! 🎓
