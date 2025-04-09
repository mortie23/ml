import streamlit as st
from streamlit_posit_app.pages.home import show_home_page  # Updated import path


def main():
    st.set_page_config(page_title="Streamlit Demo App", page_icon="👋", layout="wide")

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Home"])

    # Page routing
    if page == "Home":
        show_home_page()


if __name__ == "__main__":
    main()
