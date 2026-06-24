from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "database.db"

# ---------------- DB INIT ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person TEXT,
            task TEXT,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add_reminder():
    data = request.json

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO reminders (person, task, time) VALUES (?, ?, ?)",
        (data["person"], data["task"], data["time"])
    )
    conn.commit()
    conn.close()

    # 👉 WhatsApp hook (optional future upgrade)
    # send_whatsapp(data["person"], data["task"], data["time"])

    return jsonify({"status": "success"})


@app.route("/get")
def get_reminders():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM reminders")
    rows = c.fetchall()
    conn.close()

    reminders = []
    for r in rows:
        reminders.append({
            "id": r[0],
            "person": r[1],
            "task": r[2],
            "time": r[3]
        })
    return jsonify(reminders)


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM reminders WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"})


if __name__ == "__main__":
    app.run(debug=True)