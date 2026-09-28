from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import init_db, add_task_db, delete_task_db
from datetime import datetime, date
import sqlite3

app = Flask(__name__)
init_db()

def get_sorted_tasks():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()

    today = date.today()

    for task in tasks:
        try:
            deadline_date = datetime.strptime(task['deadline'], '%Y-%m-%d').date()
            days_left = (deadline_date - today).days
        except Exception:
            days_left = 1
        
        task['days_left'] = days_left
        weight = task['difficulty'] * task['hours']

        if days_left <= 1:
            task['priority'] = 'HIGH'
        elif days_left <= 3 and weight >= 4:
            task['priority'] = 'HIGH'
        elif weight >= 5:
            task['priority'] = 'MEDIUM'
        else:
            task['priority'] = 'LOW'

    tasks.sort(key=lambda t: (t['deadline'], -t['difficulty'], -t['hours']))
    return tasks

@app.route("/")
def home():
    tasks = get_sorted_tasks()
    total_tasks = len(tasks)
    high_count = sum(1 for t in tasks if t['priority'] == 'HIGH')
    return render_template("index.html", tasks=tasks, total=total_tasks, high=high_count)

@app.route("/add", methods=["POST"])
def add():
    subject = request.form.get("subject")
    topic = request.form.get("topic")
    deadline = request.form.get("deadline")
    hours = float(request.form.get("hours", 1))
    difficulty = int(request.form.get("difficulty", 1))

    score = difficulty * hours
    add_task_db(subject, topic, deadline, hours, difficulty, "LOW", score)
    return redirect(url_for("home"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    delete_task_db(task_id)
    return redirect(url_for("home"))

@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    data = request.get_json() or {}
    subject = data.get("subject", "").strip().lower()
    topic = data.get("topic", "").strip().lower()

    if "algebra" in topic or "algebra" in subject:
        response_text = f"""
        <div style="text-align: left;">
            <p><strong>🎯 Subject:</strong> Mathematics | <strong>Topic:</strong> Algebra</p>
            <br>
            <p><strong>1. Core Theoretical Concept:</strong><br>
            Algebra relies on representing unknown values using variables (x, y) to model relationships. Focus on balancing equations—any operation performed on the left-hand side must be mirrored on the right.</p>
            <br>
            <p><strong>2. Must-Remember Formulas:</strong><br>
            • Quadratic Formula: <code>x = [-b ± √(b² - 4ac)] / 2a</code><br>
            • Binomial Expansion: <code>(a + b)² = a² + 2ab + b²</code><br>
            • Difference of Squares: <code>a² - b² = (a - b)(a + b)</code></p>
            <br>
            <p><strong>3. Common Student Pitfall:</strong><br>
            Sign errors during bracket expansion, especially when distributing negative coefficients (e.g., <code>-(x - 3) = -x + 3</code>, not <code>-x - 3</code>).</p>
            <br>
            <p><strong>4. Recommended 25-Min Study Plan:</strong><br>
            • <strong>0-10 min:</strong> Review factoring & standard identities.<br>
            • <strong>10-25 min:</strong> Solve 3 quadratic equations using both factorization and the quadratic formula.</p>
        </div>
        """
    elif "grammar" in topic or "english" in subject or "hindi" in subject:
        response_text = f"""
        <div style="text-align: left;">
            <p><strong>🎯 Subject:</strong> Language & Linguistics | <strong>Topic:</strong> {topic.title()}</p>
            <br>
            <p><strong>1. Structural Foundation:</strong><br>
            Master Subject-Verb Agreement and Tense Consistency. The grammatical subject must always match the predicate in number and person.</p>
            <br>
            <p><strong>2. Golden Rules for Exams:</strong><br>
            • Singular indefinite pronouns (everyone, each, somebody) always take singular verbs.<br>
            • Avoid dangling modifiers; ensure descriptive phrases clearly link to the correct noun.</p>
            <br>
            <p><strong>3. Quick Self-Test:</strong><br>
            Identify error: <em>"Neither the teacher nor the students was present."</em><br>
            (Rule: In 'neither/nor', verb agrees with the closer subject → <strong>were</strong>).</p>
        </div>
        """
    else:
        response_text = f"""
        <div style="text-align: left;">
            <p><strong>🎯 Academic Deep Dive:</strong> {topic.title()} ({subject.title()})</p>
            <br>
            <p><strong>1. Core Concept & Principles:</strong><br>
            Break {topic.title()} down into first principles. Identify the primary inputs, processing rules, and standard output behaviors.</p>
            <br>
            <p><strong>2. High-Yield Exam Focus Areas:</strong><br>
            • Definitions, standard notations, and underlying assumptions.<br>
            • Edge cases or conditions under which primary theorems/rules do not hold.</p>
            <br>
            <p><strong>3. 25-Minute Tactical Plan:</strong><br>
            • <strong>Phase 1 (10 mins):</strong> Active recall—write everything you know about {topic.title()} on blank paper.<br>
            • <strong>Phase 2 (15 mins):</strong> Solve 2 previous-year university questions without referring to solution notes.</p>
        </div>
        """

    return jsonify({"reply": response_text})

if __name__ == "__main__":
    app.run(debug=True)