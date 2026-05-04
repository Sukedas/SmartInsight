import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "smartinsight"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            port=os.getenv("DB_PORT", "5432")
        )
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if conn is None:
        return False
        
    try:
        cur = conn.cursor()
        
        # Create transactions table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                amount NUMERIC(15, 2) NOT NULL,
                category VARCHAR(50) NOT NULL,
                type VARCHAR(20) NOT NULL CHECK (type IN ('Ingreso', 'Gasto')),
                is_recurring BOOLEAN DEFAULT FALSE,
                description TEXT
            )
        ''')
        
        # Create budgets table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id SERIAL PRIMARY KEY,
                category VARCHAR(50) NOT NULL,
                amount NUMERIC(15, 2) NOT NULL,
                period VARCHAR(7) NOT NULL, -- Format: YYYY-MM
                UNIQUE (category, period)
            )
        ''')
        
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error inicializando base de datos: {e}")
        return False
    finally:
        if conn:
            conn.close()
