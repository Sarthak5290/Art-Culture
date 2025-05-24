import streamlit as st
from config.settings import PAGE_CONFIG
from loaders.data_loader import load_all_data_streamlit
from utils.session import initialize_session_state
from pages import home, category_detail, item_detail


def apply_custom_css():
    """Apply custom CSS for improved UI."""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Styles */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Custom Color Palette - Blue Theme */
    :root {
        --primary-blue: #4A90E2;
        --secondary-blue: #A8D0FF;
        --deep-blue: #1E3A5F;
        --light-blue: #E8F4FD;
        --accent-blue: #2E86AB;
        --warm-white: #FEFEFE;
        --soft-gray: #F8F9FA;
        --text-dark: #2C3E50;
        --success-green: #28A745;
    }
    
    /* Typography */
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: var(--deep-blue);
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, var(--deep-blue), var(--primary-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 600;
        color: var(--deep-blue);
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
        background: white;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        overflow: hidden;
        transition: all 0.3s ease;
        border: 1px solid rgba(74, 144, 226, 0.2);
        margin-bottom: 2rem;
        position: relative;
    }
    
    .category-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.15);
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
    }
    
    .card-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--deep-blue);
        margin-bottom: 0.8rem;
        text-align: center;
    }
    
    .card-description {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: #666;
        line-height: 1.6;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Item Cards */
    .item-card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.08);
        overflow: hidden;
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(74, 144, 226, 0.1);
    }
    
    .item-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.12);
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
        background: var(--deep-blue) !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 0.4rem 1rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        border: none !important;
        transition: all 0.3s ease !important;
        margin-bottom: 1rem !important;
        width: auto !important;
        min-width: 120px !important;
    }
    
    .nav-button:hover, div[data-testid="column"]:first-child .stButton > button:hover {
        background: var(--primary-blue) !important;
        transform: translateX(-4px) !important;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, var(--light-blue), var(--soft-gray));
        padding: 4rem 2rem;
        margin: -1rem -1rem 3rem -1rem;
        text-align: center;
        border-radius: 0 0 30px 30px;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: #666;
        margin-top: 1rem;
        font-weight: 300;
    }
    
    /* Item Detail Styles */
    .item-detail-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.05);
        border: 1px solid rgba(74, 144, 226, 0.1);
    }
    
    .item-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: var(--deep-blue);
        text-align: center;
        margin-bottom: 2rem;
        line-height: 1.2;
    }
    
    .item-section-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 600;
        color: var(--deep-blue);
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid var(--primary-blue);
        padding-bottom: 0.5rem;
    }
    
    .item-content {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        line-height: 1.7;
        color: var(--text-dark);
        margin-bottom: 1.5rem;
    }
    
    /* Image Gallery */
    .image-gallery {
        margin: 2rem 0;
    }
    
    .gallery-image {
        border-radius: 15px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .gallery-image:hover {
        transform: scale(1.02);
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
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--soft-gray);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-blue);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--deep-blue);
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
    
    /* Success/Info styling */
    .stAlert {
        border-radius: 15px;
        border-left: 4px solid var(--primary-blue);
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

    # Route to appropriate page based on session state
    if st.session_state.view == "home":
        home.render(app_data)
    elif st.session_state.view == "category_detail":
        category_detail.render(app_data)
    elif st.session_state.view == "item_detail":
        item_detail.render(app_data)


if __name__ == "__main__":
    main()