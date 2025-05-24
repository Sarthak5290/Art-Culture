import streamlit as st
from components.navigation import render_back_to_categories_button
from components.cards import render_item_card

def render(app_data):
    """Render the category detail page with item cards."""
    selected_category_id = st.session_state.selected_category
    category_info = app_data.get(selected_category_id)

    render_back_to_categories_button()

    if category_info:
        st.header(category_info["displayTitle"])

        items = category_info.get("items", [])
        if not items:
            st.info(f"No items found for {category_info['displayTitle']}.")
        else:
            # Create a grid layout for item cards
            item_cols = st.columns(4)
            col_index = 0
            
            for i, item in enumerate(items):
                with item_cols[col_index]:
                    render_item_card(item, selected_category_id, i)
                col_index = (col_index + 1) % 4