import streamlit as st

def load_css():
    with open("styles/main.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.set_page_config(
    page_title="TV AI Agent",
    page_icon="📺",
    layout="wide"
)

st.logo("logos/roboai.png", size="large")

pg = st.navigation([
    st.Page("pages/home.py", title="Home", icon=":material/home:"),
    st.Page("pages/customize.py", title="Customize", icon=":material/brush:"),
])

pg.run()