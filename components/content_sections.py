import streamlit as st
from utils.formatters import format_section_title


def render_content_sections(selected_item):
    """Render content sections in an organized, visually appealing layout with enhanced UI."""

    # Define excluded keys and section priorities
    excluded_keys = {"images", "title", "generated_at", "last_modified", "references"}

    # Priority sections that should appear first
    priority_sections = [
        "description",
        "overview",
        "summary",
        "history",
        "significance",
        "background",
        "context",
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
    """Render main content sections with priority ordering and enhanced styling."""
    st.markdown(
        """
    <div style="
        background: linear-gradient(145deg, var(--card-bg), var(--surface-bg));
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 
            0 20px 60px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.05);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: -2px;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-blue), var(--secondary-blue), var(--highlight-color));
            border-radius: 20px 20px 0 0;
        "></div>
    """,
        unsafe_allow_html=True,
    )

    for key in priority_sections:
        if key in main_sections:
            render_content_section(key, main_sections[key], is_priority=True)

    # Render other main sections
    for key, value in main_sections.items():
        if key not in priority_sections:
            render_content_section(key, value, is_priority=False)

    st.markdown("</div>", unsafe_allow_html=True)


def render_list_sections(list_sections):
    """Render list sections in organized layout with modern card design."""
    st.markdown(
        """
    <div style="
        background: linear-gradient(145deg, var(--card-bg), var(--surface-bg));
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 
            0 20px 60px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.05);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: -2px;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #10B981, #059669, #047857);
            border-radius: 20px 20px 0 0;
        "></div>
        <div style="
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        ">
            <div style="
                background: linear-gradient(135deg, #10B981, #059669);
                border-radius: 12px;
                padding: 12px;
                box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
            ">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9 11H5a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7a2 2 0 0 0-2-2h-4"/>
                    <path d="M9 7V3a2 2 0 0 1 4 0v4"/>
                    <line x1="9" y1="11" x2="9" y2="13"/>
                    <line x1="15" y1="11" x2="15" y2="13"/>
                </svg>
            </div>
            <h3 style="
                color: var(--text-light);
                margin: 0;
                font-size: 1.8rem;
                font-weight: 700;
                background: linear-gradient(135deg, #10B981, #34D399);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">
                Additional Information
            </h3>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Create columns for list sections
    list_keys = list(list_sections.keys())
    if len(list_keys) <= 2:
        cols = st.columns(len(list_keys), gap="large")
    else:
        cols = st.columns(2, gap="large")

    for i, (key, value) in enumerate(list_sections.items()):
        with cols[i % len(cols)]:
            render_list_section(key, value)

    st.markdown("</div>", unsafe_allow_html=True)


def render_other_sections(other_sections):
    """Render miscellaneous sections with enhanced styling."""
    st.markdown(
        """
    <div style="
        background: linear-gradient(145deg, var(--card-bg), var(--surface-bg));
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 
            0 20px 60px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.05);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: -2px;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #8B5CF6, #A78BFA, #C4B5FD);
            border-radius: 20px 20px 0 0;
        "></div>
        <div style="
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        ">
            <div style="
                background: linear-gradient(135deg, #8B5CF6, #A78BFA);
                border-radius: 12px;
                padding: 12px;
                box-shadow: 0 8px 20px rgba(139, 92, 246, 0.3);
            ">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="8"/>
                    <path d="M21 21l-4.35-4.35"/>
                </svg>
            </div>
            <h3 style="
                color: var(--text-light);
                margin: 0;
                font-size: 1.8rem;
                font-weight: 700;
                background: linear-gradient(135deg, #8B5CF6, #C4B5FD);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">
                Detailed Information
            </h3>
        </div>
    """,
        unsafe_allow_html=True,
    )

    for key, value in other_sections.items():
        render_content_section(key, value, is_priority=False)

    st.markdown("</div>", unsafe_allow_html=True)


def render_content_section(key, value, is_priority=False):
    """Render a single content section with enhanced modern styling."""
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
    """Render summary section with special modern styling."""
    st.markdown(
        f"""
    <div style="
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 193, 7, 0.05));
        padding: 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        border: 2px solid rgba(255, 215, 0, 0.2);
        box-shadow: 
            0 12px 40px rgba(255, 215, 0, 0.15),
            inset 0 1px 0 rgba(255, 215, 0, 0.1);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #FFD700, #FFC107, #FF8F00);
        "></div>
        <div style="
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 1.5rem;
        ">
            <div style="
                background: linear-gradient(135deg, #FFD700, #FFC107);
                border-radius: 12px;
                padding: 12px;
                box-shadow: 0 8px 20px rgba(255, 215, 0, 0.3);
            ">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <path d="M14 2v6h6"/>
                    <path d="M16 13H8"/>
                    <path d="M16 17H8"/>
                    <path d="M10 9H8"/>
                </svg>
            </div>
            <h3 style="
                margin: 0;
                font-size: 1.6rem;
                font-weight: 700;
                background: linear-gradient(135deg, #FFD700, #FF8F00);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">
                Key Summary
            </h3>
        </div>
        <div style="
            background: rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.1);
            color: var(--text-light);
            line-height: 1.8;
            font-size: 1.05rem;
            font-weight: 400;
        ">
            {value}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_priority_section(display_title, value):
    """Render priority section with enhanced modern styling."""
    st.markdown(
        f"""
    <div style="
        background: linear-gradient(135deg, rgba(74, 144, 226, 0.1), rgba(107, 179, 245, 0.05));
        padding: 1.8rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        border: 1px solid rgba(74, 144, 226, 0.2);
        box-shadow: 
            0 8px 32px rgba(74, 144, 226, 0.15),
            inset 0 1px 0 rgba(255,255,255,0.05);
        position: relative;
        transition: all 0.3s ease;
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 1.2rem;
        ">
            <div style="
                background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue));
                border-radius: 10px;
                padding: 8px;
                box-shadow: 0 6px 16px rgba(74, 144, 226, 0.3);
            ">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 16v-4"/>
                    <path d="M12 8h.01"/>
                </svg>
            </div>
            <h4 style="
                margin: 0;
                font-size: 1.3rem;
                font-weight: 600;
                color: var(--text-light);
            ">
                {display_title}
            </h4>
        </div>
        <div style="
            color: var(--text-secondary);
            line-height: 1.7;
            font-size: 1rem;
            padding-left: 44px;
        ">
            {value}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_dict_section(dict_value):
    """Render dictionary content in organized modern columns."""
    cols = st.columns(2, gap="medium")
    for i, (sub_key, sub_value) in enumerate(dict_value.items()):
        with cols[i % 2]:
            st.markdown(
                f"""
            <div style="
                background: linear-gradient(135deg, var(--surface-bg), var(--card-bg));
                padding: 1.5rem;
                border-radius: 12px;
                margin: 0.8rem 0;
                border: 1px solid rgba(255,255,255,0.1);
                box-shadow: 
                    0 6px 20px rgba(0,0,0,0.2),
                    inset 0 1px 0 rgba(255,255,255,0.05);
                transition: all 0.3s ease;
                position: relative;
            ">
                <div style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 4px;
                    height: 100%;
                    background: linear-gradient(180deg, var(--primary-blue), var(--secondary-blue));
                    border-radius: 0 12px 12px 0;
                "></div>
                <div style="
                    font-size: 0.85rem;
                    color: var(--text-muted);
                    margin-bottom: 0.5rem;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    font-weight: 600;
                ">
                    {format_section_title(sub_key)}
                </div>
                <div style="
                    font-size: 1.1rem;
                    color: var(--text-light);
                    font-weight: 500;
                    line-height: 1.4;
                ">
                    {sub_value}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )


def render_standard_section(display_title, value):
    """Render standard section with modern styling."""
    st.markdown(
        f"""
    <div style="
        background: linear-gradient(135deg, var(--surface-bg), var(--card-bg));
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.2rem 0;
        border-left: 4px solid var(--highlight-color);
        box-shadow: 
            0 6px 20px rgba(0,0,0,0.2),
            inset 0 1px 0 rgba(255,255,255,0.05);
        transition: all 0.3s ease;
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 0.8rem;
        ">
            <div style="
                width: 8px;
                height: 8px;
                background: var(--highlight-color);
                border-radius: 50%;
                box-shadow: 0 0 8px rgba(255, 215, 0, 0.5);
            "></div>
            <h5 style="
                margin: 0;
                font-size: 1.1rem;
                color: var(--text-light);
                font-weight: 600;
            ">
                {display_title}
            </h5>
        </div>
        <div style="
            color: var(--text-secondary);
            line-height: 1.7;
            font-size: 1rem;
            padding-left: 18px;
        ">
            {value}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_list_section(key, value_list):
    """Render a list section with enhanced modern styling."""
    display_title = format_section_title(key)

    st.markdown(
        f"""
    <div style="
        background: linear-gradient(135deg, var(--surface-bg), var(--card-bg));
        padding: 1.8rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 
            0 8px 24px rgba(0,0,0,0.2),
            inset 0 1px 0 rgba(255,255,255,0.05);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #10B981, #34D399, #6EE7B7);
        "></div>
        <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 1.2rem;
            padding-bottom: 0.8rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        ">
            <div style="
                background: linear-gradient(135deg, #10B981, #059669);
                border-radius: 8px;
                padding: 6px;
                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
            ">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9 12l2 2 4-4"/>
                    <path d="M21 12c.552 0 1-.448 1-1V5c0-.552-.448-1-1-1H3c-.552 0-1 .448-1 1v6c0 .552.448 1 1 1h18z"/>
                </svg>
            </div>
            <h5 style="
                color: var(--text-light);
                margin: 0;
                font-size: 1.2rem;
                font-weight: 600;
            ">
                {display_title}
            </h5>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if value_list:
        for i, item in enumerate(value_list, 1):
            st.markdown(
                f"""
            <div style="
                display: flex;
                align-items: flex-start;
                gap: 12px;
                margin-bottom: 0.8rem;
                padding: 0.8rem;
                background: rgba(0,0,0,0.2);
                border-radius: 8px;
                border-left: 3px solid #10B981;
                transition: all 0.2s ease;
            ">
                <div style="
                    background: linear-gradient(135deg, #10B981, #059669);
                    color: white;
                    font-weight: 700;
                    font-size: 0.8rem;
                    padding: 4px 8px;
                    border-radius: 6px;
                    min-width: 24px;
                    text-align: center;
                    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
                ">
                    {i}
                </div>
                <span style="
                    color: var(--text-secondary);
                    line-height: 1.6;
                    font-size: 0.95rem;
                    flex: 1;
                ">
                    {item}
                </span>
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
        <div style="
            text-align: center;
            padding: 2rem;
            color: var(--text-muted);
            font-style: italic;
            opacity: 0.7;
        ">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 0.5rem;">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v6l4 2"/>
            </svg>
            <p style="margin: 0;">No items available at the moment.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def render_expandable_section(title, content, icon="📄"):
    """Render an expandable content section with modern accordion styling."""
    with st.expander(f"{icon} {title}", expanded=False):
        st.markdown(
            """
        <div style="
            background: var(--surface-bg);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            border: 1px solid rgba(255,255,255,0.1);
        ">
        """,
            unsafe_allow_html=True,
        )

        if isinstance(content, list):
            for item in content:
                st.markdown(
                    f"""
                <div style="
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    margin-bottom: 0.5rem;
                    color: var(--text-secondary);
                ">
                    <div style="
                        width: 4px;
                        height: 4px;
                        background: var(--primary-blue);
                        border-radius: 50%;
                    "></div>
                    {item}
                </div>
                """,
                    unsafe_allow_html=True,
                )
        elif isinstance(content, dict):
            for key, value in content.items():
                st.markdown(
                    f"""
                <div style="margin-bottom: 0.8rem;">
                    <strong style="color: var(--text-light);">{format_section_title(key)}:</strong>
                    <span style="color: var(--text-secondary); margin-left: 0.5rem;">{value}</span>
                </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                f"""
            <div style="color: var(--text-secondary); line-height: 1.6;">
                {content}
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)


def render_tabbed_sections(sections_dict):
    """Render sections in tabs for better organization with modern styling."""
    if not sections_dict:
        return

    tab_names = list(sections_dict.keys())
    tabs = st.tabs([format_section_title(name) for name in tab_names])

    for i, (section_name, section_content) in enumerate(sections_dict.items()):
        with tabs[i]:
            st.markdown(
                """
            <div style="
                background: var(--card-bg);
                border-radius: 16px;
                padding: 2rem;
                margin: 1rem 0;
                border: 1px solid rgba(255,255,255,0.1);
            ">
            """,
                unsafe_allow_html=True,
            )

            if isinstance(section_content, list):
                render_list_section(section_name, section_content)
            elif isinstance(section_content, dict):
                render_dict_section(section_content)
            else:
                render_content_section(section_name, section_content)

            st.markdown("</div>", unsafe_allow_html=True)


def render_highlighted_info_box(title, content, color="var(--primary-blue)"):
    """Render a highlighted information box with modern glassmorphism effect."""
    st.markdown(
        f"""
    <div style="
        background: linear-gradient(135deg, rgba(74, 144, 226, 0.1), rgba(107, 179, 245, 0.05));
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        border: 1px solid rgba(74, 144, 226, 0.2);
        box-shadow: 
            0 12px 40px rgba(74, 144, 226, 0.15),
            inset 0 1px 0 rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, {color}, rgba(74, 144, 226, 0.8));
        "></div>
        <h4 style="
            color: var(--text-light);
            margin: 0 0 1rem 0;
            font-size: 1.4rem;
            font-weight: 600;
        ">
            {title}
        </h4>
        <div style="
            color: var(--text-secondary);
            line-height: 1.7;
            font-size: 1rem;
        ">
            {content}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_stats_grid(stats_dict):
    """Render statistics in a modern grid layout with animated counters."""
    if not stats_dict:
        return

    # Determine number of columns based on number of stats
    num_stats = len(stats_dict)
    if num_stats <= 2:
        cols = st.columns(num_stats, gap="large")
    elif num_stats <= 4:
        cols = st.columns(2, gap="large")
    else:
        cols = st.columns(3, gap="large")

    for i, (key, value) in enumerate(stats_dict.items()):
        with cols[i % len(cols)]:
            st.markdown(
                f"""
            <div style="
                background: linear-gradient(135deg, var(--card-bg), var(--surface-bg));
                padding: 2rem 1.5rem;
                border-radius: 16px;
                text-align: center;
                border: 1px solid rgba(255,255,255,0.1);
                margin-bottom: 1.5rem;
                box-shadow: 
                    0 12px 32px rgba(0,0,0,0.2),
                    inset 0 1px 0 rgba(255,255,255,0.05);
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            ">
                <div style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 3px;
                    background: linear-gradient(90deg, var(--highlight-color), #FFC107);
                "></div>
                <div style="
                    background: linear-gradient(135deg, var(--highlight-color), #FFC107);
                    border-radius: 12px;
                    padding: 1rem;
                    margin-bottom: 1rem;
                    box-shadow: 0 8px 20px rgba(255, 215, 0, 0.3);
                    display: inline-block;
                ">
                    <h3 style="
                        color: white;
                        margin: 0;
                        font-size: 2.2rem;
                        font-weight: 800;
                        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
                    ">
                        {value}
                    </h3>
                </div>
                <p style="
                    color: var(--text-secondary);
                    margin: 0;
                    font-size: 0.9rem;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    font-weight: 600;
                ">
                    {format_section_title(key)}
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )


def render_interactive_timeline(timeline_data):
    """Render an interactive timeline component for historical data."""
    if not timeline_data:
        return

    st.markdown(
        """
    <div style="
        background: linear-gradient(145deg, var(--card-bg), var(--surface-bg));
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 
            0 20px 60px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.05);
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        ">
            <div style="
                background: linear-gradient(135deg, #F59E0B, #D97706);
                border-radius: 12px;
                padding: 12px;
                box-shadow: 0 8px 20px rgba(245, 158, 11, 0.3);
            ">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12,6 12,12 16,14"/>
                </svg>
            </div>
            <h3 style="
                color: var(--text-light);
                margin: 0;
                font-size: 1.8rem;
                font-weight: 700;
                background: linear-gradient(135deg, #F59E0B, #FBBF24);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">
                Timeline
            </h3>
        </div>
    """,
        unsafe_allow_html=True,
    )

    for i, (date, event) in enumerate(timeline_data.items()):
        st.markdown(
            f"""
        <div style="
            display: flex;
            gap: 20px;
            margin-bottom: 1.5rem;
            position: relative;
        ">
            <div style="
                background: linear-gradient(135deg, #F59E0B, #D97706);
                color: white;
                padding: 0.8rem 1.2rem;
                border-radius: 12px;
                font-weight: 600;
                font-size: 0.9rem;
                min-width: 100px;
                text-align: center;
                box-shadow: 0 6px 16px rgba(245, 158, 11, 0.3);
            ">
                {date}
            </div>
            <div style="
                flex: 1;
                background: rgba(0,0,0,0.2);
                padding: 1.2rem;
                border-radius: 12px;
                border-left: 4px solid #F59E0B;
                color: var(--text-secondary);
                line-height: 1.6;
            ">
                {event}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def render_image_comparison_slider(before_image, after_image, title="Before & After"):
    """Render an image comparison slider component."""
    st.markdown(
        f"""
    <div style="
        background: linear-gradient(145deg, var(--card-bg), var(--surface-bg));
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 
            0 20px 60px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.05);
        text-align: center;
    ">
        <h3 style="
            color: var(--text-light);
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
            font-weight: 600;
        ">
            {title}
        </h3>
        <div style="
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin-top: 1rem;
        ">
            <div style="
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 8px 24px rgba(0,0,0,0.3);
            ">
                <img src="{before_image}" style="width: 100%; height: auto; display: block;" alt="Before">
                <div style="
                    background: #DC2626;
                    color: white;
                    padding: 0.5rem;
                    font-weight: 600;
                    text-align: center;
                ">
                    BEFORE
                </div>
            </div>
            <div style="
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 8px 24px rgba(0,0,0,0.3);
            ">
                <img src="{after_image}" style="width: 100%; height: auto; display: block;" alt="After">
                <div style="
                    background: #059669;
                    color: white;
                    padding: 0.5rem;
                    font-weight: 600;
                    text-align: center;
                ">
                    AFTER
                </div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_quote_highlight(quote, author=""):
    """Render a highlighted quote with modern styling."""
    st.markdown(
        f"""
    <div style="
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(167, 139, 250, 0.05));
        border-left: 6px solid #8B5CF6;
        padding: 2rem;
        border-radius: 0 16px 16px 0;
        margin: 2rem 0;
        position: relative;
        box-shadow: 
            0 12px 40px rgba(139, 92, 246, 0.15),
            inset 0 1px 0 rgba(255,255,255,0.05);
    ">
        <div style="
            position: absolute;
            top: -10px;
            left: 20px;
            background: linear-gradient(135deg, #8B5CF6, #A78BFA);
            border-radius: 50%;
            padding: 8px;
            box-shadow: 0 6px 16px rgba(139, 92, 246, 0.3);
        ">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="white">
                <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h4v10h-10z"/>
            </svg>
        </div>
        <blockquote style="
            font-style: italic;
            font-size: 1.2rem;
            line-height: 1.6;
            color: var(--text-light);
            margin: 0 0 1rem 0;
            padding-left: 1rem;
        ">
            "{quote}"
        </blockquote>
        {f'<cite style="color: var(--text-muted); font-size: 0.9rem; font-weight: 500;">— {author}</cite>' if author else ''}
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_progress_indicator(sections_completed, total_sections):
    """Render a progress indicator for content sections."""
    progress_percentage = (sections_completed / total_sections) * 100

    st.markdown(
        f"""
    <div style="
        background: var(--surface-bg);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
    ">
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        ">
            <span style="color: var(--text-light); font-weight: 600;">Reading Progress</span>
            <span style="color: var(--highlight-color); font-weight: 600;">{sections_completed}/{total_sections}</span>
        </div>
        <div style="
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
            height: 8px;
            overflow: hidden;
        ">
            <div style="
                background: linear-gradient(90deg, var(--primary-blue), var(--secondary-blue));
                height: 100%;
                width: {progress_percentage}%;
                border-radius: 8px;
                transition: width 0.3s ease;
            "></div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
