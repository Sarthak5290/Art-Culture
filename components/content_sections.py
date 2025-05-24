import streamlit as st
from utils.formatters import format_section_title


def render_content_sections(selected_item):
    """Render content sections in an organized, visually appealing layout."""

    # Define excluded keys and section priorities
    excluded_keys = {"images", "title", "generated_at", "last_modified", "references"}

    # Priority sections that should appear first
    priority_sections = [
        "description",
        "overview",
        "summary",
        "history",
        "significance",
    ]

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
        render_main_sections(main_sections, priority_sections)

    # Render list sections in a separate container
    if list_sections:
        render_list_sections(list_sections)

    # Render other sections
    if other_sections:
        render_other_sections(other_sections)


def render_main_sections(main_sections, priority_sections):
    """Render main content sections with priority ordering."""
    st.markdown('<div class="item-detail-container">', unsafe_allow_html=True)

    for key in priority_sections:
        if key in main_sections:
            render_content_section(key, main_sections[key], is_priority=True)

    # Render other main sections
    for key, value in main_sections.items():
        if key not in priority_sections:
            render_content_section(key, value, is_priority=False)

    st.markdown("</div>", unsafe_allow_html=True)


def render_list_sections(list_sections):
    """Render list sections in organized layout."""
    st.markdown(
        '<div class="item-detail-container" style="margin-top: 2rem;">',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<h3 class="item-section-title" style="color: var(--text-light);">📋 Additional Information</h3>',
        unsafe_allow_html=True,
    )

    # Create columns for list sections
    list_keys = list(list_sections.keys())
    if len(list_keys) <= 2:
        cols = st.columns(len(list_keys))
    else:
        cols = st.columns(2)

    for i, (key, value) in enumerate(list_sections.items()):
        with cols[i % len(cols)]:
            render_list_section(key, value)

    st.markdown("</div>", unsafe_allow_html=True)


def render_other_sections(other_sections):
    """Render miscellaneous sections."""
    st.markdown(
        '<div class="item-detail-container" style="margin-top: 2rem;">',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<h3 class="item-section-title" style="color: var(--text-light);">🔍 Detailed Information</h3>',
        unsafe_allow_html=True,
    )

    for key, value in other_sections.items():
        render_content_section(key, value, is_priority=False)

    st.markdown("</div>", unsafe_allow_html=True)


def render_content_section(key, value, is_priority=False):
    """Render a single content section with enhanced styling."""
    display_title = format_section_title(key)
    
    # Special treatment for summary section
    if key == "summary":
        render_summary_section(display_title, value)
        return

    # Enhanced information sections
    if is_priority:
        render_priority_section(display_title, value)
    else:
        # Grid layout for key information pairs
        if isinstance(value, dict):
            render_dict_section(value)
        else:
            render_standard_section(display_title, value)


