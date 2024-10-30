import sqlite3


def connect_to_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def initial_setup():
    conn = connect_to_db()
    conn.execute(
        """
        DROP TABLE IF EXISTS photos;
        """
    )
    conn.execute(
        """
        CREATE TABLE photos (
          id INTEGER PRIMARY KEY NOT NULL,
          name TEXT,
          width INTEGER,
          height INTEGER
        );
        """
    )
    conn.commit()
    print("Table created successfully")

    photos_seed_data = [
        ("1st photo", 800, 400),
        ("2nd photo", 1024, 768),
        ("3rd photo", 200, 150),
    ]
    conn.executemany(
        """
        INSERT INTO photos (name, width, height)
        VALUES (?,?,?)
        """,
        photos_seed_data,
    )
    conn.commit()
    print("Seed data created successfully")

    conn.close()


if __name__ == "__main__":
    initial_setup()