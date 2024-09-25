import psycopg2
from psycopg2 import sql
import uuid
import os

# # Replace these with your actual database credentials
# DB_NAME = "your_database_name"
# DB_USER = "your_username"
# DB_PASSWORD = "your_password"
# DB_HOST = "your_host"
# DB_PORT = "your_port"



DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')


def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id UUID PRIMARY KEY,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id SERIAL PRIMARY KEY,
        conversation_id UUID REFERENCES conversations(id),
        feedback INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def save_conversation(question, answer):
    conn = get_db_connection()
    cur = conn.cursor()
    
    conversation_id = uuid.uuid4()
    
    cur.execute(
        "INSERT INTO conversations (id, question, answer) VALUES (%s, %s, %s)",
        (conversation_id, question, answer)
    )
    
    conn.commit()
    cur.close()
    conn.close()
    
    return conversation_id

def save_feedback(conversation_id, feedback):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO feedback (conversation_id, feedback) VALUES (%s, %s)",
        (conversation_id, feedback)
    )
    
    conn.commit()
    cur.close()
    conn.close()

# Call this function when setting up your application
create_tables()