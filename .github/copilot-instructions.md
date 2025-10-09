# Gemini-Agent-Strands Copilot Guide

## Project map
- `debate_room_facilitator.py`: CLI orchestrator that spawns the tools server, maintains session state, and routes prompts through `MCPClient` + `GeminiAgent`.
- `debate_room_tools.py`: FastMCP server on `http://localhost:8000` exposing topic selection, turn management, and pulse analysis; responses stay stringified for the facilitator to `eval`.
- `geminiAgent.py`: Thin wrapper over `strands.Agent` using `GeminiModel`; demands `GEMINI_API_KEY` in `.env` and runs inside the uv-managed venv.
- Docs under `docs/` (especially `IMPLEMENTATION_SUMMARY.md` and `DEBATE_ROOM_README.md`) capture architecture, CLI flow, and customization notes—skim them before large refactors.

## Run & test
- Bootstrap once with `./setup.sh`, then `source ~/.venv/bin/activate`; this installs uv, Python 3.12, and clones the `strands-agents` sources into the venv.
- Ensure a root-level `.env` containing `GEMINI_API_KEY=...` before instantiating `GeminiAgent`; import fails fast if the key is missing.
- Main experience: `uv run debate_room_facilitator.py` launches the CLI and background MCP server thread (sleeping 2s for startup).
- Component checks live in `python3 test_debate_room.py`; it spins the server in-process and asserts each MCP tool plus facilitator wiring.
- `uv run mcp_calculator.py` is a minimal MCP sample if you need a reference for additional tools or transports.

## MCP patterns
- All tools are registered via `@mcp.tool` in `debate_room_tools.py`; keep the server on port 8000 unless you update both the facilitator and helper scripts.
- The facilitator wraps tool calls in `with self.mcp_client:`; reuse that pattern to avoid leaking transports when adding new interactions.
- Tool payloads must remain simple text (e.g., stringified lists/dicts) because `setup_room` currently `eval`s the reply; migrate both sides together if you move to JSON.
- The CLI reads only `result['content'][0]['text']`; multi-part messages or binary outputs will be dropped.
- Avoid long-running work inside tools—each round waits synchronously for replies, so keep processing lightweight or offload to background jobs.

## Facilitator logic
- Participant state lives in `self.turn_order` + `self.current_speaker_index`; always advance turns via `advance_turn()` so wrap-around math stays correct.
- Statements append to `self.conversation_history`; `get_agent_feedback()` only considers the last five entries when crafting the Gemini prompt.
- `initialize_agent()` builds the system prompt with room-type templating—tune tone or capabilities here rather than modifying `GeminiAgent` directly.
- Feedback cadence is controlled by `statements_since_feedback`; rounds with only skips shouldn’t trigger agent output.
- `start_debate_server()` imports `debate_room_tools` lazily and sleeps for two seconds; adjust the delay together with the tests if server startup time changes.

## Extending
- To add new MCP tools, declare them in `debate_room_tools.py`, restart the server, and expose them through the `self.tools` list obtained via `list_tools_sync()`.
- Add facilitator capabilities by composing new helper methods that call MCP tools and append structured entries to `conversation_history`; mimic the assertions in `test_debate_room.py` for coverage.
- Keep topic data in the `TOPICS` list and enforce the 1-6 participant guardrails inside `initialize_room()` whenever you touch validation logic.
- Reuse `docs/QUICKSTART.md` and `docs/DEBATE_ROOM_README.md` for copy-ready CLI instructions or when documenting new flows.

## Debugging cues
- Port conflicts manifest as connection errors; clear with `lsof -ti:8000 | xargs kill -9` before reruns.
- Missing Strands dependencies show up as import errors—rerun `./setup.sh` or re-activate the virtualenv to restore cloned packages.
- If the agent goes silent, confirm `.env` is loaded (`GeminiAgent` calls `load_dotenv()`) and that `conversation_history` isn’t empty.
- Hanging tests usually mean the server thread never bound to the port; tweak the startup delay in `test_debate_room.py::test_debate_tools_server` alongside the production path.
- Preserve the existing indentation style (tabs in `geminiAgent.py`, spaces elsewhere) to avoid noisy diffs against vendored upstream files.
