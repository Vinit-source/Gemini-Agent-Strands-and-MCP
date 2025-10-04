# Gemini-Agent-Strands-and-MCP

Learnings from the different repositories within the [Strands Agents](https://github.com/strands-agents).

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
