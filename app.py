from flask import Flask, request, jsonify, render_template, send_from_directory
from supabase_client import upload_media, add_project, list_projects, delete_project, update_project
import hashlib, json, os

app = Flask(__name__)

# -------------------- Password Config --------------------
PASS_FILE = "admin_password.json"

def hash_pass(p): return hashlib.sha256(p.encode()).hexdigest()

def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE, "r") as f:
            data = json.load(f)
            return data.get("password")
    return None

def set_password(new_pass):
    with open(PASS_FILE, "w") as f:
        json.dump({"password": hash_pass(new_pass)}, f)

# -------------------- Routes --------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/projects")
def get_projects():
    projects = list_projects() or []
    return jsonify(projects)

@app.route("/api/upload", methods=["POST"])
def upload_project():
    password = request.form.get("password")
    if hash_pass(password) != get_password():
        return jsonify({"success": False, "error": "Invalid admin password"}), 403
    title = request.form.get("title")
    desc = request.form.get("description")
    file = request.files.get("file")
    if file and title and desc:
        url = upload_media(file)
        file_type = file.content_type.split("/")[0]
        add_project(title, desc, url, file_type)
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Missing fields"}), 400

@app.route("/api/delete/<project_id>", methods=["POST"])
def delete(project_id):
    password = request.form.get("password")
    if hash_pass(password) != get_password():
        return jsonify({"success": False, "error": "Invalid admin password"}), 403
    delete_project(project_id)
    return jsonify({"success": True})

@app.route("/api/update/<project_id>", methods=["POST"])
def update(project_id):
    password = request.form.get("password")
    if hash_pass(password) != get_password():
        return jsonify({"success": False, "error": "Invalid admin password"}), 403
    title = request.form.get("title")
    desc = request.form.get("description")
    file = request.files.get("file")
    file_url = None
    file_type = None
    if file:
        file_url = upload_media(file)
        file_type = file.content_type.split("/")[0]
    update_project(project_id, title, desc, file_url, file_type)
    return jsonify({"success": True})

@app.route("/api/change-password", methods=["POST"])
def change_password():
    old = request.form.get("old")
    new = request.form.get("new")
    confirm = request.form.get("confirm")
    if hash_pass(old) != get_password():
        return jsonify({"success": False, "error": "Old password incorrect"}), 403
    if new != confirm:
        return jsonify({"success": False, "error": "New passwords do not match"}), 400
    if len(new) < 5:
        return jsonify({"success": False, "error": "Password too short"}), 400
    set_password(new)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
