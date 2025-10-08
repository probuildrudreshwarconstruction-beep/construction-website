import streamlit as st
import os, uuid, hashlib, json
from pathlib import Path

# ---------------- CONFIG ----------------
UPLOAD_FOLDER = "uploads"
PROJECTS_FILE = "projects.json"
ADMIN_PASS_FILE = "admin_pass.json"
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)

# ---------------- HELPERS ----------------
def hash_pass(pw): return hashlib.sha256(pw.encode()).hexdigest()
def get_admin_pass():
    if os.path.exists(ADMIN_PASS_FILE):
        return json.load(open(ADMIN_PASS_FILE)).get("password")
    return hash_pass("admin123")
def set_admin_pass(pw): json.dump({"password": hash_pass(pw)}, open(ADMIN_PASS_FILE,"w"))
def load_projects():
    if os.path.exists(PROJECTS_FILE):
        return json.load(open(PROJECTS_FILE))
    return []
def save_projects(projs): json.dump(projs, open(PROJECTS_FILE,"w"))
def add_project(title, desc, filename, file_type):
    projects = load_projects()
    projects.append({"id": str(uuid.uuid4()), "title": title, "description": desc, "filename": filename, "type": file_type})
    save_projects(projects)
def delete_project(pid):
    projects = load_projects()
    projects = [p for p in projects if p["id"]!=pid]
    save_projects(projects)

# ---------------- STYLES ----------------
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ---------------- HEADER ----------------
st.markdown("""
<div style="display:flex;align-items:center;gap:12px;margin-bottom:24px;">
    <div style="width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#00e0ff,#6b5cff);
                display:flex;justify-content:center;align-items:center;color:#fff;font-weight:700;">L</div>
    <h1 style="color:#D4AF37;">MyCompany</h1>
</div>
""", unsafe_allow_html=True)

# ---------------- ADMIN LOGIN ----------------
if not st.session_state.admin_logged_in:
    pw = st.text_input("Admin Password", type="password")
    if st.button("Login"):
        if hash_pass(pw) == get_admin_pass():
            st.session_state.admin_logged_in = True
            st.success("Admin authenticated.")
        else: st.error("Wrong password!")

# ---------------- ADMIN PANEL ----------------
if st.session_state.admin_logged_in:
    st.markdown("<h2>Admin Panel</h2>", unsafe_allow_html=True)
    with st.form("upload_form", clear_on_submit=True):
        title = st.text_input("Title")
        desc = st.text_input("Description")
        file = st.file_uploader("Upload image/video", type=["png","jpg","jpeg","mp4"])
        submit = st.form_submit_button("Upload")
        if submit and title and desc and file:
            path = os.path.join(UPLOAD_FOLDER, file.name)
            with open(path,"wb") as f: f.write(file.getbuffer())
            ftype = file.type.split("/")[0]
            add_project(title, desc, file.name, ftype)
            st.success("Project uploaded!")

    # Change Password
    with st.form("pw_form", clear_on_submit=True):
        old = st.text_input("Old Password", type="password")
        new = st.text_input("New Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Change Password")
        if submit:
            if hash_pass(old)!=get_admin_pass():
                st.error("Old password incorrect!")
            elif new!=confirm:
                st.error("Passwords do not match!")
            else:
                set_admin_pass(new)
                st.success("Password changed!")

    # Existing projects
    st.markdown("<h3>Existing Projects</h3>", unsafe_allow_html=True)
    projects = load_projects()
    for p in projects:
        cols = st.columns([4,1])
        cols[0].markdown(f"**{p['title']}**: {p['description']}")
        if cols[1].button("Delete", key=p["id"]):
            delete_project(p["id"])
            st.experimental_rerun()

# ---------------- SECTIONS ----------------
st.markdown("<hr>")

st.markdown("<h1>About Us</h1><p>Demo About content.</p>", unsafe_allow_html=True)
st.markdown("<h1>Services</h1>", unsafe_allow_html=True)
st.markdown("""
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;">
<div style="padding:12px;background:rgba(255,255,255,0.02);border-radius:12px;text-align:center;">Service 1</div>
<div style="padding:12px;background:rgba(255,255,255,0.02);border-radius:12px;text-align:center;">Service 2</div>
<div style="padding:12px;background:rgba(255,255,255,0.02);border-radius:12px;text-align:center;">Service 3</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<h1>Projects</h1>", unsafe_allow_html=True)
projects = load_projects()
for p in projects:
    st.markdown(f"**{p['title']}**: {p['description']}")
    if p["type"]=="image":
        st.image(os.path.join(UPLOAD_FOLDER,p["filename"]))
    else:
        st.video(os.path.join(UPLOAD_FOLDER,p["filename"]))

st.markdown("<h1>Contact</h1>", unsafe_allow_html=True)
st.markdown("""
<a href='https://wa.me/1234567890' style='margin-right:12px;padding:12px;border-radius:8px;background:#2a7f62;color:#fff;text-decoration:none;'>WhatsApp</a>
<a href='https://www.instagram.com/' style='margin-right:12px;padding:12px;border-radius:8px;background:#E1306C;color:#fff;text-decoration:none;'>Instagram</a>
<a href='https://forms.gle/' style='margin-right:12px;padding:12px;border-radius:8px;background:#87CEFA;color:#000;text-decoration:none;'>Google Form</a>
""", unsafe_allow_html=True)
