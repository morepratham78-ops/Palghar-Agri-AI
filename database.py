"""
Database module for PALGHAR AGRI AI
"""
import sqlite3
import hashlib
import os
from config import DB_PATH


def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str) -> str:
    """Hash password with salt."""
    salt = "palghar_agri_2024"
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


def init_db():
    """Initialize database tables and seed initial farmer account if empty."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            phone TEXT,
            village TEXT,
            language TEXT DEFAULT 'mr',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            crop_name TEXT NOT NULL,
            area_acres REAL,
            sowing_date TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diagnosis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            image_path TEXT,
            disease_name TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()
    
    # Check if we should seed default farmer data
    user_count = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if user_count == 0:
        cursor.execute(
            """INSERT INTO users (username, password_hash, full_name, phone, village, language)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                "farmer",
                hash_password("farmer123"),
                "रमेश पाटील (Ramesh Patil)",
                "9823456789",
                "पालघर (Palghar)",
                "mr"
            )
        )
        user_id = cursor.lastrowid
        
        # Seed realistic Palghar crops
        cursor.execute(
            """INSERT INTO crops (user_id, crop_name, area_acres, sowing_date, notes)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, "Rice / भात / धान", 2.5, "2024-06-20", "वाडा कोलम (Wada Kolam) - पालघर प्रसिद्ध तांदूळ")
        )
        cursor.execute(
            """INSERT INTO crops (user_id, crop_name, area_acres, sowing_date, notes)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, "Chickoo / चिकू", 1.5, "2022-04-10", "डहाणू घोलवड चिकू (Dahanu Gholvad GI tag)")
        )
        cursor.execute(
            """INSERT INTO crops (user_id, crop_name, area_acres, sowing_date, notes)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, "Tomato / टोमॅटो / टमाटर", 0.5, "2024-09-15", "ठिबक सिंचनावर लागवड (Drip irrigation)")
        )
        
        # Seed realistic diagnosis history
        cursor.execute(
            """INSERT INTO diagnosis_history (user_id, image_path, disease_name, confidence)
               VALUES (?, ?, ?, ?)""",
            (user_id, "", "Tomato - Early Blight (टोमॅटो लवकर करपा)", 0.89)
        )
        
        conn.commit()
        
    conn.close()


def register_user(username: str, password: str, full_name: str = "", phone: str = "", village: str = "") -> tuple[bool, str]:
    """Register a new user. Returns (success, message)."""
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (username, password_hash, full_name, phone, village) VALUES (?, ?, ?, ?, ?)",
            (username.strip(), hash_password(password), full_name.strip(), phone.strip(), village.strip())
        )
        conn.commit()
        return True, "register_success"
    except sqlite3.IntegrityError:
        return False, "already_exists"
    finally:
        conn.close()


def login_user(username: str, password: str) -> dict | None:
    """Login user. Returns user dict or None."""
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password_hash = ?",
        (username.strip(), hash_password(password))
    ).fetchone()
    conn.close()
    if user:
        return dict(user)
    return None


def update_user_language(user_id: int, language: str):
    """Update user's preferred language."""
    if user_id <= 0:
        return
    conn = get_db()
    conn.execute("UPDATE users SET language = ? WHERE id = ?", (language, user_id))
    conn.commit()
    conn.close()


def get_user_crops(user_id: int) -> list:
    """Get all crops for a user."""
    conn = get_db()
    crops = conn.execute(
        "SELECT * FROM crops WHERE user_id = ? ORDER BY created_at DESC", (user_id,)
    ).fetchall()
    conn.close()
    return [dict(c) for c in crops]


def add_crop(user_id: int, crop_name: str, area_acres: float, sowing_date: str, notes: str = ""):
    """Add a crop for user."""
    conn = get_db()
    conn.execute(
        "INSERT INTO crops (user_id, crop_name, area_acres, sowing_date, notes) VALUES (?, ?, ?, ?, ?)",
        (user_id, crop_name, area_acres, sowing_date, notes)
    )
    conn.commit()
    conn.close()


def delete_crop(crop_id: int, user_id: int):
    """Delete a crop (with user ownership check)."""
    conn = get_db()
    conn.execute("DELETE FROM crops WHERE id = ? AND user_id = ?", (crop_id, user_id))
    conn.commit()
    conn.close()


def save_diagnosis(user_id: int, image_path: str, disease_name: str, confidence: float):
    """Save a diagnosis record."""
    if user_id <= 0:
        return
    conn = get_db()
    conn.execute(
        "INSERT INTO diagnosis_history (user_id, image_path, disease_name, confidence) VALUES (?, ?, ?, ?)",
        (user_id, image_path, disease_name, confidence)
    )
    conn.commit()
    conn.close()


def get_diagnosis_history(user_id: int, limit: int = 10) -> list:
    """Get diagnosis history for a user."""
    conn = get_db()
    records = conn.execute(
        "SELECT * FROM diagnosis_history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in records]


# Initialize DB on import
init_db()
