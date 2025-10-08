import streamlit as st
from streamlit.components.v1 import html
from supabase_client import upload_media, add_project, list_projects, delete_project, update_project
import os
import base64
import json
import hashlib

# -------------------- Password Config --------------------
PASS_FILE = "admin_password.json"

def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE, "r") as f:
            data = json.load(f)
            return data.get("password")
    elif "admin_password" in st.secrets:
        return hash_pass(st.secrets["admin_password"])
    else:
        return None

def set_password(new_pass):
    with open(PASS_FILE, "w") as f:
        json.dump({"password": hash_pass(new_pass)}, f)

# -------------------- Load external CSS --------------------
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style.css")

# -------------------- Page Config --------------------
st.set_page_config(page_title="☬ProBuild Rudreshwar☬", layout="wide")

# -------------------- Hero Section --------------------
hero_image_path = "assets/b1.jpg"
img_b64 = ""
if os.path.exists(hero_image_path):
    with open(hero_image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

# -------------------- Fetch Projects --------------------
try:
    projects = list_projects() or []
except Exception as e:
    st.error(f"Error fetching projects: {e}")
    projects = []

projects_json = json.dumps(projects)

# -------------------- Render Frontend HTML --------------------
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ProBuild Rudreshwar</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
body {{ font-family: 'Arial', sans-serif; margin:0; padding:0; }}
.hero {{ background-image: url('data:image/jpg;base64,{img_b64}'); background-size: cover; background-position: center; height:60vh; display:flex; align-items:center; justify-content:center; color:white; text-align:center; }}
.project-card {{ transition: transform 0.3s ease; }}
.project-card:hover {{ transform: scale(1.05); }}
.service-item {{ background:#f7fafc; padding:1rem; border-radius:0.5rem; box-shadow:0 2px 6px rgba(0,0,0,0.1); }}
</style>
</head>
<body>

<!-- Hero -->
<section class="hero">
  <div>
    <h1 class="text-5xl font-bold mb-4">☬ ProBuild Rudreshwar ☬</h1>
    <p class="text-xl">Crafting Excellence in Construction</p>
  </div>
</section>

<!-- About -->
<section class="py-16 px-4 bg-gray-100">
  <div class="max-w-7xl mx-auto text-center">
    <h2 class="text-3xl font-semibold mb-6">☬ All About Us ☬</h2>
    <p class="text-lg mb-4">ProBuild Rudreshwar Construction & Developers, led by Er. Rushikesh Shivarkar, B.E. Civil — Govt. Contractor & Vastu Expert, has been delivering trusted construction solutions since 2015.</p>
    <p class="text-lg">We specialize in residential and industrial projects, offering modern designs with structural integrity.</p>
  </div>
</section>

<!-- Services -->
<section class="py-16 px-4">
  <div class="max-w-7xl mx-auto text-center">
    <h2 class="text-3xl font-semibold mb-6">☬ Our Services ☬</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div class="service-item">PMC, PMRDA Plan Sanctioning</div>
      <div class="service-item">Architectural Drawing & Design</div>
      <div class="service-item">Structural Steel Designing</div>
      <div class="service-item">3D Bungalow / Building Designing</div>
      <div class="service-item">Interior Design — Lock & Key Projects</div>
      <div class="service-item">Estimation, Costing & Property Evaluation</div>
      <div class="service-item">Pre-Engineering Buildings</div>
      <div class="service-item">Warehouses & Godowns</div>
    </div>
  </div>
</section>

<!-- Projects -->
<section class="py-16 px-4 bg-gray-100">
  <div class="max-w-7xl mx-auto text-center">
    <h2 class="text-3xl font-semibold mb-6">☬ Our Projects ☬</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
      <script>
        const projects = {projects_json};
        projects.forEach(project => {{
          document.write(`
            <div class="project-card bg-white shadow-lg rounded-lg overflow-hidden">
              <img src="${{project.file_url}}" alt="${{project.title}}" class="w-full h-48 object-cover">
              <div class="p-4">
                <h3 class="text-xl font-semibold">${{project.title}}</h3>
                <p class="text-gray-600">${{project.description}}</p>
              </div>
            </div>
          `);
        }});
      </script>
    </div>
  </div>
</section>

<!-- CTA -->
<section class="py-16 px-4 text-center bg-gray-800 text-white">
  <h2 class="text-3xl font-semibold mb-6">Let's Build Together</h2>
  <p class="text-lg mb-4">Contact us today to discuss your next project.</p>
  <a href="https://wa.me/919999999999" target="_blank" class="inline-block bg-green-500 hover:bg-green-600 text-white py-2 px-6 rounded-lg">Contact on WhatsApp</a>
</section>

</body>
</html>
"""

html(html_content, height=1500)

# -------------------- Admin Panel --------------------
if "admin_visible" not in st.session_state:
    st.session_state.admin_visible = False
if "admin_edit_id" not in st.session_state:
    st.session_state.admin_edit_id = None

st.markdown("<hr>", unsafe_allow_html=True)
if st.button("🔒 Toggle Admin Panel"):
    st.session_state.admin_visible = not st.session_state.admin_visible

if st.session_state.admin_visible:
    st.markdown('<div class="admin-panel">', unsafe_allow_html=True)

    password = st.text_input("⚜️ Admin Password", type="password", key="admin_pw", placeholder="Enter admin password")
    stored_password = get_password()

    if stored_password and password and hash_pass(password) == stored_password:
        st.success("Admin authenticated — upload/manage projects below.")

        # Change Password
        with st.expander("🔐 Change Admin Password"):
            old = st.text_input("Old Password", type="password", key="old_pass")
            new = st.text_input("New Password", type="password", key="new_pass")
            confirm = st.text_input("Confirm New Password", type="password", key="confirm_pass")
            if st.button("Change Password"):
                if hash_pass(old) != stored_password:
                    st.error("❌ Old password is incorrect.")
                elif new != confirm:
                    st.warning("⚠️ New passwords do not match.")
                elif len(new) < 5:
                    st.warning("⚠️ Password must be at least 5 characters.")
                else:
                    set_password(new)
                    st.success("✅ Password changed successfully!")
                    st.rerun()

        # Upload New Project
        st.markdown('<h2 class="admin-heading">Upload New Project</h2>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload media (image/video)", type=["jpg","png","mp4","mov"], key="upload_file")
        up_title = st.text_input("Project Title", key="upload_title")
        up_desc = st.text_area("Project Description", key="upload_desc")
        
        if st.button("Submit Project"):
            if uploaded and up_title and up_desc:
                url = upload_media(uploaded)
                file_type = uploaded.type.split("/")[0]
                add_project(up_title, up_desc, url, file_type)
                st.success("Project uploaded successfully!")
                st.rerun()

        # Manage Existing Projects
        st.markdown('<h2 class="admin-heading">Manage Existing Projects</h2>', unsafe_allow_html=True)
        projects = list_projects() or []

        for pr in projects:
            project_id = pr.get("id")
            project_title = pr.get("title", "Untitled")

            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
            with col1:
                st.markdown(f"<div class='project-item'><b>{project_title}</b></div>", unsafe_allow_html=True)
            with col2:
                if st.button("Edit", key=f"edit-{project_id}"):
                    st.session_state.admin_edit_id = project_id
                    st.session_state.admin_edit_title = pr.get("title")
                    st.session_state.admin_edit_desc = pr.get("description")
            with col3:
                if st.button("Delete", key=f"delete-{project_id}"):
                    delete_project(project_id)
                    st.success("Deleted successfully!")
                    st.rerun()

        # Edit Form
        if st.session_state.admin_edit_id:
            st.markdown('<h2 class="admin-heading">Edit Project</h2>', unsafe_allow_html=True)
            new_title = st.text_input("Title", st.session_state.admin_edit_title)
            new_desc = st.text_area("Description", st.session_state.admin_edit_desc)
            new_file = st.file_uploader("Replace Media (optional)", type=["jpg","png","mp4","mov"])
            if st.button("Save Changes"):
                file_url = None
                file_type = None
                if new_file:
                    file_url = upload_media(new_file)
                    file_type = new_file.type.split("/")[0]
                update_project(st.session_state.admin_edit_id, new_title, new_desc, file_url, file_type)
                st.success("Updated!")
                st.session_state.admin_edit_id = None
                st.rerun()
    else:
        if password:
            st.error("❌ Wrong password.")

    st.markdown("</div>", unsafe_allow_html=True)
