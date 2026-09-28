import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            deadline TEXT NOT NULL,
            hours REAL NOT NULL,
            difficulty INTEGER NOT NULL,
            priority TEXT,
            score REAL
        )
    ''')
    conn.commit()
    conn.close()

def add_task_db(subject, topic, deadline, hours, difficulty, priority, score):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (subject, topic, deadline, hours, difficulty, priority, score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (subject, topic, deadline, hours, difficulty, priority, score))
    conn.commit()
    conn.close()

def get_tasks_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY score DESC')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task_db(task_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()