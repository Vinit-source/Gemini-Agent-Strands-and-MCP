"""
Grammar Tools MCP Server

Provides grammar checking and language analysis tools.
"""

from mcp.server import FastMCP

# Create MCP server for grammar tools
mcp = FastMCP("Grammar Tools Server")


@mcp.tool(description="Check grammar and provide feedback on a text statement")
def check_grammar(text: str, speaker_name: str = "Speaker") -> str:
	"""
	Analyze text for grammar errors and provide constructive feedback.
	
	Args:
		text: The text to analyze for grammar
		speaker_name: Name of the person who made the statement
		
	Returns:
		Analysis result with feedback
	"""
	# This is a placeholder that returns the text for processing by the grammar agent
	# The actual grammar checking is done by the GrammarAgent
	return f"GRAMMAR_CHECK_REQUEST:{speaker_name}:{text}"


@mcp.tool(description="Get grammar statistics for a session")
def get_grammar_stats(participant_name: str = "all") -> str:
	"""
	Get grammar statistics for participants.
	
	Args:
		participant_name: Name of participant or "all" for everyone
		
	Returns:
		Statistics about grammar feedback provided
	"""
	# Placeholder for tracking grammar feedback
	return f"Grammar stats for {participant_name}: Statistics tracked per session."


@mcp.tool(description="Set grammar feedback frequency")
def set_feedback_frequency(frequency: str = "every_statement") -> str:
	"""
	Set how often grammar feedback should be provided.
	
	Args:
		frequency: "every_statement", "every_round", or "on_request"
		
	Returns:
		Confirmation message
	"""
	valid_frequencies = ["every_statement", "every_round", "on_request"]
	if frequency not in valid_frequencies:
		return f"Invalid frequency. Choose from: {', '.join(valid_frequencies)}"
	
	return f"Grammar feedback frequency set to: {frequency}"


def start_grammar_tools_server():
	"""Start the grammar tools MCP server."""
	print("Starting Grammar Tools MCP Server on http://localhost:8001")
	mcp.run(transport="streamable-http", port=8001)


if __name__ == "__main__":
	start_grammar_tools_server()
