import streamlit as st

# Create or get the session state
def get_session_state():
    if 'session_state' not in st.session_state:
        st.session_state.session_state = {}

    return st.session_state.session_state
