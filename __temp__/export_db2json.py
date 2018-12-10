import sqlite3
import json
import os

DB = "./timexlog.db"

def get_all_users(json_str = False):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name']
    db = conn.cursor()

    rows = db.execute('''
    SELECT * from post
    ''').fetchall()

    conn.commit()
    conn.close()

    if json_str:
        return json.dumps([dict(ix) for ix in rows]) # create json

    return rows


lst = get_all_users(json_str=True)

with open('timexlog.db.post.json', 'w+') as f:
    f.write(lst)
