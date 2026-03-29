import streamlit as st
from pathlib import Path

st.title("Customize Layout")

result = st.session_state.get("generated_result")

if not result:
    st.warning("No generated layout found. Please generate first.")
    st.stop()

file_path = result.get("file_path")
powerpoint_paths = result.get("powerpoint_paths", [])
png_image_path = result.get("png_image_path")

st.write("### Generated Output")
st.write("**Folder Path:**", file_path)
st.write("**PowerPoint Files:**", powerpoint_paths)
st.write("**Preview Image Path:**", png_image_path)

if png_image_path:
    try:
        st.image(png_image_path, caption="Generated Layout Preview", use_container_width=True)
    except Exception as e:
        st.error(f"Could not load preview image: {e}")

if powerpoint_paths:
    st.write("### Generated PowerPoints")
    for ppt in powerpoint_paths:
        st.write(ppt)