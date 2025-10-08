# supabase_client.py
import streamlit as st
from supabase import create_client
import re
import uuid
import time
import traceback

# ------------------------------------------------------------------
# Load keys from Streamlit secrets
# ------------------------------------------------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]                # anon/public key (reads)
SERVICE_KEY = st.secrets.get("SUPABASE_SERVICE_KEY")     # service role key (writes)

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def get_supabase_client(service: bool = False):
    """
    Returns a supabase client. If service=True, uses service role key (for uploads/inserts).
    Otherwise uses anon/public key for safe reads.
    """
    key = SERVICE_KEY if service and SERVICE_KEY else SUPABASE_KEY
    return create_client(SUPABASE_URL, key)


def sanitize_filename(filename: str) -> str:
    """Replace spaces and forbidden characters with underscores to create safe storage keys."""
    return re.sub(r"[^\w\.\-]", "_", filename)


# ------------------------------------------------------------------
# Media Upload
# ------------------------------------------------------------------
def upload_media(file) -> str:
    """
    Upload a Streamlit UploadedFile to Supabase Storage 'media' bucket and return public URL.
    Uses service key (write permissions).
    """
    try:
        # ✅ Create supabase client with service key for write access
        supabase = get_supabase_client(service=True)

        # ✅ Sanitize filename
        safe_name = sanitize_filename(file.name)

        # ✅ Add unique suffix to prevent duplicate name errors
        unique_suffix = f"_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        name_parts = safe_name.split(".")
        if len(name_parts) > 1:
            new_name = f"{'.'.join(name_parts[:-1])}{unique_suffix}.{name_parts[-1]}"
        else:
            new_name = f"{safe_name}{unique_suffix}"

        file_path = f"media/{new_name}"
        file_bytes = file.read()

        # ✅ Upload to Supabase Storage
        supabase.storage.from_("media").upload(file_path, file_bytes)

        # ✅ Get public URL
        public_url = supabase.storage.from_("media").get_public_url(file_path)
        st.success("✅ File uploaded successfully!")
        return public_url

    except Exception as e:
        traceback.print_exc()  # Full traceback in logs
        st.error(f"❌ Upload failed — raw error: {repr(e)}")
        raise


# ------------------------------------------------------------------
# Projects Table Operations
# ------------------------------------------------------------------
def add_project(title: str, description: str, file_url: str, file_type: str, is_banner: bool = False):
    """
    Insert a new project row into 'projects' table.
    Uses service key (write access).
    """
    supabase = get_supabase_client(service=True)
    payload = {
        "title": title,
        "description": description,
        "file_url": file_url,
        "file_type": file_type,
        "is_banner": is_banner
    }
    res = supabase.table("projects").insert(payload).execute()
    return res


def list_projects(limit: int = 1000):
    """
    Fetch projects using anon/public key (safe read).
    Returns list of dicts.
    """
    supabase = get_supabase_client(service=False)
    try:
        res = supabase.table("projects").select("*").order("created_at", desc=True).limit(limit).execute()
        if hasattr(res, "data") and res.data is not None:
            return res.data
        try:
            return res.get("data", [])
        except Exception:
            return []
    except Exception as e:
        print("Error listing projects:", e)
        return []


def delete_project(project_id: int):
    """Delete project row by id (uses service key)."""
    supabase = get_supabase_client(service=True)
    res = supabase.table("projects").delete().eq("id", project_id).execute()
    return res


def update_project(project_id: int, title: str, description: str, file_url: str = None,
                   file_type: str = None, is_banner: bool = None):
    """
    Update project row. Pass only fields you want to change (file_url/file_type optional).
    Uses service key.
    """
    supabase = get_supabase_client(service=True)
    payload = {"title": title, "description": description}
    if file_url:
        payload["file_url"] = file_url
    if file_type:
        payload["file_type"] = file_type
    if is_banner is not None:
        payload["is_banner"] = is_banner
    res = supabase.table("projects").update(payload).eq("id", project_id).execute()
    return res
