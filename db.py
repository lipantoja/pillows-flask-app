import sqlite3

def connect_to_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def initial_setup():
    conn = connect_to_db()
    conn.execute("DROP TABLE IF EXISTS pillows")
    conn.execute("DROP TABLE IF EXISTS users")
    conn.execute("DROP TABLE IF EXISTS sessions")

    conn.execute(
        """
        CREATE TABLE pillows (
            id INTEGER PRIMARY KEY NOT NULL,
            name TEXT,
            image_url TEXT,
            description TEXT,
            size TEXT
        );
        """
    )
    
    conn.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    
    conn.execute(
        """
        CREATE TABLE sessions (
            id INTEGER PRIMARY KEY NOT NULL,
            user_id INTEGER NOT NULL,
            token TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
    )
    
    conn.commit()
    print("Tables created successfully")
    
    pillows_seed_data = [
        ("1st pillow", "https://cdn11.bigcommerce.com/s-r7rkk91ha4/images/stencil/1280x1280/products/440/3843/Garfield_1__36923.1729699225.jpg?c=1", "Garfield the Cat, as a pillow", "Medium")
    ]
    
    conn.executemany(
        """
        INSERT INTO pillows (name, image_url, description, size)
        VALUES (?,?,?,?)
        """,
        pillows_seed_data,
    )
    
    conn.commit()
    print("Seed data created successfully")
    conn.close()

def pillows_all():
    conn = connect_to_db()
    rows = conn.execute(
        """
        SELECT * FROM pillows
        """
    ).fetchall()
    return [dict(row) for row in rows]

def create_user(email, password, name):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (email, password, name)
        VALUES (?, ?, ?)
        """,
        (email, password, name)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def get_user_by_email(email):
    conn = connect_to_db()
    row = conn.execute(
        """
        SELECT * FROM users WHERE email = ?
        """,
        (email,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_id(user_id):
    conn = connect_to_db()
    row = conn.execute(
        """
        SELECT * FROM users WHERE id = ?
        """,
        (user_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None

if __name__ == "__main__":
    initial_setup()