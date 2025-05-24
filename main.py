import streamlit as st
from config.settings import PAGE_CONFIG
from loaders.data_loader import load_all_data_streamlit
from utils.session import initialize_session_state
from utils.router import router
from pages import home, category_detail, item_detail


def apply_custom_css():
    """Apply custom dark theme CSS for improved UI."""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Styles */
    .main {
        padding: 0rem 1rem;
        background-color: #0E1117;
    }
    
    /* Custom Color Palette - Dark Theme */
    :root {
        --primary-blue: #4A90E2;
        --secondary-blue: #6BA3F5;
        --deep-blue: #2E5984;
        --dark-bg: #0E1117;
        --card-bg: #1E1E1E;
        --surface-bg: #262730;
        --accent-blue: #3B82F6;
        --text-light: #FFFFFF;
        --text-secondary: #B8BCC8;
        --text-muted: #8B949E;
        --border-color: #30363D;
        --success-green: #28A745;
        --gradient-start: #1E1E1E;
        --gradient-end: #2A2D3A;
        --highlight-color: #FFD700;
    }
    
    /* Typography */
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: var(--text-light);
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 600;
        color: var(--text-light);
        text-align: center;
        margin: 2rem 0 3rem 0;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-blue), var(--secondary-blue));
        border-radius: 2px;
    }
    
    /* Category Cards */
    .category-card {
        background: var(--card-bg);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        overflow: hidden;
        transition: all 0.3s ease;
        border: 1px solid var(--border-color);
        margin-bottom: 2rem;
        position: relative;
    }
    
    .category-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.4);
        border-color: var(--primary-blue);
    }
    
    .category-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-blue), var(--secondary-blue));
    }
    
    .card-image-container {
        position: relative;
        overflow: hidden;
        height: 200px;
    }
    
    .card-image-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
    }
    
    .category-card:hover .card-image-container img {
        transform: scale(1.05);
    }
    
    .card-content {
        padding: 1.5rem;
        background: var(--card-bg);
        color: var(--text-light);
        border-top: 1px solid var(--border-color);
    }
    
    .card-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--text-light);
        margin-bottom: 0.8rem;
        text-align: center;
    }
    
    .card-description {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: var(--text-secondary);
        line-height: 1.6;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Item Cards */
    .item-card {
        background: var(--card-bg);
        border-radius: 15px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.25);
        overflow: hidden;
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
    }
    
    .item-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.35);
        border-color: var(--primary-blue);
    }
    
    .item-image-container {
        position: relative;
        overflow: hidden;
        height: 180px;
    }
    
    .item-image-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
    }
    
    .item-card:hover .item-image-container img {
        transform: scale(1.03);
    }
    
    /* Custom Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue));
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.7rem 2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(74, 144, 226, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.4);
        background: linear-gradient(135deg, var(--secondary-blue), var(--primary-blue));
    }
    
    /* Navigation Buttons */
    .nav-button, div[data-testid="column"]:first-child .stButton > button {
        background: var(--surface-bg) !important;
        color: var(--text-light) !important;
        border-radius: 20px !important;
        padding: 0.4rem 1rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        border: 1px solid var(--border-color) !important;
        transition: all 0.3s ease !important;
        margin-bottom: 1rem !important;
        width: auto !important;
        min-width: 120px !important;
    }
    
    .nav-button:hover, div[data-testid="column"]:first-child .stButton > button:hover {
        background: var(--primary-blue) !important;
        transform: translateX(-4px) !important;
        border-color: var(--primary-blue) !important;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
        padding: 4rem 2rem;
        margin: -1rem -1rem 3rem -1rem;
        text-align: center;
        border-radius: 0 0 30px 30px;
        border-bottom: 2px solid var(--border-color);
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: var(--text-secondary);
        margin-top: 1rem;
        font-weight: 300;
    }
    
    /* Item Detail Styles */
    .item-detail-container {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
        border: 1px solid var(--border-color);
    }
    
    .item-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: var(--text-light);
        text-align: center;
        margin-bottom: 2rem;
        line-height: 1.2;
    }
    
    .item-section-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 600;
        color: var(--text-light);
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid var(--primary-blue);
        padding-bottom: 0.5rem;
    }
    
    .item-content {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        line-height: 1.7;
        color: var(--text-secondary);
        margin-bottom: 1.5rem;
    }
    
    /* Image Gallery */
    .image-gallery {
        margin: 2rem 0;
    }
    
    .gallery-image {
        border-radius: 15px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.3);
        transition: transform 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .gallery-image:hover {
        transform: scale(1.02);
    }
    
    /* Featured Cards */
    .featured-card {
        background: linear-gradient(135deg, var(--card-bg), var(--surface-bg));
        border: 2px solid var(--highlight-color);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(255, 215, 0, 0.2);
        overflow: hidden;
        transition: all 0.3s ease;
        margin-bottom: 2rem;
        position: relative;
    }
    
    .featured-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(255, 215, 0, 0.3);
    }
    
    /* Compact Navigation Button Styles */
    .compact-nav-button button {
        background: var(--surface-bg) !important;
        color: var(--text-light) !important;
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
    }
    
    .compact-nav-button button:hover {
        background: var(--primary-blue) !important;
        transform: translateX(-1px) !important;
        border-color: var(--primary-blue) !important;
    }
    
    .compact-nav-button {
        text-align: left !important;
        margin-bottom: 1rem !important;
    }
    
    /* Override Streamlit default styles for dark theme */
    .stSelectbox > div > div {
        background-color: var(--surface-bg);
        color: var(--text-light);
        border-color: var(--border-color);
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--primary-blue);
    }
    
    /* Info boxes and containers */
    div[data-testid="stContainer"] > div {
        background-color: transparent;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .section-title {
            font-size: 2rem;
        }
        
        .item-title {
            font-size: 2.2rem;
        }
        
        .hero-section {
            padding: 3rem 1rem;
        }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar for dark theme */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--dark-bg);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-blue);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-blue);
    }
    
    /* Loading animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(74, 144, 226, 0.3);
        border-radius: 50%;
        border-top-color: var(--primary-blue);
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Success/Info styling for dark theme */
    .stAlert {
        border-radius: 15px;
        border-left: 4px solid var(--primary-blue);
        background-color: var(--card-bg);
        color: var(--text-light);
    }
    
    /* Additional dark theme improvements */
    .stExpander {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 10px;
    }
    
    .stExpander summary {
        color: var(--text-light);
    }
    
    /* Override any remaining light backgrounds */
    div[data-testid="column"] > div {
        background-color: transparent;
    }
    
    /* Statistics cards styling for dark theme */
    .stats-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        color: var(--text-light);
    }
    
    .stats-card h3 {
        color: var(--highlight-color);
    }
    
    .stats-card h4 {
        color: var(--text-light);
    }
    
    .stats-card p {
        color: var(--text-secondary);
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    # Configure page
    enhanced_config = {
        **PAGE_CONFIG,
        "page_title": "🎨 Art & Culture Explorer",
        "page_icon": "🎨"
    }
    st.set_page_config(**enhanced_config)

    # Apply custom CSS
    apply_custom_css()

    # Initialize session state
    initialize_session_state()

    # Load data
    app_data = load_all_data_streamlit()

    if app_data is None:
        st.error("Unable to load application data. Please check your data directory.")
        st.stop()

    # Sync session state with URL parameters
    router.sync_session_from_url(app_data)

    # Route to appropriate page based on session state
    if st.session_state.view == "home":
        home.render(app_data)
    elif st.session_state.view == "category_detail":
        category_detail.render(app_data)
    elif st.session_state.view == "item_detail":
        item_detail.render(app_data)


if __name__ == "__main__":
    main()