import os
import sqlite3
import json
from datetime import datetime
import socket
import platform
js_data = 'paths.json'
try:
    pform = str(platform.mac_ver()[0])[:2]
    machine_name = str(socket.gethostname()).split('.')[0]

except:
    pform = ""
    print('not on a mac')
    machine_name = "bob"



with open(js_data, "r") as f:
    ldbk = f"dbPath{machine_name}"
    p = json.load(f)
    root = os.path.split(p["dbPathMaster"])[0]
    ldbv = os. path.join(root, f"dbPath_{machine_name}.db")
    p.update({ldbk: ldbv})


with open(js_data, 'w') as f:
    data = json.dumps(p, indent=4)
    f.write(data)





rt = p['os'][pform]


directory_to_sync = rt + p["syncDir"]
dbPathMaster = rt + p["dbPathMaster"]

print(dbPathMaster)

try:

    conn = sqlite3.connect(dbPathMaster)
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
        new_attrs_str = str(dict(attrs))
        current_timestamp = datetime.now()
        c.execute("SELECT attributes FROM file_attributes WHERE filename= ?",
                  (file_path,))

        row = c.fetchone()
        if row:
            current_attr_str = row[0]
            if current_attr_str != new_attrs_str:
                c.execute("UPDATE file_attributes SET attributes = ?, timestamp = ? WHERE filename = ?",
                          (new_attrs_str, current_timestamp, file_path))
                # c.execute("INSERT OR REPLACE INTO file_attributes (filename, attributes, timestamp) VALUES (?, ?, ?)",
                #           (file_path, new_attrs_str, current_timestamp))
                conn.commit()
                print(f"updated: {file_path}")

        else:
            c.execute("INSERT INTO file_attributes (filename, attributes, timestamp) VALUES (?, ?, ?)",
                      (new_attrs_str, current_timestamp, file_path))
            conn.commit()

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
