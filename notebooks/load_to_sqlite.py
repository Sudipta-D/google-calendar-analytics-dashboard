import sqlite3
import pandas as pd
import os

# Create SQLite DB file in your project folder
db_path = "data/calendar_events.db"

# Read CSV
csv_path = "data/calendar_events.csv"
df = pd.read_csv(csv_path)

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS calendar_events (
    event_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    start_time TEXT,
    end_time TEXT,
    status TEXT,
    description TEXT,
    location TEXT,
    event_type TEXT,
    with_whom TEXT
)
''')

# Insert data
df.to_sql("calendar_events", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("✅ CSV loaded into SQLite at data/calendar_events.db")
