import os
import sqlite3
import json
from datetime import datetime
import socket

os_type = os.name
with open("paths.json", "r") as f:
    p = json.load(f)
directory_to_sync = p["syncDir"]
db_path = p["dbPath"]

try:
    # Define the directory you want to scan

    # Connect to the SQLite database
    # db_path = r"/Volumes/GoogleDrive/My Drive/PLICO_CLOUD/ADMIN/file_attributes.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS file_attributes
                 (filename TEXT, attributes TEXT, timestamp DATETIME, PRIMARY KEY (filename, timestamp))''')
except sqlite3.OperationalError as error:
    pass


# Function to store attributes in the database
def store_attributes(file_path):
    if os_type != 'nt':
        import xattr
        try:
            attrs = xattr.xattr(file_path)
            attrs_str = str(dict(attrs))
            current_timestamp = datetime.now()
            c.execute("INSERT INTO file_attributes (filename, attributes, timestamp) VALUES (?, ?, ?)",
                      (file_path, attrs_str, current_timestamp))
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    else:
        print('wrong os')


try:
    for root, dirs, files in os.walk(directory_to_sync):

        # the program will have a list of computer and the path to their respective "drive" first part of the path

        for file in files:

            try:
                std_root = str(root).replace('Mon','My ')
            except:
                std_root = root

            file_path = os.path.join(std_root, file)
            # STORE THE COMPUTER IDS IN THE PATH PATHS JSON
            store_attributes(file_path)

    # Commit changes and close the connection

    conn.commit()
    conn.close()
except NameError as error:
    pass
