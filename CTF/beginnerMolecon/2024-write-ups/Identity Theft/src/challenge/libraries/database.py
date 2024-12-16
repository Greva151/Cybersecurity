import sqlite3
import psycopg2 as psy
import time

DB_PATH = "session_data.db"
DATABASE="Identity_Theft_db"
USER="DuffyDuck"
PASSWORD="77sdvgeragrfgsgaeraheah"
HOST="db"
PORT=5432


def init_db():
    with psy.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            user_id TEXT PRIMARY KEY,
            secret TEXT,  -- Storing secret as TEXT to handle large integers
            prime TEXT,   -- Storing prime as TEXT to handle large integers
            ts REAL
        );
        """)
        conn.commit()

def save_session(user_id, secret, prime, ts):
    secret_hex = hex(secret)  
    
    
    if prime is None:
        prime_hex = '0'  
    else:
        prime_hex = hex(prime) 
    
    with psy.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO sessions (user_id, secret, prime, ts) 
        VALUES (%s, %s, %s, %s)
        ON CONFLICT(user_id) DO UPDATE SET 
            secret=EXCLUDED.secret,
            prime=EXCLUDED.prime,
            ts=EXCLUDED.ts;
        """, (user_id, secret_hex, prime_hex, ts))
        conn.commit()



def get_session(user_id):
    with psy.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT secret, prime, ts FROM sessions WHERE user_id = %s;", (user_id,))
        result = cursor.fetchone()
        if result:
            secret = int(result[0], 16) if result[0] else None 
            prime = int(result[1], 16) if result[1] else None   
            return {"secret": secret, "prime": prime, "ts": result[2]}
        return None


def delete_expired_sessions(timeout):
    current_time = time.time()
    with psy.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE %s - ts > %s;", (current_time, timeout))
        conn.commit()

def delete_session(user_id):
    with psy.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE user_id = %s;", (user_id,))
        conn.commit()


init_db()

