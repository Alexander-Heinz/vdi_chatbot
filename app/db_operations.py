import psycopg2
from psycopg2 import sql
import uuid
import os

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')



expected_schema = {
    'conversations': {
        'id': 'UUID PRIMARY KEY',
        'question': 'TEXT NOT NULL',
        'answer': 'TEXT NOT NULL',
        'language': 'TEXT',
        'session_id': 'TEXT',
        'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    },
    'feedback': {
        'id': 'SERIAL PRIMARY KEY',
        'conversation_id': 'UUID REFERENCES conversations(id)',
        'feedback': 'INTEGER NOT NULL',
        'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
    },
    'usage_stats': {
        'id': 'SERIAL PRIMARY KEY',
        'session_id': 'TEXT',
        'interaction_type': 'TEXT',
        'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
        'prompt_tokens': 'INTEGER',
        'completion_tokens': 'INTEGER',
        'total_tokens': 'INTEGER'
    }
}


def update_table_schema(table_name, expected_columns):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get the current columns in the table
    cur.execute(sql.SQL("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = %s
    """), (table_name,))
    
    current_columns = {row[0] for row in cur.fetchall()}
    
    # Compare with expected columns and add any missing ones
    for column_name, column_definition in expected_columns.items():
        if column_name not in current_columns:
            try:
                cur.execute(sql.SQL("""
                ALTER TABLE {} 
                ADD COLUMN {} {}
                """).format(sql.Identifier(table_name), sql.Identifier(column_name), sql.SQL(column_definition)))
            except Exception as e:
                print(f"Error altering table {table_name}: {e}")

    
    conn.commit()
    cur.close()
    conn.close()




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
    
    # Create tables if they don't exist
    for table_name, columns in expected_schema.items():
        # Create the SQL column definitions
        column_definitions = ', '.join([f"{col_name} {col_def}" for col_name, col_def in columns.items()])
        
        # Use proper formatting for SQL execution
        create_table_query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS {} (
            {}
        )
        """).format(sql.Identifier(table_name), sql.SQL(column_definitions))
        try:
            cur.execute(create_table_query)
            print(f"Table {table_name} created or already exists.")
        except Exception as e:
            print(f"Error creating table {table_name}: {e}")    
            
    # Update the schema to add any missing columns
    for table_name, columns in expected_schema.items():
        update_table_schema(table_name, columns)
    
    conn.commit()
    cur.close()
    conn.close()



def save_conversation(question, answer, language, session_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    conversation_id = str(uuid.uuid4())
    
    cur.execute(
        "INSERT INTO conversations (id, question, answer, language, session_id) VALUES (%s, %s, %s, %s, %s)",
        (conversation_id, question, answer, language, session_id)
    )
    
    conn.commit()
    cur.close()
    conn.close()
    
    return conversation_id

def save_feedback(conversation_id, feedback):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check if feedback already exists
    cur.execute(
        "SELECT COUNT(*) FROM feedback WHERE conversation_id = %s",
        (conversation_id,)
    )
    feedback_count = cur.fetchone()[0]
    
    if feedback_count == 0:
        cur.execute(
            "INSERT INTO feedback (conversation_id, feedback) VALUES (%s, %s)",
            (conversation_id, feedback)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    else:
        cur.close()
        conn.close()
        return False
    

def check_feedback_exists(conversation_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "SELECT COUNT(*) FROM feedback WHERE conversation_id = %s",
        (conversation_id,)
    )
    feedback_count = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    return feedback_count > 0

def log_interaction(session_id, interaction_type, prompt_tokens=None, completion_tokens=None, total_tokens=None):
    create_tables()
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        """
        INSERT INTO usage_stats 
        (session_id, interaction_type, prompt_tokens, completion_tokens, total_tokens) 
        VALUES (%s, %s, %s, %s, %s)
        """,
        (session_id, interaction_type, prompt_tokens, completion_tokens, total_tokens)
    )
    
    conn.commit()
    cur.close()
    conn.close()


