# Debate Room Chat Application

A real-time web-based chat application for the Debate Room Facilitator, featuring WebSocket communication, React UI, and SQLite persistence.

## Features

- **Real-time Chat**: WebSocket-based communication for instant messaging
- **Multi-client Support**: Multiple participants can join the same room
- **AI Facilitation**: Gemini-powered agent provides intelligent feedback
- **Persistent Storage**: SQLite database stores all conversations
- **Modern UI**: Clean, responsive React interface
- **Room Types**: Support for both debates and discussions

## Architecture

```
┌─────────────────────┐
│   React Frontend    │
│  (debate-room-ui)   │
└──────────┬──────────┘
           │ WebSocket
           │ REST API
           ▼
┌─────────────────────┐
│  FastAPI Backend    │
│(debate_chat_server) │
├─────────────────────┤
│  - WebSocket Hub    │
│  - Room Manager     │
│  - DB Manager       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────┐
│  Debate Room Facilitator        │
│  + MCP Tools Server             │
│  + Gemini Agent                 │
└─────────────────────────────────┘
```

## Setup

### Prerequisites

- Python 3.12+
- Node.js 20+
- npm 10+
- GEMINI_API_KEY in `.env` file

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your Gemini API key:
```bash
echo 'GEMINI_API_KEY="your_gemini_api_key_here"' > .env
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd debate-room-ui
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start the Backend Server

In the root directory:
```bash
python debate_chat_server.py
```

The server will start on `http://localhost:8080`

### Start the Frontend

In a new terminal, navigate to the frontend directory:
```bash
cd debate-room-ui
npm run dev
```

The frontend will start on `http://localhost:5173` (default Vite port)

## Usage

### Creating a Room

1. Open the application in your browser
2. Enter your name
3. Select room type (Discussion or Debate)
4. Set the number of participants (1-6)
5. Enter participant names
6. Click "Create Room"

### Chatting

1. Once in the room, you'll see:
   - Room ID and topic
   - List of participants
   - Chat history
   - Message input area

2. Type your message and click "Send" or press Enter

3. The facilitator agent will automatically provide feedback every 3 messages

4. You can manually request feedback using the "Request Feedback" button

### Leaving a Room

Click the "Leave Room" button in the chat header to return to the setup screen.

## API Endpoints

### REST API

- `GET /` - API information
- `POST /api/rooms` - Create a new room
- `GET /api/rooms` - List all active rooms
- `GET /api/rooms/{room_id}` - Get room details and message history

### WebSocket

- `WS /ws/{room_id}` - Connect to a room for real-time chat

#### WebSocket Message Types

**Client → Server:**
```json
{
  "type": "message",
  "speaker": "Alice",
  "content": "Hello, everyone!"
}
```

```json
{
  "type": "request_feedback"
}
```

**Server → Client:**
```json
{
  "type": "message",
  "speaker": "Alice",
  "content": "Hello, everyone!",
  "message_type": "user",
  "timestamp": "2025-10-22T16:00:00.000Z"
}
```

```json
{
  "type": "message",
  "speaker": "Facilitator",
  "content": "I notice excellent engagement...",
  "message_type": "agent",
  "timestamp": "2025-10-22T16:01:00.000Z"
}
```

## Database Schema

### Tables

**rooms**
- `room_id` (TEXT, PRIMARY KEY)
- `room_type` (TEXT)
- `topic` (TEXT)
- `participants` (TEXT, JSON array)
- `created_at` (TIMESTAMP)
- `is_active` (INTEGER)

**messages**
- `id` (INTEGER, PRIMARY KEY)
- `room_id` (TEXT, FOREIGN KEY)
- `speaker` (TEXT)
- `content` (TEXT)
- `message_type` (TEXT: 'user' or 'agent')
- `timestamp` (TIMESTAMP)

## Technology Stack

### Backend
- **FastAPI**: Modern web framework for building APIs
- **WebSockets**: Real-time bidirectional communication
- **SQLite**: Lightweight database for persistence
- **Uvicorn**: ASGI server

### Frontend
- **React**: UI framework
- **Vite**: Build tool and dev server
- **WebSocket API**: Native browser WebSocket support
- **CSS3**: Modern styling

## Customization

### Adding New Topics

Edit `debate_room_tools.py` and add topics to the `TOPICS` list:

```python
TOPICS = [
    "Your new topic here",
    # ... existing topics
]
```

### Changing Feedback Frequency

In `debate_chat_server.py`, modify the feedback condition:

```python
# Change from every 3 messages to every N messages
if len(facilitator.conversation_history) % N == 0:
    feedback = facilitator.get_agent_feedback()
```

### Styling

Frontend styles are in:
- `debate-room-ui/src/index.css` - Global styles
- `debate-room-ui/src/components/*.css` - Component-specific styles

## Troubleshooting

### Backend Issues

**Server won't start:**
- Check if port 8080 is already in use
- Ensure all Python dependencies are installed
- Verify GEMINI_API_KEY is set in `.env`

**WebSocket connection fails:**
- Confirm the MCP tools server is running (should start automatically)
- Check if port 8000 is available for MCP tools
- Look at server logs for error messages

### Frontend Issues

**Can't connect to backend:**
- Ensure backend server is running on `http://localhost:8080`
- Check browser console for CORS errors
- Verify WebSocket URL is correct in `ChatRoom.jsx`

**Build errors:**
- Delete `node_modules` and run `npm install` again
- Clear npm cache: `npm cache clean --force`

## Development

### Backend Development

The FastAPI server includes automatic reload with `uvicorn`:

```bash
uvicorn debate_chat_server:app --reload --host 0.0.0.0 --port 8080
```

### Frontend Development

Vite provides hot module replacement:

```bash
cd debate-room-ui
npm run dev
```

Changes to React components will update immediately in the browser.

## Security Considerations

**For Production:**

1. **CORS**: Update `allow_origins` in `debate_chat_server.py` to specific domains
2. **Authentication**: Add user authentication and session management
3. **Rate Limiting**: Implement rate limiting on API endpoints
4. **Input Validation**: Add comprehensive input sanitization
5. **HTTPS**: Use SSL/TLS for production deployment
6. **API Keys**: Store sensitive keys in environment variables or secrets manager

## License

Same as the parent project.

## Support

For issues or questions, please refer to the main project README or open an issue on GitHub.
