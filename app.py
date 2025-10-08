import streamlit as st
import os, base64, json, hashlib
from io import BytesIO
from supabase_client import upload_media, add_project, list_projects, delete_project, update_project
from PIL import Image
import subprocess

# -------------------- Config --------------------
PASS_FILE = "admin_password.json"
st.set_page_config(page_title="ProBuild Rudreshwar", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<meta name="viewport" content="width=device-width, initial-scale=1">""", unsafe_allow_html=True)

# -------------------- Password Hashing --------------------
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

# -------------------- CSS --------------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style.css")

# -------------------- Caching --------------------
@st.cache_data(show_spinner=False)
def cached_projects():
    return list_projects() or []

@st.cache_data(show_spinner=False)
def get_hero_image_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# -------------------- Media Compression --------------------
def compress_media(file):
    filename = file.name
    filetype = file.type

    # Image compression
    if filetype.startswith("image"):
        img = Image.open(file)
        img = img.convert("RGB")
        max_w = 1280
        if img.width > max_w:
            ratio = max_w / img.width
            new_size = (max_w, int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=80, optimize=True)
        buf.seek(0)
        buf.name = filename
        return buf

    # Video compression (basic)
    if filetype.startswith("video"):
        temp_in = f"temp_in_{filename}"
        temp_out = f"temp_out_{filename}"
        with open(temp_in, "wb") as f:
            f.write(file.getbuffer())
        try:
            subprocess.run([
                "ffmpeg", "-i", temp_in,
                "-b:v", "1M", "-vf", "scale=1280:-2",
                "-c:a", "aac", "-y", temp_out
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            with open(temp_out, "rb") as f:
                data = f.read()
            os.remove(temp_in); os.remove(temp_out)
            return BytesIO(data)
        except Exception:
            return file

    return file

# -------------------- Session --------------------
if "admin_visible" not in st.session_state: st.session_state.admin_visible = False
if "admin_edit_id" not in st.session_state: st.session_state.admin_edit_id = None

FORM_URL = st.secrets.get("GOOGLE_FORM_URL", "#")
WHATSAPP = st.secrets.get("WHATSAPP_NUMBER", "")
wa_link = f"https://wa.me/{WHATSAPP}" if WHATSAPP else "#"

# -------------------- Hero Section --------------------
hero_image_path = "assets/b1.jpg"
if os.path.exists(hero_image_path):
    img_b64 = get_hero_image_b64(hero_image_path)
    st.markdown(f"""
    <header class="hero w3-display-container">
        <img src="data:image/jpg;base64,{img_b64}" class="hero-img" loading="lazy">
    </header>
    """, unsafe_allow_html=True)

# -------------------- About Us --------------------
st.markdown("""
<section class="fancy-section" id="about">
  <h1 class="section-title">All About Us</h1>
  <div class="fancy-content">
    <div class="left">
      <p>ProBuild Rudreshwar Construction & Developers is led by Er. Rushikesh Shivarkar, B.E. Civil — Govt. Contractor & Vastu Expert.</p>
      <ul>
        <li>Trusted Construction Solutions since 2015</li>
        <li>Residential & Industrial Projects</li>
        <li>Modern Design with Structural Integrity</li>
      </ul>
    </div>
    <div class="divider"></div>
    <div class="right">
      <p>We specialize in delivering timely and high-quality construction services tailored to client needs.</p>
      <ul>
        <li>Timely Delivery & Cost-effective Solutions</li>
        <li>Address: Lane No.1, Laxmi Colony, Pune</li>
        <li>Contact: +91 7745065820</li>
      </ul>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)

# -------------------- Projects --------------------
st.markdown("""<section class="fancy-section" id="projects"><h1 class="section-title">Our Projects</h1></section>""", unsafe_allow_html=True)
projects = cached_projects()
if not projects:
    projects = [
        {"title":"Luxury Villa","description":"Modern villa with eco-friendly materials.","file_url":"https://www.w3schools.com/w3images/fjords.jpg","file_type":"image"},
        {"title":"Commercial Renovation","description":"Revamped commercial complex.","file_url":"https://www.w3schools.com/w3images/lights.jpg","file_type":"image"},
        {"title":"Interior Design","description":"Elegant interior design.","file_url":"https://www.w3schools.com/w3images/mountains.jpg","file_type":"image"}
    ]

