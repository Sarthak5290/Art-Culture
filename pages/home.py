import streamlit as st
from components.cards import render_category_card


def render(app_data):
    """Render the enhanced home page with hero section and category cards."""
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="main-title">Art & Culture Explorer</h1>
        <p class="hero-subtitle">Discover the rich tapestry of human creativity and cultural heritage</p>
    </div>
    """, unsafe_allow_html=True)

    # Categories Section
    st.markdown('<h2 class="section-title">Explore Categories</h2>', unsafe_allow_html=True)

    # Create responsive grid layout
    categories = list(app_data.keys())
    
    # For better responsive design, use different column layouts based on screen size
    if len(categories) <= 2:
        cols = st.columns(len(categories))
    elif len(categories) == 3:
        cols = st.columns([1, 1, 1])
    else:
        # For 4 categories, use 2x2 grid on larger screens, stack on mobile
        cols = st.columns(2)
        
    # Render category cards
    if len(categories) <= 4:
        for i, category_id in enumerate(categories):
            category_info = app_data[category_id]
            with cols[i % len(cols)]:
                render_category_card(category_id, category_info)
    else:
        # For more than 4 categories, use a different layout
        for i, category_id in enumerate(categories):
            category_info = app_data[category_id]
            col_index = i % 2
            with cols[col_index]:
                render_category_card(category_id, category_info)

    # Add some spacing and a call-to-action section
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Statistics or additional info section - Updated for dark theme
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stats-card" style="text-align: center; padding: 1.5rem; background: var(--card-bg); border-radius: 15px; box-shadow: 0 4px 16px rgba(0,0,0,0.25); border: 1px solid var(--border-color);">
            <h3 style="color: var(--highlight-color); margin-bottom: 0.5rem;">🏛️</h3>
            <h4 style="color: var(--text-light); margin: 0;">Architectural Wonders</h4>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0.5rem 0 0 0;">Explore magnificent structures</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card" style="text-align: center; padding: 1.5rem; background: var(--card-bg); border-radius: 15px; box-shadow: 0 4px 16px rgba(0,0,0,0.25); border: 1px solid var(--border-color);">
            <h3 style="color: var(--highlight-color); margin-bottom: 0.5rem;">🎨</h3>
            <h4 style="color: var(--text-light); margin: 0;">Artistic Masterpieces</h4>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0.5rem 0 0 0;">Discover timeless artworks</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-card" style="text-align: center; padding: 1.5rem; background: var(--card-bg); border-radius: 15px; box-shadow: 0 4px 16px rgba(0,0,0,0.25); border: 1px solid var(--border-color);">
            <h3 style="color: var(--highlight-color); margin-bottom: 0.5rem;">🎭</h3>
            <h4 style="color: var(--text-light); margin: 0;">Cultural Festivals</h4>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0.5rem 0 0 0;">Experience vibrant traditions</p>
        </div>
        """, unsafe_allow_html=True)

    # Footer section - Updated for dark theme
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end)); border-radius: 20px; margin-top: 3rem; border: 1px solid var(--border-color);">
        <p style="color: var(--text-secondary); font-style: italic; margin: 0;">
            "Art and culture are the soul of human civilization, connecting us across time and space."
        </p>
    </div>
    """, unsafe_allow_html=True)