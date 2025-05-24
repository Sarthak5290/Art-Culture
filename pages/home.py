import streamlit as st
from components.cards import render_category_card

def render(app_data):
    """Render the home page with category cards."""
    st.title("Art & Culture")
    st.header("Categories")

    # Create a grid layout for category cards using columns
    categories = list(app_data.keys())
    cols = st.columns(len(categories))

    for i, category_id in enumerate(categories):
        category_info = app_data[category_id]
        with cols[i]:
            render_category_card(category_id, category_info)