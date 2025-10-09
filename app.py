import streamlit as st
import base64
import os
from datetime import datetime

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="ProBuild Rudreshwar Constructions",
    page_icon="🏗️",
    layout="wide"
)

# -------------------- LOAD SECRETS --------------------
COMPANY_NAME = st.secrets.get("COMPANY_NAME", "Company")
TAGLINE = st.secrets.get("TAGLINE", "")
FORM_URL = st.secrets.get("GOOGLE_FORM_URL", "#")
FORM_RESPONSES_URL = st.secrets.get("GOOGLE_FORM_RESPONSES_URL", "#")
WHATSAPP_NUMBER = st.secrets.get("WHATSAPP_NUMBER", "")
EMAIL = st.secrets.get("EMAIL", "")
INSTAGRAM_URL = st.secrets.get("INSTAGRAM_URL", "")
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "")

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
/* Remove Streamlit default top bar */
header[data-testid="stHeader"] {
    display: none !important;
}

/* Hide hamburger menu */
#MainMenu {visibility: hidden;}

/* Hide footer */
footer {visibility: hidden;}

/* Remove top spacing */
main.block-container {
    padding-top: 0rem !important;
    margin-top: -3rem !important;
}

/* Optional padding fix */
section[data-testid="stAppViewBlockContainer"] {
    padding-top: 0rem !important;
    margin-top: -2rem !important;
}

/* Hide floating GitHub icon */
a[data-testid="stActionButtonIcon"] {
    display: none !important;
}

/* Hide "Hosted with Streamlit" toolbar */
[data-testid="stBottomToolbar"] {
    display: none !important;
}

/* Typography */
.hero-title {
    font-family: 'Cinzel', serif;
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 0.5rem;
}

.hero-tagline {
    text-align: center;
    font-size: 1.2rem;
    color: gray;
    margin-bottom: 2rem;
}

/* CTA Buttons */
.cta-button {
    background: #1e1e1e;
    color: #d4af37;
    padding: 10px 20px;
    font-size: 1rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

.cta-button:hover {
    background: #d4af37;
    color: #1e1e1e;
}

/* Centered section */
.center {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 15px;
    flex-wrap: wrap;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER SECTION --------------------
st.markdown(f'<h1 class="hero-title">{COMPANY_NAME}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="hero-tagline">{TAGLINE}</p>', unsafe_allow_html=True)

# -------------------- SOCIAL & ENQUIRY BUTTONS --------------------
st.markdown('<div class="center">', unsafe_allow_html=True)

if FORM_URL != "#":
    st.markdown(f"""
        <a href="{FORM_URL}" target="_blank">
            <button class="cta-button">📩 Enquire via Google Form</button>
        </a>
    """, unsafe_allow_html=True)

if WHATSAPP_NUMBER:
    st.markdown(f"""
        <a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank">
            <button class="cta-button">💬 WhatsApp</button>
        </a>
    """, unsafe_allow_html=True)

if EMAIL:
    st.markdown(f"""
        <a href="{EMAIL}" target="_blank">
            <button class="cta-button">📧 Email</button>
        </a>
    """, unsafe_allow_html=True)

if INSTAGRAM_URL:
    st.markdown(f"""
        <a href="{INSTAGRAM_URL}" target="_blank">
            <button class="cta-button">📸 Instagram</button>
        </a>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------- ADMIN SECTION --------------------
st.markdown("---")
st.markdown("### 🛡️ Admin Panel")

password = st.text_input("Enter admin password", type="password")

if password:
    if password == ADMIN_PASSWORD:
        st.success("✅ Admin authenticated successfully")

        # 📬 Feedback Section
        st.markdown('<h2 class="admin-heading">📬 Feedback</h2>', unsafe_allow_html=True)
        if FORM_RESPONSES_URL != "#":
            st.markdown(f"""
                <a href="{FORM_RESPONSES_URL}" target="_blank">
                    <button class="cta-button">📄 See Feedback</button>
                </a>
            """, unsafe_allow_html=True)
        else:
            st.info("No feedback link configured.")

        # 📦 Project management placeholder (you can expand this)
        with st.expander("🧰 Project Management (Future Section)"):
            st.write("Here you can add file upload, gallery, etc.")

        # 🔐 Change Password Placeholder
        with st.expander("🔐 Change Admin Password"):
            st.info("This feature can be added later to update admin password securely.")

    else:
        st.error("❌ Incorrect password. Access denied.")

# -------------------- FOOTER --------------------
st.markdown("---")
st.caption(f"© {datetime.now().year} {COMPANY_NAME}. All rights reserved.")

        # -------------------- Change Password --------------------
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

        # -------------------- Upload New Project --------------------
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

        # -------------------- Manage Existing Projects --------------------
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

        # -------------------- Edit Project Form --------------------
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
