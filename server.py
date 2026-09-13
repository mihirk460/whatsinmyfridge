import os
import sqlite3
from flask import Flask, jsonify, request, send_from_directory

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "fridge.db")

app = Flask(__name__, static_folder=os.path.join(HERE, "static"))


def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


with db() as conn:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS items ("
        "id INTEGER PRIMARY KEY, name TEXT NOT NULL, "
        "expiry TEXT NOT NULL, percent INTEGER NOT NULL DEFAULT 100)"
    )


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/items")
def list_items():
    with db() as conn:
        rows = conn.execute("SELECT * FROM items ORDER BY expiry").fetchall()
    return jsonify([dict(r) for r in rows])


@app.post("/api/items")
def add_item():
    data = request.get_json()
    name, expiry = data.get("name", "").strip(), data.get("expiry", "")
    if not name or not expiry:
        return jsonify(error="name and expiry required"), 400
    with db() as conn:
        cur = conn.execute("INSERT INTO items (name, expiry) VALUES (?, ?)", (name, expiry))
    return jsonify(id=cur.lastrowid), 201


@app.patch("/api/items/<int:item_id>")
def update_item(item_id):
    percent = int(request.get_json().get("percent", 100))
    with db() as conn:
        conn.execute("UPDATE items SET percent = ? WHERE id = ?", (percent, item_id))
    return "", 204


@app.delete("/api/items/<int:item_id>")
def delete_item(item_id):
    with db() as conn:
        conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
