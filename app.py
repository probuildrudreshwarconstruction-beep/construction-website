import streamlit as st
from supabase_client import upload_media, add_project, list_projects, delete_project, update_project
import os
import base64

st.set_page_config(page_title="ProBuild Rudreshwar Construction", layout="wide")

# -------------------- Load CSS --------------------
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    st.warning("Could not load style.css")

# -------------------- Session State --------------------
if 'admin_edit_id' not in st.session_state:
    st.session_state.admin_edit_id = None

# -------------------- Secrets --------------------
ADMIN_PASS = st.secrets.get("ADMIN_PASSWORD", "")
FORM_URL = st.secrets.get("GOOGLE_FORM_URL", "#")
WHATSAPP = st.secrets.get("WHATSAPP_NUMBER", "")
wa_link = f"https://wa.me/{WHATSAPP}" if WHATSAPP else "#"

# -------------------- Helper: Convert Image to Base64 --------------------
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# -------------------- Hero Section --------------------
hero_image_path = "assets/banner1.jpg"
if os.path.exists(hero_image_path):
    img_b64 = get_base64_image(hero_image_path)
    st.markdown(f"""
    <div class="hero" style="background-image: url('data:image/jpg;base64,{img_b64}'); border:5px solid red;">
        <div class="hero-content">
            <h1>ProBuild Rudreshwar</h1>
            <p>Building dreams that last a lifetime</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("Hero image not found in assets folder.")

# -------------------- Who We Are Section --------------------
st.markdown("""
<section class="who-we-are">
  <h2>WHO WE ARE</h2>
  <p>When we focus on mutual success, everyone wins.</p>
  <p>The flexibility to mobilize the right people to deliver unique solutions, an unwavering focus to delivering value to your business bottom line; and the capability to leverage innovation to meet emerging challenges and keep you at the fore. This is ProBuild.</p>
  <p>As a company that is 100 percent employee-owned, we collaborate and innovate to help our partners thrive. Our culture of ownership drives your success.</p>
  <p>Whether you are in the buildings, civil, or industrial market, partnering with ProBuild means you're gaining a proven, reliable and trusted full-service partner with a mobile network of experts and seasoned professionals across India.</p>
  <p>From advanced digital construction technologies to innovative offsite modular manufacturing, to cutting-edge solutions, we deliver excellence in every project.</p>
</section>
""", unsafe_allow_html=True)

# -------------------- What We Do Section --------------------
st.markdown("""
<section class="what-we-do">
  <h2>WHAT WE DO</h2>
  <p>We have a vision for the future of construction. ProBuild delivers innovative, sustainable, and high-quality projects across residential, commercial, and industrial sectors.</p>
</section>
""", unsafe_allow_html=True)

# -------------------- Ready to Work Together Section --------------------
st.markdown(f"""
<section class="contact-cta">
  <h2>Ready to work together?</h2>
  <p>Whether you have a project in mind and you’re looking for a reliable construction partner or you’re looking to take the next step in your career, we want to hear from you!</p>
  <div class="cta-buttons">
    <a href="{FORM_URL}" target="_blank"><button class="cta-button">📝 Fill Google Form</button></a>
    <a href="{wa_link}" target="_blank"><button class="cta-button">💬 Message on WhatsApp</button></a>
  </div>
</section>
""", unsafe_allow_html=True)

# -------------------- Project Showcase Section --------------------
st.markdown("<section id='projects'><h2>Project Showcase</h2></section>", unsafe_allow_html=True)

try:
    projects = list_projects() or []
except:
    projects = []

if not projects:
    projects = [
        {"id":1, "title":"Luxury Villa","description":"Modern villa with eco-friendly materials.","location":"Rudreshwar","market":"Residential","file_url":"assets/banner1.jpg","file_type":"image"},
        {"id":2, "title":"Commercial Renovation","description":"Revamped commercial complex.","location":"Rudreshwar","market":"Commercial","file_url":"assets/banner2.jpg","file_type":"image"},
        {"id":3, "title":"Interior Design Showcase","description":"Elegant interior design.","location":"Rudreshwar","market":"Interior Design","file_url":"assets/banner3.jpg","file_type":"image"}
    ]

for proj in projects:
    if proj["file_type"]=="image":
        file_tag = f'<img src="{proj["file_url"]}" style="width:100%; height:100%; object-fit:cover;">'
    else:
        # Video: show controls, no autoplay
        file_tag = f'<video src="{proj["file_url"]}" controls style="width:100%; height:100%; object-fit:cover;"></video>'
    st.markdown(f"""
    <div class="project-showcase-card">
        <div class="project-media" onclick="openModal('{proj['file_url']}','{proj['file_type']}','{proj['title']}','{proj['description']}','{proj.get('location','')}','{proj.get('market','')}')">
            {file_tag}
        </div>
        <div class="project-info">
            <h3>{proj['title']}</h3>
            <p>{proj['description'][:150]}...</p>
            <p><strong>LOCATION:</strong> {proj.get('location','')} &nbsp;&nbsp; <strong>MARKET:</strong> {proj.get('market','')}</p>
            <button class="cta-button" onclick="openModal('{proj['file_url']}','{proj['file_type']}','{proj['title']}','{proj['description']}','{proj.get('location','')}','{proj.get('market','')}')">Learn More</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------- Modal for Project Details --------------------
st.markdown("""
<div id="mediaModal" class="modal">
  <span class="modal-close" onclick="closeModal()">&times;</span>
  <h2 id="modalTitle" style="color:#ffcc00;"></h2>
  <div id="modalMediaContainer"></div>
  <p id="modalDesc" style="color:#fff;"></p>
  <p id="modalLoc" style="color:#fff;"></p>
  <p id="modalMarket" style="color:#fff;"></p>
</div>

<script>
function openModal(file,type,title,desc,loc,market){
    var modal = document.getElementById('mediaModal');
    var mediaContainer = document.getElementById('modalMediaContainer');
    var mediaTag = '';
    if(type=='image'){
        mediaTag = '<img src="'+file+'" style="width:100%; border-radius:8px;">';
    }else{
        // video with controls, no autoplay
        mediaTag = '<video src="'+file+'" controls style="width:100%; border-radius:8px;"></video>';
    }
    mediaContainer.innerHTML = mediaTag;
    document.getElementById('modalTitle').innerText = title;
    document.getElementById('modalDesc').innerText = desc;
    document.getElementById('modalLoc').innerHTML = '<strong>LOCATION:</strong> ' + loc;
    document.getElementById('modalMarket').innerHTML = '<strong>MARKET:</strong> ' + market;
    modal.style.display='block';
}
function closeModal(){
    var modal = document.getElementById('mediaModal');
    modal.style.display='none';
    var video = modal.querySelector('video');
    if(video){ video.pause(); }
}
</script>
""", unsafe_allow_html=True)

# -------------------- Admin Panel --------------------
st.markdown("<hr><h2>Admin Panel</h2>", unsafe_allow_html=True)
admin_pw_input = st.text_input("Enter admin password", type="password")
if admin_pw_input:
    if admin_pw_input == ADMIN_PASS:
        st.success("Admin authenticated — upload/manage projects below.")
        with st.expander("Upload New Project", expanded=True):
            uploaded = st.file_uploader("Upload media (image/video)", type=["jpg","jpeg","png","mp4","mov"])
            up_title = st.text_input("Project / Site Name")
            up_desc = st.text_area("Project Description")
            up_location = st.text_input("Project Location")
            up_market = st.text_input("Project Market")
            if st.button("Submit Project"):
                if uploaded and up_title and up_desc:
                    url = upload_media(uploaded)
                    file_type = uploaded.type.split("/")[0]
                    add_project(up_title, up_desc, url, file_type, up_location, up_market)
                    st.success("Project uploaded successfully!")
                    st.rerun()
                else:
                    st.error("Provide media, title, description, location, and market.")

        st.markdown("**Manage Existing Projects**")
        for pr in list_projects() or []:
            st.markdown(f"**{pr.get('title','Untitled')}**")
            cols = st.columns([3,1,1])
            with cols[1]:
                if st.button("Edit", key=f"edit-{pr.get('id')}"):
                    st.session_state.admin_edit_id = pr.get("id")
                    st.session_state.admin_edit_title = pr.get("title")
                    st.session_state.admin_edit_desc = pr.get("description")
                    st.session_state.admin_edit_location = pr.get("location","")
                    st.session_state.admin_edit_market = pr.get("market","")
            with cols[2]:
                if st.button("Delete", key=f"delete-{pr.get('id')}"):
                    delete_project(pr.get("id"))
                    st.success("Deleted!")
                    st.rerun()
        if st.session_state.admin_edit_id:
            st.markdown("### Edit Project")
            new_title = st.text_input("Title", value=st.session_state.admin_edit_title)
            new_desc = st.text_area("Description", value=st.session_state.admin_edit_desc)
            new_location = st.text_input("Location", value=st.session_state.admin_edit_location)
            new_market = st.text_input("Market", value=st.session_state.admin_edit_market)
            new_file = st.file_uploader("Replace Media (optional)", type=["jpg","png","mp4","mov"])
            if st.button("Save Changes"):
                file_url, file_type = None, None
                if new_file:
                    file_url = upload_media(new_file)
                    file_type = new_file.type.split("/")[0]
                update_project(st.session_state.admin_edit_id, new_title, new_desc, file_url, file_type, new_location, new_market)
                st.success("Updated!")
                st.session_state.admin_edit_id = None
                st.rerun()
    else:
        st.error("Wrong password.")

# -------------------- Footer --------------------
st.markdown("""
<footer>
  <p>© 2025 ProBuild Rudreshwar Constructions</p>
</footer>
""", unsafe_allow_html=True)

