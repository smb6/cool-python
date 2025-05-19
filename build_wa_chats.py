import sqlite3

def get_chat_sessions_with_messages(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Retrieve all chat sessions
    cursor.execute("SELECT * FROM chat_sessions")
    sessions = cursor.fetchall()

    # Get column names for chat_sessions table
    session_columns = [description[0] for description in cursor.description]

    # Dictionary to store sessions and their messages
    sessions_with_messages = {}

    for session in sessions:
        # Create a dictionary for session data
        session_data = dict(zip(session_columns, session))
        session_id = session_data['id']  # Adjust 'id' to your primary key column name

        # Retrieve messages associated with this session
        cursor.execute("SELECT * FROM messages WHERE session_id = ?", (session_id,))
        messages = cursor.fetchall()

        # Get column names for messages table
        message_columns = [description[0] for description in cursor.description]

        # Convert messages to list of dictionaries
        messages_data = [dict(zip(message_columns, message)) for message in messages]

        # Attach messages to the session data
        session_data['messages'] = messages_data

        # Add the session data to the dictionary
        sessions_with_messages[session_id] = session_data

    # Close the connection
    conn.close()
    return sessions_with_messages

# Example usage
db_path = 'your_database.sqlite'  # Replace with your database path
chat_data = get_chat_sessions_with_messages(db_path)

# Display the data
for session_id, session_info in chat_data.items():
    print(f"Session ID: {session_id}")
    print("Session Info:")
    for key, value in session_info.items():
        if key != 'messages':
            print(f"  {key}: {value}")
    print("Messages:")
    for message in session_info['messages']:
        print(f"  Message ID: {message['id']}, Content: {message['content']}")
    print("-" * 40)
