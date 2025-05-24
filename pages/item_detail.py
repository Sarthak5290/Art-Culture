import streamlit as st
from components.navigation import render_back_to_category_button


def render(app_data):
    """Render the enhanced item detail page."""
    selected_item = st.session_state.selected_item

    # Enhanced navigation
    render_back_to_category_button()

    if selected_item:
        render_item_details(selected_item)


def render_item_details(selected_item):
    """Render detailed information about an item with enhanced styling."""
    
    # Item title with hero styling
    item_title = selected_item.get("title", "Untitled Item")
    st.markdown(f"""
    <div class="hero-section" style="margin-bottom: 3rem;">
        <h1 class="item-title">{item_title}</h1>
    </div>
    """, unsafe_allow_html=True)

    # Image gallery section
    render_image_gallery(selected_item)

    # Content sections in organized layout
    render_content_sections(selected_item)


def render_image_gallery(selected_item):
    """Render an enhanced image gallery."""
    images = selected_item.get("images", [])
    
    if images and len(images) > 0:
        st.markdown('<h3 class="item-section-title">🖼️ Gallery</h3>', unsafe_allow_html=True)
        
        # Main image display
        if len(images) == 1:
            st.markdown("""
            <div style="text-align: center; margin: 2rem 0;">
            """, unsafe_allow_html=True)
            st.image(images[0], use_container_width=True, caption="Main Image")
            st.markdown("</div>", unsafe_allow_html=True)
        
        elif len(images) <= 4:
            # Display all images in a grid
            cols = st.columns(min(len(images), 4))
            for i, image_url in enumerate(images):
                with cols[i]:
                    st.markdown(f"""
                    <div class="gallery-image">
                    """, unsafe_allow_html=True)
                    st.image(image_url, use_container_width=True, caption=f"Image {i+1}")
                    st.markdown("</div>", unsafe_allow_html=True)
        
        else:
            # Main image + thumbnail grid for multiple images
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Main image viewer
                if 'selected_image_idx' not in st.session_state:
                    st.session_state.selected_image_idx = 0
                
                selected_idx = st.session_state.selected_image_idx
                st.image(images[selected_idx], use_container_width=True, caption=f"Image {selected_idx + 1} of {len(images)}")
                
                # Navigation buttons
                nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
                with nav_col1:
                    if st.button("◀ Previous", disabled=(selected_idx == 0)):
                        st.session_state.selected_image_idx = max(0, selected_idx - 1)
                        st.rerun()
                
                with nav_col3:
                    if st.button("Next ▶", disabled=(selected_idx == len(images) - 1)):
                        st.session_state.selected_image_idx = min(len(images) - 1, selected_idx + 1)
                        st.rerun()
            
            with col2:
                # Thumbnail grid
                st.markdown("**All Images:**")
                for i, image_url in enumerate(images):
                    is_selected = i == st.session_state.selected_image_idx
                    border_style = "border: 3px solid #D4AF37;" if is_selected else "border: 1px solid #ddd;"
                    
                    st.markdown(f"""
                    <div style="{border_style} border-radius: 8px; overflow: hidden; margin-bottom: 0.5rem; cursor: pointer;">
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"🖼️", key=f"thumb_{i}", help=f"View image {i+1}"):
                        st.session_state.selected_image_idx = i
                        st.rerun()
                    
                    st.image(image_url, width=100)
                    st.markdown("</div>", unsafe_allow_html=True)


def render_content_sections(selected_item):
    """Render content sections in an organized, visually appealing layout."""
    
    # Define excluded keys and section priorities
    excluded_keys = {'images', 'title', 'generated_at', 'last_modified', 'references'}
    
    # Priority sections that should appear first
    priority_sections = ['description', 'overview', 'summary', 'history', 'significance']
    
    # Categorize sections
    main_sections = {}
    list_sections = {}
    other_sections = {}
    
    for key, value in selected_item.items():
        if key not in excluded_keys and value:  # Only include non-empty values
            if isinstance(value, list):
                list_sections[key] = value
            elif key in priority_sections:
                main_sections[key] = value
            else:
                other_sections[key] = value
    
    # Render priority/main content sections first
    if main_sections:
        st.markdown('<div class="item-detail-container">', unsafe_allow_html=True)
        
        for key in priority_sections:
            if key in main_sections:
                render_content_section(key, main_sections[key], is_priority=True)
        
        # Render other main sections
        for key, value in main_sections.items():
            if key not in priority_sections:
                render_content_section(key, value, is_priority=False)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Render list sections in a separate container
    if list_sections:
        st.markdown('<div class="item-detail-container" style="margin-top: 2rem;">', unsafe_allow_html=True)
        st.markdown('<h3 class="item-section-title">📋 Additional Information</h3>', unsafe_allow_html=True)
        
        # Create columns for list sections
        list_keys = list(list_sections.keys())
        if len(list_keys) <= 2:
            cols = st.columns(len(list_keys))
        else:
            cols = st.columns(2)
        
        for i, (key, value) in enumerate(list_sections.items()):
            with cols[i % len(cols)]:
                render_list_section(key, value)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Render other sections
    if other_sections:
        st.markdown('<div class="item-detail-container" style="margin-top: 2rem;">', unsafe_allow_html=True)
        st.markdown('<h3 class="item-section-title">🔍 Detailed Information</h3>', unsafe_allow_html=True)
        
        for key, value in other_sections.items():
            render_content_section(key, value, is_priority=False)
        
        st.markdown('</div>', unsafe_allow_html=True)


def render_content_section(key, value, is_priority=False):
    """Render a single content section with appropriate styling."""
    display_title = format_section_title(key)
    
    if is_priority:
        st.markdown(f'<h4 class="item-section-title" style="font-size: 1.4rem;">✨ {display_title}</h4>', unsafe_allow_html=True)
    else:
        st.markdown(f'<h5 style="color: #1E3A5F; margin: 1.5rem 0 0.8rem 0; font-size: 1.1rem;">📌 {display_title}</h5>', unsafe_allow_html=True)
    
    if isinstance(value, dict):
        render_dict_content(value)
    else:
        content = str(value)
        if len(content) > 500:
            # For long content, add expandable section
            with st.expander(f"Read full {display_title.lower()}", expanded=is_priority):
                st.markdown(f'<div class="item-content">{content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="item-content">{content}</div>', unsafe_allow_html=True)


def render_list_section(key, value_list):
    """Render a list section with enhanced styling."""
    display_title = format_section_title(key)
    
    st.markdown(f"""
    <div style="background: #F8F9FA; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid #D4AF37;">
        <h5 style="color: #1E3A5F; margin: 0 0 1rem 0; font-size: 1.1rem;">📋 {display_title}</h5>
    """, unsafe_allow_html=True)
    
    if value_list:
        for i, item in enumerate(value_list, 1):
            st.markdown(f"""
            <div style="margin-bottom: 0.5rem; padding: 0.5rem 0; border-bottom: 1px solid #E0E0E0;">
                <span style="color: #D4AF37; font-weight: 600;">{i}.</span>
                <span style="color: #444; margin-left: 0.5rem;">{item}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<p style="color: #888; font-style: italic; margin: 0;">No items available.</p>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_dict_content(dict_value):
    """Render dictionary content in an organized way."""
    st.markdown("""
    <div style="background: #F8F9FA; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    """, unsafe_allow_html=True)
    
    for sub_key, sub_value in dict_value.items():
        display_key = format_section_title(sub_key)
        st.markdown(f"""
        <div style="margin-bottom: 0.8rem;">
            <strong style="color: #1E3A5F;">{display_key}:</strong>
            <span style="color: #444; margin-left: 0.5rem;">{sub_value}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def format_section_title(key):
    """Format section keys into readable titles."""
    # Handle special cases
    title_mappings = {
        'notable_works': 'Notable Works',
        'art_style': 'Art Style',
        'time_period': 'Time Period',
        'birth_date': 'Birth Date',
        'death_date': 'Death Date',
        'birth_place': 'Birth Place',
        'architectural_style': 'Architectural Style',
        'construction_period': 'Construction Period',
        'cultural_significance': 'Cultural Significance'
    }
    
    if key in title_mappings:
        return title_mappings[key]
    
    # Default formatting: replace underscores with spaces and capitalize
    return key.replace('_', ' ').title()