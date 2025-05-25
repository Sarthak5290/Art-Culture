import streamlit as st
from components.cards import render_category_card

# Note: Move this `set_page_config` call to the very top of your main script,
# before any other Streamlit commands or imports that use st.*
# For example, place it at the top of main.py:
# st.set_page_config(
#     page_title="Art & Culture Explorer",
#     page_icon="🎨",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )


# Custom CSS for styling
def inject_styles():
    st.markdown(
        """
        <style>
        /* Global theme variables - Light Blue Theme */
        :root {
            --primary-color: #1E88E5;
            --secondary-color: #42A5F5;
            --bg-color: #F0F8FF;
            --card-bg: #FFFFFF;
            --text-dark: #1A237E;
            --text-secondary: #1976D2;
            --border-color: #BBDEFB;
            --gradient-start: #E3F2FD;
            --gradient-end: #BBDEFB;
            --shadow-light: rgba(30, 136, 229, 0.1);
        }
        
        /* Hide Streamlit menu & footer */
        #MainMenu, footer {
            visibility: hidden;
        }

        /* Hero Section */
        .hero {
           position: relative;
            background: linear-gradient(135deg, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.1)),
                        url('https://images.unsplash.com/photo-1541961017774-22349e4a1262?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
            background-size: cover;
            background-position: center;
            height: 60vh;
            border-radius: 15px;
            margin-bottom: 2rem;
            margin-top: 2rem;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3); 
        }
     .hero-overlay {
            background: rgba(0, 0, 0, 0.5);
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            border-radius: 15px;
        }

        .hero-text {
            position: relative;
            z-index: 1;
        }
        .hero-title {
            font-size: 3rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .hero-subtitle {
            font-size: 1.25rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        
        /* Section Titles */
        .section-title {
            font-size: 2rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
            text-align: center;
        }

        /* Stats Cards */
        .stats-card:hover {
            transform: translateY(-5px);
            transition: 0.3s;
            box-shadow: 0 8px 25px var(--shadow-light);
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
            border-radius: 20px;
            margin-top: 3rem;
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-style: italic;
            box-shadow: 0 4px 16px var(--shadow-light);
        }
        
        /* Enhanced Category Cards for Light Theme */
        .category-card {
            background: var(--card-bg);
            border-radius: 20px;
            box-shadow: 0 8px 32px var(--shadow-light);
            overflow: hidden;
            transition: all 0.3s ease;
            border: 1px solid var(--border-color);
            margin-bottom: 2rem;
            position: relative;
        }
        
        .category-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 16px 48px rgba(30, 136, 229, 0.2);
            border-color: var(--primary-color);
        }
        
        .category-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        }
        
        .card-content {
            padding: 1.5rem;
            background: var(--card-bg);
            color: var(--text-dark);
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
        
        /* App Background */
        .stApp {
            background-color: var(--bg-color);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render(app_data):
    """Render the enhanced home page with hero section and category cards."""
    inject_styles()

    # Hero Section
    st.markdown(
        """
        <div class="hero">
            <div class="hero-overlay"></div>
            <div class="hero-text">
                <h1 class="hero-title">Art & Culture Explorer</h1>
                <p class="hero-subtitle">Discover the rich tapestry of human creativity and cultural heritage</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Explore Categories
    st.markdown(
        '<h2 class="section-title mb-50px">Explore Categories</h2>',
        unsafe_allow_html=True,
    )
    cols_per_row = 4
    categories = list(app_data.items())

    # Render in grid
    for i in range(0, len(categories), cols_per_row):
        cols = st.columns(cols_per_row, gap="large")
        for j, (category_id, category_info) in enumerate(
            categories[i : i + cols_per_row]
        ):
            with cols[j]:
                render_category_card(category_id, category_info)
