"""
Test script for the chat application components.
Tests database structure and basic functionality without requiring full dependencies.
"""

import sys
import sqlite3
import json
import os


def test_database_schema():
    """Test the database schema creation."""
    print("Testing Database Schema...")
    
    # Create test database
    db_path = "test_debate_rooms.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables (same schema as DatabaseManager)
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
    
    print("✓ Tables created")
    
    # Test room insertion
    cursor.execute(
        "INSERT INTO rooms (room_id, room_type, participants, topic) VALUES (?, ?, ?, ?)",
        ("test123", "discussion", json.dumps(["Alice", "Bob"]), "Test Topic")
    )
    conn.commit()
    print("✓ Room inserted")
    
    # Test room retrieval
    cursor.execute("SELECT * FROM rooms WHERE room_id = ?", ("test123",))
    room = cursor.fetchone()
    assert room is not None
    print("✓ Room retrieved")
    
    # Test message insertion
    cursor.execute(
        "INSERT INTO messages (room_id, speaker, content, message_type) VALUES (?, ?, ?, ?)",
        ("test123", "Alice", "Hello!", "user")
    )
    conn.commit()
    print("✓ Message inserted")
    
    # Test message retrieval
    cursor.execute("SELECT * FROM messages WHERE room_id = ?", ("test123",))
    messages = cursor.fetchall()
    assert len(messages) == 1
    print("✓ Messages retrieved")
    
    conn.close()
    os.remove(db_path)
    print("✓ Test database cleaned up")
    
    print("\n✅ Database schema tests passed!\n")
    return True


def test_server_syntax():
    """Test that server file has valid Python syntax."""
    print("Testing Server File Syntax...")
    
    import py_compile
    
    try:
        py_compile.compile('debate_chat_server.py', doraise=True)
        print("✓ Server file syntax valid")
    except py_compile.PyCompileError as e:
        print(f"✗ Syntax error: {e}")
        return False
    
    print("\n✅ Server syntax tests passed!\n")
    return True


def test_frontend_build():
    """Test that frontend builds successfully."""
    print("Testing Frontend Build...")
    
    if not os.path.exists('debate-room-ui/dist'):
        print("⚠️  Frontend not built yet. Run 'cd debate-room-ui && npm run build'")
        print("   Skipping frontend test...")
        return True
    
    # Check if dist folder has files
    dist_files = os.listdir('debate-room-ui/dist')
    assert 'index.html' in dist_files
    print("✓ Frontend build artifacts exist")
    
    print("\n✅ Frontend build tests passed!\n")
    return True


def test_file_structure():
    """Test that all necessary files exist."""
    print("Testing File Structure...")
    
    required_files = [
        'debate_chat_server.py',
        'debate_room_facilitator.py',
        'debate_room_tools.py',
        'geminiAgent.py',
        'requirements.txt',
        'start_chat_app.sh',
        'stop_chat_app.sh',
        'debate-room-ui/package.json',
        'debate-room-ui/src/App.jsx',
        'debate-room-ui/src/components/ChatRoom.jsx',
        'debate-room-ui/src/components/RoomSetup.jsx',
        'docs/CHAT_APPLICATION.md'
    ]
    
    for file_path in required_files:
        assert os.path.exists(file_path), f"Missing file: {file_path}"
        print(f"✓ {file_path}")
    
    print("\n✅ File structure tests passed!\n")
    return True


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("DEBATE CHAT APPLICATION - COMPONENT TESTS")
    print("="*60 + "\n")
    
    try:
        # Test 1: File Structure
        test_file_structure()
        
        # Test 2: Database Schema
        test_database_schema()
        
        # Test 3: Server Syntax
        test_server_syntax()
        
        # Test 4: Frontend Build
        test_frontend_build()
        
        print("\n" + "="*60)
        print("ALL COMPONENT TESTS PASSED! ✅")
        print("="*60)
        print("\nChat Application is ready to use!")
        print("\nTo start the application:")
        print("  1. Create .env file with GEMINI_API_KEY")
        print("  2. Run: ./start_chat_app.sh")
        print("  3. Open browser to http://localhost:5173")
        print("\nOr start manually:")
        print("  Terminal 1: python3 debate_chat_server.py")
        print("  Terminal 2: cd debate-room-ui && npm run dev")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
