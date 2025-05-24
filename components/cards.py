import streamlit as st
from utils.session import navigate_to_category, navigate_to_item

def render_category_card(category_id, category_info):
    """Render a category card with image, title, description and explore button."""
    with st.container(border=True):
        st.image(category_info["mainCardImage"], use_container_width=True)
        st.subheader(category_info["displayTitle"])
        st.write(category_info["displayDescription"])
        if st.button(f"Explore {category_info['displayTitle']}", key=f"explore_cat_{category_id}"):
            navigate_to_category(category_id)

def render_item_card(item, category_id, item_index):
    """Render an item card with image, title and view details button."""
    with st.container(border=True):
        # Use the first image from the 'images' array, or a placeholder
        image_url = (item.get("images") and len(item["images"]) > 0) \
                    and item["images"][0] or 'https://via.placeholder.com/150?text=No+Image'
        st.image(image_url, use_container_width=True)
        st.subheader(item.get("title", "Untitled Item"))
        if st.button("View Details", key=f"view_item_{category_id}_{item_index}"):
            navigate_to_item(item)