cols = st.columns(3)
for idx, proj in enumerate(projects):
    col = cols[idx % 3]
    with col:
        file_url = proj.get("file_url", "")
        file_type = (proj.get("file_type") or "").lower()
        title = proj.get("title", "Untitled")
        desc = proj.get("description", "")

        st.markdown(f"""
        <div class="project-container" onclick="document.getElementById('modal-{idx}').style.display='block'">
          {'<video src="'+file_url+'" autoplay muted loop playsinline></video>' if file_type in ('video','mp4','mov') else '<img src="'+file_url+'" loading="lazy">'}
          <div class="project-overlay">{title}</div>
        </div>
        <div id="modal-{idx}" class="modal">
          <span class="modal-close" onclick="document.getElementById('modal-{idx}').style.display='none'">&times;</span>
          {'<video src="'+file_url+'" controls autoplay style="width:100%; max-height:80vh;"></video>' if file_type in ('video','mp4','mov') else '<img class="modal-content" src="'+file_url+'">'}
        </div>
        """, unsafe_allow_html=True)

        with st.expander("View More"):
            formatted_desc = "".join([f"<li>{line.strip()}</li>" for line in desc.split("\n") if line.strip()])
            st.markdown(f"<ul class='viewmore-list'>{formatted_desc}</ul>", unsafe_allow_html=True)

# -------------------- CTA Marathi --------------------
st.markdown(f"""
<section class="fancy-section" id="cta">
  <h1 class="section-title">तर मग काय वाट बघता? संपर्क करा! 🚀</h1>
  <div class="fancy-content">
    <div class="left">
      <div class="fancy-bullet-wrapper">
        <span class="fancy-bullet"></span>
        <a href="{FORM_URL}" target="_blank">
          <button class="cta-button" style="background:var(--gold); color:#000;">
            📄 Enquire via Forms
          </button>
        </a>
      </div>
    </div>
    <div class="divider"></div>
    <div class="right">
      <div class="fancy-bullet-wrapper">
        <span class="fancy-bullet"></span>
        <a href="{wa_link}" target="_blank">
          <button class="cta-button" style="background:var(--bronze); color:#fff;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" 
                 style="height:22px; vertical-align:middle; margin-right:8px;">
            Contact on WhatsApp
          </button>
        </a>
      </div>
    </div>
  </div>
  <p style="text-align:center; margin-top:12px; font-size:0.9rem; opacity:0.8;">© 2025 ProBuild Rudreshwar Constructions</p>
</section>
""", unsafe_allow_html=True)

# -------------------- Admin Panel --------------------
if st.button("🔒"): st.session_state.admin_visible = not st.session_state.admin_visible
if st.session_state.admin_visible:
    st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
    password = st.text_input("⚜️", type="password", key="admin_pw")
    stored_password = get_password()

    if stored_password and password and hash_pass(password) == stored_password:
        st.success("Admin authenticated — upload/manage projects below.")
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
                    set_password(new); st.success("✅ Password changed successfully!"); st.rerun()

        uploaded = st.file_uploader("Upload media", type=["jpg","png","mp4","mov"], key="upload_file")
        up_title = st.text_input("⚜️ Project Title", key="upload_title")
        up_desc = st.text_area("⚜️ Project Description", key="upload_desc")

        if st.button("Submit Project"):
            if uploaded and up_title and up_desc:
                compressed = compress_media(uploaded)
                url = upload_media(compressed)
                file_type = uploaded.type.split("/")[0]
                add_project(up_title, up_desc, url, file_type)
                st.success("Project uploaded successfully!")
                st.cache_data.clear()
                st.rerun()

        st.markdown('<h2 class="admin-heading">Manage Existing Projects</h2>', unsafe_allow_html=True)
        for pr in cached_projects():
            project_id = pr.get("id")
            title = pr.get("title", "Untitled")
            col1, col2, col3 = st.columns([0.7,0.15,0.15])
            with col1: st.markdown(f"<div class='project-item'><b>{title}</b></div>", unsafe_allow_html=True)
            with col2:
                if st.button("Edit", key=f"edit-{project_id}"):
                    st.session_state.admin_edit_id = project_id
                    st.session_state.admin_edit_title = pr.get("title")
                    st.session_state.admin_edit_desc = pr.get("description")
            with col3:
                if st.button("Delete", key=f"delete-{project_id}"):
                    delete_project(project_id)
                    st.success("Deleted successfully!")
                    st.cache_data.clear()
                    st.rerun()

        if st.session_state.admin_edit_id:
            new_title = st.text_input("Title", st.session_state.admin_edit_title)
            new_desc = st.text_area("Description", st.session_state.admin_edit_desc)
            new_file = st.file_uploader("Replace Media (optional)", type=["jpg","png","mp4","mov"])
            if st.button("Save Changes"):
                file_url = None; file_type = None
                if new_file:
                    compressed = compress_media(new_file)
                    file_url = upload_media(compressed)
                    file_type = new_file.type.split("/")[0]
                update_project(st.session_state.admin_edit_id, new_title, new_desc, file_url, file_type)
                st.success("Updated!")
                st.session_state.admin_edit_id = None
                st.cache_data.clear()
                st.rerun()

    else:
        if password: st.error("❌ Wrong password.")
    st.markdown("</div>", unsafe_allow_html=True)