def render_summary_section(display_title, value):
    """Render summary section with special styling."""
    st.markdown(f"""
    <div style="
        background: var(--surface-bg);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 4px solid var(--highlight-color);
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 1.2rem;
            color: var(--highlight-color);
        ">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <path d="M14 2v6h6"></path>
                <path d="M16 13H8"></path>
                <path d="M16 17H8"></path>
                <path d="M10 9H8"></path>
            </svg>
            <h3 style="
                margin: 0;
                font-size: 1.4rem;
                font-weight: 600;
                color: var(--text-light);
            ">
                Key Summary
            </h3>
        </div>
        <div style="
            color: var(--text-secondary);
            line-height: 1.7;
            font-size: 1rem;
            background: linear-gradient(to right, var(--surface-bg), var(--background-color));
            padding: 1rem;
            border-radius: 8px;
        ">
            {value}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_priority_section(display_title, value):
    """Render priority section with enhanced styling."""
    st.markdown(f"""
    <div style="
        margin: 1.5rem 0;
        padding: 1.25rem;
        background: var(--surface-bg);
        border-radius: 12px;
        border: 1px solid var(--border-color);
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 1rem;
            color: var(--highlight-color);
        ">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M12 16v-4"></path>
                <path d="M12 8h.01"></path>
            </svg>
            <h4 style="
                margin: 0;
                font-size: 1.2rem;
                font-weight: 600;
                color: var(--text-light);
            ">
                {display_title}
            </h4>
        </div>
        <div style="
            color: var(--text-secondary);
            line-height: 1.6;
            font-size: 0.95rem;
        ">
            {value}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_dict_section(dict_value):
    """Render dictionary content in organized columns."""
    cols = st.columns(2)
    for i, (sub_key, sub_value) in enumerate(dict_value.items()):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="
                background: var(--surface-bg);
                padding: 1rem;
                border-radius: 8px;
                margin: 0.5rem 0;
                border: 1px solid var(--border-color);
            ">
                <div style="
                    font-size: 0.9rem;
                    color: var(--text-muted);
                    margin-bottom: 0.25rem;
                ">
                    {format_section_title(sub_key)}
                </div>
                <div style="
                    font-size: 1rem;
                    color: var(--text-light);
                    font-weight: 500;
                ">
                    {sub_value}
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_standard_section(display_title, value):
    """Render standard section with basic styling."""
    st.markdown(f"""
    <div style="
        background: var(--surface-bg);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 3px solid var(--highlight-color);
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 0.5rem;
        ">
            <div style="
                width: 6px;
                height: 6px;
                background: var(--highlight-color);
                border-radius: 50%;
            "></div>
            <h5 style="
                margin: 0;
                font-size: 1rem;
                color: var(--text-light);
            ">
                {display_title}
            </h5>
        </div>
        <div style="
            color: var(--text-secondary);
            line-height: 1.6;
            font-size: 0.95rem;
        ">
            {value}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_list_section(key, value_list):
    """Render a list section with enhanced styling."""
    display_title = format_section_title(key)

    st.markdown(
        f"""
    <div style="background: var(--surface-bg); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid var(--highlight-color); border: 1px solid var(--border-color);">
        <h5 style="color: var(--text-light); margin: 0 0 1rem 0; font-size: 1.1rem;">📋 {display_title}</h5>
    """,
        unsafe_allow_html=True,
    )

    if value_list:
        for i, item in enumerate(value_list, 1):
            st.markdown(
                f"""
            <div style="margin-bottom: 0.5rem; padding: 0.5rem 0; border-bottom: 1px solid var(--border-color);">
                <span style="color: var(--highlight-color); font-weight: 600;">{i}.</span>
                <span style="color: var(--text-secondary); margin-left: 0.5rem;">{item}</span>
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<p style="color: var(--text-muted); font-style: italic; margin: 0;">No items available.</p>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def render_expandable_section(title, content, icon="📄"):
    """Render an expandable content section."""
    with st.expander(f"{icon} {title}"):
        if isinstance(content, list):
            for item in content:
                st.write(f"• {item}")
        elif isinstance(content, dict):
            for key, value in content.items():
                st.write(f"**{format_section_title(key)}:** {value}")
        else:
            st.write(content)


def render_tabbed_sections(sections_dict):
    """Render sections in tabs for better organization."""
    if not sections_dict:
        return
    
    tab_names = list(sections_dict.keys())
    tabs = st.tabs([format_section_title(name) for name in tab_names])
    
    for i, (section_name, section_content) in enumerate(sections_dict.items()):
        with tabs[i]:
            if isinstance(section_content, list):
                render_list_section(section_name, section_content)
            elif isinstance(section_content, dict):
                render_dict_section(section_content)
            else:
                render_content_section(section_name, section_content)


def render_highlighted_info_box(title, content, color="var(--primary-blue)"):
    """Render a highlighted information box."""
    st.markdown(f"""
    <div style="
        background: var(--surface-bg);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid {color};
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    ">
        <h4 style="
            color: var(--text-light);
            margin: 0 0 1rem 0;
            font-size: 1.2rem;
        ">
            {title}
        </h4>
        <div style="
            color: var(--text-secondary);
            line-height: 1.6;
            font-size: 0.95rem;
        ">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_stats_grid(stats_dict):
    """Render statistics in a grid layout."""
    if not stats_dict:
        return
    
    # Determine number of columns based on number of stats
    num_stats = len(stats_dict)
    if num_stats <= 2:
        cols = st.columns(num_stats)
    elif num_stats <= 4:
        cols = st.columns(2)
    else:
        cols = st.columns(3)
    
    for i, (key, value) in enumerate(stats_dict.items()):
        with cols[i % len(cols)]:
            st.markdown(f"""
            <div style="
                background: var(--card-bg);
                padding: 1.5rem;
                border-radius: 12px;
                text-align: center;
                border: 1px solid var(--border-color);
                margin-bottom: 1rem;
            ">
                <h3 style="
                    color: var(--highlight-color);
                    margin: 0 0 0.5rem 0;
                    font-size: 2rem;
                ">
                    {value}
                </h3>
                <p style="
                    color: var(--text-secondary);
                    margin: 0;
                    font-size: 0.9rem;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                ">
                    {format_section_title(key)}
                </p>
            </div>
            """, unsafe_allow_html=True)