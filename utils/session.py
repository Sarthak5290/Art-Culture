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
    if not category_id:
        # If no category is selected, we can't navigate to item
        # This shouldn't happen in normal flow, but handle gracefully
        st.error("Cannot navigate to item without selecting a category first.")
        return
    
    router.navigate_to_item(item, category_id)


def back_to_category():
    """Navigate back to category detail page."""
    router.back_to_category()


def get_current_view():
    """Get the current view from session state."""
    return st.session_state.get('view', 'home')


def get_selected_category():
    """Get the currently selected category."""
    return st.session_state.get('selected_category')


def get_selected_item():
    """Get the currently selected item."""
    return st.session_state.get('selected_item')


def set_view(view_name):
    """Set the current view (use with caution - prefer navigation methods)."""
    st.session_state.view = view_name