import sys
import streamlit as st
from dotenv import load_dotenv
import os

# Add the package directory to Python path
sys.path.append("streamlit_posit_app")

from pages.home import show_home_page

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")  # Changed from DATABASE_PATH to DATABASE_URL


def main():
    st.set_page_config(page_title="Streamlit Demo App", page_icon="👋", layout="wide")

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Home"])

    # Page routing
    if page == "Home":
        show_home_page(DATABASE_URL)


if __name__ == "__main__":
    main()
