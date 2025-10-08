import streamlit as st
from supabase_client import upload_media, add_project, list_projects, delete_project, update_project
import os
import base64

# -------------------- Load external CSS --------------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# -------------------- Page Config --------------------
st.set_page_config(page_title="☬ProBuild Rudreshwar☬", layout="wide")

# -------------------- Session State --------------------
if "admin_visible" not in st.session_state:
    st.session_state.admin_visible = False
if "admin_edit_id" not in st.session_state:
    st.session_state.admin_edit_id = None

# -------------------- Secrets --------------------
ADMIN_PASS = st.secrets.get("ADMIN_PASSWORD", "")
FORM_URL = st.secrets.get("GOOGLE_FORM_URL", "#")
WHATSAPP = st.secrets.get("WHATSAPP_NUMBER", "")
wa_link = f"https://wa.me/{WHATSAPP}" if WHATSAPP else "#"

# -------------------- Hero Section --------------------
hero_image_path = "assets/banner1.jpg"
if os.path.exists(hero_image_path):
    with open(hero_image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <header class="hero w3-display-container">
        <img src="data:image/jpg;base64,{img_b64}" class="hero-img">
        <div class="w3-display-bottomleft w3-padding-large hero-text">
            <h1 class="hero-title">☬ProBuild Rudreshwar☬</h1>
            <h3>Construction & Developers</h3>
            <p>Er. Rushikesh Shivarkar — B.E. Civil | Govt. Contractor | Vastu Expert</p>
            <a class="hero-button" href="{wa_link}" target="_blank">🛠 Contact on WhatsApp 🛠</a>
        </div>
    </header>
    """, unsafe_allow_html=True)

# -------------------- About Us --------------------
st.markdown("""
<section class="fancy-section" id="about">
  <h1 class="section-title">☬ All About Us ☬</h1>
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

# -------------------- Our Projects Section --------------------
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
            st.write(desc)

# -------------------- Marathi CTA --------------------
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
st.markdown("<hr><h2>Admin & Contact</h2><hr>", unsafe_allow_html=True)

if st.button("🔒 Admin Panel"):
    st.session_state.admin_visible = not st.session_state.admin_visible

if st.session_state.admin_visible:
    st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
    
    password = st.text_input("Enter admin password", type="password", key="admin_pw", placeholder="Enter admin password")
    
    if password:
        if password == ADMIN_PASS:
            st.success("Admin authenticated — upload/manage projects below.")
            
            # ===== Upload New Project =====
            st.markdown('<h2 class="admin-heading">Upload New Project</h2>', unsafe_allow_html=True)
            uploaded = st.file_uploader("Upload media (image/video)", type=["jpg","png","mp4","mov"], key="upload_file")
            up_title = st.text_input("Project / Site Name", key="upload_title", placeholder="Project / Site Name")
            up_desc = st.text_area("Project Description", key="upload_desc", placeholder="Project Description")
            
            if st.button("Submit Project"):
                if uploaded and up_title and up_desc:
                    url = upload_media(uploaded)
                    file_type = uploaded.type.split("/")[0]
                    add_project(up_title, up_desc, url, file_type)
                    st.success("Project uploaded successfully!")
                    st.rerun()

            # ===== Manage Existing Projects =====
            st.markdown('<h2 class="admin-heading">Manage Existing Projects</h2>', unsafe_allow_html=True)
            projects = list_projects() or []

            for pr in projects:
                project_id = pr.get("id")
                project_title = pr.get("title", "Untitled")

                # Create inline flex layout for title and buttons
                col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
                with col1:
                    st.markdown(
                        f"<div class='project-item'><div class='title'><b>{project_title}</b></div></div>",
                        unsafe_allow_html=True,
                    )
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

            # ===== Edit Project Form =====
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
            st.error("Wrong password.")
    
    st.markdown("</div>", unsafe_allow_html=True)
