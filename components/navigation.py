import streamlit as st
from utils.session import navigate_to_home, back_to_category

def render_back_to_categories_button():
    """Render back to categories button."""
    if st.button("← Back to Categories"):
        navigate_to_home()

def render_back_to_category_button():
    """Render back to category button."""
    if st.button("← Back to Category"):
        back_to_category()