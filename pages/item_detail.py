import streamlit as st
from components.navigation import render_back_to_category_button
from components.image_gallery import render_image_gallery
from components.content_sections import render_content_sections
from utils.formatters import format_section_title
from utils.story_gen import generate_story  # Fixed typo: was 'stroy_gen'
from components.map_view import render_street_view


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
    """Render the enhanced item detail page."""
    selected_item = st.session_state.selected_item

    if not selected_item:
        render_no_item_selected()
        return

    render_item_details(selected_item)


def render_no_item_selected():
    """Render message when no item is selected."""
    st.markdown(
        """
    <div style="
        text-align: center;
        padding: 0 3rem;
        background: var(--card-bg);
        border-radius: 20px;
        margin: 0 0;
        border: 1px solid var(--border-color);
    ">
        <h3 style="color: var(--text-secondary);">🔍 No item selected</h3>
        <p style="color: var(--text-muted);">
            Please select an item from a category to view its details.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_item_details(selected_item):
    """Render detailed information about an item with enhanced styling."""
    # Initialize session state variables if they don't exist
    if "story_loading" not in st.session_state:
        st.session_state.story_loading = False
    if "generated_story" not in st.session_state:
        st.session_state.generated_story = None
    if "map_loading" not in st.session_state:
        st.session_state.map_loading = False

    # Item title at the top
    render_item_title(selected_item)

    # Image gallery section
    render_image_gallery(selected_item)

    # --- STORY GENERATION SECTION ---
    st.markdown('<hr style="margin: 3rem 0;">', unsafe_allow_html=True)

    # Check if selected item has changed and clear previous story/loading state
    if st.session_state.get("current_item_title") != selected_item.get("title"):
        st.session_state.generated_story = None
        st.session_state.story_loading = False
        st.session_state.current_item_title = selected_item.get("title")

    # Display button or loading/story
    if not st.session_state.story_loading and st.session_state.generated_story is None:
        if st.button(
            "📜 View Historical Significance Story",
            key="gen_story_btn",
            use_container_width=True,
        ):
            st.session_state.story_loading = True
            # Story generation is handled in the subsequent block on rerun
            st.rerun()

    if st.session_state.story_loading:
        # Colorful AI loading animation with model name
        model_name = "gemini-2.5-flash-preview-04-17"  # Explicitly use the model name
        # Define CSS separately
        loading_css = """
        <style>
        @keyframes spin { 100% { transform: rotate(360deg); } }
        </style>
        """
        st.markdown(loading_css, unsafe_allow_html=True)

        # Define HTML structure using an f-string to include model_name
        loading_html = f"""
        <div style="display: flex; flex-direction: column; align-items: center; margin: 3rem 0; padding: 2rem; background: var(--surface-bg); border-radius: 15px; border: 2px solid var(--primary-color);">
            <div style="width: 80px; height: 80px; border-radius: 50%; background: conic-gradient(from 0deg, #4A90E2, #6FB3E0, #F1F5F9, #FFD700, #FF6F61, #4A90E2); animation: spin 1.5s linear infinite; margin-bottom: 1.5rem;"></div>
            <p style="color: var(--text-light); font-weight: bold; font-size: 1.3rem; text-align: center;">Gathering historical information and generating story with {model_name}...</p>
            <p style="color: var(--text-secondary); font-size: 0.9rem;">This may take a moment as AI analyzes historical context and writes.</p>
        </div>
        """
        st.markdown(loading_html, unsafe_allow_html=True)
        # Trigger the story generation function call immediately in the script rerun
        # The function call is now outside the button check but inside the loading state check
        if st.session_state.generated_story is None and st.session_state.get(
            "current_item_title"
        ) == selected_item.get("title"):
            story = generate_story(selected_item.get("title", "Untitled"))
            st.session_state.generated_story = story
            st.session_state.story_loading = False
            st.rerun()  # Rerun one more time to display the story

    # Display the story if it's generated and matches the current item
    if st.session_state.generated_story is not None and st.session_state.get(
        "current_item_title"
    ) == selected_item.get("title"):
        # Styled story output
        st.markdown(
            f"""
        <div style="
            background: var(--surface-bg);
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            border: 2px solid var(--highlight-color);
            box-shadow: 0 6px 25px rgba(0,0,0,0.15);
        ">
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 1.8rem; color: var(--highlight-color);">
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path></svg>
                <h4 style="margin: 0; font-size: 1.6rem; font-weight: 700; color: var(--text-light);">Historical Significance</h4>
            </div>
            <p style="font-size: 0.9em; color: var(--text-muted); margin-top: -1.5rem; margin-bottom: 1.5rem;">Generated by AI</p>
            <div style="color: var(--text-secondary); line-height: 1.8; font-size: 1.1rem; white-space: pre-wrap; overflow-wrap: break-word;">
                {st.session_state.generated_story}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Street View section for architecture items
    category_id = st.session_state.get("selected_category")
    if category_id == "sculptures_architecture":
        location = selected_item.get("location") or selected_item.get("title")
        if location:
            st.markdown('<hr style="margin: 2rem 0;">', unsafe_allow_html=True)

            # Check if selected item has changed and clear previous map state
            if st.session_state.get("current_item_title") != selected_item.get("title"):
                st.session_state.map_loading = False
                st.session_state.current_item_title = selected_item.get("title")

            # Display map section
            st.markdown("### 🗺️ Street View")

            # Show loading state or map
            if st.session_state.map_loading:
                st.markdown(
                    """
                <div style="
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    margin: 2rem 0;
                    padding: 2rem;
                    background: var(--surface-bg);
                    border-radius: 15px;
                    border: 2px solid var(--primary-color);
                ">
                    <div style="width: 60px; height: 60px; border-radius: 50%; background: conic-gradient(from 0deg, #4A90E2, #6FB3E0, #F1F5F9, #FFD700, #FF6F61, #4A90E2); animation: spin 1.5s linear infinite; margin-bottom: 1rem;"></div>
                    <p style="color: var(--text-light); font-weight: bold; text-align: center;">Loading street view...</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                render_street_view(location)

    # Main content sections
    render_content_sections(selected_item)

    # Quick Stats section
    render_quick_stats(selected_item)

    # Additional metadata if available
    render_metadata_section(selected_item)

    # Related Items section
    render_related_items_section()

    # Item Actions buttons
    render_item_actions()

    # Accessibility Info
    render_accessibility_info()


def render_item_title_with_back_button(selected_item):
    """Render the item title with enhanced styling and back button."""
    title = selected_item.get("title", "Untitled Item")

    # Header with title
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
    text-align: center;
    padding: 2rem 1rem;
    margin: -1rem -1rem 2rem -1rem;
    border-radius: 0 0 25px 25px;
    border-bottom: 2px solid var(--border-color);
    box-shadow: 0 4px 20px var(--shadow-light);
    position: relative;
">
    <div class="background-overlay"></div>
    <div style="position: relative; z-index: 1;">
        <h1 class="item-title" style="
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: white;
            margin: 0;
            line-height: 1.2;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        ">
            {title}
        </h1>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Back button positioned after the header
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
        if st.button("←", key="back_arrow_item", help="Go back to category"):
            from utils.session import back_to_category

            back_to_category()
        st.markdown("</div>", unsafe_allow_html=True)


def render_item_title(selected_item):
    """Render the item title with enhanced styling and background image."""
    title = selected_item.get("title", "Untitled Item")

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
    text-align: center;
    padding: 2rem 1rem;
    margin: -1rem -1rem 2rem -1rem;
    border-radius: 0 0 25px 25px;
    border-bottom: 2px solid var(--border-color);
    box-shadow: 0 4px 20px var(--shadow-light);
    position: relative;
">
    <div class="background-overlay"></div>
    <div style="position: relative; z-index: 1;">
        <h1 class="item-title" style="
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: white;
            margin: 0;
            line-height: 1.2;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        ">
            {title}
        </h1>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_metadata_section(selected_item):
    """Render metadata section if relevant data exists."""
    metadata_keys = [
        "generated_at",
        "last_modified",
        "references",
        "source",
        "curator_notes",
    ]
    metadata = {
        key: value
        for key, value in selected_item.items()
        if key in metadata_keys and value
    }

    if not metadata:
        return

    st.markdown(
        """
    <div style="
        margin-top: 3rem;
        padding: 1.5rem;
        background: var(--surface-bg);
        border-radius: 12px;
        border: 1px solid var(--border-color);
        border-top: 3px solid var(--text-muted);
    ">
        <h4 style="
            color: var(--text-muted);
            margin: 0 0 1rem 0;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        ">
            📄 Metadata
        </h4>
    """,
        unsafe_allow_html=True,
    )

    for key, value in metadata.items():
        if key == "references" and isinstance(value, list):
            formatted_value = format_references(value)
        else:
            formatted_value = str(value)

        st.markdown(
            f"""
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding: 0.5rem 0;
            border-bottom: 1px solid var(--border-color);
        ">
            <span style="
                color: var(--text-muted);
                font-size: 0.9rem;
                min-width: 120px;
            ">
                {format_section_title(key)}:
            </span>
            <span style="
                color: var(--text-secondary);
                font-size: 0.9rem;
                text-align: right;
                flex: 1;
                margin-left: 1rem;
            ">
                {formatted_value}
            </span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def format_references(references):
    """Format references list for display."""
    if not references:
        return "None"

    if len(references) == 1:
        return references[0]
    elif len(references) <= 3:
        return "; ".join(references)
    else:
        return f"{'; '.join(references[:2])} and {len(references) - 2} more"


def render_quick_stats(selected_item):
    """Render quick statistics about the item."""
    stats = {}

    # Extract relevant stats
    if "year" in selected_item or "date" in selected_item:
        year = selected_item.get("year") or selected_item.get("date")
        if year:
            stats["Year"] = str(year)

    if "location" in selected_item:
        stats["Location"] = selected_item["location"]

    if "artist" in selected_item or "creator" in selected_item:
        creator = selected_item.get("artist") or selected_item.get("creator")
        if creator:
            stats["Creator"] = creator

    if "style" in selected_item or "period" in selected_item:
        style = selected_item.get("style") or selected_item.get("period")
        if style:
            stats["Style/Period"] = style

    if not stats:
        return

    # Render stats in a grid
    st.markdown("### 📊 Quick Facts")

    num_stats = len(stats)
    if num_stats <= 2:
        cols = st.columns(num_stats)
    elif num_stats <= 4:
        cols = st.columns(2)
    else:
        cols = st.columns(3)

    for i, (key, value) in enumerate(stats.items()):
        with cols[i % len(cols)]:
            st.markdown(
                f"""
            <div style="
                background: var(--card-bg);
                padding: 1.2rem;
                border-radius: 10px;
                text-align: center;
                border: 1px solid var(--border-color);
                margin-bottom: 1rem;
                transition: transform 0.2s ease;
            ">
                <h4 style="
                    color: var(--text-light);
                    margin: 0 0 0.5rem 0;
                    font-size: 1rem;
                    font-weight: 600;
                ">
                    {value}
                </h4>
                <p style="
                    color: var(--text-muted);
                    margin: 0;
                    font-size: 0.8rem;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                ">
                    {key}
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )


def render_related_items_section():
    """Render related items section (placeholder for future enhancement)."""
    st.markdown(
        """
    <div style="
        margin-top: 3rem;
        padding: 2rem;
        background: var(--card-bg);
        border-radius: 15px;
        text-align: center;
        border: 1px solid var(--border-color);
    ">
        <h4 style="color: var(--text-secondary); margin-bottom: 1rem;">
            🔗 Related Items
        </h4>
        <p style="color: var(--text-muted); font-style: italic;">
            Related items feature coming soon! This will show similar artworks, 
            pieces by the same artist, or items from the same period.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_item_actions():
    """Render action buttons for the item."""
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📤 Share Item", help="Share this item", use_container_width=True):
            st.success("Share functionality coming soon!")

    with col2:
        if st.button(
            "⭐ Add to Favorites", help="Add to favorites", use_container_width=True
        ):
            st.success("Favorites functionality coming soon!")

    with col3:
        if st.button(
            "🖨️ Print Details", help="Print item details", use_container_width=True
        ):
            st.success("Print functionality coming soon!")


def render_accessibility_info():
    """Render accessibility information if available."""
    st.markdown(
        """
    <div style="
        margin-top: 2rem;
        padding: 1rem;
        background: var(--surface-bg);
        border-radius: 8px;
        border-left: 4px solid var(--primary-blue);
    ">
        <h5 style="color: var(--text-light); margin: 0 0 0.5rem 0;">
            ♿ Accessibility Features
        </h5>
        <p style="color: var(--text-secondary); margin: 0; font-size: 0.9rem;">
            This page includes image descriptions, keyboard navigation support, 
            and screen reader friendly content structure.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
