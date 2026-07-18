""""
Weather Station API
To run: python app.py
Then open http://localhost:5001/api/weather in your browser to see the data (json)
And for the website select the index.html -> open in browser
"""

from flask import Flask, jsonify, render_template
from flask_cors import CORS
import sqlite3
import configparser

app = Flask(__name__)
CORS(app)
config = configparser.ConfigParser()
config.read("config.ini")



DB_PATH = config["broker.config"]["database_name"]

# index page
@app.route("/")
def index():
    #return "index"
    return render_template("index.html")


# returns all sensor data
@app.route("/api/weather")
def get_weather():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM "211097D05BECC882" ORDER BY date DESC""")
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
    cursor.execute("""SELECT * FROM "211097D05BECC882" ORDER BY date DESC LIMIT 1""")
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row is None:
        return jsonify({})
    return jsonify(dict(row))


if __name__ == "__main__":
    print("API running at http://localhost:5001")
    app.run(debug=True,host="0.0.0.0", port=5001)