"""
WebSocket-enabled chat server for Debate Room Facilitator.

This server provides:
- WebSocket endpoints for real-time chat
- REST API for room management
- SQLite persistence for conversations
- Multi-client support
"""

import asyncio
import json
import sqlite3
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Set
from contextlib import contextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from debate_room_facilitator import DebateRoomFacilitator, start_debate_server


# Pydantic models for API
class CreateRoomRequest(BaseModel):
    room_type: str
    participant_names: List[str]

class JoinRoomRequest(BaseModel):
    room_id: str
    participant_name: str

class MessageRequest(BaseModel):
    room_id: str
    speaker: str
    content: str


# Database manager
class DatabaseManager:
    """Manages SQLite database for conversation persistence."""
    
    def __init__(self, db_path: str = "debate_rooms.db"):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Rooms table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                    room_id TEXT PRIMARY KEY,
                    room_type TEXT NOT NULL,
                    topic TEXT,
                    participants TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active INTEGER DEFAULT 1
                )
            """)
            
            # Messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_id TEXT NOT NULL,
                    speaker TEXT NOT NULL,
                    content TEXT NOT NULL,
                    message_type TEXT DEFAULT 'user',
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (room_id) REFERENCES rooms (room_id)
                )
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_room_id 
                ON messages (room_id)
            """)
    
    def create_room(self, room_id: str, room_type: str, participants: List[str], topic: str = None):
        """Create a new room."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO rooms (room_id, room_type, participants, topic) VALUES (?, ?, ?, ?)",
                (room_id, room_type, json.dumps(participants), topic)
            )
    
    def get_room(self, room_id: str) -> Optional[Dict]:
        """Get room details."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rooms WHERE room_id = ?", (room_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    def add_message(self, room_id: str, speaker: str, content: str, message_type: str = "user"):
        """Add a message to the conversation."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO messages (room_id, speaker, content, message_type) VALUES (?, ?, ?, ?)",
                (room_id, speaker, content, message_type)
            )
    
    def get_messages(self, room_id: str, limit: int = 100) -> List[Dict]:
        """Get messages for a room."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM messages WHERE room_id = ? ORDER BY timestamp DESC LIMIT ?",
                (room_id, limit)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in reversed(rows)]
    
    def list_active_rooms(self) -> List[Dict]:
        """List all active rooms."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rooms WHERE is_active = 1 ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]


# Connection manager for WebSockets
class ConnectionManager:
    """Manages WebSocket connections for rooms."""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, room_id: str):
        """Connect a client to a room."""
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
        self.active_connections[room_id].add(websocket)
    
    def disconnect(self, websocket: WebSocket, room_id: str):
        """Disconnect a client from a room."""
        if room_id in self.active_connections:
            self.active_connections[room_id].discard(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
    
    async def broadcast(self, message: dict, room_id: str):
        """Broadcast a message to all clients in a room."""
        if room_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[room_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.add(connection)
            
            # Clean up disconnected clients
            for connection in disconnected:
                self.active_connections[room_id].discard(connection)


# Room manager
class RoomManager:
    """Manages debate room facilitators."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.facilitators: Dict[str, DebateRoomFacilitator] = {}
    
    def create_room(self, room_id: str, room_type: str, participants: List[str]) -> DebateRoomFacilitator:
        """Create a new debate room."""
        facilitator = DebateRoomFacilitator(room_type=room_type)
        facilitator.setup_room(participants)
        
        # Select topic
        topic = facilitator.select_topic()
        
        # Initialize agent
        facilitator.initialize_agent()
        
        # Store in database
        self.db_manager.create_room(room_id, room_type, participants, topic)
        
        # Cache facilitator
        self.facilitators[room_id] = facilitator
        
        return facilitator
    
    def get_facilitator(self, room_id: str) -> Optional[DebateRoomFacilitator]:
        """Get a facilitator for a room."""
        if room_id in self.facilitators:
            return self.facilitators[room_id]
        
        # Try to load from database
        room = self.db_manager.get_room(room_id)
        if room and room['is_active']:
            # Recreate facilitator
            facilitator = DebateRoomFacilitator(room_type=room['room_type'])
            participants = json.loads(room['participants'])
            facilitator.setup_room(participants)
            facilitator.topic = room['topic']
            facilitator.initialize_agent()
            
            # Restore conversation history
            messages = self.db_manager.get_messages(room_id)
            for msg in messages:
                if msg['message_type'] == 'user':
                    facilitator.conversation_history.append({
                        "speaker": msg['speaker'],
                        "content": msg['content']
                    })
            
            self.facilitators[room_id] = facilitator
            return facilitator
        
        return None


