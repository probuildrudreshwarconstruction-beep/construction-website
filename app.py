import streamlit as st
from supabase_client import upload_media, add_project, list_projects, delete_project, update_project
import os
import hashlib
import json

# -------------------- Password Config --------------------
PASS_FILE = "admin_password.json"
def hash_pass(p): return hashlib.sha256(p.encode()).hexdigest()
def get_password():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE,"r") as f: return json.load(f).get("password")
    elif "admin_password" in st.secrets:
        return hash_pass(st.secrets["admin_password"])
    else: return None
def set_password(new_pass):
    with open(PASS_FILE,"w") as f: json.dump({"password": hash_pass(new_pass)}, f)

# -------------------- CSS --------------------
def local_css(file_name):
    with open(file_name) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style.css")

# -------------------- Page Config --------------------
st.set_page_config(page_title="☬ProBuild Rudreshwar☬", layout="wide")

if "admin_visible" not in st.session_state: st.session_state.admin_visible = False
if "admin_edit_id" not in st.session_state: st.session_state.admin_edit_id = None

FORM_URL = st.secrets.get("GOOGLE_FORM_URL","#")
WHATSAPP = st.secrets.get("WHATSAPP_NUMBER","")
wa_link = f"https://wa.me/{WHATSAPP}" if WHATSAPP else "#"

# -------------------- Hero Section --------------------
hero_image_path = "assets/b1.jpg"
if os.path.exists(hero_image_path):
    st.markdown(f"""
    <header class="hero w3-display-container">
        <img src="{hero_image_path}" class="hero-img" loading="lazy">
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

# -------------------- Projects --------------------
st.markdown("""<section class="fancy-section" id="projects"><h1 class="section-title">☬ Our Projects ☬</h1></section>""", unsafe_allow_html=True)

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
        file_url = proj.get("file_url","")
        file_type = (proj.get("file_type") or "").lower()
        title = proj.get("title","Untitled")
        desc = proj.get("description","")

        # Lazy load videos/images
        media_html = ""
        if file_type in ("video","mp4","mov"):
            media_html = f'<video src="{file_url}" controls preload="metadata" playsinline style="width:100%;max-height:250px;"></video>'
        else:
            media_html = f'<img src="{file_url}" loading="lazy" style="width:100%;max-height:250px;">'

        st.markdown(f"""
        <div class="project-container" onclick="document.getElementById('modal-{idx}').style.display='block'">
          {media_html}
          <div class="project-overlay">{title}</div>
        </div>
        <div id="modal-{idx}" class="modal">
          <span class="modal-close" onclick="document.getElementById('modal-{idx}').style.display='none'">&times;</span>
          {media_html}
        </div>
        """, unsafe_allow_html=True)

        with st.expander("View More"):
             formatted_desc = "".join([f"<li>{line.strip()}</li>" for line in desc.split("\n") if line.strip()])
             st.markdown(f"<ul class='viewmore-list'>{formatted_desc}</ul>", unsafe_allow_html=True)

# -------------------- CTA & Admin Panel --------------------
st.markdown(f"""
<section class="fancy-section" id="cta">
  <h1 class="section-title">तर मग काय वाट बघता? संपर्क करा! 🚀</h1>
  <div class="fancy-content">
    <div class="left">
      <a href="{FORM_URL}" target="_blank"><button class="cta-button" style="background:var(--gold); color:#000;">📄 Enquire via Forms</button></a>
    </div>
    <div class="divider"></div>
    <div class="right">
      <a href="{wa_link}" target="_blank"><button class="cta-button" style="background:var(--bronze); color:#fff;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" style="height:22px;vertical-align:middle;margin-right:8px;">Contact on WhatsApp</button></a>
    </div>
  </div>
  <p style="text-align:center;font-size:0.9rem;opacity:0.8;">© 2025 ProBuild Rudreshwar Constructions</p>
</section>
""", unsafe_allow_html=True)

# -------------------- Admin panel unchanged --------------------
# All your existing admin panel code remains as-is
