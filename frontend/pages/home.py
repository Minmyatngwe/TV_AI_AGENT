import os
from pathlib import Path
import requests
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_URL = "http://127.0.0.1:8000"
TEMPLATE_SAVE_DIR = PROJECT_ROOT / "backend" / "template"
TEMPLATE_SAVE_DIR.mkdir(parents=True, exist_ok=True)


def load_existing_templates():
    templates = []
    allowed_exts = {".png", ".jpg", ".jpeg", ".webp"}

    if not TEMPLATE_SAVE_DIR.exists():
        return templates

    for file_path in TEMPLATE_SAVE_DIR.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in allowed_exts:
            templates.append({
                "name": file_path.stem,
                "path": str(file_path),
                "type": file_path.suffix.lower()
            })

    image_dir = TEMPLATE_SAVE_DIR / "image"
    if image_dir.exists() and image_dir.is_dir():
        for file_path in image_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in allowed_exts:
                templates.append({
                    "name": file_path.stem,
                    "path": str(file_path),
                    "type": file_path.suffix.lower()
                })

    templates.sort(key=lambda x: x["name"].lower())
    print(templates)
    return templates


def save_uploaded_template(uploaded_file):
    save_path = TEMPLATE_SAVE_DIR / uploaded_file.name
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(save_path)


# session state defaults
if "current_template_paths" not in st.session_state:
    st.session_state["current_template_paths"] = []

if "selected_layout" not in st.session_state:
    st.session_state["selected_layout"] = []

if "generated_result" not in st.session_state:
    st.session_state["generated_result"] = None

if "generated_file_path" not in st.session_state:
    st.session_state["generated_file_path"] = None

if "generated_powerpoint_paths" not in st.session_state:
    st.session_state["generated_powerpoint_paths"] = []

if "generated_png_image_paths" not in st.session_state:
    st.session_state["generated_png_image_paths"] = []

if "generated_web_text" not in st.session_state:
    st.session_state["generated_web_text"] = ""

if "generated_placeholders" not in st.session_state:
    st.session_state["generated_placeholders"] = []


if "image_counter" not in st.session_state:
    st.session_state["image_counter"] = 0

st.markdown('<div class="hero-title">Generate Layouts</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Paste a link and upload one or more PPTX layout templates</div>',
    unsafe_allow_html=True
)

left_col, center_col, right_col = st.columns([0.5, 5, 0.5], gap="large")

with center_col:
    tab1, tab2 = st.tabs(["URL", "File"])

    with tab1:
        st.markdown("#### Generate from URL")

        website_url = st.text_input(
            "Website URL",
            placeholder="https://example.com"
        )

        st.markdown('<div class="layout-title">Current Layouts</div>', unsafe_allow_html=True)

        image_layouts = load_existing_templates()

        if image_layouts:
            st.markdown("#### Available Layouts")

            cols_per_row = 3
            selected_layouts = st.session_state.get("selected_layouts", [])

            for row_start in range(0, len(image_layouts), cols_per_row):
                row_items = image_layouts[row_start:row_start + cols_per_row]
                cols = st.columns(cols_per_row)

                for col, layout in zip(cols, row_items):
                    with col:
                        is_selected = any(
                            item["path"] == layout["path"]
                            for item in selected_layouts
                        )

                        st.markdown("**✅ Selected**" if is_selected else "** **")

                        st.image(layout["path"], width="stretch")
                        st.caption(layout["name"])

                        if st.button(
                            "Unselect" if is_selected else "Select",
                            key=f"select_{layout['path']}",
                            width="stretch",
                            type="primary" if is_selected else "secondary"
                        ):
                            if is_selected:
                                st.session_state["selected_layouts"] = [
                                    item for item in selected_layouts
                                    if item["path"] != layout["path"]
                                ]
                            else:
                                st.session_state["selected_layouts"] = selected_layouts + [{
                                    "name": layout["name"],
                                    "path": layout["path"],
                                    "type": layout.get("type", "")
                                }]
                            st.rerun()

                        if st.button(
                            "Delete",
                            key=f"delete_{layout['path']}",
                            width="stretch"
                        ):
                            try:
                                os.remove(layout["path"])

                                st.session_state["selected_layouts"] = [
                                    item for item in st.session_state.get("selected_layouts", [])
                                    if item["path"] != layout["path"]
                                ]
                                st.rerun()
                            except Exception as e:
                                st.error(f"Delete failed: {e}")
        else:
            st.info("No image layouts found.")
        existing_pptx_layouts=[]
        for layout in load_existing_templates():
            file_name=layout['name']
            
            
            
            tempo_parent_path=os.path.dirname(os.path.dirname(layout['path']))
            full_path=os.path.join(tempo_parent_path,f"{file_name}.pptx")
            existing_pptx_layouts.append(full_path)
            
     
        print(existing_pptx_layouts)

        selected_existing_names = []


        generate_clicked = st.button(
            "Generate Layouts",
            use_container_width=True,
            type="primary"
        )

        if generate_clicked:
            print("selected layout")
            print(st.session_state["selected_layouts"])
            if not website_url.strip():
                st.warning("Please enter a valid website URL.")
                st.stop()

            try:
                selected_paths = []

                selected_existing_names=[name['name'] for name in st.session_state["selected_layouts"] ]
                selected_paths = [
                                    path for path in existing_pptx_layouts
                                    if os.path.splitext(os.path.basename(path))[0] in selected_existing_names
                                ]
                print(selected_paths)
                

                if len(selected_paths) > 5:
                    st.warning("You can use a maximum of 5 layout templates.")
                    st.stop()

                st.session_state["current_template_paths"] = selected_paths

                payload = {
                    "link": website_url,
                    "template_paths": selected_paths,

                }
                print(f"payload: {payload}")

                status_box = st.empty()
                status_box.info("Sending request to backend...")

                with st.spinner("Generating layouts... Please wait..."):
                    response = requests.post(
                        f"{BACKEND_URL}/generate",
                        json=payload,
                        timeout=800
                    )

                if response.status_code != 200:
                    status_box.error("Generation failed.")
                    st.error(f"Backend error {response.status_code}")
                    st.code(response.text)
                    st.stop()
   

                print(f"Response: {response.text}")

                result = response.json()

                # save everything frontend needs
                st.session_state["generated_result"] = result
                st.session_state["generated_from_url"] = website_url
                st.session_state["generated_file_path"] = result.get("file_path")

                # directly use backend response
                st.session_state["generated_powerpoint_paths"] = result.get("powerpoint_paths", [])
                st.session_state["generated_png_image_paths"] = result.get("png_image_paths", [])

                st.session_state["generated_web_text"] = result.get("web_text", "")
                st.session_state["generated_placeholders"] = result.get("placeholders", [])

                status_box.success("Generation complete. Redirecting to customize page...")
                st.switch_page("pages/customize.py")

            except requests.exceptions.Timeout:
                st.error("Backend took too long to respond.")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

    with tab2:
        st.markdown("#### Generate from File")
        uploaded_template_files = None

        uploaded_template_files = st.file_uploader(
            "Upload new layout template files (.pptx)",
            type=["pptx"],
            accept_multiple_files=True,
            key="template_files_url"
        )