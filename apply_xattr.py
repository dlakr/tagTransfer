import os
import sqlite3
import xattr

# Define the directory where the synced files are located
directory_to_sync = "/path/to/synced/files"

# Connect to the SQLite database
conn = sqlite3.connect('file_attributes.db')
c = conn.cursor()

# Function to apply attributes to a file
def apply_attributes(file_path, attributes_str):
    try:
        attributes = eval(attributes_str)
        for key, value in attributes.items():
            xattr.setxattr(file_path, key, value)
    except Exception as e:
        print(f"Error applying attributes to {file_path}: {e}")

# Retrieve and apply only the latest attributes
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
