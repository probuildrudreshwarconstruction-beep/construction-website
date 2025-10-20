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
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# -------------------- Load external CSS --------------------
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS file '{file_name}' not found.")

local_css("style.css")

# -------------------- Hide Streamlit Default Header & Footer --------------------
st.markdown("""
<style>
header[data-testid="stHeader"] {display: none !important;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
main.block-container {padding-top: 0rem;}
</style>
""", unsafe_allow_html=True)

# -------------------- Page Config --------------------
st.set_page_config(page_title="ProBuild Rudreshwar", layout="wide")

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
INSTA2 = st.secrets.get("INSTAGRAM2_URL", "https://instagram.com/")
RESPONSES_LINK = st.secrets.get("RESPONSES_LINK", "#")
wa_link = f"https://wa.me/{WHATSAPP.replace('+','').replace(' ','')}" if WHATSAPP else "#"

# -------------------- Header --------------------
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
  <h1 class="section-title">All About Us</h1>
  <div class="fancy-content">
    <div class="left">
      <p>ProBuild Rudreshwar Construction & Developers is led by <b>Er. Rushikesh Shivarkar</b>, B.E. Civil — Govt. Contractor & Vastu Expert.</p>
      <ul>
        <li>Trusted Construction Solutions since 2015</li>
        <li>Residential & Industrial Projects</li>
        <li>Modern Design with Structural Integrity</li>
        <li>Timely Delivery & Cost-effective Solutions</li>

      
  </div>
</section>
""", unsafe_allow_html=True)

# -------------------- Our Services --------------------
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
        <li>Interior DesignLock & key Project</li>
        <li>Estimation, Costing & Property Evaluation</li>
        <li>Pre-Engineering Buildings</li>
        <li>Conventional Industrial Building</li>
        <li>Warehouses & Godowns</li>
      </ul>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)

# -------------------- Projects Section --------------------
st.markdown("<h1 class='section-title' style='text-align:center;'>Our Projects</h1>", unsafe_allow_html=True)

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
for idx, proj in enumerate(projects):
    col = cols[idx % 3]
    with col:
        title = proj.get("title","Untitled")
        desc = proj.get("description","")
        file_url = proj.get("file_url","")
        file_type = (proj.get("file_type") or "").lower()

        container_html = f"""
        <div style="
            width:100%;
            max-width:350px;
            height:220px;
            margin:10px auto;
            border:3px solid #D4AF37;
            border-radius:12px;
            display:flex;
            justify-content:center;
            align-items:center;
            background-color:#000;
            overflow:hidden;
        ">
            {f'<video src="{file_url}" controls style="width:100%; height:100%; object-fit:contain;"></video>'
              if file_type in ("video","mp4","mov") else f'<img src="{file_url}" style="width:100%; height:100%; object-fit:contain;">'}
        </div>
        <div style="text-align:center; font-weight:bold; margin-top:6px; color:#8B4513;">{title}</div>
        """
        st.markdown(container_html, unsafe_allow_html=True)

        
# -------------------- Address --------------------
# -------------------- Team Members Section --------------------
# -------------------- Team & Address Section --------------------
st.markdown("""
<section class="team-section">
  <h1 class="section-title">Our Team</h1>

  <div class="team-member">
    <h2>Rushikesh Shivarkar</h2>
    <p>Founder & Managing Director — A qualified Civil Engineer with hands-on experience in residential and industrial construction. He leads the company with a focus on quality, technical precision, and client satisfaction.</p>
  </div>

  <div class="team-member">
    <h2>Rampal Prajapati</h2>
    <p>Project Manager / Site Supervisor — Oversees daily site operations, ensures timely completion, and maintains safety and quality standards on every project.</p>
  </div>

  <div class="team-member">
    <h2>Rohan Kathare</h2>
    <p>Design & Planning Engineer — Responsible for architectural and structural design, project planning, and innovative layout solutions tailored to client needs.</p>
  </div>

  <div class="team-member">
    <h2>Tanaji Damgude</h2>
    <p>Fabrication & Shed Expert — Specialist in industrial, PEB, and conventional steel shed construction, ensuring strength, precision, and durability in every structure.</p>
  </div>

  <div class="team-member">
    <h2>Skilled Labour & On-Site Team</h2>
    <p>Our hardworking labour force forms the backbone of every project — ensuring fine craftsmanship and timely delivery.</p>
  </div>

  <div class="team-member">
    <h2>🏢 Office Address</h2>
    <p><br>
    Address: Lane No.1, Laxmi Colony, Pune – 411043<br>
    </p>
  </div>
</section>
""", unsafe_allow_html=True)

# -------------------- Contact --------------------
# -------------------- Contact --------------------
whatsapp_logo = "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg"
email_logo = "https://upload.wikimedia.org/wikipedia/commons/4/4e/Mail_%28iOS%29.svg"
insta_logo = "https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg"

st.markdown(f"""
<section class="fancy-section" id="cta">
  <h1 class="section-title">Contact Us</h1>

  <div class="fancy-content">
    <div class="left">
      <a href="{FORM_URL}" target="_blank">
        <button class="cta-button" style="background:var(--gold); color:#000;">
          📄 Enquiry Form
        </button>
      </a>
    </div>
    <div class="right">
      <a href="{wa_link}" target="_blank">
        <button class="cta-button" style="background:#25D366; color:#075E54; font-weight:bold; border:none;">
          <img src="{whatsapp_logo}" style="width:20px; height:20px; vertical-align:middle; margin-right:6px;">
          WhatsApp
        </button>
      </a>
    </div>
  </div>

  <div class="fancy-content" style="margin-top:40px;">
    <div class="left">
      <a href="{EMAIL}" target="_blank">
        <button class="cta-button" style="background:#1e1e1e; color:var(--gold);">
          <img src="{email_logo}" style="width:20px; height:20px; vertical-align:middle; margin-right:6px;">
          Email Us
        </button>
      </a>
    </div>
    <div class="right">
      <a href="{INSTA}" target="_blank">
        <button class="cta-button" style="background:linear-gradient(45deg,#f58529,#dd2a7b,#8134af,#515bd4); color:white;">
          <img src="{insta_logo}" style="width:20px; height:20px; vertical-align:middle; margin-right:6px;">
          ProBuild Rudreshwar
        </button>
      </a>
    </div>
  </div>

  <!-- Second Instagram Button -->
  <div class="fancy-content" style="margin-top:20px; justify-content:center;">
    <a href="{INSTA2}" target="_blank">
      <button class="cta-button" style="background:linear-gradient(45deg,#f58529,#dd2a7b,#8134af,#515bd4); color:white;">
        <img src="{insta_logo}" style="width:20px; height:20px; vertical-align:middle; margin-right:6px;">
        श्री ᴀꜱᴛʀᴏ ᴠᴀꜱᴛᴜ
      </button>
    </a>
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

        if st.button("📊 Check Responses"):
            st.markdown(f"<meta http-equiv='refresh' content='0; url={RESPONSES_LINK}'>", unsafe_allow_html=True)

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
                    st.success("✅ Password changed successfully! It will apply on next login.")
                    st.rerun()

        # Upload Project
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

        # Manage Projects
        st.markdown('<h2 class="admin-heading">Manage Existing Projects</h2>', unsafe_allow_html=True)
        projects = list_projects() or []
        for pr in projects:
            project_id = pr.get("id")
            project_title = pr.get("title", "Untitled")
            col1, col2, col3 = st.columns([0.7,0.15,0.15])
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
