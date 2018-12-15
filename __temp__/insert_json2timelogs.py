# mv to project root
from datetime import datetime
import sqlite3
import json
# import os

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return None


def create_timelog(conn, timelog):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    sql = ''' INSERT INTO timelog(user_id, customer, project, task, datetime_start, datetime_end, time_correction, billable, comment, closed, date_created)
              VALUES(?,?,?,?,?,?,?,?,?,?,?);'''
    cur = conn.cursor()
    cur.execute(sql, timelog)
    return cur.lastrowid


DB = "./timexlog/timexlog.db"
json_str = open('timelog.json').read()
json_data = json.loads(json_str)
fmt = '%Y-%m-%d %H:%M:%S'

conn = create_connection(DB)
print(conn)
with conn:
    for json_item in json_data['timelogs']:
        start = datetime.strptime(json_item['datetime_start'], fmt)
        end = datetime.strptime(json_item['datetime_end'], fmt)
        timelog = (json_item['user_id'], json_item['customer'], \
                  json_item['project'],json_item['task'], start, end, \
                  float(json_item['time_correction']), json_item['billable'], \
                  json_item['comment'], json_item['closed'], start)
        print(timelog)
        create_timelog(conn, timelog)
