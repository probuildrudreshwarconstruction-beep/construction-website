import streamlit as st
from supabase_client import upload_media, add_project, list_projects, delete_project, update_project
import os, base64, json, hashlib

# ---------------- Password Config ----------------
PASS_FILE = "admin_password.json"
def hash_pass(p): return hashlib.sha256(p.encode()).hexdigest()
def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE) as f:
            return json.load(f).get("password")
    elif "admin_password" in st.secrets:
        return hash_pass(st.secrets["admin_password"])
    return None
def set_password(new_pass):
    with open(PASS_FILE, "w") as f:
        json.dump({"password": hash_pass(new_pass)}, f)

# ---------------- Load CSS ----------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style.css")

# ---------------- Page Config ----------------
st.set_page_config(page_title="LNTecc Demo", layout="wide")

# ---------------- Session State ----------------
if "admin_visible" not in st.session_state: st.session_state.admin_visible = False
if "admin_edit_id" not in st.session_state: st.session_state.admin_edit_id = None

# ---------------- Hero ----------------
hero_path = "assets/hero.jpg"
if os.path.exists(hero_path):
    with open(hero_path,"rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <header class="hero">
        <img src="data:image/jpg;base64,{img_b64}" class="hero-img">
    </header>
    """, unsafe_allow_html=True)

# ---------------- About ----------------
st.markdown("""
<section id="about" class="fancy-section">
  <h1 class="section-title">About Us</h1>
  <div class="fancy-content">
    <div class="left">
      <p>Demo content for About section.</p>
      <ul>
        <li>Trusted Construction Solutions since 2015</li>
        <li>Residential & Industrial Projects</li>
        <li>Modern Design with Structural Integrity</li>
      </ul>
    </div>
    <div class="divider"></div>
    <div class="right">
      <p>High-quality construction services tailored to client needs.</p>
      <ul>
        <li>Timely Delivery & Cost-effective Solutions</li>
        <li>Address: Lane No.1, Laxmi Colony, Pune</li>
        <li>Contact: +91 7745065820</li>
      </ul>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)

# ---------------- Services ----------------
st.markdown("""
<section id="services" class="fancy-section">
  <h1 class="section-title">Services</h1>
  <div class="grid-3">
    <div class="feature">• PMC, PMRDA Plan Sanctioning • Architectural Drawing & Design</div>
    <div class="feature">• Structural Steel Designing • 3D Bunglow, Building Designing</div>
    <div class="feature">• Interior DesignLock & key Project • Estimation, Costing & Property</div>
  </div>
</section>
""", unsafe_allow_html=True)

# ---------------- Projects ----------------
st.markdown("<section id='projects' class='fancy-section'><h1 class='section-title'>Projects</h1></section>", unsafe_allow_html=True)

try:
    projects = list_projects() or []
except:
    projects = []

if not projects:
    projects = [
        {"title":"Luxury Villa","description":"Modern villa with eco-friendly materials.","file_url":"https://www.w3schools.com/w3images/fjords.jpg","file_type":"image"},
        {"title":"Commercial Renovation","description":"Revamped commercial complex.","file_url":"https://www.w3schools.com/w3images/lights.jpg","file_type":"image"},
        {"title":"Interior Design","description":"Elegant interior design.","file_url":"https://www.w3schools.com/w3images/mountains.jpg","file_type":"image"}
    ]

cols = st.columns(3)
for idx, pr in enumerate(projects):
    col = cols[idx % 3]
    with col:
        file_type = pr.get("file_type","image").lower()
        url = pr.get("file_url","")
        title = pr.get("title","")
        desc = pr.get("description","")

        st.markdown(f"""
        <div class="feature" onclick="document.getElementById('modal-{idx}').style.display='block'">
            {'<video src="'+url+'" autoplay muted loop></video>' if file_type=='video' else '<img src="'+url+'">'}
            <div class="project-overlay">{title}</div>
        </div>
        <div id="modal-{idx}" class="modal">
            <span class="modal-close" onclick="document.getElementById('modal-{idx}').style.display='none'">&times;</span>
            {'<video src="'+url+'" controls autoplay style="width:100%; max-height:80vh;"></video>' if file_type=='video' else '<img class="modal-content" src="'+url+'">'}
        </div>
        """, unsafe_allow_html=True)

# ---------------- Admin Panel ----------------
st.markdown("<hr>", unsafe_allow_html=True)
if st.button("🔒 Admin Panel"):
    st.session_state.admin_visible = not st.session_state.admin_visible

if st.session_state.admin_visible:
    st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
    pw_input = st.text_input("Enter Admin Password:", type="password")
    stored_pw = get_password()
    if pw_input and stored_pw and hash_pass(pw_input)==stored_pw:
        st.success("Admin Authenticated!")

        # Upload Projects
        uploaded = st.file_uploader("Upload Media", type=["jpg","png","mp4","mov"])
        up_title = st.text_input("Project Title")
        up_desc = st.text_area("Project Description")
        if st.button("Upload Project"):
            if uploaded and up_title and up_desc:
                file_url = upload_media(uploaded)
                file_type = uploaded.type.split("/")[0]
                add_project(up_title, up_desc, file_url, file_type)
                st.success("Project uploaded!")
                st.rerun()

        # Manage Projects
        st.markdown("<h2>Existing Projects</h2>", unsafe_allow_html=True)
        projects = list_projects() or []
        for pr in projects:
            pr_id = pr.get("id")
            pr_title = pr.get("title")
            col1, col2, col3 = st.columns([0.7,0.15,0.15])
            with col1: st.markdown(f"<b>{pr_title}</b>", unsafe_allow_html=True)
            with col2:
                if st.button("Edit", key=f"edit-{pr_id}"):
                    st.session_state.admin_edit_id = pr_id
                    st.session_state.admin_edit_title = pr.get("title")
                    st.session_state.admin_edit_desc = pr.get("description")
            with col3:
                if st.button("Delete", key=f"delete-{pr_id}"):
                    delete_project(pr_id)
                    st.success("Deleted successfully!")
                    st.rerun()

        # Edit Form
        if st.session_state.admin_edit_id:
            st.markdown("<h2>Edit Project</h2>", unsafe_allow_html=True)
            new_title = st.text_input("Title", st.session_state.admin_edit_title)
            new_desc = st.text_area("Description", st.session_state.admin_edit_desc)
            new_file = st.file_uploader("Replace Media (optional)", type=["jpg","png","mp4","mov"])
            if st.button("Save Changes"):
                file_url = None; file_type = None
                if new_file:
                    file_url = upload_media(new_file)
                    file_type = new_file.type.split("/")[0]
                update_project(st.session_state.admin_edit_id,new_title,new_desc,file_url,file_type)
                st.success("Updated!")
                st.session_state.admin_edit_id=None
                st.rerun()
    else:
        if pw_input:
            st.error("Wrong password!")
    st.markdown("</div>", unsafe_allow_html=True)
