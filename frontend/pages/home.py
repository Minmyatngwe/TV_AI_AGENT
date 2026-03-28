import streamlit as st

st.markdown('<div class="hero-title">Generate Layouts</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Paste a link or upload a file</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["URL", "File"])

with tab1:
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        with st.form("url_form"):
            website_url = st.text_input(
                "Enter the URL",
                placeholder="https://example.com",
            )

            reference_file = st.file_uploader(
                "Layout File",
                type=["png", "jpg", "jpeg", "pdf", "pptx"],
                key="reference_file"
            )

            url_submit = st.form_submit_button(
                "Generate Layouts",
                use_container_width=True
            )

        if url_submit:
            if website_url.strip():
                st.session_state["input_type"] = "url"
                st.session_state["website_url"] = website_url

                if reference_file is not None:
                    st.session_state["reference_file_name"] = reference_file.name

                st.success(f"URL captured: {website_url}")
            else:
                st.warning("Please enter a valid link.")

with tab2:
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        with st.form("file_form"):
            uploaded_file = st.file_uploader(
                "Upload a file",
                type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
                key="source_file"
            )

            file_submit = st.form_submit_button(
                "Generate Layouts",
                use_container_width=True
            )

        if file_submit:
            if uploaded_file is not None:
                st.session_state["input_type"] = "file"
                st.session_state["uploaded_file_name"] = uploaded_file.name
                st.success(f"File captured: {uploaded_file.name}")
            else:
                st.warning("Please upload a file.")