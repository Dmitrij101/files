from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__, static_folder="admin")
DB_FILE = "database.json"

# Инициализация БД
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/api/progress")
def progress():
    user_id = request.args.get("user_id")
    db = load_db()
    user = db.get(user_id, {"coins": 0})
    return jsonify({"coins": user.get("coins", 0)})

@app.route("/api/save", methods=["POST"])
def save():
    data = request.json
    db = load_db()
    db[str(data["user_id"])] = data
    save_db(db)
    return jsonify({"status": "ok"})

@app.route("/admin")
def admin():
    return send_from_directory("admin", "dashboard.html")

@app.route("/api/stats")
def stats():
    db = load_db()
    users = list(db.values())
    total_spins = sum(1 for u in users if u.get("last_spin"))
    total_wins = sum(1 for u in users if u.get("win"))
    return jsonify({
        "total_users": len(users),
        "total_spins": total_spins,
        "total_wins": total_wins,
        "top_players": sorted(users, key=lambda x: x.get("coins", 0), reverse=True)[:10]
    })

@app.route("/sounds/<path:filename>")
def sounds(filename):
    return send_from_directory("sounds", filename)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)