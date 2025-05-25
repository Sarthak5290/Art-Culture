import streamlit as st
from utils.session import navigate_to_home, back_to_category, navigate_to_category


def render_back_to_categories_button():
    """Render a compact, left-aligned back to categories button."""
    st.markdown(
        """
    <style>
    .compact-nav-button button {
        background: var(--surface-bg) !important;
        color: var(--text-primary) !important;
        border-radius: 12px !important;
        padding: 0.3rem 0.6rem !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        border: 1px solid var(--border-color) !important;
        width: auto !important;
        min-width: 80px !important;
        max-width: 90px !important;
        transition: all 0.3s ease !important;
        margin: 0 !important;
        box-shadow: 0 2px 4px var(--shadow-light) !important;
    }
    
    .compact-nav-button button:hover {
        background: var(--primary-blue) !important;
        color: white !important;
        transform: translateX(-1px) !important;
        border-color: var(--primary-blue) !important;
        box-shadow: 0 4px 8px var(--shadow-medium) !important;
    }
    
    .compact-nav-button {
        text-align: left !important;
        margin-bottom: 1rem !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="compact-nav-button">', unsafe_allow_html=True)
    if st.button(
        "🏠 Categories",
        key="back_to_categories",
        help="Return to the main categories page",
    ):
        navigate_to_home()
    st.markdown("</div>", unsafe_allow_html=True)


def render_back_to_category_button():
    """Render a compact, left-aligned back to category button."""
    st.markdown(
        """
    <style>
    .compact-nav-button button {
        background: var(--surface-bg) !important;
        color: var(--text-primary) !important;
        border-radius: 12px !important;
        padding: 0.3rem 0.6rem !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        border: 1px solid var(--border-color) !important;
        width: auto !important;
        min-width: 80px !important;
        max-width: 90px !important;
        transition: all 0.3s ease !important;
        margin: 0 !important;
        box-shadow: 0 2px 4px var(--shadow-light) !important;
    }
    
    .compact-nav-button button:hover {
        background: var(--primary-blue) !important;
        color: white !important;
        transform: translateX(-1px) !important;
        border-color: var(--primary-blue) !important;
        box-shadow: 0 4px 8px var(--shadow-medium) !important;
    }
    
    .compact-nav-button {
        text-align: left !important;
        margin-bottom: 1rem !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="compact-nav-button">', unsafe_allow_html=True)
    if st.button(
        "📂 Category", key="back_to_category", help="Return to the category overview"
    ):
        back_to_category()
    st.markdown("</div>", unsafe_allow_html=True)


def render_breadcrumb_navigation():
    """Render breadcrumb navigation for better user orientation."""
    breadcrumbs = []

    if st.session_state.view == "home":
        breadcrumbs = ["🏠 Home"]
    elif st.session_state.view == "category_detail":
        category_id = st.session_state.selected_category
        if category_id:
            breadcrumbs = ["🏠 Home", f"📂 {format_category_name(category_id)}"]
    elif st.session_state.view == "item_detail":
        category_id = st.session_state.selected_category
        item_title = (
            st.session_state.selected_item.get("title", "Item")
            if st.session_state.selected_item
            else "Item"
        )
        if category_id:
            breadcrumbs = [
                "🏠 Home",
                f"📂 {format_category_name(category_id)}",
                f"📄 {item_title}",
            ]

    if len(breadcrumbs) > 1:
        breadcrumb_html = " → ".join(breadcrumbs)
        st.markdown(
            f"""
        <div style="background: var(--card-bg); padding: 0.8rem 1rem; border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 2px 8px var(--shadow-light); border-left: 4px solid var(--primary-blue); text-align: left; max-width: 400px; border: 1px solid var(--border-color);">
            <p style="margin: 0; color: var(--text-secondary); font-size: 0.85rem;">
                {breadcrumb_html}
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_navigation_header():
    """Render a comprehensive navigation header."""
    if st.session_state.view != "home":
        st.markdown(
            """
        <style>
        .compact-home-button button {
            background: var(--surface-bg) !important;
            color: var(--text-primary) !important;
            border-radius: 12px !important;
            padding: 0.3rem 0.6rem !important;
            font-size: 0.75rem !important;
            font-weight: 500 !important;
            border: 1px solid var(--border-color) !important;
            width: auto !important;
            min-width: 70px !important;
            max-width: 80px !important;
            transition: all 0.3s ease !important;
            margin: 0 0 1rem 0 !important;
            box-shadow: 0 2px 4px var(--shadow-light) !important;
        }
        
        .compact-home-button button:hover {
            background: var(--primary-blue) !important;
            color: white !important;
            transform: translateX(-1px) !important;
            border-color: var(--primary-blue) !important;
            box-shadow: 0 4px 8px var(--shadow-medium) !important;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="compact-home-button">', unsafe_allow_html=True)
        if st.button("🏠 Home", key="nav_home", help="Go to main page"):
            navigate_to_home()
        st.markdown("</div>", unsafe_allow_html=True)

    render_breadcrumb_navigation()


def render_quick_navigation(app_data):
    """Render quick navigation menu for easy category switching."""
    if st.session_state.view != "home" and app_data:
        st.markdown("### Quick Navigation")

        categories = list(app_data.keys())
        category_names = [format_category_name(cat_id) for cat_id in categories]

        # Create a horizontal navigation menu
        nav_cols = st.columns(len(categories))

        for i, (cat_id, cat_name) in enumerate(zip(categories, category_names)):
            with nav_cols[i]:
                is_current = st.session_state.selected_category == cat_id
                button_style = "🔍" if is_current else "📂"

                if st.button(
                    f"{button_style} {cat_name}",
                    key=f"quick_nav_{cat_id}",
                    help=f"Go to {cat_name}",
                    disabled=is_current,
                ):
                    navigate_to_category(cat_id)


def format_category_name(category_id):
    """Format category ID into a readable name."""
    name_mappings = {
        "sculptures_architecture": "Sculptures & Architecture",
        "handicrafts_paintings": "Handicrafts & Paintings",
        "performing_arts_festivals": "Performing Arts & Festivals",
        "artists": "Artists",
    }

    return name_mappings.get(category_id, category_id.replace("_", " ").title())


def render_floating_navigation():
    """Render a floating navigation button for mobile-friendly experience."""
    # This creates a floating action button for better mobile navigation
    if st.session_state.view != "home":
        st.markdown(
            """
        <div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
            <div style="background: var(--primary-blue); color: white; border-radius: 50%; width: 56px; height: 56px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 16px var(--shadow-medium); cursor: pointer; transition: all 0.3s ease;">
                🏠
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )


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
                    disabled=is_current,
                ):
                    navigate_to_category(cat_id)

        # Additional sidebar content
        st.markdown("---")
        st.markdown(
            """
        ### About
        Explore the rich world of art and culture through our curated collections.
        
        ### Features
        - 🎨 Diverse art categories
        - 🖼️ High-quality images
        - 📚 Detailed information
        - 🔍 Easy navigation
        """
        )

        # Theme toggle (updated for light theme)
        st.markdown("---")
        if st.button("☀️ Light Mode", key="theme_toggle", use_container_width=True):
            st.info("You're already using the beautiful light-blue theme!")


def render_enhanced_navigation_bar(app_data):
    """Render an enhanced navigation bar with category quick access."""
    if st.session_state.view != "home":
        st.markdown(
            """
        <style>
        .enhanced-nav-bar {
            background: var(--card-bg);
            padding: 0.8rem 1.5rem;
            border-radius: 15px;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px var(--shadow-light);
            border: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        .nav-section {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .nav-title {
            color: var(--text-primary);
            font-weight: 600;
            font-size: 1.1rem;
            margin: 0;
        }
        
        .nav-breadcrumb {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
        
        .quick-nav-buttons {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        
        .quick-nav-btn {
            background: var(--surface-bg);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.3rem 0.8rem;
            font-size: 0.8rem;
            text-decoration: none;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        
        .quick-nav-btn:hover {
            background: var(--primary-blue);
            color: white;
            border-color: var(--primary-blue);
        }
        
        .quick-nav-btn.active {
            background: var(--primary-blue);
            color: white;
            border-color: var(--primary-blue);
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        # Get current context
        current_view = st.session_state.view
        selected_category = st.session_state.selected_category

        # Create navigation context
        nav_title = "🏠 Home"
        if current_view == "category_detail" and selected_category:
            nav_title = f"📂 {format_category_name(selected_category)}"
        elif current_view == "item_detail":
            item_title = (
                st.session_state.selected_item.get("title", "Item")
                if st.session_state.selected_item
                else "Item"
            )
            nav_title = f"📄 {item_title[:30]}{'...' if len(item_title) > 30 else ''}"

        st.markdown(
            f"""
        <div class="enhanced-nav-bar">
            <div class="nav-section">
                <h3 class="nav-title">{nav_title}</h3>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_mobile_navigation():
    """Render mobile-friendly navigation at the bottom of the screen."""
    if st.session_state.view != "home":
        st.markdown(
            """
        <style>
        .mobile-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: var(--card-bg);
            border-top: 1px solid var(--border-color);
            padding: 0.5rem 1rem;
            display: flex;
            justify-content: center;
            gap: 1rem;
            z-index: 1000;
            box-shadow: 0 -2px 8px var(--shadow-light);
        }
        
        .mobile-nav-btn {
            background: var(--surface-bg);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 0.5rem 1rem;
            font-size: 0.8rem;
            text-decoration: none;
            transition: all 0.2s ease;
            cursor: pointer;
            min-width: 80px;
            text-align: center;
        }
        
        .mobile-nav-btn:hover {
            background: var(--primary-blue);
            color: white;
            border-color: var(--primary-blue);
        }
        
        @media (min-width: 768px) {
            .mobile-nav {
                display: none;
            }
        }
        </style>
        
        <div class="mobile-nav">
            <button class="mobile-nav-btn" onclick="window.location.reload()">🏠 Home</button>
            <button class="mobile-nav-btn" onclick="history.back()">← Back</button>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_contextual_navigation():
    """Render contextual navigation based on current page."""
    current_view = st.session_state.view

    if current_view == "category_detail":
        render_back_to_categories_button()
    elif current_view == "item_detail":
        col1, col2 = st.columns([1, 4])
        with col1:
            render_back_to_category_button()
        # Breadcrumb is handled separately

    # Always show breadcrumb if not on home
    if current_view != "home":
        render_breadcrumb_navigation()
