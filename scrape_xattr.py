import os
import sqlite3
import xattr
import json
from datetime import datetime

with open("paths.json", "r") as f:
    p = json.load(f)

# Define the directory you want to scan
directory_to_sync = p["syncDir"]
db_path = p["dbPath"]
# Connect to the SQLite database
# db_path = r"/Volumes/GoogleDrive/My Drive/PLICO_CLOUD/ADMIN/file_attributes.db"
conn = sqlite3.connect(db_path)
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


for root, dirs, files in os.walk(directory_to_sync):

    # the program will have a list of computer and the path to their respective "drive" first part of the path

    for file in files:

        drive = " Drive"
        file_path = os.path.join(root, file)
        path_parts = file_path.split(drive)
        path_start = path_parts[0]
        path_end = drive + path_parts[1]
        # STORE THE COMPUTER IDS IN THE PATH PATHS JSON
        print(path_start)
        store_attributes(path_end)

# Commit changes and close the connection
conn.commit()
conn.close()
