"""
Debate/Discussion Room Facilitator Agent

This agent facilitates debates and discussions by:
- Selecting topics
- Managing turn sequences
- Providing feedback with fact-checking
- Navigating discussions to convergence
- Exploring common and diverging points
"""

import threading
import time
from typing import List, Dict, Optional
from mcp.client.streamable_http import streamablehttp_client
from geminiAgent import GeminiAgent
from strands.tools.mcp.mcp_client import MCPClient


class DebateRoomFacilitator:
    """
    A facilitator agent for debate and discussion rooms.
    
    Manages turn-taking, provides feedback, and guides discussions.
    """
    
    def __init__(self, room_type: str = "discussion"):
        """
        Initialize the debate room facilitator.
        
        Args:
            room_type: 'debate' or 'discussion'
        """
        self.room_type = room_type
        self.participants = []
        self.turn_order = []
        self.current_speaker_index = 0
        self.topic = None
        self.conversation_history = []
        self.agent = None
        self.tools = None
        
        # Connect to the debate tools MCP server
        def create_debate_tools_transport():
            return streamablehttp_client("http://localhost:8001/mcp/")
        
        self.mcp_client = MCPClient(create_debate_tools_transport)
    
    def setup_room(self, participant_names: List[str]):
        """
        Set up the debate/discussion room with participants.
        
        Args:
            participant_names: List of participant names (1-6)
        """
        with self.mcp_client:
            self.tools = self.mcp_client.list_tools_sync()
            
            # Initialize room
            result = self.mcp_client.call_tool_sync(
                tool_use_id="init-room",
                name="initialize_room",
                arguments={
                    "participant_names": participant_names,
                    "room_type": self.room_type
                }
            )
            
            room_config = eval(result['content'][0]['text'])
            
            if not room_config.get('success'):
                raise ValueError(room_config.get('message'))
            
            self.participants = room_config['participants']
            self.turn_order = room_config['turn_order']
            self.current_speaker_index = 0
            
            print(f"\n{'='*60}")
            print(f"Room Type: {self.room_type.upper()}")
            print(f"Participants: {', '.join(self.participants)}")
            print(f"{'='*60}\n")
    
    def select_topic(self) -> str:
        """Select a topic for the debate/discussion."""
        with self.mcp_client:
            result = self.mcp_client.call_tool_sync(
                tool_use_id="select-topic",
                name="topic_selector",
                arguments={}
            )
            self.topic = result['content'][0]['text']
            return self.topic
    
    def get_current_speaker(self) -> str:
        """Get the name of the current speaker."""
        if not self.turn_order:
            return "agent"
        return self.turn_order[self.current_speaker_index]
    
    def advance_turn(self):
        """Advance to the next speaker in the turn order."""
        if self.turn_order:
            self.current_speaker_index = (self.current_speaker_index + 1) % len(self.turn_order)
    
    def initialize_agent(self):
        """Initialize the GeminiAgent with debate facilitation capabilities."""
        system_prompt = f"""
You are a humble, kind, and insightful debate/discussion room facilitator. Your role is to:

1. **Listen Actively**: Pay close attention to what each participant says
2. **Provide Thoughtful Feedback**: When it's your turn, offer:
   - Fact-checking on claims made (gently correct misinformation)
   - Observations about the pulse of the discussion
   - Insights on common ground and points of divergence
   
3. **Guide the Conversation**: 
   - For DISCUSSIONS: Navigate toward convergence and consensus
   - For DEBATES: Highlight both common points and diverging viewpoints
   - Ensure balanced participation from all members
   
4. **Be Humble and Kind**: 
   - Use phrases like "I notice that...", "It seems...", "Perhaps we could consider..."
   - Acknowledge good points made by participants
   - Encourage respectful dialogue
   
5. **Current Context**:
   - Room Type: {self.room_type}
   - Topic: {self.topic if self.topic else 'To be determined'}
   - Participants: {', '.join(self.participants)}

Remember: You are a facilitator, not a participant. Your goal is to help the group have a productive conversation.
"""
        
        with self.mcp_client:
            self.agent = GeminiAgent(system_prompt=system_prompt, tools=self.tools)
    
    def process_statement(self, speaker: str, content: str):
        """
        Process a statement from a participant.
        
        Args:
            speaker: Name of the speaker
            content: Content of their statement
        """
        self.conversation_history.append({
            "speaker": speaker,
            "content": content
        })
    
    def get_agent_feedback(self) -> str:
        """
        Get feedback from the agent based on recent conversation.
        
        Returns:
            Agent's feedback message
        """
        if not self.conversation_history:
            return "Let's begin the discussion. Who would like to start?"
        
        # Build context from recent conversation
        recent_statements = self.conversation_history[-5:]  # Last 5 statements
        context = f"Topic: {self.topic}\n\nRecent statements:\n"
        
        for stmt in recent_statements:
            context += f"- {stmt['speaker']}: {stmt['content']}\n"
        
        prompt = f"""{context}

As the facilitator, provide your feedback on the discussion so far. Consider:
1. Any factual claims that need verification
2. The overall direction and pulse of the conversation
3. Common ground emerging between participants
4. Areas of divergence that could be explored
5. Suggestions to guide the conversation productively

Keep your response concise (2-3 paragraphs) and encouraging."""
        
        response = self.agent(prompt)
        return response


