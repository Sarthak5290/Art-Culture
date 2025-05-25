import streamlit as st
from config.settings import PAGE_CONFIG
from loaders.data_loader import load_all_data_streamlit
from utils.session import initialize_session_state
from utils.router import router
from pages import home, category_detail, item_detail


def apply_custom_css():
    """Apply custom light-blue theme CSS for improved UI."""
    st.markdown(
        """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide sidebar collapse/expand button */
    .css-1vbkxwb {display: none;}
    button[data-testid="collapsedControl"] {display: none;}
    .css-1rs6os {display: none;}
    .css-1cypcdb {display: none;}
    .streamlit-expanderHeader {display: none;}
    div[data-testid="stSidebarCollapsedControl"] {display: none;}
    .css-1outpf7 {display: none;}
    
        /* Hide Streamlit elements */
    #MainMenu {display: none;}
    footer {display: none;}
    header {display: none;}
    
    /* Hide Sidebar Completely */
    .css-1d391kg {display: none;}
    .css-1aumxhk {display: none;}
    section[data-testid="stSidebar"] {display: none;}
    .css-17eq0hr {display: none;}
    .css-1cypcdb {display: none;}
    .css-1544g2n {display: none;}
    div[data-testid="stSidebarNav"] {display: none;}
    .css-1lcbmhc {display: none;}
    .css-1outpf7 {display: none;}
    
    /* Remove top spacing and adjust main content to full width */
    .stApp {
        margin-top: -100px !important;
        padding-top: 0 !important;
    }
    
    .main .block-container {
        padding-top: 0 !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: none !important;
        width: 100% !important;
        margin-top: 0 !important;
    }
    
    /* Ensure content uses full width and removes top spacing */
    .stApp > div:first-child {
        margin-left: 0 !important;
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Remove any default top margins/padding */
    div[data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    div[data-testid="stMain"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Global Styles - Light Blue Theme */
    .main {
        padding: 0rem 1rem;
        background-color: #F0F8FF;
        margin-top: 0 !important;
    }
    
    /* Custom Color Palette - Light Blue Theme */
    :root {
        --primary-blue: #1E88E5;
        --secondary-blue: #42A5F5;
        --deep-blue: #1565C0;
        --light-bg: #F0F8FF;
        --card-bg: #FFFFFF;
        --surface-bg: #E3F2FD;
        --accent-blue: #2196F3;
        --text-dark: #1A237E;
        --text-primary: #0D47A1;
        --text-secondary: #1976D2;
        --text-muted: #5C6BC0;
        --border-color: #BBDEFB;
        --success-green: #4CAF50;
        --gradient-start: #E3F2FD;
        --gradient-end: #BBDEFB;
        --highlight-color: #FF9800;
        --shadow-light: rgba(30, 136, 229, 0.1);
        --shadow-medium: rgba(30, 136, 229, 0.2);
        --shadow-strong: rgba(30, 136, 229, 0.3);
    }
    
    /* Typography */
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: var(--text-dark);
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(30, 136, 229, 0.1);
        background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 600;
        color: var(--text-dark);
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
        box-shadow: 0 8px 32px var(--shadow-light);
        overflow: hidden;
        transition: all 0.3s ease;
        border: 1px solid var(--border-color);
        margin-bottom: 2rem;
        margin-top: 3rem;
        position: relative;
    }
    
    .category-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px var(--shadow-medium);
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
        color: var(--text-dark);
        border-top: 1px solid var(--border-color);
    }
    
    .card-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--text-dark);
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
        box-shadow: 0 6px 24px var(--shadow-light);
        overflow: hidden;
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
    }
    
    .item-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px var(--shadow-medium);
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
        box-shadow: 0 4px 16px var(--shadow-light);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px var(--shadow-medium);
        background: linear-gradient(135deg, var(--secondary-blue), var(--primary-blue));
    }
    
    /* Navigation Buttons */
    .nav-button, div[data-testid="column"]:first-child .stButton > button {
        background: var(--surface-bg) !important;
        color: var(--text-primary) !important;
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
        color: white !important;
        transform: translateX(-4px) !important;
        border-color: var(--primary-blue) !important;
    }
    
    /* Hero Section - Updated for light theme */
    .hero-section {
        background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
        padding: 4rem 2rem;
        margin: -1rem -1rem 3rem -1rem;
        text-align: center;
        border-radius: 0 0 30px 30px;
        border-bottom: 2px solid var(--border-color);
        margin-top: -1rem !important;
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
        box-shadow: 0 8px 32px var(--shadow-light);
        border: 1px solid var(--border-color);
    }
    
    .item-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: var(--text-dark);
        text-align: center;
        margin-bottom: 2rem;
        line-height: 1.2;
    }
    
    .item-section-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 600;
        color: var(--text-dark);
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
        box-shadow: 0 6px 24px var(--shadow-light);
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
        box-shadow: 0 8px 32px rgba(255, 152, 0, 0.2);
        overflow: hidden;
        transition: all 0.3s ease;
        margin-bottom: 2rem;
        position: relative;
    }
    
    .featured-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(255, 152, 0, 0.3);
    }
    
    /* Compact Navigation Button Styles */
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
    }
    
    .compact-nav-button button:hover {
        background: var(--primary-blue) !important;
        color: white !important;
        transform: translateX(-1px) !important;
        border-color: var(--primary-blue) !important;
    }
    
    .compact-nav-button {
        text-align: left !important;
        margin-bottom: 1rem !important;
    }
    
    /* Override Streamlit default styles for light theme */
    .stSelectbox > div > div {
        background-color: var(--card-bg);
        color: var(--text-dark);
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
    
    /* Custom scrollbar for light theme */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--light-bg);
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
        border: 3px solid rgba(30, 136, 229, 0.3);
        border-radius: 50%;
        border-top-color: var(--primary-blue);
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Success/Info styling for light theme */
    .stAlert {
        border-radius: 15px;
        border-left: 4px solid var(--primary-blue);
        background-color: var(--surface-bg);
        color: var(--text-dark);
    }
    
    /* Additional light theme improvements */
    .stExpander {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 10px;
    }
    
    .stExpander summary {
        color: var(--text-dark);
    }
    
    /* Override any remaining backgrounds */
    div[data-testid="column"] > div {
        background-color: transparent;
    }
    
    /* Statistics cards styling for light theme */
    .stats-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        color: var(--text-dark);
        box-shadow: 0 4px 16px var(--shadow-light);
    }
    
    .stats-card h3 {
        color: var(--highlight-color);
    }
    
    .stats-card h4 {
        color: var(--text-dark);
    }
    
    .stats-card p {
        color: var(--text-secondary);
    }
    
    /* Light theme specific adjustments */
    .stApp {
        background-color: var(--light-bg);
    }
    
    /* Text inputs and form elements */
    .stTextInput > div > div > input {
        background-color: var(--card-bg);
        color: var(--text-dark);
        border-color: var(--border-color);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 2px rgba(30, 136, 229, 0.2);
    }
    
    /* Dataframe and table styling */
    .stDataFrame {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 10px;
    }
    
    /* Warning and error messages */
    .stWarning {
        background-color: rgba(255, 193, 7, 0.1);
        color: #856404;
        border-left: 4px solid #ffc107;
    }
    
    .stError {
        background-color: rgba(220, 53, 69, 0.1);
        color: #721c24;
        border-left: 4px solid #dc3545;
    }
    
    .stSuccess {
        background-color: rgba(40, 167, 69, 0.1);
        color: #155724;
        border-left: 4px solid #28a745;
    }
    
    .stInfo {
        background-color: rgba(30, 136, 229, 0.1);
        color: var(--text-primary);
        border-left: 4px solid var(--primary-blue);
    }
    
    /* Enhanced visual hierarchy with light blue gradients */
    .gradient-bg-light {
        background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
    }
    
    .gradient-bg-medium {
        background: linear-gradient(135deg, #BBDEFB, #90CAF9);
    }
    
    .gradient-text {
        background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Hover effects for better interactivity */
    .hover-lift {
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .hover-lift:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px var(--shadow-medium);
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def main():
    # Configure page
    enhanced_config = {
        **PAGE_CONFIG,
        "page_title": "🎨 Art & Culture Explorer",
        "page_icon": "🎨",
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
