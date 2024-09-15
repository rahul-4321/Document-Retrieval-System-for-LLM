import psycopg2
from app.config import settings

def get_db_connection():
    return psycopg2.connect(settings.POSTGRES_URL)

def check_rate_limit(user_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT call_count FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        
        if result is None:
            cursor.execute("INSERT INTO users (user_id, call_count) VALUES (%s, 1)", (user_id,))
            return True
        elif result[0] < settings.RATE_LIMIT:
            cursor.execute("UPDATE users SET call_count = call_count + 1 WHERE user_id = %s", (user_id,))
            return True
        else:
            return False
    
    finally:
        conn.commit()
        cursor.close()
        conn.close()