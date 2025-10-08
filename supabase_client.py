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
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]          # anon/public key (reads)
SERVICE_KEY = st.secrets.get("SERVICE_KEY")        # service role key (writes)

if not SERVICE_KEY:
    st.error("❌ SERVICE_KEY is missing in Streamlit secrets! Uploads will fail.")

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def get_supabase_client(service: bool = False):
    key = SERVICE_KEY if service and SERVICE_KEY else SUPABASE_KEY
    return create_client(SUPABASE_URL, key)


def sanitize_filename(filename: str) -> str:
    return re.sub(r"[^\w\.\-]", "_", filename)


def upload_media(file):
    file_bytes = file.read()
    file_path = sanitize_filename(file.name)

    unique_suffix = f"_{int(time.time())}_{uuid.uuid4().hex[:6]}"
    name_parts = file_path.split(".")
    if len(name_parts) > 1:
        file_path = f"{'.'.join(name_parts[:-1])}{unique_suffix}.{name_parts[-1]}"
    else:
        file_path = f"{file_path}{unique_suffix}"

    try:
        supabase = get_supabase_client(service=True)
        supabase.storage.from_("media").upload(file_path, file_bytes)
        url = supabase.storage.from_("media").get_public_url(file_path)
        st.success("✅ File uploaded successfully!")
        return url
    except Exception as e:
        traceback.print_exc()
        st.error(f"❌ Upload failed — raw error: {repr(e)}")
        raise


def add_project(title: str, description: str, file_url: str, file_type: str, is_banner: bool = False):
    supabase = get_supabase_client(service=True)
    payload = {
        "title": title,
        "description": description,
        "file_url": file_url,
        "file_type": file_type,
        "is_banner": is_banner
    }
    return supabase.table("projects").insert(payload).execute()


def list_projects(limit: int = 1000):
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
    supabase = get_supabase_client(service=True)
    return supabase.table("projects").delete().eq("id", project_id).execute()


def update_project(project_id: int, title: str, description: str, file_url: str = None,
                   file_type: str = None, is_banner: bool = None):
    supabase = get_supabase_client(service=True)
    payload = {"title": title, "description": description}
    if file_url:
        payload["file_url"] = file_url
    if file_type:
        payload["file_type"] = file_type
    if is_banner is not None:
        payload["is_banner"] = is_banner
    return supabase.table("projects").update(payload).eq("id", project_id).execute()
