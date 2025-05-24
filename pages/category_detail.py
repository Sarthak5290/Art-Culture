import streamlit as st
from components.navigation import render_back_to_categories_button
from components.cards import (
    render_item_card,
    render_featured_card,
    render_compact_item_list,
)


def render(app_data):
    """Render the enhanced category detail page with improved layout."""
    selected_category_id = st.session_state.selected_category
    category_info = app_data.get(selected_category_id)

    if category_info:
        # Category header with hero styling - Updated for dark theme with moved up positioning
        st.markdown(
            f"""
        <div style="background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end)); padding: 2.5rem 2rem; margin: -1rem -1rem 2rem -1rem; border-radius: 0 0 25px 25px; text-align: center; border-bottom: 2px solid var(--border-color);">
            <h1 class="section-title" style="margin: 0; font-size: 2.8rem; color: var(--text-light);">{category_info['displayTitle']}</h1>
            <p style="font-size: 1.1rem; color: var(--text-secondary); margin-top: 1rem; font-style: italic;">
                {category_info['displayDescription']}
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        items = category_info.get("items", [])

        if not items:
            st.markdown(
                """
            <div style="text-align: center; padding: 3rem; background: var(--card-bg); border-radius: 20px; margin: 2rem 0; border: 1px solid var(--border-color);">
                <h3 style="color: var(--text-secondary);">🎨 No items found</h3>
                <p style="color: var(--text-muted);">We're working on adding more content to this category. Check back soon!</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            # Show item count and category stats - Updated for dark theme
            st.markdown(
                f"""
             <div style="background: #1E1E1E; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 16px rgba(0,0,0,0.4); border: 1px solid #30363D;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #FFFFFF;">📚 Collection Overview</h4>
                    <p style="margin: 0.5rem 0 0 0; color: #B8BCC8;">Discover {len(items)} amazing pieces in this collection</p>
                </div>
                <div style="text-align: right;">
                    <span style="background: #FFD700; color: #0E1117; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600; box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);">
                        {len(items)} Items
                    </span>
                </div>
            </div>
             </div>
            """,
                unsafe_allow_html=True,
            )

            # Featured item (if we have items)
            if len(items) > 0:
                st.markdown("### ⭐ Featured Item")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    render_featured_card(
                        items[0], selected_category_id, 0, is_featured=True
                    )

                st.markdown("<br>", unsafe_allow_html=True)

            # Layout options for items
            layout_col1, layout_col2 = st.columns([3, 1])

            with layout_col1:
                st.markdown("### 🎯 All Items in this Category")

            with layout_col2:
                view_mode = st.selectbox(
                    "View as:",
                    ["Grid", "List", "Compact"],
                    key=f"view_mode_{selected_category_id}",
                )

            # Render items based on selected view mode
            if view_mode == "Grid":
                render_grid_view(items, selected_category_id)
            elif view_mode == "List":
                render_list_view(items, selected_category_id)
            else:  # Compact
                render_compact_item_list(items, selected_category_id)


def render_grid_view(items, category_id):
    """Render items in a responsive grid layout."""
    # Skip the first item since it's featured
    items_to_show = items[1:] if len(items) > 1 else items

    if not items_to_show:
        st.info("No additional items to display.")
        return

    # Create responsive grid
    items_per_row = 3
    for i in range(0, len(items_to_show), items_per_row):
        cols = st.columns(items_per_row)

        for j in range(items_per_row):
            item_index = i + j
            if item_index < len(items_to_show):
                with cols[j]:
                    render_item_card(
                        items_to_show[item_index], category_id, item_index + 1
                    )


def render_list_view(items, category_id):
    """Render items in a detailed list layout."""
    items_to_show = items[1:] if len(items) > 1 else items

    if not items_to_show:
        st.info("No additional items to display.")
        return

    for i, item in enumerate(items_to_show):
        render_detailed_list_item(item, category_id, i + 1)
        if i < len(items_to_show) - 1:
            st.markdown("---")


def render_detailed_list_item(item, category_id, item_index):
    """Render a single item in detailed list format."""
    from components.cards import get_item_image_url, get_item_preview

    image_url = get_item_image_url(item)
    item_title = item.get("title", "Untitled Item")
    preview_text = get_item_preview(item)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(image_url, use_container_width=True)

    with col2:
        st.markdown(
            f"""
        <div style="padding-left: 1.5rem;">
            <h4 style="color: var(--text-light); margin-bottom: 0.8rem; font-size: 1.4rem;">{item_title}</h4>
            <p style="color: var(--text-secondary); line-height: 1.6; margin-bottom: 1.5rem;">{preview_text}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(
            "🔍 Explore Details",
            key=f"list_item_{category_id}_{item_index}",
            help=f"Learn more about {item_title}",
        ):
            from utils.session import navigate_to_item

            navigate_to_item(item)
