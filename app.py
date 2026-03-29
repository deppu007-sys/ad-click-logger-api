from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('clicks.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_name TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# Home route
@app.route('/')
def home():
    return "Ad Click Logger Running 🚀"

# Track click
@app.route('/click')
def click():
    ad = request.args.get('ad')

    conn = sqlite3.connect('clicks.db')
    c = conn.cursor()

    c.execute("INSERT INTO clicks (ad_name) VALUES (?)", (ad,))
    conn.commit()
    conn.close()

    return "Click recorded ✅"

# Report
@app.route('/report')
def report():
    conn = sqlite3.connect('clicks.db')
    c = conn.cursor()

    c.execute("SELECT ad_name, COUNT(*) FROM clicks GROUP BY ad_name")
    data = c.fetchall()

    conn.close()

    return jsonify(data)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
