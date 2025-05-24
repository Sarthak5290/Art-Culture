import streamlit as st
from utils.session import navigate_to_home, back_to_category


def render_back_to_categories_button():
    """Render a compact, left-aligned back to categories button."""
    st.markdown("""
    <style>
    .compact-nav-button button {
        background: #1E3A5F !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.3rem 0.6rem !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        border: none !important;
        width: auto !important;
        min-width: 80px !important;
        max-width: 90px !important;
        transition: all 0.3s ease !important;
        margin: 0 !important;
    }
    
    .compact-nav-button button:hover {
        background: #4A90E2 !important;
        transform: translateX(-1px) !important;
    }
    
    .compact-nav-button {
        text-align: left !important;
        margin-bottom: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="compact-nav-button">', unsafe_allow_html=True)
    if st.button("◀ Categories", key="back_to_categories", help="Return to the main categories page"):
        navigate_to_home()
    st.markdown('</div>', unsafe_allow_html=True)


def render_back_to_category_button():
    """Render a compact, left-aligned back to category button."""
    st.markdown("""
    <style>
    .compact-nav-button button {
        background: #1E3A5F !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.3rem 0.6rem !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        border: none !important;
        width: auto !important;
        min-width: 80px !important;
        max-width: 90px !important;
        transition: all 0.3s ease !important;
        margin: 0 !important;
    }
    
    .compact-nav-button button:hover {
        background: #4A90E2 !important;
        transform: translateX(-1px) !important;
    }
    
    .compact-nav-button {
        text-align: left !important;
        margin-bottom: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="compact-nav-button">', unsafe_allow_html=True)
    if st.button("◀ Category", key="back_to_category", help="Return to the category overview"):
        back_to_category()
    st.markdown('</div>', unsafe_allow_html=True)


def render_breadcrumb_navigation():
    """Render breadcrumb navigation for better user orientation."""
    breadcrumbs = []
    
    if st.session_state.view == 'home':
        breadcrumbs = ["🏠 Home"]
    elif st.session_state.view == 'category_detail':
        category_id = st.session_state.selected_category
        if category_id:
            breadcrumbs = ["🏠 Home", f"📂 {format_category_name(category_id)}"]
    elif st.session_state.view == 'item_detail':
        category_id = st.session_state.selected_category
        item_title = st.session_state.selected_item.get("title", "Item") if st.session_state.selected_item else "Item"
        if category_id:
            breadcrumbs = ["🏠 Home", f"📂 {format_category_name(category_id)}", f"📄 {item_title}"]
    
    if len(breadcrumbs) > 1:
        breadcrumb_html = " → ".join(breadcrumbs)
        st.markdown(f"""
        <div style="background: white; padding: 0.8rem 1rem; border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-left: 4px solid #4A90E2; text-align: left; max-width: 400px;">
            <p style="margin: 0; color: #666; font-size: 0.85rem;">
                {breadcrumb_html}
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_navigation_header():
    """Render a comprehensive navigation header."""
    if st.session_state.view != 'home':
        st.markdown("""
        <style>
        .compact-home-button button {
            background: #1E3A5F !important;
            color: white !important;
            border-radius: 12px !important;
            padding: 0.3rem 0.6rem !important;
            font-size: 0.75rem !important;
            font-weight: 500 !important;
            border: none !important;
            width: auto !important;
            min-width: 70px !important;
            max-width: 80px !important;
            transition: all 0.3s ease !important;
            margin: 0 0 1rem 0 !important;
        }
        
        .compact-home-button button:hover {
            background: #4A90E2 !important;
            transform: translateX(-1px) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="compact-home-button">', unsafe_allow_html=True)
        if st.button("🏠 Home", key="nav_home", help="Go to main page"):
            navigate_to_home()
        st.markdown('</div>', unsafe_allow_html=True)
    
    render_breadcrumb_navigation()


def render_quick_navigation(app_data):
    """Render quick navigation menu for easy category switching."""
    if st.session_state.view != 'home' and app_data:
        st.markdown("### Quick Navigation")
        
        categories = list(app_data.keys())
        category_names = [format_category_name(cat_id) for cat_id in categories]
        
        # Create a horizontal navigation menu
        nav_cols = st.columns(len(categories))
        
        for i, (cat_id, cat_name) in enumerate(zip(categories, category_names)):
            with nav_cols[i]:
                is_current = st.session_state.selected_category == cat_id
                button_style = "🔍" if is_current else "📂"
                
                if st.button(f"{button_style} {cat_name}", 
                           key=f"quick_nav_{cat_id}", 
                           help=f"Go to {cat_name}",
                           disabled=is_current):
                    from utils.session import navigate_to_category
                    navigate_to_category(cat_id)


def format_category_name(category_id):
    """Format category ID into a readable name."""
    name_mappings = {
        "sculptures_architecture": "Sculptures & Architecture",
        "handicrafts_paintings": "Handicrafts & Paintings", 
        "performing_arts_festivals": "Performing Arts & Festivals",
        "artists": "Artists"
    }
    
    return name_mappings.get(category_id, category_id.replace('_', ' ').title())


def render_floating_navigation():
    """Render a floating navigation button for mobile-friendly experience."""
    # This creates a floating action button for better mobile navigation
    if st.session_state.view != 'home':
        st.markdown("""
        <div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
            <div style="background: #4A90E2; color: white; border-radius: 50%; width: 56px; height: 56px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 16px rgba(0,0,0,0.2); cursor: pointer; transition: all 0.3s ease;">
                🏠
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar_navigation(app_data):
    """Render navigation in sidebar for better space utilization."""
    with st.sidebar:
        st.markdown("## Navigation")
        
        # Home button
        if st.button("🏠 Home", key="sidebar_home", use_container_width=True):
            navigate_to_home()
        
        st.markdown("---")
        
        # Category navigation
        if app_data:
            st.markdown("### Categories")
            for cat_id in app_data.keys():
                cat_name = format_category_name(cat_id)
                is_current = st.session_state.selected_category == cat_id
                
                if st.button(
                    f"{'🔍' if is_current else '📂'} {cat_name}",
                    key=f"sidebar_cat_{cat_id}",
                    use_container_width=True,
                    disabled=is_current
                ):
                    from utils.session import navigate_to_category
                    navigate_to_category(cat_id)
        
        # Additional sidebar content
        st.markdown("---")
        st.markdown("""
        ### About
        Explore the rich world of art and culture through our curated collections.
        
        ### Features
        - 🎨 Diverse art categories
        - 🖼️ High-quality images
        - 📚 Detailed information
        - 🔍 Easy navigation
        """)
        
        # Theme toggle (placeholder for future implementation)
        st.markdown("---")
        if st.button("🌙 Dark Mode", key="theme_toggle", use_container_width=True):
            st.info("Dark mode coming soon!")