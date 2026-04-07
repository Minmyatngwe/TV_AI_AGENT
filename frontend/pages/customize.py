import streamlit as st
import requests
import os
from pathlib import Path
import io 
import zipfile
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

if "show_form" not in st.session_state:
    st.session_state.show_form = False

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

# custom_prompt = st.text_area(
#     "Enter customization prompt",
#     placeholder="Example: Make the title shorter and more modern. Replace the image with a more technical one.",
#     height=120,
# )

# selected_slide_path = None
# if powerpoint_paths:
    
#     selected_slide_path = st.selectbox(
#         "Choose PowerPoint to customize",
#         options=[os.path.basename(i) for i in powerpoint_paths]
#     )

custom_prompt = st.text_area(
    "Enter customization prompt",
    placeholder="Example: Make the title shorter and more modern. Replace the image with a more technical one.",
    height=120,
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

left_col, sp1, middle_col, sp, right_col = st.columns([20,20,20,25,10])
    
with left_col:
    if st.button("Change image",type="primary"):
        
        try:
            payload = {
                "slide_path": [selected_slide_path],
                "number": image_counter,
                "ai_response": placeholders,
                "file_path": file_path
            }
            print(payload)
            with st.spinner("Changing image..."):
                response = requests.post(
                    f"{BACKEND_URL}/change_image",
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

with middle_col:
    if st.button("Apply Customization", type="primary", use_container_width=True):
        if not custom_prompt.strip():
            st.warning("Please enter a customization prompt.")
            st.stop()
        payload = {
            "web_text":web_text,
            "prompt":custom_prompt,
            "placeholder":placeholders,
            "slide_path": [selected_slide_path],
            "file_path": file_path
        }
        print(payload)
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

@st.dialog("Enter video settings")
def video_dialog():
    duration = st.number_input("Duration (Seconds)", 0, 10, 1)
    if st.button("OK"):
        payload = {
            "path": selected_slide_path,
            "duration": duration,
        }

        response = requests.post(f"{BACKEND_URL}/download", json=payload, timeout=600)

        if response.status_code == 200:
            video_path = response.json()["video_path"]
        else:
            st.error(response.text)
        powerpoint_path=os.path.dirname(os.path.dirname(video_path))
        powerpoint_full_path=os.path.join(powerpoint_path,"powerpoint",os.path.basename(selected_slide_path))
        zip_buffer=io.BytesIO()
        with zipfile.ZipFile(zip_buffer,"w",zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.write(video_path,arcname=os.path.basename(video_path))
            zip_file.write(powerpoint_full_path,arcname=os.path.basename(powerpoint_full_path))
        zip_buffer.seek(0)
            
        st.download_button(
            label="Download video + PowerPoint",
            data=zip_buffer,
            file_name="zip_file.zip",
            mime="application/zip"
        )




with right_col:
    if st.button("Download",type="primary"):
        video_dialog()
        
    
# with middle_col:
#     if st.button("Back to Home", type="secondary"):
#         st.switch_page("pages/home.py")