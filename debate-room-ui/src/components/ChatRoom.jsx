import { useState, useEffect, useRef } from 'react'
import './ChatRoom.css'

function ChatRoom({ roomData, participantName, onLeaveRoom }) {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [ws, setWs] = useState(null)
  const [isConnected, setIsConnected] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // Connect to WebSocket
    const websocket = new WebSocket(`ws://localhost:8080/ws/${roomData.room_id}`)
    
    websocket.onopen = () => {
      console.log('WebSocket connected')
      setIsConnected(true)
    }
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      
      if (data.type === 'connected') {
        console.log('Connected to room:', data.room_id)
      } else if (data.type === 'message') {
        setMessages(prev => [...prev, {
          speaker: data.speaker,
          content: data.content,
          messageType: data.message_type,
          timestamp: data.timestamp
        }])
      } else if (data.type === 'error') {
        console.error('WebSocket error:', data.message)
      }
    }
    
    websocket.onerror = (error) => {
      console.error('WebSocket error:', error)
      setIsConnected(false)
    }
    
    websocket.onclose = () => {
      console.log('WebSocket disconnected')
      setIsConnected(false)
    }
    
    setWs(websocket)
    
    return () => {
      websocket.close()
    }
  }, [roomData.room_id])

  const sendMessage = () => {
    if (!inputMessage.trim() || !ws || !isConnected) return
    
    ws.send(JSON.stringify({
      type: 'message',
      speaker: participantName,
      content: inputMessage.trim()
    }))
    
    setInputMessage('')
  }

  const requestFeedback = () => {
    if (!ws || !isConnected) return
    
    ws.send(JSON.stringify({
      type: 'request_feedback'
    }))
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="chat-room">
      <div className="chat-container">
        <div className="chat-header">
          <div className="room-info">
            <h2>Room: {roomData.room_id}</h2>
            <p className="topic">📚 {roomData.topic}</p>
            <p className="room-type">
              {roomData.room_type === 'debate' ? '⚔️ Debate' : '🤝 Discussion'}
            </p>
          </div>
          <div className="participants-info">
            <strong>Participants:</strong>
            <div className="participant-list">
              {roomData.participants.map((p, i) => (
                <span key={i} className="participant-badge">
                  {p}
                </span>
              ))}
            </div>
          </div>
          <button onClick={onLeaveRoom} className="leave-button">
            Leave Room
          </button>
        </div>
        
        <div className="chat-messages">
          {messages.length === 0 ? (
            <div className="empty-state">
              <p>💬 No messages yet. Start the discussion!</p>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div 
                key={index} 
                className={`message ${msg.messageType === 'agent' ? 'agent-message' : 'user-message'} ${msg.speaker === participantName ? 'own-message' : ''}`}
              >
                <div className="message-header">
                  <span className="speaker">
                    {msg.messageType === 'agent' ? '🤖' : '👤'} {msg.speaker}
                  </span>
                  <span className="timestamp">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <div className="message-content">
                  {msg.content}
                </div>
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>
        
        <div className="chat-input-container">
          <div className="connection-status">
            {isConnected ? (
              <span className="connected">🟢 Connected</span>
            ) : (
              <span className="disconnected">🔴 Disconnected</span>
            )}
          </div>
          <div className="input-row">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              className="message-input"
              rows="3"
              disabled={!isConnected}
            />
            <div className="button-group">
              <button 
                onClick={sendMessage}
                disabled={!inputMessage.trim() || !isConnected}
                className="send-button"
              >
                Send
              </button>
              <button 
                onClick={requestFeedback}
                disabled={!isConnected || messages.length === 0}
                className="feedback-button"
              >
                Request Feedback
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChatRoom
