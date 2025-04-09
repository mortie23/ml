import streamlit as st


def show_home_page():
    st.title("👋 Welcome to the Demo App!")
    st.write(
        """
    This is a simple Streamlit application that will be deployed to Posit Connect.
    More features will be added later!
    """
    )

    if st.button("Click me!"):
        st.balloons()
