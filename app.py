import streamlit as st
from supabase_client import upload_media, add_project, list_projects, delete_project, update_project
import os, base64, json, hashlib, io
from PIL import Image
import tempfile
from moviepy.editor import VideoFileClip

# -------------------- Password Config --------------------
PASS_FILE = "admin_password.json"

def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

def get_password():
    """✅ Reads password from JSON or Streamlit secrets."""
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE, "r") as f:
            data = json.load(f)
            return data.get("password")
    elif "admin_password" in st.secrets:
        return hash_pass(st.secrets["admin_password"])
    return None

def set_password(new_pass):
    with open(PASS_FILE, "w") as f:
        json.dump({"password": hash_pass(new_pass)}, f)

# -------------------- Load external CSS --------------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style.css")

# -------------------- Page Config --------------------
st.set_page_config(page_title="ProBuild Rudreshwar", layout="wide")
st.markdown("<meta name='viewport' content='width=device-width, initial-scale=1.0'>", unsafe_allow_html=True)

# -------------------- Session State --------------------
if "admin_visible" not in st.session_state:
    st.session_state.admin_visible = False
if "admin_edit_id" not in st.session_state:
    st.session_state.admin_edit_id = None

# -------------------- Secrets --------------------
FORM_URL = st.secrets.get("GOOGLE_FORM_URL", "#")
WHATSAPP = st.secrets.get("WHATSAPP_NUMBER", "")
wa_link = f"https://wa.me/{WHATSAPP}" if WHATSAPP else "#"

# -------------------- Image Compression --------------------
def compress_image(file):
    img = Image.open(file)
    img_format = img.format or "JPEG"
    buf = io.BytesIO()
    img.save(buf, format=img_format, optimize=True, quality=75)
    buf.seek(0)
    return buf

# -------------------- Video Compression --------------------
def compress_video(file):
    temp_in = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_in.write(file.read())
    temp_in.flush()
    temp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")

    clip = VideoFileClip(temp_in.name)
    clip.write_videofile(temp_out.name, codec="libx264", bitrate="800k", audio_codec="aac", verbose=False, logger=None)
    clip.close()

    with open(temp_out.name, "rb") as f:
        data = io.BytesIO(f.read())

    temp_in.close()
    temp_out.close()
    return data

# -------------------- Hero Section --------------------
hero_image_path = "assets/b1.jpg"

