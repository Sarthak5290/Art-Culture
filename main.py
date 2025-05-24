import streamlit as st
from config.settings import PAGE_CONFIG
from loaders.data_loader import load_all_data_streamlit
from utils.session import initialize_session_state
from pages import home, category_detail, item_detail


def main():
    # Configure page
    st.set_page_config(**PAGE_CONFIG)

    # Initialize session state
    initialize_session_state()

    # Load data
    app_data = load_all_data_streamlit()

    if app_data is None:
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
