import streamlit as st

st.markdown('<div class="hero-title">Generate Layouts</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Paste a link or upload a file, then use a reference layout if available</div>',
    unsafe_allow_html=True
)

# Initialize session state
if "reference_layout" not in st.session_state:
    st.session_state["reference_layout"] = None

if "reference_layout_name" not in st.session_state:
    st.session_state["reference_layout_name"] = None

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

            reference_file_url = st.file_uploader(
                "Upload reference layout image",
                type=["png", "jpg", "jpeg"],
                key="reference_file_url"
            )

            url_submit = st.form_submit_button(
                "Generate Layouts",
                use_container_width=True
            )

        if url_submit:
            if website_url.strip():
                st.session_state["input_type"] = "url"
                st.session_state["website_url"] = website_url

                if reference_file_url is not None:
                    st.session_state["reference_layout"] = reference_file_url
                    st.session_state["reference_layout_name"] = reference_file_url.name

                st.success("URL captured successfully.")
            else:
                st.warning("Please enter a valid website link.")

    with tab2:
        with st.form("file_form"):
            st.markdown("#### Generate from File")

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
            if uploaded_file is not None:
                st.session_state["input_type"] = "file"
                st.session_state["uploaded_file_name"] = uploaded_file.name

                if reference_file_upload is not None:
                    st.session_state["reference_layout"] = reference_file_upload
                    st.session_state["reference_layout_name"] = reference_file_upload.name

                st.success("File captured successfully.")
            else:
                st.warning("Please upload a source file.")

with right_col:
    st.markdown('<div class="layout-title">Current Layout</div>', unsafe_allow_html=True)
    st.markdown('<div class="layout-preview-box">', unsafe_allow_html=True)

    if st.session_state["reference_layout"] is not None:
        st.image(
            st.session_state["reference_layout"],
            caption=st.session_state["reference_layout_name"],
            use_container_width=True
        )
    else:
        st.info("No current layout uploaded.")
    st.markdown("</div>", unsafe_allow_html=True)