if os.path.exists(hero_image_path):
    with open(hero_image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <header class="hero">
        <img src="data:image/jpg;base64,{img_b64}" class="hero-img" alt="Hero Banner">
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

# -------------------- Services --------------------
st.markdown("""
<section class="fancy-section" id="services">
  <h1 class="section-title">Our Services</h1>
  <div class="fancy-content">
    <div class="left">
      <ul>
        <li>PMC, PMRDA Plan Sanctioning</li>
        <li>Architectural Drawing & Design</li>
        <li>Structural Steel Designing</li>
        <li>3D Bungalow / Building Designing</li>
      </ul>
    </div>
    <div class="divider"></div>
    <div class="right">
      <ul>
        <li>Interior Design — Lock & Key Projects</li>
        <li>Estimation, Costing & Property Evaluation</li>
        <li>Pre-Engineering Buildings</li>
        <li>Warehouses & Godowns</li>
      </ul>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)

# -------------------- Projects Section --------------------
st.markdown("<section class='fancy-section' id='projects'><h1 class='section-title'>Our Projects</h1></section>", unsafe_allow_html=True)

@st.cache_data
def cached_projects():
    try:
        return list_projects() or []
    except Exception as e:
        st.error(f"Error fetching projects: {e}")
        return []

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
          {'<video src="'+file_url+'" autoplay muted loop playsinline></video>' if file_type in ('video','mp4','mov') else '<img src="'+file_url+'">'}
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

# -------------------- Marathi CTA --------------------
st.markdown(f"""
<section class="fancy-section" id="cta">
  <h1 class="section-title">तर मग काय वाट बघता? संपर्क करा! 🚀</h1>
  <div class="fancy-content">
    <div class="left">
      <div class="fancy-bullet-wrapper">
        <span class="fancy-bullet"></span>
        <a href="{FORM_URL}" target="_blank">
          <button class="cta-button forms-btn">📄 Enquire via Forms</button>
        </a>
      </div>
    </div>
    <div class="divider"></div>
    <div class="right">
      <div class="fancy-bullet-wrapper">
        <span class="fancy-bullet"></span>
        <a href="{wa_link}" target="_blank">
          <button class="cta-button whatsapp-btn">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" style="height:22px;vertical-align:middle;margin-right:8px;">
            Contact on WhatsApp
          </button>
        </a>
      </div>
    </div>
  </div>
  <p style="text-align:center;margin-top:12px;font-size:0.9rem;opacity:0.8;">© 2025 ProBuild Rudreshwar Constructions</p>
</section>
""", unsafe_allow_html=True)

# -------------------- Admin Panel --------------------
st.markdown("<hr>", unsafe_allow_html=True)
if st.button("🔒"):
    st.session_state.admin_visible = not st.session_state.admin_visible

if st.session_state.admin_visible:
    st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
    password = st.text_input("⚜️", type="password", key="admin_pw", placeholder="Enter admin password")
    stored_password = get_password()

    if stored_password and password and hash_pass(password) == stored_password:
        st.success("Admin authenticated — upload/manage projects below.")
        with st.expander("🔐 Change Admin Password"):
            old = st.text_input("Old Password", type="password")
            new = st.text_input("New Password", type="password")
            confirm = st.text_input("Confirm New Password", type="password")
            if st.button("Change Password"):
                if hash_pass(old) != stored_password:
                    st.error("❌ Old password incorrect.")
                elif new != confirm:
                    st.warning("⚠️ New passwords do not match.")
                elif len(new) < 5:
                    st.warning("⚠️ Password too short.")
                else:
                    set_password(new)
                    st.success("✅ Password updated! Restart app.")
                    st.rerun()

        # ===== Upload Project =====
        st.markdown('<h2 class="admin-heading">Upload New Project</h2>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload media (image/video)", type=["jpg","png","mp4","mov"])
        up_title = st.text_input("⚜️ Project Title")
        up_desc = st.text_area("⚜️ Project Description")

        if st.button("Submit Project"):
            if uploaded and up_title and up_desc:
                ext = uploaded.type.split("/")[0]
                if ext == "image":
                    compressed_file = compress_image(uploaded)
                elif ext == "video":
                    compressed_file = compress_video(uploaded)
                else:
                    compressed_file = uploaded
                url = upload_media(compressed_file)
                add_project(up_title, up_desc, url, ext)
                st.success("✅ Project uploaded successfully!")
                st.rerun()

        # ===== Manage Projects =====
        st.markdown('<h2 class="admin-heading">Manage Existing Projects</h2>', unsafe_allow_html=True)
        for pr in projects:
            pid = pr.get("id")
            title = pr.get("title", "Untitled")
            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
            with col1:
                st.markdown(f"<div class='project-item'><div class='title'><b>{title}</b></div></div>", unsafe_allow_html=True)
            with col2:
                if st.button("Edit", key=f"edit-{pid}"):
                    st.session_state.admin_edit_id = pid
                    st.session_state.admin_edit_title = pr.get("title")
                    st.session_state.admin_edit_desc = pr.get("description")
            with col3:
                if st.button("Delete", key=f"delete-{pid}"):
                    delete_project(pid)
                    st.success("Deleted successfully!")
                    st.rerun()

        # ===== Edit Form =====
        if st.session_state.admin_edit_id:
            st.markdown('<h2 class="admin-heading">Edit Project</h2>', unsafe_allow_html=True)
            new_title = st.text_input("Title", st.session_state.admin_edit_title)
            new_desc = st.text_area("Description", st.session_state.admin_edit_desc)
            new_file = st.file_uploader("Replace Media (optional)", type=["jpg","png","mp4","mov"])
            if st.button("Save Changes"):
                file_url, file_type = None, None
                if new_file:
                    file_type = new_file.type.split("/")[0]
                    compressed = compress_image(new_file) if file_type == "image" else compress_video(new_file)
                    file_url = upload_media(compressed)
                update_project(st.session_state.admin_edit_id, new_title, new_desc, file_url, file_type)
                st.success("✅ Project updated!")
                st.session_state.admin_edit_id = None
                st.rerun()
    else:
        if password:
            st.error("❌ Wrong password.")
    st.markdown("</div>", unsafe_allow_html=True)
