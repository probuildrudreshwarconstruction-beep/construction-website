import streamlit as st
from supabase_client import upload_media, add_project, list_projects, delete_project, update_project
import os, base64, json, hashlib, random, string

# -------------------- Safari Cache Bust Fix --------------------
cache_bust = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
st.experimental_set_query_params(_cb=cache_bust)

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
    with open(file_name) as f:
        css_content = f.read()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

local_css(f"style.css?cb={cache_bust}")  # Add cache-busting query

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

# -------------------- Contact Us --------------------
st.markdown(f"""
<section class="fancy-section" id="cta">
  <h1 class="section-title">☬ Contact Us ☬</h1>
  <div class="fancy-content">
    <div class="left">
      <a href="{FORM_URL}" target="_blank">
        <button class="cta-button forms-btn">📄 Enquire via Google Form</button>
      </a>
    </div>
    <div class="right">
      <a href="{wa_link}" target="_blank">
        <button class="cta-button whatsapp-btn">💬 WhatsApp</button>
      </a>
    </div>
  </div>
  <div class="fancy-content" style="margin-top:40px;">
    <div class="left">
      <a href="{EMAIL}" target="_blank">
        <button class="cta-button forms-btn">✉️ Email Us</button>
      </a>
    </div>
    <div class="right">
      <a href="{INSTA}" target="_blank">
        <button class="cta-button forms-btn">📸 Instagram</button>
      </a>
    </div>
  </div>
  <p style="text-align:center; margin-top:12px; font-size:0.7rem;">© ProBuild Rudreshwar Constructions 2025</p>
</section>
""", unsafe_allow_html=True)
