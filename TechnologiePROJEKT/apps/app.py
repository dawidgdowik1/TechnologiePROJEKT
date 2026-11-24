import socket
import pymysql
from flask import Flask, request, redirect, render_template_string, jsonify

app = Flask(__name__)

DB = {
    "host": "voting-db.cv6egisu2rke.us-east-1.rds.amazonaws.com",
    "user": "admin",
    "password": "HasloProjekt123!",
    "database": "voting_db",
    "port": 3306,
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}


def get_conn():
    return pymysql.connect(**DB)


def init_db():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS candidates (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    club VARCHAR(100),
                    votes INT DEFAULT 0
                )"""
            )
            cur.execute("SELECT COUNT(*) AS cnt FROM candidates")
            if cur.fetchone()["cnt"] == 0:
                cur.executemany(
                    "INSERT INTO candidates (name, club, votes) VALUES (%s,%s,0)",
                    [
                        ("Robert Lewandowski", "Chicago Fire"),
                        ("Piotr Zieliñski", "Inter Mediolan"),
                        ("Jakub Kiwior", "FC Porto"),
                        ("Nicola Zalewski", "Atalanta"),
                    ],
                )
    finally:
        conn.close()


HTML = """<!DOCTYPE html><html lang="pl"><head><meta charset="UTF-8">
<title>Zawodnik Meczu</title><style>
body{font-family:Arial,sans-serif;max-width:700px;margin:40px auto;background:#f4f6f9}
.card{background:#fff;padding:24px;border-radius:10px;box-shadow:0 2px 8px #0001}
.badge{background:#e8f0fe;color:#1967d2;padding:8px 12px;border-radius:6px;margin-bottom:20px}
.row{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid #eee}
button{background:#1967d2;color:#fff;border:none;padding:8px 16px;border-radius:5px;cursor:pointer;font-weight:bold}
.votes{font-size:18px;font-weight:bold;margin-right:15px}
</style></head><body><div class="card">
<h1>G³osowanie: Zawodnik Meczu</h1>
<div class="badge">Obs³uguje instancja EC2: <strong>{{ host }}</strong></div>
{% for c in candidates %}<div class="row">
<div><strong>{{ c.name }}</strong><br><small>{{ c.club }}</small></div>
<div><span class="votes">{{ c.votes }} g³osów</span>
<form action="/vote" method="post" style="display:inline">
<input type="hidden" name="candidate_id" value="{{ c.id }}">
<button type="submit">G³osuj</button></form></div></div>{% endfor %}
</div></body></html>"""


@app.route("/")
def index():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM candidates ORDER BY id")
            rows = cur.fetchall()
    finally:
        conn.close()
    return render_template_string(HTML, candidates=rows, host=socket.gethostname())


@app.route("/vote", methods=["POST"])
def vote():
    data = request.get_json(silent=True) or {}
    cid = request.form.get("candidate_id") or data.get("candidate_id") or 1
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE candidates SET votes = votes + 1 WHERE id = %s", (cid,))
    finally:
        conn.close()
    if request.is_json or request.headers.get("X-Load-Test"):
        return jsonify({"status": "ok"}), 200
    return redirect("/")


@app.route("/health")
def health():
    return "OK", 200


