import { useState } from 'react'
import './App.css'
import RoomSetup from './components/RoomSetup'
import ChatRoom from './components/ChatRoom'

function App() {
  const [currentRoom, setCurrentRoom] = useState(null)
  const [participantName, setParticipantName] = useState('')

  const handleRoomCreated = (roomData, name) => {
    setCurrentRoom(roomData)
    setParticipantName(name)
  }

  const handleLeaveRoom = () => {
    setCurrentRoom(null)
    setParticipantName('')
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎤 Debate Room Chat</h1>
        <p>AI-Facilitated Discussion Platform</p>
      </header>
      
      <main className="app-main">
        {!currentRoom ? (
          <RoomSetup onRoomCreated={handleRoomCreated} />
        ) : (
          <ChatRoom 
            roomData={currentRoom} 
            participantName={participantName}
            onLeaveRoom={handleLeaveRoom}
          />
        )}
      </main>
      
      <footer className="app-footer">
        <p>Powered by Gemini Agent & Strands</p>
      </footer>
    </div>
  )
}

export default App
