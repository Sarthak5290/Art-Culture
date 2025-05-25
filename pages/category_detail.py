import streamlit as st
from components.navigation import render_back_to_categories_button
from components.cards import (
    render_item_card,
    render_featured_card,
    render_compact_item_list,
)


def ensure_top_scroll():
    """Ensure the page scrolls to top when loaded."""
    st.markdown(
        """
    <script>
        // Immediate scroll to top
        window.scrollTo(0, 0);
        document.documentElement.scrollTop = 0;
        document.body.scrollTop = 0;
        
        // Backup methods
        setTimeout(() => {
            window.scrollTo(0, 0);
            document.documentElement.scrollTop = 0;
            document.body.scrollTop = 0;
        }, 100);
    </script>
    """,
        unsafe_allow_html=True,
    )


def render(app_data):
    ensure_top_scroll()

    """Render the enhanced category detail page with improved layout."""
    selected_category_id = st.session_state.selected_category
    category_info = app_data.get(selected_category_id)

    if category_info:
        # Category header with hero styling and embedded back arrow
        st.markdown(
            f"""
<style>
.background-overlay {{
    background: rgba(0, 0, 0, 0.5);
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    border-radius: 0 0 25px 25px;
}}
</style>

<div style="
    background: url('https://images.unsplash.com/photo-1541961017774-22349e4a1262?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    padding: 2.5rem 2rem; 
    margin: -1rem -1rem 2rem -1rem; 
    border-radius: 0 0 25px 25px; 
    text-align: center; 
    border-bottom: 2px solid var(--border-color); 
    box-shadow: 0 4px 20px var(--shadow-light); 
    position: relative;
">
    <div class="background-overlay"></div>
    <div style="position: relative; z-index: 1;">
        <h1 class="section-title" style="
            margin: 0; 
            font-size: 2.8rem; 
            color: white; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            font-weight: 700;
        ">
            {category_info['displayTitle']}
        </h1>
        <p style="
            font-size: 1.1rem; 
            color: rgba(255, 255, 255, 0.9); 
            margin-top: 1rem; 
            font-style: italic;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            font-weight: 400;
        ">
            {category_info['displayDescription']}
        </p>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        # Small back arrow button placed after the header
        col1, col2, col3 = st.columns([1, 6, 1])
        with col1:
            st.markdown(
                """
            <style>
            .small-back-btn button {
    position: absolute !important;
    left: 25px !important;
    top: 25px !important;
    background: var(--primary-blue) !important;
    color: white !important;
    border: none !important;
    border-radius: 50% !important;
    width: 40px !important;
    height: 40px !important;
    font-size: 1.2rem !important;
    font-weight: bold !important;
    margin-top: -30px !important;
    margin-bottom: 1rem !important;
    box-shadow: 0 4px 12px var(--shadow-medium) !important;
    transition: all 0.3s ease !important;
}

            
            .small-back-btn button:hover {
                background: var(--secondary-blue) !important;
                transform: scale(1.1) !important;
                box-shadow: 0 6px 16px var(--shadow-strong) !important;
            }
            </style>
            """,
                unsafe_allow_html=True,
            )

            st.markdown('<div class="small-back-btn">', unsafe_allow_html=True)
            if st.button("←", key="back_arrow", help="Go back to categories"):
                from utils.session import navigate_to_home

                navigate_to_home()
            st.markdown("</div>", unsafe_allow_html=True)

        items = category_info.get("items", [])

        if not items:
            st.markdown(
                """
            <div style="text-align: center; padding: 3rem; background: var(--card-bg); border-radius: 20px; margin: 2rem 0; border: 1px solid var(--border-color); box-shadow: 0 4px 16px var(--shadow-light);">
                <h3 style="color: var(--text-secondary);">🎨 No items found</h3>
                <p style="color: var(--text-muted);">We're working on adding more content to this category. Check back soon!</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            # Show item count and category stats - Updated for light-blue theme
            st.markdown(
                f"""
             <div style="background: var(--card-bg); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 16px var(--shadow-light); border: 1px solid var(--border-color);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: var(--text-dark);">📚 Collection Overview</h4>
                    <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">Discover {len(items)} amazing pieces in this collection</p>
                </div>
                <div style="text-align: right;">
                    <span style="background: var(--highlight-color); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600; box-shadow: 0 2px 8px rgba(255, 152, 0, 0.3);">
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
            <h4 style="color: var(--text-dark); margin-bottom: 0.8rem; font-size: 1.4rem;">{item_title}</h4>
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
