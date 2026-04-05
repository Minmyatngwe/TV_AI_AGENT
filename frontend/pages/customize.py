import streamlit as st
import requests
import os
from pathlib import Path
BACKEND_URL = "http://127.0.0.1:8000"

st.markdown('<div class="hero-title">Customize Layouts</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Review and customize the generated layouts</div>',
    unsafe_allow_html=True
)

generated_result = st.session_state.get("generated_result")
file_path = st.session_state.get("generated_file_path")
powerpoint_paths = st.session_state.get("generated_powerpoint_paths", [])
png_image_paths = st.session_state.get("generated_png_image_paths", [])
web_text = st.session_state.get("generated_web_text", "")
placeholders = st.session_state.get("generated_placeholders", [])
image_counter=st.session_state.get("image_counter") or 0
if not generated_result:
    st.warning("No generated layout data found. Please generate layouts first.")
    if st.button("Go to Home", type="primary"):
        st.switch_page("pages/home.py")
    st.stop()

st.write("### Generated Layout Previews")

if png_image_paths:
    cwd=os.getcwd()
    cwd=Path(cwd).parent
    backend_path=cwd/"backend"
    
    cols = st.columns(2)
    for i, image_path in enumerate(png_image_paths):
        slide_name=os.path.basename(image_path)
        real_path=Path(image_path)
        full_path=backend_path/real_path
        print(full_path)
        with cols[i % 2]:
            st.image(full_path, caption=slide_name, use_container_width=True)
else:
    st.info("No preview images found.")

# st.write("### Generated PowerPoint Files")
# if powerpoint_paths:
#     for ppt in powerpoint_paths:
#         st.code(ppt)
# else:
#     st.info("No generated PowerPoint files found.")

# st.write("### Source Web Text")
# if web_text:
#     with st.expander("Show extracted web text"):
#         st.write(web_text)

#st.write("### Placeholder Data")
#if placeholders:
#    st.json(placeholders)
#else:
#    st.info("No placeholder data found.")


st.write("### Customize Content")

custom_prompt = st.text_area(
    "Enter customization prompt",
    placeholder="Example: Make the title shorter and more modern. Replace the image with a more technical one.",
    height=120
)

selected_slide_path = None
if powerpoint_paths:
    
    choose  = st.selectbox(
        "Choose PowerPoint to customize",
        options=[os.path.basename(i) for i in powerpoint_paths]
    )
    for i in powerpoint_paths:
        if os.path.basename(i)==choose:
            selected_slide_path=i

if st.button("Apply Customization", type="primary", use_container_width=True):
    if not custom_prompt.strip():
        st.warning("Please enter a customization prompt.")
        st.stop()

    if not selected_slide_path:
        st.warning("No PowerPoint file selected.")
        st.stop()

    try:
        payload = {
            "web_text": web_text,
            "prompt": custom_prompt,
            "placeholder": placeholders,
            "slide_path": [selected_slide_path],
            "file_path": file_path
        }

        with st.spinner("Applying customization..."):
            response = requests.post(
                f"{BACKEND_URL}/cutomize",
                json=payload,
                timeout=600
            )

        if response.status_code != 200:
            st.error(f"Backend error {response.status_code}")
            st.code(response.text)
            st.stop()

        st.session_state["generated_placeholders"]=response.json().get("ai_response")
        st.success("Customization complete.")
        st.rerun()

    except requests.exceptions.Timeout:
        st.error("Customization request timed out.")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")


if st.button("Chnage image",type="primary"):
    
    try:
        payload = {
            "slide_path": [selected_slide_path],
            "number": image_counter,
            "ai_response": placeholders,
            "file_path": file_path
        }
        print(payload)
        with st.spinner("Channging image..."):
            response = requests.post(
                f"{BACKEND_URL}/chnage_image",
                json=payload,
                timeout=600
            )

        if response.status_code != 200:
            st.error(f"Backend error {response.status_code}")
            st.code(response.text)
            st.stop()
        st.session_state["image_counter"]=response.json().get('image_counter',0)

        st.success("Customization complete.")
        st.rerun()
    except requests.exceptions.Timeout:
        st.error("Customization request timed out.")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")


    

if st.button("Back to Home", type="secondary"):
    st.switch_page("pages/home.py")