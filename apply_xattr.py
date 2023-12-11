import os
import sqlite3
import json
import socket
import platform

with open("paths.json", "r") as f:
    p = json.load(f)

try:
    pform = str(platform.mac_ver()[0])[:2]

except:
    pform = ""
    print('not on a mac')
rt = p['os'][pform]


directory_to_sync = rt + p["syncDir"]
db_path = rt + p["dbPath"]

try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
except sqlite3.OperationalError as error:
    print(error)


def apply_attributes(file_path, attributes_str):
    try:
        import xattr
        attributes = eval(attributes_str)
        for key, value in attributes.items():
            xattr.setxattr(file_path, key, value)
    except Exception as e:
        print(f"Error applying attributes to {file_path}: {e}")

try:

    for row in c.execute('''
        SELECT filename, attributes FROM file_attributes 
        WHERE filename IN file_attributes 
    '''):
        filename, attrs_str = row
        machine_name = socket.gethostname()
        if machine_name.upper() == "PLICO-B":
            fname = str(filename).replace("My ", "Mon ")
        else:
            fname = filename
        f_path = os.path.join(directory_to_sync, fname)
        if os.path.exists(f_path):
            apply_attributes(f_path, attrs_str)
            print(f"applied {attrs_str} to {f_path}")

    # Close the connection
    conn.close()
except NameError as error:
    print(error)


