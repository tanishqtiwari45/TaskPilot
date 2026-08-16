"""
database.py
=============
Database connection handler and table creation script.
Uses PyMySQL with DictCursor for easy-to-read results.
"""
import pymysql
from pymysql.cursors import DictCursor
from config import Config


def get_db():
    """
    Create and return a new database connection.
    Each call returns a fresh connection — remember to close it!
    """
    return pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        cursorclass=DictCursor,
        autocommit=True,
    )


def init_db():
    """
    Create the database and tables if they don't exist.
    Safe to run multiple times — uses IF NOT EXISTS.
    """
    # First connect without specifying a database to create it
    conn = pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        autocommit=True,
    )
    cursor = conn.cursor()

    print(f"[+] Creating database '{Config.DB_NAME}' if not exists...")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
    cursor.execute(f"USE {Config.DB_NAME}")

    # ── Users Table ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_username (username),
            INDEX idx_email (email)
        )
    """)
    print("  [OK] users table ready")

    # ── Tasks Table (updated with user_id) ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            title VARCHAR(150) NOT NULL,
            description TEXT,
            status VARCHAR(20) DEFAULT 'pending' NOT NULL,
            priority VARCHAR(20) DEFAULT 'medium' NOT NULL,
            due_date DATETIME,
            is_deleted TINYINT(1) DEFAULT 0 NOT NULL,
            deleted_at DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_user_id (user_id),
            INDEX idx_status (status),
            INDEX idx_due_date (due_date)
        )
    """)
    print("  [OK] tasks table ready")

    # ── Create default user if it doesn't exist ──
    cursor.execute("SELECT id FROM users WHERE username = 'demo' LIMIT 1")
    if not cursor.fetchone():
        from werkzeug.security import generate_password_hash
        demo_password_hash = generate_password_hash("demo123")
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            ("demo", "demo@taskpilot.local", demo_password_hash)
        )
        print("  [OK] demo user created (username: demo, password: demo123)")

    cursor.close()
    conn.close()
    print(f"\n[SUCCESS] Database '{Config.DB_NAME}' is ready!")
    return True


if __name__ == "__main__":
    """Run this directly to initialize the database."""
    init_db()

