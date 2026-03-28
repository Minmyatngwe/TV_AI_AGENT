import os
from pathlib import Path
import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"

TEMPLATE_SAVE_DIR = Path("/home/user/persistent/TV_AI_AGENT/backend/template")
TEMPLATE_SAVE_DIR.mkdir(parents=True, exist_ok=True)


def load_existing_templates():
    if not TEMPLATE_SAVE_DIR.exists():
        return []

    templates = []
    allowed_exts = {".pptx", ".png", ".jpg", ".jpeg", ".webp"}

    for file_path in TEMPLATE_SAVE_DIR.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in allowed_exts:
            templates.append({
                "name": file_path.name,
                "path": str(file_path),
                "type": file_path.suffix.lower()
            })

    templates.sort(key=lambda x: x["name"].lower())
    return templates


def save_uploaded_template(uploaded_file):
    save_path = TEMPLATE_SAVE_DIR / uploaded_file.name
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(save_path)


if "current_template_paths" not in st.session_state:
    st.session_state["current_template_paths"] = []

if "selected_layout" not in st.session_state:
    st.session_state["selected_layout"] = None

st.markdown('<div class="hero-title">Generate Layouts</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Paste a link and upload one or more PPTX layout templates</div>',
    unsafe_allow_html=True
)

left_col, right_col = st.columns([1.2, 1], gap="large")

with left_col:
    tab1, tab2 = st.tabs(["URL", "File"])

    with tab1:
        with st.form("url_form"):
            st.markdown("#### Generate from URL")

            website_url = st.text_input(
                "Website URL",
                placeholder="https://example.com"
            )

            template_files = st.file_uploader(
                "Upload layout template files (.pptx)",
                type=["pptx"],
                accept_multiple_files=True,
                key="template_files_url"
            )

            url_submit = st.form_submit_button(
                "Generate Layouts",
                use_container_width=True
            )

        if url_submit:
            if not website_url.strip():
                st.warning("Please enter a valid website URL.")
            elif not template_files:
                st.warning("Please upload at least one PPTX template file.")
            else:
                try:
                    saved_paths = [save_uploaded_template(f) for f in template_files]
                    st.session_state["current_template_paths"] = saved_paths

                    payload = {
                        "link": website_url,
                        "template_paths": saved_paths
                    }

                    response = requests.post(
                        f"{BACKEND_URL}/generate",
                        json=payload,
                        timeout=300
                    )

                    if response.status_code != 200:
                        st.error(f"Backend error {response.status_code}")
                        st.code(response.text)

                    response.raise_for_status()
                    st.success("Template generation request sent successfully.")
                    st.rerun()

                except Exception as e:
                    st.error(f"Request failed: {e}")

    with tab2:
        with st.form("file_form"):
            st.markdown("#### Generate from File")
            st.caption("This tab is UI-only for now. The current backend /generate endpoint requires a link and template_paths.")

            uploaded_file = st.file_uploader(
                "Upload source file",
                type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
                key="source_file"
            )

            reference_file_upload = st.file_uploader(
                "Upload reference layout image",
                type=["png", "jpg", "jpeg"],
                key="reference_file_upload"
            )

            file_submit = st.form_submit_button(
                "Generate Layouts",
                use_container_width=True
            )

        if file_submit:
            if uploaded_file is None:
                st.warning("Please upload a source file.")
            else:
                if reference_file_upload is not None:
                    st.success(f"File captured: {uploaded_file.name} | Reference image: {reference_file_upload.name}")
                else:
                    st.success(f"File captured: {uploaded_file.name}")

with right_col:
    st.markdown('<div class="layout-title">Current Layouts</div>', unsafe_allow_html=True)

    layouts = load_existing_templates()

    if layouts:
        for i, layout in enumerate(layouts):
            row1, row2 = st.columns([6, 2])

            with row1:
                file_ext = layout.get("type", "").lower()

                if file_ext in [".png", ".jpg", ".jpeg", ".webp"]:
                    label = f"🖼️ {layout['name']}"
                elif file_ext == ".pptx":
                    label = f"📄 {layout['name']}"
                else:
                    label = f"📁 {layout['name']}"

                if st.button(label, key=f"layout_{i}", use_container_width=True):
                    st.session_state["selected_layout"] = layout
                    st.switch_page("pages/layout_preview.py")

            with row2:
                if st.button("Delete", key=f"delete_{i}", use_container_width=True):
                    try:
                        os.remove(layout["path"])

                        selected = st.session_state.get("selected_layout")
                        if selected and selected["path"] == layout["path"]:
                            st.session_state["selected_layout"] = None

                        st.rerun()
                    except Exception as e:
                        st.error(f"Delete failed: {e}")
    else:
        st.info("No layouts found.")