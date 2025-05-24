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
        /* Global theme variables */
        :root {
            --primary-color: #4A90E2;
            --secondary-color: #1C2541;
            --bg-color: #0F172A;
            --card-bg: #1E293B;
            --text-light: #F1F5F9;
            --text-secondary: #94A3B8;
            --border-color: #334155;
            --gradient-start: #4A90E2;
            --gradient-end: #6FB3E0;
        }
        
        /* Hide Streamlit menu & footer */
        #MainMenu, footer {
            visibility: hidden;
        }

        /* Hero Section */
        .hero {
            position: relative;
            background-image: url('https://images.unsplash.com/photo-1551958355-02e3c7860535?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80');
            background-size: cover;
            background-position: center;
            height: 50vh;
            border-radius: 15px;
            margin-bottom: 2rem;
            color: var(--text-light);
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
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
        }
        .hero-subtitle {
            font-size: 1.25rem;
        }
        
        /* Section Titles */
        .section-title {
            font-size: 2rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
        }

        /* Stats Cards */
        .stats-card:hover {
            transform: translateY(-5px);
            transition: 0.3s;
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
        '<h2 class="section-title mb-50px">Explore Categories</h2>', unsafe_allow_html=True
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
