import os
import sqlite3
import xattr
from datetime import datetime

# Define the directory you want to scan
directory_to_scan = "/path/to/google/drive/folder"

# Connect to the SQLite database
conn = sqlite3.connect('file_attributes.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS file_attributes
             (filename TEXT, attributes TEXT, timestamp DATETIME, PRIMARY KEY (filename, timestamp))''')

# Function to store attributes in the database
def store_attributes(file_path):
    try:
        attrs = xattr.xattr(file_path)
        attrs_str = str(dict(attrs))
        current_timestamp = datetime.now()
        c.execute("INSERT INTO file_attributes (filename, attributes, timestamp) VALUES (?, ?, ?)",
                  (file_path, attrs_str, current_timestamp))
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Walk through the directory
for root, dirs, files in os.walk(directory_to_scan):
    for file in files:
        file_path = os.path.join(root, file)
        store_attributes(file_path)

# Commit changes and close the connection
conn.commit()
conn.close()