def start_debate_server():
    """Start the debate tools MCP server in a background thread."""
    from debate_room_tools import start_debate_tools_server
    server_thread = threading.Thread(target=start_debate_tools_server, daemon=True)
    server_thread.start()
    time.sleep(2)  # Wait for server to start


def simulate_debate_room():
    """
    Simulate a debate/discussion room on CLI with multiple participants.
    """
    print("\n" + "="*60)
    print("DEBATE/DISCUSSION ROOM FACILITATOR")
    print("="*60)
    
    # Get room configuration
    room_type = input("\nRoom type (debate/discussion) [discussion]: ").strip().lower()
    if room_type not in ['debate', 'discussion']:
        room_type = 'discussion'
    
    # Get number of participants
    num_participants = input("Number of participants (1-6) [3]: ").strip()
    try:
        num_participants = int(num_participants)
        if num_participants < 1 or num_participants > 6:
            num_participants = 3
    except ValueError:
        num_participants = 3
    
    # Get participant names
    participant_names = []
    print(f"\nEnter names for {num_participants} participant(s):")
    for i in range(num_participants):
        name = input(f"Participant {i+1} name: ").strip()
        if not name:
            name = f"Participant{i+1}"
        participant_names.append(name)
    
    # Start the MCP server
    print("\nStarting debate room tools server...")
    start_debate_server()
    
    # Initialize facilitator
    facilitator = DebateRoomFacilitator(room_type=room_type)
    
    try:
        facilitator.setup_room(participant_names)
        
        # Select topic
        print("Selecting topic...")
        topic = facilitator.select_topic()
        print(f"\nTopic: {topic}\n")
        
        # Initialize agent
        print("Initializing facilitator agent...")
        facilitator.initialize_agent()
        
        print("\n" + "="*60)
        print("DISCUSSION STARTED")
        print("="*60)
        print("\nInstructions:")
        print("- Each participant will be prompted to speak in turn")
        print("- Type your statement when it's your turn")
        print("- The agent will provide feedback periodically")
        print("- Type 'exit' to end the discussion")
        print("- Type 'skip' to skip your turn")
        print("="*60 + "\n")
        
        round_count = 0
        statements_since_feedback = 0
        
        while True:
            round_count += 1
            print(f"\n--- Round {round_count} ---\n")
            
            # Each participant speaks in turn
            for i, participant in enumerate(facilitator.turn_order):
                current_speaker = facilitator.get_current_speaker()
                print(f"[Turn: {current_speaker}]")
                
                user_input = input(f"{current_speaker}: ").strip()
                
                if user_input.lower() == 'exit':
                    print("\nEnding discussion...")
                    # Get final feedback from agent
                    if facilitator.conversation_history:
                        print("\n" + "="*60)
                        print("FACILITATOR'S CLOSING REMARKS")
                        print("="*60)
                        final_feedback = facilitator.get_agent_feedback()
                        print(f"\n{final_feedback}\n")
                    return
                
                if user_input.lower() == 'skip':
                    print(f"{current_speaker} skipped their turn.\n")
                    facilitator.advance_turn()
                    continue
                
                if user_input:
                    facilitator.process_statement(current_speaker, user_input)
                    statements_since_feedback += 1
                
                facilitator.advance_turn()
            
            # Agent provides feedback after each round
            if statements_since_feedback > 0:
                print("\n" + "-"*60)
                print("FACILITATOR FEEDBACK")
                print("-"*60)
                feedback = facilitator.get_agent_feedback()
                print(f"\n{feedback}\n")
                print("-"*60 + "\n")
                statements_since_feedback = 0
    
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point for the debate room simulation."""
    try:
        simulate_debate_room()
    except KeyboardInterrupt:
        print("\n\nDiscussion interrupted. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
