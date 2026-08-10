import sqlite3
import os

DATABASE = "library.db"
SCHEMA_FILE = "schema.sql"
POPULATE_FILE = "populate.sql"

def initialize_database():
    if os.path.exists(DATABASE):
        print("Removing old " + DATABASE)
        os.remove(DATABASE)
    else:
        print("No old database found. Creating a new one")

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    conn.execute("PRAGMA foreign_keys = ON;")

    try:
        with open(SCHEMA_FILE, 'r') as f:
            schema_script = f.read()
        print("Executing " + SCHEMA_FILE)
        cur.executescript(schema_script)
    except FileNotFoundError:
        print("Error: Could not find " + SCHEMA_FILE + ". Ensure it is in the same folder.")
        conn.close()
        return
    except sqlite3.OperationalError as e:
        print("SQLite Error in schema: " + str(e))
        conn.close()
        return

    try:
        with open(POPULATE_FILE, 'r') as f:
            populate_script = f.read()
        print("Executing " + POPULATE_FILE)
        cur.executescript(populate_script)
    except FileNotFoundError:
        print("Error: Could not find " + POPULATE_FILE + ". Ensure it is in the same folder.")
        conn.close()
        return
    except sqlite3.OperationalError as e:
        print("SQLite Error in populate data: " + str(e))
        conn.close()
        return

    conn.commit()
    conn.close()
    print("\nSuccess! The database has been initialized and is ready to use.")

if __name__ == "__main__":
    initialize_database()