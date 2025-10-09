import streamlit as st
from supabase_client import upload_media, add_project, list_projects, delete_project, update_project
import os, base64, json, hashlib

# -------------------- Password Config --------------------
PASS_FILE = "admin_password.json"

def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE, "r") as f:
            return json.load(f).get("password")
    elif "admin_password" in st.secrets:
        return hash_pass(st.secrets["admin_password"])
    return None

def set_password(new_pass):
    with open(PASS_FILE, "w") as f:
        json.dump({"password": hash_pass(new_pass)}, f)

# -------------------- Base64 Image Helper --------------------
def get_base64_image(image_path):
    """Convert image to Base64 so Streamlit can display it inside HTML."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# -------------------- Load external CSS --------------------
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS file '{file_name}' not found.")

local_css("style.css")  # Load your style.css directly

# -------------------- Page Config --------------------
st.set_page_config(page_title="☬ ProBuild Rudreshwar ☬", layout="wide")

# -------------------- Session State --------------------
if "admin_visible" not in st.session_state:
    st.session_state.admin_visible = False
if "admin_edit_id" not in st.session_state:
    st.session_state.admin_edit_id = None

# -------------------- Secrets --------------------
FORM_URL = st.secrets.get("GOOGLE_FORM_URL", "#")
WHATSAPP = st.secrets.get("WHATSAPP_NUMBER", "")
EMAIL = st.secrets.get("EMAIL", "mailto:probuilder@example.com")
INSTA = st.secrets.get("INSTAGRAM_URL", "https://instagram.com/")
wa_link = f"https://wa.me/{WHATSAPP}" if WHATSAPP else "#"

# -------------------- Header (Logo + Name) --------------------
logo_base64 = get_base64_image("assets/logo.png")

st.markdown(f"""
<header class="top-header">
  <div class="header-left">
    <img src="data:image/png;base64,{logo_base64}" class="company-logo" alt="Logo">
    <h1 class="company-name">ProBuild Rudreshwar Constructions</h1>
  </div>
</header>
""", unsafe_allow_html=True)

# -------------------- About Us --------------------
st.markdown("""
<section class="fancy-section" id="about">
  <h1 class="section-title">☬ All About Us ☬</h1>
  <div class="fancy-content">
    <div class="left">
      <p>ProBuild Rudreshwar Construction & Developers is led by <b>Er. Rushikesh Shivarkar</b>, B.E. Civil — Govt. Contractor & Vastu Expert.</p>
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

