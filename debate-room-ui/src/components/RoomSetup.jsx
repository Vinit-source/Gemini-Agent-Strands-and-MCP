import { useState } from 'react'
import './RoomSetup.css'

const API_BASE_URL = 'http://localhost:8080'

function RoomSetup({ onRoomCreated }) {
  const [roomType, setRoomType] = useState('discussion')
  const [participantCount, setParticipantCount] = useState(3)
  const [participants, setParticipants] = useState(['', '', ''])
  const [yourName, setYourName] = useState('')
  const [isCreating, setIsCreating] = useState(false)
  const [error, setError] = useState(null)

  const handleParticipantCountChange = (count) => {
    setParticipantCount(count)
    const newParticipants = Array(count).fill('').map((_, i) => 
      participants[i] || ''
    )
    setParticipants(newParticipants)
  }

  const handleParticipantChange = (index, value) => {
    const newParticipants = [...participants]
    newParticipants[index] = value
    setParticipants(newParticipants)
  }

  const handleCreateRoom = async () => {
    setError(null)
    
    // Validation
    if (!yourName.trim()) {
      setError('Please enter your name')
      return
    }
    
    const filledParticipants = participants.filter(p => p.trim()).map(p => p.trim())
    
    if (filledParticipants.length === 0) {
      setError('Please enter at least one participant name')
      return
    }
    
    if (filledParticipants.length > 6) {
      setError('Maximum 6 participants allowed')
      return
    }
    
    setIsCreating(true)
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/rooms`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          room_type: roomType,
          participant_names: filledParticipants
        })
      })
      
      if (!response.ok) {
        throw new Error('Failed to create room')
      }
      
      const roomData = await response.json()
      onRoomCreated(roomData, yourName)
    } catch (err) {
      setError(err.message || 'Failed to create room. Make sure the server is running.')
    } finally {
      setIsCreating(false)
    }
  }

  return (
    <div className="room-setup">
      <div className="setup-card">
        <h2>Create a Debate Room</h2>
        
        <div className="form-group">
          <label>Your Name:</label>
          <input
            type="text"
            value={yourName}
            onChange={(e) => setYourName(e.target.value)}
            placeholder="Enter your name"
            className="form-input"
          />
        </div>
        
        <div className="form-group">
          <label>Room Type:</label>
          <div className="radio-group">
            <label className="radio-label">
              <input
                type="radio"
                value="discussion"
                checked={roomType === 'discussion'}
                onChange={(e) => setRoomType(e.target.value)}
              />
              Discussion (Convergence)
            </label>
            <label className="radio-label">
              <input
                type="radio"
                value="debate"
                checked={roomType === 'debate'}
                onChange={(e) => setRoomType(e.target.value)}
              />
              Debate (Exploration)
            </label>
          </div>
        </div>
        
        <div className="form-group">
          <label>Number of Participants (1-6):</label>
          <input
            type="number"
            min="1"
            max="6"
            value={participantCount}
            onChange={(e) => handleParticipantCountChange(parseInt(e.target.value))}
            className="form-input"
          />
        </div>
        
        <div className="form-group">
          <label>Participant Names:</label>
          {participants.map((name, index) => (
            <input
              key={index}
              type="text"
              value={name}
              onChange={(e) => handleParticipantChange(index, e.target.value)}
              placeholder={`Participant ${index + 1}`}
              className="form-input participant-input"
            />
          ))}
          <p className="help-text">Enter at least one participant name</p>
        </div>
        
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
        
        <button 
          onClick={handleCreateRoom}
          disabled={isCreating}
          className="create-button"
        >
          {isCreating ? 'Creating...' : 'Create Room'}
        </button>
      </div>
    </div>
  )
}

export default RoomSetup
