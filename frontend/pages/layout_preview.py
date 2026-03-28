import streamlit as st
from pathlib import Path

selected = st.session_state.get("selected_layout")

if not selected:
    st.warning("No layout selected.")
    if st.button("Back"):
        st.switch_page("pages/home.py")
    st.stop()

st.markdown("## Layout Preview")

file_type = selected.get("type", "").lower()

if file_type in [".png", ".jpg", ".jpeg", ".webp"]:
    st.image(selected["path"], use_container_width=True)
elif file_type == ".pptx":
    st.info("PowerPoint preview is not available as an image yet.")
    st.write(f"Selected file: {selected['name']}")
    st.code(selected["path"])
else:
    st.warning("Unsupported file type.")

if st.button("← Back"):
    st.switch_page("pages/home.py")