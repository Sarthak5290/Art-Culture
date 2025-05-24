import streamlit as st
import json
import os
from config.settings import DATA_ROOT, INITIAL_CATEGORIES

@st.cache_data
def load_all_data_streamlit():
    """
    Scans the 'data' directory, loads all JSON files, and organizes them
    into a dictionary structure for the Streamlit application.
    Returns the full item data.
    """
    # Get the absolute path to the data folder (go up one level from loaders/ to app root)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_folder_path = os.path.join(base_dir, DATA_ROOT)

    app_data = {}
    app_data.update(INITIAL_CATEGORIES)

    if not os.path.exists(data_folder_path):
        st.error(f"Data folder not found at: {data_folder_path}")
        return None

    # Walk through the DATA_ROOT directory
    for category_id in INITIAL_CATEGORIES.keys():
        category_path = os.path.join(data_folder_path, category_id)

        if not os.path.isdir(category_path):
            st.warning(f"Category folder '{category_id}' not found at {category_path}")
            continue

        for root, dirs, files in os.walk(category_path):
            for file_name in files:
                if file_name.endswith('.json'):
                    json_file_path = os.path.join(root, file_name)
                    try:
                        with open(json_file_path, 'r', encoding='utf-8') as f:
                            item_data = json.load(f)
                        app_data[category_id]["items"].append(item_data)

                    except json.JSONDecodeError:
                        st.warning(f"Error: Invalid JSON in {json_file_path}")
                    except Exception as e:
                        st.warning(f"Error loading {json_file_path}: {e}")
    
    return app_data