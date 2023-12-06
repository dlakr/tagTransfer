import os
import sqlite3
import json
import socket
with open("paths.json", "r") as f:
    p = json.load(f)

# Define the directory you want to scan
directory_to_sync = p["syncDir"]

# Connect to the SQLite database
# db_path = r"/Volumes/GoogleDrive/My Drive/PLICO_CLOUD/ADMIN/file_attributes.db"
try:
    conn = sqlite3.connect(p["dbPath"])
    # Define the directory where the synced files are located

    # Connect to the SQLite database
    c = conn.cursor()
except sqlite3.OperationalError as error:
    pass

# Function to apply attributes to a file
def apply_attributes(file_path, attributes_str):
    try:
        import xattr
        machine_name = socket.gethostname()
        attributes = eval(attributes_str)
        for key, value in attributes.items():
            xattr.setxattr(file_path, key, value)
    except Exception as e:
        print(f"Error applying attributes to {file_path}: {e}")

# Retrieve and apply only the latest attributes
try:

    for row in c.execute('''
        SELECT filename, attributes FROM file_attributes 
        WHERE (filename, timestamp) IN (
            SELECT filename, MAX(timestamp) FROM file_attributes GROUP BY filename
        )
    '''):
        filename, attrs_str = row
        file_path = os.path.join(directory_to_sync, filename)
        if os.path.exists(file_path):
            apply_attributes(file_path, attrs_str)

    # Close the connection
    conn.close()
except NameError as error:
    pass

