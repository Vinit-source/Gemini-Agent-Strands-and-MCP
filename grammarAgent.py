"""
Grammar Correction Agent

This agent provides instant feedback on English grammar, sentence structure,
and language usage for debate/discussion participants.
"""

import os
from strands import Agent
from strands.models.gemini import GeminiModel
from dotenv import load_dotenv


class GrammarAgent(Agent):
	"""
	An agent specialized in English grammar correction and language feedback.
	
	This agent analyzes participant statements and provides constructive feedback on:
	- Grammar errors
	- Sentence structure
	- Word choice and vocabulary
	- Clarity and coherence
	"""
	
	def __init__(self, tools=None):
		"""
		Initialize the Grammar Agent.
		
		Args:
			tools: Optional list of MCP tools the agent can use
		"""
		# Load environment variables
		load_dotenv()
		_api_key = os.getenv("GEMINI_API_KEY")
		
		if not _api_key:
			raise ValueError("GEMINI_API_KEY environment variable not set.")
		
		# Initialize the Gemini Model optimized for grammar correction
		self.gemini_model = GeminiModel(
			model_id="gemini-2.5-flash",
			params={
				"temperature": 0.3,  # Lower temperature for more consistent grammar correction
			}
		)
		
		# Define the system prompt for grammar correction
		system_prompt = """
You are a helpful English grammar and language coach. Your role is to:

1. **Analyze Language**: Review statements for grammar, punctuation, and sentence structure
2. **Provide Constructive Feedback**: Offer clear, actionable suggestions for improvement
3. **Be Encouraging**: Focus on what's done well and suggest improvements kindly
4. **Be Concise**: Keep feedback brief (2-3 sentences max) unless major issues exist
5. **Prioritize**: Focus on the most important issues first

When analyzing text, consider:
- Grammar errors (subject-verb agreement, tense, etc.)
- Sentence structure and clarity
- Word choice and vocabulary
- Punctuation and capitalization
- Overall coherence and flow

Format your feedback as:
✓ If the statement is grammatically correct, say: "✓ Well said! The grammar and structure are clear."
⚠ If there are minor issues, provide: "⚠ Suggestion: [specific improvement]"
✗ If there are significant issues, provide: "✗ Consider revising: [clear explanation and example]"

Always be respectful and encouraging. Your goal is to help people improve their English communication.
"""
		
		# Initialize the agent with the model and system prompt
		super().__init__(model=self.gemini_model, tools=tools, system_prompt=system_prompt)
	
	def analyze_statement(self, speaker: str, content: str) -> str:
		"""
		Analyze a participant's statement for grammar and language quality.
		
		Args:
			speaker: Name of the person who made the statement
			content: The text of the statement to analyze
			
		Returns:
			Feedback message with grammar corrections and suggestions
		"""
		prompt = f"""
Analyze the following statement from {speaker} for English grammar, sentence structure, and clarity:

"{content}"

Provide brief, constructive feedback focusing on the most important language issues or confirming if it's well-written.
"""
		
		response = self(prompt)
		return response


if __name__ == "__main__":
	# Example usage
	agent = GrammarAgent()
	
	# Test cases
	test_statements = [
		("Alice", "AI will replace many jobs in the future."),
		("Bob", "I thinks that AI are creating new opportunities for peoples."),
		("Carol", "We needs to focus on retraining workers, it's very important thing."),
	]
	
	print("="*60)
	print("GRAMMAR AGENT TEST")
	print("="*60 + "\n")
	
	for speaker, statement in test_statements:
		print(f"[{speaker}]: {statement}")
		feedback = agent.analyze_statement(speaker, statement)
		print(f"Grammar Feedback: {feedback}\n")
		print("-"*60 + "\n")