# FastAPI app
app = FastAPI(title="Debate Room Chat Server")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global managers
db_manager = DatabaseManager()
connection_manager = ConnectionManager()
room_manager = RoomManager(db_manager)


@app.on_event("startup")
async def startup_event():
    """Start the debate tools MCP server on startup."""
    print("Starting debate tools MCP server...")
    start_debate_server()
    print("Debate tools MCP server started")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Debate Room Chat Server",
        "version": "1.0.0",
        "endpoints": {
            "create_room": "POST /api/rooms",
            "list_rooms": "GET /api/rooms",
            "get_room": "GET /api/rooms/{room_id}",
            "websocket": "WS /ws/{room_id}"
        }
    }


@app.post("/api/rooms")
async def create_room(request: CreateRoomRequest):
    """Create a new debate room."""
    import uuid
    
    room_id = str(uuid.uuid4())[:8]
    
    # Validate participants
    if len(request.participant_names) < 1 or len(request.participant_names) > 6:
        raise HTTPException(status_code=400, detail="Participant count must be between 1 and 6")
    
    if request.room_type not in ["debate", "discussion"]:
        raise HTTPException(status_code=400, detail="Room type must be 'debate' or 'discussion'")
    
    try:
        facilitator = room_manager.create_room(room_id, request.room_type, request.participant_names)
        
        return {
            "room_id": room_id,
            "room_type": request.room_type,
            "participants": request.participant_names,
            "topic": facilitator.topic,
            "message": "Room created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/rooms")
async def list_rooms():
    """List all active rooms."""
    rooms = db_manager.list_active_rooms()
    for room in rooms:
        room['participants'] = json.loads(room['participants'])
    return {"rooms": rooms}


@app.get("/api/rooms/{room_id}")
async def get_room(room_id: str):
    """Get details about a specific room."""
    room = db_manager.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    room['participants'] = json.loads(room['participants'])
    messages = db_manager.get_messages(room_id)
    
    return {
        "room": room,
        "messages": messages
    }


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    """WebSocket endpoint for real-time chat."""
    await connection_manager.connect(websocket, room_id)
    
    try:
        # Send connection confirmation
        await websocket.send_json({
            "type": "connected",
            "room_id": room_id,
            "timestamp": datetime.now().isoformat()
        })
        
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            message_type = data.get("type")
            
            if message_type == "message":
                speaker = data.get("speaker")
                content = data.get("content")
                
                if not speaker or not content:
                    continue
                
                # Get facilitator
                facilitator = room_manager.get_facilitator(room_id)
                if not facilitator:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Room not found or inactive"
                    })
                    continue
                
                # Save message to database
                db_manager.add_message(room_id, speaker, content, "user")
                
                # Process statement
                facilitator.process_statement(speaker, content)
                
                # Broadcast user message
                await connection_manager.broadcast({
                    "type": "message",
                    "speaker": speaker,
                    "content": content,
                    "message_type": "user",
                    "timestamp": datetime.now().isoformat()
                }, room_id)
                
                # Check if we should get facilitator feedback
                # Get feedback after every 3 messages or on request
                if len(facilitator.conversation_history) % 3 == 0:
                    feedback = facilitator.get_agent_feedback()
                    
                    # Save feedback to database
                    db_manager.add_message(room_id, "Facilitator", feedback, "agent")
                    
                    # Broadcast facilitator feedback
                    await connection_manager.broadcast({
                        "type": "message",
                        "speaker": "Facilitator",
                        "content": feedback,
                        "message_type": "agent",
                        "timestamp": datetime.now().isoformat()
                    }, room_id)
            
            elif message_type == "request_feedback":
                # Manually request facilitator feedback
                facilitator = room_manager.get_facilitator(room_id)
                if facilitator and facilitator.conversation_history:
                    feedback = facilitator.get_agent_feedback()
                    
                    # Save feedback to database
                    db_manager.add_message(room_id, "Facilitator", feedback, "agent")
                    
                    # Broadcast facilitator feedback
                    await connection_manager.broadcast({
                        "type": "message",
                        "speaker": "Facilitator",
                        "content": feedback,
                        "message_type": "agent",
                        "timestamp": datetime.now().isoformat()
                    }, room_id)
    
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, room_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        connection_manager.disconnect(websocket, room_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