# -------------------- Our Services --------------------
st.markdown("""
<section class="fancy-section" id="services">
  <h1 class="section-title">☬ Our Services ☬</h1>
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

# -------------------- Our Projects --------------------
st.markdown("""
<section class="fancy-section" id="projects">
  <h1 class="section-title">☬ Our Projects ☬</h1>
</section>
""", unsafe_allow_html=True)

try:
    projects = list_projects() or []
except Exception as e:
    st.error(f"Error fetching projects: {e}")
    projects = []

if not projects:
    projects = [
        {"title": "Luxury Villa", "description": "Modern villa with eco-friendly materials.", "file_url": "https://www.w3schools.com/w3images/fjords.jpg", "file_type": "image"},
        {"title": "Commercial Renovation", "description": "Revamped commercial complex.", "file_url": "https://www.w3schools.com/w3images/lights.jpg", "file_type": "image"},
        {"title": "Interior Design", "description": "Elegant interior design.", "file_url": "https://www.w3schools.com/w3images/mountains.jpg", "file_type": "image"}
    ]

cols = st.columns(3)
for idx, proj in enumerate(projects):
    col = cols[idx % 3]
    with col:
        file_url = proj.get("file_url", "")
        file_type = (proj.get("file_type") or "").lower()
        title = proj.get("title", "Untitled")
        desc = proj.get("description", "")

        # 🟢 CHANGE HERE — video now shows a thumbnail with play button
        if file_type in ('video', 'mp4', 'mov'):
            media_html = f"""
            <div class="video-thumb" onclick="document.getElementById('modal-{idx}').style.display='block'">
              <video src="{file_url}" muted preload="metadata"></video>
              <div class="play-button">▶</div>
            </div>
            """
        else:
            media_html = f"""
            <div class="image-thumb" onclick="document.getElementById('modal-{idx}').style.display='block'">
              <img src="{file_url}">
            </div>
            """

        st.markdown(f"""
        <div class="project-container">
          {media_html}
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

# -------------------- Address Section --------------------
st.markdown("""
<section class="fancy-section address-section">
  <h1 class="section-title">☬ Address ☬</h1>
  <div class="address-card">
    <p><b>Owner:</b> Er. Rushikesh Shivarkar</p>
    <p><b>Address:</b> Lane No.1, Laxmi Colony, Pune – 411043</p>
    <p><b>Contact:</b> +91 7745065820</p>
  </div>
</section>
""", unsafe_allow_html=True)

# -------------------- Contact Us (CTA) --------------------
st.markdown(f"""
<section class="fancy-section" id="cta">
  <h1 class="section-title">☬ Contact Us ☬</h1>
  <div class="fancy-content">
    <div class="left">
      <a href="{FORM_URL}" target="_blank">
        <button class="cta-button" style="background:var(--gold); color:#000;">
          📄 Enquire via Google Form
        </button>
      </a>
    </div>
    <div class="right">
      <a href="{wa_link}" target="_blank">
        <button class="cta-button" style="background:var(--bronze); color:#fff;">
          💬 WhatsApp
        </button>
      </a>
    </div>
  </div>
  <div class="fancy-content" style="margin-top:40px;">
    <div class="left">
      <a href="{EMAIL}" target="_blank">
        <button class="cta-button" style="background:#1e1e1e; color:var(--gold);">
          ✉️ Email Us
        </button>
      </a>
    </div>
    <div class="right">
      <a href="{INSTA}" target="_blank">
        <button class="cta-button" style="background:linear-gradient(45deg,#f58529,#dd2a7b,#8134af,#515bd4); color:white;">
          📸 Instagram
        </button>
      </a>
    </div>
  </div>
  <p style="text-align:center; margin-top:12px; font-size:0.9rem; opacity:0.8;">© 2025 ProBuild Rudreshwar Constructions</p>
</section>
""", unsafe_allow_html=True)


# -------------------- Admin Panel --------------------
st.markdown("<hr><h2></h2><hr>", unsafe_allow_html=True)

if st.button("🔒"):
    st.session_state.admin_visible = not st.session_state.admin_visible

if st.session_state.admin_visible:
    st.markdown('<div class="admin-panel">', unsafe_allow_html=True)

    password = st.text_input("⚜️", type="password", key="admin_pw", placeholder="Enter admin password")
    stored_password = get_password()

    if stored_password and password and hash_pass(password) == stored_password:
        st.success("Admin authenticated — upload/manage projects below.")

        # Change Password
        with st.expander("🔐 Change Admin Password"):
            old = st.text_input("Old Password", type="password", key="old_pass")
            new = st.text_input("New Password", type="password", key="new_pass")
            confirm = st.text_input("Confirm New Password", type="password", key="confirm_pass")
            change_btn = st.button("Change Password")

            if change_btn:
                if hash_pass(old) != stored_password:
                    st.error("❌ Old password is incorrect.")
                elif new != confirm:
                    st.warning("⚠️ New passwords do not match.")
                elif len(new) < 5:
                    st.warning("⚠️ Password must be at least 5 characters.")
                else:
                    set_password(new)
                    st.success("✅ Password changed successfully! It will apply on next login.")
                    st.rerun()

        # Upload New Project
        st.markdown('<h2 class="admin-heading">Upload New Project</h2>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload media (image/video)", type=["jpg","png","mp4","mov"], key="upload_file")
        up_title = st.text_input("⚜️", key="upload_title", placeholder="Enter Project / Site Name")
        up_desc = st.text_area("⚜️", key="upload_desc", placeholder="Enter Project Description")
        
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
                st.markdown(f"<div class='project-item'><div class='title'><b>{project_title}</b></div></div>", unsafe_allow_html=True)
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

        # Edit Project Form
        if st.session_state.admin_edit_id:
            st.markdown('<h2 class="admin-heading">Edit Project</h2>', unsafe_allow_html=True)
            new_title = st.text_input("Title", st.session_state.admin_edit_title, placeholder="Project / Site Name")
            new_desc = st.text_area("Description", st.session_state.admin_edit_desc, placeholder="Project Description")
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
