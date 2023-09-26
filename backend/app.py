from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Create an SQLite database and a tasks table if they don't exist.
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT
    )
''')
conn.commit()
conn.close()

@app.route('/add', methods=['POST'])
def add_task():
    data = request.json
    task_text = data.get('task_text')
    if task_text:
        # Insert the task into the database.
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (text) VALUES (?)', (task_text,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Task added successfully."}), 201
    return jsonify({"message": "Invalid request."}), 400

@app.route('/tasks', methods=['GET'])
def task_list():
    # Retrieve tasks from the database.
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = [{'id': row[0], 'text': row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(tasks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)

