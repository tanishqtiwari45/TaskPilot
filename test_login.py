#!/usr/bin/env python
"""Test script to debug login"""

from database import get_db
from auth import verify_password

# Check if demo user exists
db = get_db()
try:
    with db.cursor() as cursor:
        print("Querying for demo user...")
        cursor.execute("SELECT id, username, email, password_hash FROM users WHERE username = %s", ("demo",))
        user = cursor.fetchone()
        
        if user:
            print(f"Found user: {user}")
            print(f"User ID: {user['id']}")
            print(f"Username: {user['username']}")
            print(f"Email: {user['email']}")
            print(f"Password Hash: {user['password_hash'][:50]}...")
            
            # Test password verification
            is_valid = verify_password("demo123", user['password_hash'])
            print(f"Password verification: {is_valid}")
        else:
            print("Demo user not found!")
            
        # List all users
        print("\nAll users in database:")
        cursor.execute("SELECT id, username, email FROM users")
        users = cursor.fetchall()
        for u in users:
            print(f"  - {u['username']} (ID: {u['id']})")
            
finally:
    db.close()
