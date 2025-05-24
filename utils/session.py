import streamlit as st

def initialize_session_state():
    """Initialize session state variables if not already set."""
    if 'view' not in st.session_state:
        st.session_state.view = 'home'
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None
    if 'selected_item' not in st.session_state:
        st.session_state.selected_item = None

def navigate_to_home():
    """Navigate to home page and clear selections."""
    st.session_state.view = 'home'
    st.session_state.selected_category = None
    st.session_state.selected_item = None
    st.rerun()

def navigate_to_category(category_id):
    """Navigate to category detail page."""
    st.session_state.view = 'category_detail'
    st.session_state.selected_category = category_id
    st.rerun()

def navigate_to_item(item):
    """Navigate to item detail page."""
    st.session_state.view = 'item_detail'
    st.session_state.selected_item = item
    st.rerun()

def back_to_category():
    """Navigate back to category detail page."""
    st.session_state.view = 'category_detail'
    st.session_state.selected_item = None
    st.rerun()