import os
import sqlite3
import json
from datetime import datetime
import socket
import platform

try:
    pform = str(platform.mac_ver()[0])[:2]

except:
    pform = ""
    print('not on a mac')

with open("paths.json", "r") as f:
    p = json.load(f)

machine_name = str(socket.gethostname()).split('.')[0]
rt = p['os'][pform]


directory_to_sync = rt + p["syncDir"]
db_path = rt + p["dbPath"]
print(db_path)

try:

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # c.execute('''CREATE TABLE IF NOT EXISTS file_attributes
    #              (filename TEXT PRIMARY KEY, attributes TEXT, timestamp DATETIME (filename, timestamp))''')
    c.execute('''CREATE TABLE IF NOT EXISTS file_attributes
                 (filename TEXT PRIMARY KEY, 
                  attributes TEXT, 
                  timestamp DATETIME)''')
except sqlite3.OperationalError as error:
    print(error)
    pass
# def insert_or_update(file_path, attrs_str, current_timestamp):
#     c.execute(F"SELECT id FROM file_attributes WHERE filename = ?", (file_path,))
#     exists = c.fetchone()
#     if exists:
#         c.execute("UPDATE file_attributes SET (attributes, timestamp) WHERE filename VALUES (?, ?, ?)",
#                   (file_path, attrs_str, current_timestamp))
#     else:
#         c.execute("INSERT OR REPLACE INTO file_attributes (filename, attributes, timestamp) VALUES (?, ?, ?)",
#                   (file_path, attrs_str, current_timestamp))
#     pass

def store_attributes(file_path):

    try:
        import xattr
        attr = 'com.apple.FinderInfo'
        attrs = xattr.xattr(file_path)
        attrs_str = str(dict(attrs))
        current_timestamp = datetime.now()

        c.execute("INSERT OR REPLACE INTO file_attributes (filename, attributes, timestamp) VALUES (?, ?, ?)",
                  (file_path, attrs_str, current_timestamp))

    except Exception as e:
        print(f"Error processing {file_path}: {e}")



try:
    for root, dirs, files in os.walk(directory_to_sync):

        # the program will have a list of computer and the path to their respective "drive" first part of the path

        for file in files:

            std_root = str(root).replace('Mon', 'My ')
            f_path = os.path.join(std_root, file)
            # STORE THE COMPUTER IDS IN THE PATH PATHS JSON
            store_attributes(f_path)

    # Commit changes and close the connection

    conn.commit()
    conn.close()
except NameError as error:
    print(error)
    pass
