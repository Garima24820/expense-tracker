from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    description TEXT,
                    amount REAL,
                    date TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_expense():
    data = request.get_json
    category = data['category']
    description = data['description']
    amount = float(data['amount'])
    date = data['date'] or datetime.now().strftime('%Y-%m-%d')

    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (category, description, amount, date) VALUES (?, ?, ?, ?)",
              (category, description, amount, date))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'}), 200

@app.route('/expenses')
def get_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT category, description, amount, date FROM expenses ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
