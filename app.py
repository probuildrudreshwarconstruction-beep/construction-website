# app.py
import streamlit as st
from supabase_client import upload_media, add_project, list_projects, delete_project, update_project
import os
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

# -------------------- Session State --------------------
if "admin_visible" not in st.session_state:
    st.session_state.admin_visible = False
if "admin_edit_id" not in st.session_state:
    st.session_state.admin_edit_id = None

# -------------------- Secrets --------------------
FORM_URL = st.secrets.get("GOOGLE_FORM_URL", "#")
WHATSAPP = st.secrets.get("WHATSAPP_NUMBER", "")
wa_link = f"https://wa.me/{WHATSAPP}" if WHATSAPP else "#"

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

# -------------------- Our Projects --------------------
st.markdown("<h1 class='section-title'>☬ Our Projects ☬</h1>", unsafe_allow_html=True)

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

        if file_type in ('video','mp4','mov'):
            st.video(file_url)
        else:
            st.image(file_url, use_column_width=True)

        st.markdown(f"<b>{title}</b>", unsafe_allow_html=True)
        st.markdown(f"<p>{desc}</p>", unsafe_allow_html=True)

# -------------------- Marathi CTA --------------------
st.markdown(f"""
<section class="fancy-section" id="cta">
  <h1 class="section-title">तर मग काय वाट बघता? संपर्क करा! 🚀</h1>
  <div class="fancy-content">
    <div class="left">
      <a href="{FORM_URL}" target="_blank">
          <button class="cta-button" style="background:var(--gold); color:#000;">
            📄 Enquire via Forms
          </button>
      </a>
    </div>
    <div class="divider"></div>
    <div class="right">
      <a href="{wa_link}" target="_blank">
          <button class="cta-button" style="background:var(--bronze); color:#fff;">
            WhatsApp Contact
          </button>
      </a>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)

# -------------------- Admin Panel --------------------
if st.button("🔒 Show/Hide Admin Panel"):
    st.session_state.admin_visible = not st.session_state.admin_visible

if st.session_state.admin_visible:
    st.markdown('<div class="admin-panel">', unsafe_allow_html=True)

    # Admin login
    password = st.text_input("Admin Password", type="password")
    stored_password = get_password()
    if stored_password and password and hash_pass(password) == stored_password:
        st.success("Admin authenticated — upload/manage projects below.")

        # Change password
        with st.expander("Change Admin Password"):
            old = st.text_input("Old Password", type="password", key="old")
            new = st.text_input("New Password", type="password", key="new")
            confirm = st.text_input("Confirm New Password", type="password", key="confirm")
            if st.button("Update Password"):
                if hash_pass(old) != stored_password:
                    st.error("Old password incorrect")
                elif new != confirm:
                    st.warning("Passwords do not match")
                else:
                    set_password(new)
                    st.success("Password changed successfully")

        # Upload new project
        uploaded = st.file_uploader("Upload media (image/video)", type=["jpg","png","mp4","mov"])
        up_title = st.text_input("Project Name")
        up_desc = st.text_area("Project Description")

        if st.button("Submit Project"):
            if uploaded and up_title and up_desc:
                url = upload_media(uploaded)
                file_type = uploaded.type.split("/")[0]
                add_project(up_title, up_desc, url, file_type)
                st.success("Project uploaded successfully!")

    else:
        if password:
            st.error("❌ Wrong password.")

    st.markdown('</div>', unsafe_allow_html=True)
