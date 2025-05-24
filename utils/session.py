import streamlit as st
from utils.router import router


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
    router.navigate_to_home()


def navigate_to_category(category_id):
    """Navigate to category detail page."""
    router.navigate_to_category(category_id)


def navigate_to_item(item):
    """Navigate to item detail page."""
    category_id = st.session_state.get('selected_category')
    router.navigate_to_item(item, category_id)


def back_to_category():
    """Navigate back to category detail page."""
    router.back_to_category()