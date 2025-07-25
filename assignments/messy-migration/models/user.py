import sqlite3
from typing import Optional, List, Dict, Any
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database connection and create tables if needed"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def _get_connection(self):
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_user(self, name: str, email: str, password: str) -> Optional[int]:
        """Create a new user with hashed password"""
        try:
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                    (name, email, password_hash)
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None  # Email already exists
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID (without password hash)"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT id, name, email, created_at FROM users WHERE id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users (without password hashes)"""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT id, name, email, created_at FROM users")
            return [dict(row) for row in cursor.fetchall()]
    
    def update_user(self, user_id: int, name: str = None, email: str = None) -> bool:
        """Update user information"""
        if not name and not email:
            return False
        
        try:
            with self._get_connection() as conn:
                if name and email:
                    conn.execute(
                        "UPDATE users SET name = ?, email = ? WHERE id = ?",
                        (name, email, user_id)
                    )
                elif name:
                    conn.execute(
                        "UPDATE users SET name = ? WHERE id = ?",
                        (name, user_id)
                    )
                elif email:
                    conn.execute(
                        "UPDATE users SET email = ? WHERE id = ?",
                        (email, user_id)
                    )
                
                return conn.total_changes > 0
        except sqlite3.IntegrityError:
            return False  # Email already exists
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID"""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            return conn.total_changes > 0
    
    def search_users_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search users by name (partial match)"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT id, name, email, created_at FROM users WHERE name LIKE ?",
                (f"%{name}%",)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with email and password"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT id, name, email, password_hash FROM users WHERE email = ?",
                (email,)
            )
            row = cursor.fetchone()
            
            if row and bcrypt.check_password_hash(row['password_hash'], password):
                return {
                    'id': row['id'],
                    'name': row['name'],
                    'email': row['email']
                }
            return None