""""
Weather Station API
To run: python app.py
Then open http://localhost:5001/api/weather in your browser to see the data (json)
And for the website select the index.html -> open in browser
"""

from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_PATH = "database.db"

# returns all sensor data
@app.route("/api/weather")
def get_weather():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensors ORDER BY date DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(rows)

# returns only the latest reading
@app.route("/api/weather/latest")
def get_latest():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensors ORDER BY date DESC LIMIT 1")
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row is None:
        return jsonify({})
    return jsonify(dict(row))

if __name__ == "__main__":
    print("API running at http://localhost:5001")
    app.run(debug=True, port=5001)