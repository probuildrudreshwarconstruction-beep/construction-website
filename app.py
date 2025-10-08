# app.py
import streamlit as st
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

# -------------------- Helper: choose hero source (webp first) --------------------
def hero_src_html():
    """
    Prefer webp/smaller files in assets/ if present.
    If none present, fallback to original base64 embedding (keeps original behaviour).
    This avoids encoding a very large base64 blob in mobile browsers unless necessary.
    """
    hero_base = "assets/b1"
    candidates = [
        (f"{hero_base}-small.webp", "image/webp"),
        (f"{hero_base}.webp", "image/webp"),
        (f"{hero_base}.avif", "image/avif"),
        (f"{hero_base}.jpg", "image/jpeg"),
        (f"{hero_base}.png", "image/png"),
    ]
    available = [p for p, t in candidates if os.path.exists(p)]
    if available:
        # build responsive picture block
        picture = '<picture>\n'
        # prefer AVIF/WebP sources first
        for p, t in candidates:
            if os.path.exists(p) and (t in ("image/avif","image/webp")):
                picture += f'  <source srcset="{p}" type="{t}">\n'
        # fallback sources (jpeg/png)
        for p, t in candidates:
            if os.path.exists(p) and t in ("image/jpeg","image/png"):
                picture += f'  <source srcset="{p}" type="{t}">\n'
        # final <img>
        fallback = available[-1]
        picture += f'  <img src="{fallback}" alt="ProBuild Rudreshwar" class="hero-img" loading="lazy" decoding="async" width="1200" height="800">\n'
        picture += '</picture>\n'
        return picture
    else:
        # fallback to your original base64 behaviour to preserve exact visual
        hero_image_path = "assets/b1.jpg"
        if os.path.exists(hero_image_path):
            with open(hero_image_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            return f'<img src="data:image/jpg;base64,{img_b64}" class="hero-img" alt="ProBuild Rudreshwar" loading="lazy" decoding="async">'
        else:
            # nothing found: return a lightweight placeholder so the page still renders quickly
            return '<div class="hero-placeholder" style="width:100%;height:240px;display:flex;align-items:center;justify-content:center;background:#0d0d0d;color:#f9f5ef">ProBuild Rudreshwar</div>'

# -------------------- Small inline JS for lazy modal media loading --------------------
# This script ensures modal media src is only assigned when the modal opens,
# and removed when it closes — preventing mobile Safari from preloading all videos.
modal_script = """
<script>
function openModal(idx){
  var mod = document.getElementById('modal-'+idx);
  if(!mod) return;
  var media = mod.querySelector('[data-src]');
  if(media && !media.getAttribute('src')){
    media.setAttribute('src', media.getAttribute('data-src'));
    // if video, start playing if autoplay desired
    if(media.tagName.toLowerCase()==='video'){
      try { media.play().catch(()=>{}); } catch(e){}
    }
  }
  mod.style.display = 'block';
}
function closeModal(idx){
  var mod = document.getElementById('modal-'+idx);
  if(!mod) return;
  var media = mod.querySelector('[data-src]');
  if(media){
    if(media.tagName.toLowerCase()==='video'){
      try { media.pause(); } catch(e){}
      media.removeAttribute('src');
      media.load();
    } else {
      media.removeAttribute('src');
    }
  }
  mod.style.display = 'none';
}
window.addEventListener('click', function(e){
  // click outside the modal content closes it
  if(e.target && e.target.classList && e.target.classList.contains('modal')){
    e.target.style.display = 'none';
    var media = e.target.querySelector('[data-src]');
    if(media){
      media.removeAttribute('src');
      if(media.tagName && media.tagName.toLowerCase()==='video'){
        try { media.pause(); } catch(e){}
        media.load();
      }
    }
  }
});
</script>
"""

st.markdown(modal_script, unsafe_allow_html=True)

# -------------------- Hero Section --------------------
st.markdown("<header class='hero'>", unsafe_allow_html=True)
st.markdown(hero_src_html(), unsafe_allow_html=True)
st.markdown("</header>", unsafe_allow_html=True)

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

# fetch projects (keeps original behaviour)
try:
    projects = list_projects() or []
except Exception as e:
    st.error(f"Error fetching projects: {e}")
    projects = []

# fallback sample projects (unchanged)
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

        # For thumbnails: images use loading lazy, videos have poster if possible and preload="none"
        if file_type in ('video','mp4','mov'):
            thumb_html = f'''
            <div class="project-container" onclick="openModal({idx})" role="button" tabindex="0">
              <video class="project-thumb" data-src="{file_url}" preload="none" playsinline muted loop poster="" style="width:100%;height:100%;object-fit:cover;border-radius:10px;filter:brightness(70%);"></video>
              <div class="project-overlay">{title}</div>
            </div>
            '''
            modal_media_html = f'<video data-src="{file_url}" controls preload="none" playsinline style="width:100%; max-height:80vh; border-radius:8px;"></video>'
        else:
            # image thumbnail uses lazy loading; modal image uses data-src to avoid preloading
            thumb_html = f'''
            <div class="project-container" onclick="openModal({idx})" role="button" tabindex="0">
              <img loading="lazy" decoding="async" src="{file_url}" alt="{title}" style="width:100%;height:100%;object-fit:cover;border-radius:10px;filter:brightness(80%);">
              <div class="project-overlay">{title}</div>
            </div>
            '''
            modal_media_html = f'<img data-src="{file_url}" alt="{title}" style="width:100%; max-height:80vh; object-fit:contain; border-radius:8px;">'

        # render thumbnail + modal (modal content doesn't have src yet - it will be set when user opens)
        st.markdown(f"""
        {thumb_html}
        <div id="modal-{idx}" class="modal" aria-hidden="true">
          <span class="modal-close" onclick="closeModal({idx})">&times;</span>
          {modal_media_html}
        </div>
        """, unsafe_allow_html=True)

        # view more (keeps behavior exactly)
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

# -------------------- Admin Panel (unchanged features) --------------------
st.markdown("<hr><h2></h2><hr>", unsafe_allow_html=True)

if st.button("🔒"):
    st.session_state.admin_visible = not st.session_state.admin_visible

if st.session_state.admin_visible:
    st.markdown('<div class="admin-panel">', unsafe_allow_html=True)

    # 🔐 Admin Login
    password = st.text_input("⚜️", type="password", key="admin_pw", placeholder="Enter admin password")
    stored_password = get_password()

    if stored_password and password and hash_pass(password) == stored_password:
        st.success("Admin authenticated — upload/manage projects below.")

        # 🔑 ===== Change Password Section =====
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

        # ===== Upload New Project =====
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

        # ===== Manage Existing Projects =====
        st.markdown('<h2 class="admin-heading">Manage Existing Projects</h2>', unsafe_allow_html=True)
        projects = list_projects() or []

        for pr in projects:
            project_id = pr.get("id")
            project_title = pr.get("title", "Untitled")

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
        if password:
            st.error("❌ Wrong password.")
    
    st.markdown("</div>", unsafe_allow_html=True)
