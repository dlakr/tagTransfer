# import apply_xattr
# import scrape_xattr
import os
import sqlite3
import json
import socket
import platform
from datetime import datetime
js_data = 'paths.json'
try:
    pform = str(platform.mac_ver()[0])[:2]
    machine_name = str(socket.gethostname()).split('.')[0]


except Exception as e:
    pform = ""
    print('not on a mac')
    machine_name = "bob"


with open(js_data, "r") as f:
    p = json.load(f)

local = p[f"dbPath{machine_name}"]
master = p[f"dbPathMaster"]


def compare_and_update_databases(db_a_path, db_b_path):
    # Connect to both databases
    conn_a = sqlite3.connect(db_a_path)
    conn_b = sqlite3.connect(db_b_path)

    cursor_a = conn_a.cursor()
    cursor_b = conn_b.cursor()

    # Fetch all data from Database A
    cursor_a.execute("SELECT filename, attributes, timestamp FROM file_attributes")
    records_a = cursor_a.fetchall()

    for filename, attributes_a, timestamp_a in records_a:
        # Convert timestamp to a datetime object
        timestamp_a = datetime.strptime(timestamp_a, '%Y-%m-%d %H:%M:%S')

        # Fetch corresponding data from Database B
        cursor_b.execute("SELECT attributes, timestamp FROM file_attributes WHERE filename = ?", (filename,))
        record_b = cursor_b.fetchone()

        if record_b:
            attributes_b, timestamp_b = record_b
            timestamp_b = datetime.strptime(timestamp_b, '%Y-%m-%d %H:%M:%S')

            # Compare timestamps and attributes
            if timestamp_a > timestamp_b and attributes_a != attributes_b:
                # Update Database B
                cursor_b.execute("UPDATE file_attributes SET attributes = ?, timestamp = ? WHERE filename = ?",
                                 (attributes_a, timestamp_a.strftime('%Y-%m-%d %H:%M:%S'), filename))
                print(f"Updated: {filename}")

    # Commit the changes to Database B and close connections
    conn_b.commit()
    conn_a.close()
    conn_b.close()


if __name__ == '__main__':
    compare_and_update_databases(local, master)

