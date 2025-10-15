from flask import Flask, render_template, request, jsonify, g, redirect, url_for, session
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = "un_secret_super_securise"  # pour la session admin

# -----------------------------
# Mot de passe admin
# -----------------------------
ADMIN_PASSWORD = "MonSuperMDP123"  # change par ton mot de passe

# -----------------------------
# Base SQLite
# -----------------------------
DATABASE = 'database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# -----------------------------
# Pages publiques
# -----------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/about/")
def about():
    return render_template('about.html')

@app.route("/services/")
def services():
    return render_template('services.html')

@app.route("/projects/")
def projects():
    return render_template('projects.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

# -----------------------------
# API Contact (formulaire)
# -----------------------------
@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"error": "Tous les champs sont requis."}), 400

    db = get_db()
    db.execute(
        "INSERT INTO messages (name, email, message, created_at) VALUES (?, ?, ?, ?)",
        (name, email, message, datetime.utcnow().isoformat())
    )
    db.commit()

    print("Message enregistré :", name, email, message)
    return jsonify({"message": "Merci pour votre message, nous vous répondrons rapidement."})

# -----------------------------
# Page admin login
# -----------------------------
@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_messages'))
        else:
            return render_template('admin_login.html', error="Mot de passe incorrect.")
    return render_template('admin_login.html')

# -----------------------------
# Page admin messages
# -----------------------------
@app.route('/admin/messages/')
def admin_messages():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    db = get_db()
    cursor = db.execute("SELECT id, name, email, message, created_at FROM messages ORDER BY created_at DESC")
    messages = cursor.fetchall()
    return render_template('admin_messages.html', messages=messages)

# -----------------------------
# Supprimer un message
# -----------------------------
@app.route('/admin/messages/delete/<int:message_id>/', methods=['POST'])
def delete_message(message_id):
    if not session.get('admin_logged_in'):
        return jsonify({"success": False, "error": "Non autorisé"}), 403

    db = get_db()
    db.execute("DELETE FROM messages WHERE id = ?", (message_id,))
    db.commit()
    return jsonify({"success": True})

# -----------------------------
# Déconnexion admin
# -----------------------------
@app.route('/admin/logout/')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

# -----------------------------
# Lancement de l'application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
