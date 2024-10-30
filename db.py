import sqlite3


def connect_to_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def initial_setup():
    conn = connect_to_db()
    conn.execute(
        """
        DROP TABLE IF EXISTS pillows;
        """
    )
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
    conn.commit()
    print("Table created successfully")

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


if __name__ == "__main__":
    initial_setup()

def pillows_all():
    conn = connect_to_db()
    rows = conn.execute(
        """
        SELECT * FROM pillows
        """
    ).fetchall()
    return [dict(row) for row in rows]

def pillows_create(name, image_url, description, size):
    conn = connect_to_db()
    row = conn.execute(
        """
        INSERT INTO pillows (name, image_url, description, size)
        VALUES (?, ?, ?, ?)
        RETURNING *
        """,
        (name, image_url, description, size),
    ).fetchone()
    conn.commit()
    return dict(row)