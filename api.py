#coding: utf-8
from flask import Flask, jsonify, request
import sqlite3, json

api = Flask(__name__)

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

db = "tasks.db"
conn = create_connection(db)

cur = conn.cursor()
cur.execute("""
        create table if not exists tasks(
            id integer primary key autoincrement,
            task text not null,
            done boolean not null)
            """)
conn.commit()
cur.close()
conn.close()
@api.route('/api/tasks', methods=['POST'])
def save_task():
    conn = create_connection("tasks.db")
    cur = conn.cursor()
    data = request.get_json()
    columns = ', '.join(data.keys())
    placeholders = ', '.join('?' * (len(data)))
    sql = 'insert into tasks ({}) values ({})'.format(columns, placeholders)
    d=""
    values=[]
    for i,v in data.items():
        if i=='task':
            t=v
        elif i=='done':
            d=v
            if d == True:
                d=1
            else:
                d=0
 
    cur.execute(sql, (t,d))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(data), 201

@api.route('/api/tasks', methods=['GET'])
def home():
    def dict_factory(cursor, row):
        d={}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    conn = create_connection("tasks.db")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute("select * from tasks")
    results = cur.fetchall()    
    conn.close()
    
    return jsonify(results), 200

@api.route('/api/tasks/<int:id>', methods=['PUT'])
def change_done(id):
    conn = create_connection("tasks.db")
    cur = conn.cursor()
    data = request.get_json().get('done')
    if data == True:
        data = 1
    else:
        data = 0
    cur.execute("""UPDATE tasks SET done = ? WHERE id = ?""", (data, id))
    conn.commit()
    cur.close()
    
    return jsonify(data), 200

@api.route('/tasks/<int:id>', methods=['DELETE'])
def remove_task(id):
    data = request.get_json()
    conn = create_connection("tasks.db")
    cur = conn.cursor()
    cur.execute("""DELETE FROM tasks WHERE id = ?""", (id, ))
    conn.commit()
    cur.close()

    return jsonify(data), 204

conn.close()

if __name__ == '__main__':
    api.run(debug=True)
