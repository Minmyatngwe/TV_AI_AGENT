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
    st.session_state["selected_layout"] = None

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

        #layouts = load_existing_templates()

        # if layouts:
        #     for i, layout in enumerate(layouts):
        #         row1, row2 = st.columns([6, 2])

        #         with row1:
        #             file_ext = layout.get("type", "").lower()

        #             if file_ext in [".png", ".jpg", ".jpeg", ".webp"]:
        #                 label = f"🖼️ {layout['name']}"
        #             #elif file_ext == ".pptx":
        #             #    label = f"📄 {layout['name']}"
        #             else:
        #                 label = f"📁 {layout['name']}"

        #             if st.button(label, key=f"layout_{i}", use_container_width=True):
        #                 st.session_state["selected_layout"] = layout
        #                 st.switch_page("pages/layout_preview.py")

        #         with row2:
        #             if st.button("Delete", key=f"delete_{i}", use_container_width=True, type="secondary"):
        #                 try:
        #                     os.remove(layout["path"])

        #                     selected = st.session_state.get("selected_layout")
        #                     if selected and selected["path"] == layout["path"]:
        #                         st.session_state["selected_layout"] = None

        #                     st.rerun()
        #                 except Exception as e:
        #                     st.error(f"Delete failed: {e}")
        # else:
        #     st.info("No layouts found.")

        image_layouts = load_existing_templates()

        if image_layouts:
            st.markdown("#### Available Layouts")

            cols_per_row = 3
            selected_layout = st.session_state.get("selected_layout")

            for row_start in range(0, len(image_layouts), cols_per_row):
                row_items = image_layouts[row_start:row_start + cols_per_row]
                cols = st.columns(cols_per_row)

                for col, layout in zip(cols, row_items):
                    with col:
                        is_selected = (
                            selected_layout is not None
                            and selected_layout.get("path") == layout.get("path")
                        )

                        if is_selected:
                            st.markdown("**✅ Selected**")
                        else:
                            st.markdown("** **")

                        st.image(layout["path"], use_container_width=True)
                        st.caption(layout["name"])

                        if st.button(
                            "Select" if not is_selected else "Selected",
                            key=f"select_{layout['path']}",
                            use_container_width=True,
                            type="primary" if is_selected else "secondary"
                        ):
                            st.session_state["selected_layout"] = layout
                            st.rerun()

                        if st.button(
                            "Delete",
                            key=f"delete_{layout['path']}",
                            use_container_width=True
                        ):
                            try:
                                os.remove(layout["path"])

                                selected = st.session_state.get("selected_layout")
                                if selected and selected["path"] == layout["path"]:
                                    st.session_state["selected_layout"] = None

                                st.rerun()
                            except Exception as e:
                                st.error(f"Delete failed: {e}")
        else:
            st.info("No image layouts found.")

        # layout_source = st.radio(
        #     "Layout source",
        #     ["Use existing layouts", "Upload new layouts"],
        #     horizontal=True
        # )

        existing_pptx_layouts = [
            layout for layout in load_existing_templates()
            if layout["type"].lower() == ".pptx"
        ]

        selected_existing_names = []
        uploaded_template_files = None

        # if layout_source == "Use existing layouts":
        #     if existing_pptx_layouts:
        #         selected_existing_names = st.multiselect(
        #             "Select existing layout templates",
        #             options=[layout["name"] for layout in existing_pptx_layouts],
        #             default=[]
        #         )
        #     else:
        #         st.info("No existing PPTX layouts found. Please upload a new one.")

        #else:
        uploaded_template_files = st.file_uploader(
            "Upload new layout template files (.pptx)",
            type=["pptx"],
            accept_multiple_files=True,
            key="template_files_url"
        )

        layout_count = st.number_input(
            "How many layouts do you need?",
            min_value=1,
            max_value=5,
            value=1,
            step=1
        )

        generate_clicked = st.button(
            "Generate Layouts",
            use_container_width=True,
            type="primary"
        )

        if generate_clicked:
            if not website_url.strip():
                st.warning("Please enter a valid website URL.")
                st.stop()

            try:
                selected_paths = []

                #if layout_source == "Use existing layouts":
                #    if not selected_existing_names:
                #        st.warning("Please select at least one existing PPTX layout.")
                #        st.stop()

                selected_paths = [
                        layout["path"]
                        for layout in existing_pptx_layouts
                        if layout["name"] in selected_existing_names
                    ]

                #else:
                #    if not uploaded_template_files:
                #        st.warning("Please upload at least one PPTX template file.")
                #        st.stop()

                selected_paths = [save_uploaded_template(f) for f in uploaded_template_files]

                if len(selected_paths) > 5:
                    st.warning("You can use a maximum of 5 layout templates.")
                    st.stop()

                st.session_state["current_template_paths"] = selected_paths

                payload = {
                    "link": website_url,
                    "template_paths": selected_paths,
                    "layout_count": int(layout_count)
                }

                status_box = st.empty()
                status_box.info("Sending request to backend...")

                with st.spinner("Generating layouts... Please wait..."):
                    response = requests.post(
                        f"{BACKEND_URL}/generate",
                        json=payload,
                        timeout=300
                    )

                if response.status_code != 200:
                    status_box.error("Generation failed.")
                    st.error(f"Backend error {response.status_code}")
                    st.code(response.text)
                    st.stop()

                result = response.json()

                # save everything frontend needs
                st.session_state["generated_result"] = result
                st.session_state["generated_from_url"] = website_url
                st.session_state["generated_file_path"] = result.get("file_path")
                st.session_state["generated_powerpoint_paths"] = result.get("powerpoint_paths", [])
                st.session_state["generated_png_image_paths"] = result.get("png_image_paths", [])
                st.session_state["generated_web_text"] = result.get("web_text", "")
                st.session_state["generated_placeholders"] = result.get("placeholders", [])
                st.session_state["layout_count"] = int(layout_count)

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
        st.caption("This tab is UI-only for now.")

# with right_col:
#     st.markdown('<div class="layout-title">Current Layouts</div>', unsafe_allow_html=True)

#     layouts = load_existing_templates()

#     if layouts:
#         for i, layout in enumerate(layouts):
#             row1, row2 = st.columns([6, 2])

#             with row1:
#                 file_ext = layout.get("type", "").lower()

#                 if file_ext in [".png", ".jpg", ".jpeg", ".webp"]:
#                     label = f"🖼️ {layout['name']}"
#                 elif file_ext == ".pptx":
#                     label = f"📄 {layout['name']}"
#                 else:
#                     label = f"📁 {layout['name']}"

#                 if st.button(label, key=f"layout_{i}", use_container_width=True):
#                     st.session_state["selected_layout"] = layout
#                     st.switch_page("pages/layout_preview.py")

#             with row2:
#                 if st.button("Delete", key=f"delete_{i}", use_container_width=True, type="secondary"):
#                     try:
#                         os.remove(layout["path"])

#                         selected = st.session_state.get("selected_layout")
#                         if selected and selected["path"] == layout["path"]:
#                             st.session_state["selected_layout"] = None

#                         st.rerun()
#                     except Exception as e:
#                         st.error(f"Delete failed: {e}")
#     else:
#         st.info("No layouts found.")