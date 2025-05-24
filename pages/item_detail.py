import streamlit as st
from components.navigation import render_back_to_category_button

def render(app_data):
    """Render the item detail page."""
    selected_item = st.session_state.selected_item

    render_back_to_category_button()

    if selected_item:
        render_item_details(selected_item)

def render_item_details(selected_item):
    """Render detailed information about an item."""
    # Display images at the top
    images = selected_item.get("images", [])
    if images and len(images) > 0:
        st.subheader("IMAGES")
        image_cols = st.columns(min(len(images), 4))
        for i, image_url in enumerate(images):
            with image_cols[i % 4]:
                st.image(image_url, use_container_width=True)

    # Display the main title
    st.title(selected_item.get("title", "Untitled Item"))

    # Display all other key-value pairs and lists
    excluded_keys = ['images', 'title', 'generated_at', 'last_modified', 'references']
    for key, value in selected_item.items():
        if key not in excluded_keys:
            st.subheader(key.replace('_', ' ').upper())
            if isinstance(value, list):
                if value:
                    for item in value:
                        st.write(f"- {item}")
                else:
                    st.write("No items available.")
            elif isinstance(value, dict):
                st.json(value)
            else:
                st.write(value)