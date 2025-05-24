import streamlit as st
import json
import os

# --- Helper function to load data from JSON files ---
@st.cache_data # Cache the data loading
def load_all_data_streamlit():
    """
    Scans the 'data' directory, loads all JSON files, and organizes them
    into a dictionary structure for the Streamlit application.
    Returns the full item data.
    """
    data_root = 'data'
    # Get the absolute path to the data folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder_path = os.path.join(base_dir, data_root)

    app_data = {}

    # Define the main categories and their display information
    initial_categories = {
        "sculptures_architecture": {
            "displayTitle": "Sculptures & Architecture",
            "displayDescription": "Explore the world of sculptures and architectural marvels.",
            "mainCardImage": "https://lh3.googleusercontent.com/aida-public/AB6AXuCIMvvu009IYKKR23kFB_VvCT-k_d0ry8A1jYHGa30XDXzMdboQ_-yBYPsyw0nqO4PHd9n7cIEdhCymPozDsDegpFXfmjvQNqhQ_6aA0m0Nm0KXRwEjVWwv4QstI7JTIgfzRLfk7xLNjAkmgPkFs79VrUq8SwPllItyxctRykAQLuGd-O9xyAL_NcC9fIlgCxlMw3G77q1RtkanFLBgDDaDChWXcrFqGQW1J2x7_qABbDcy4gyOrWi3HrUn3VcahfLzesNlAd2ils",
            "items": []
        },
        "handicrafts_paintings": {
            "displayTitle": "Handicrafts & Paintings",
            "displayDescription": "Discover the beauty of handicrafts and paintings.",
            "mainCardImage": "https://lh3.googleusercontent.com/aida-public/AB6AXuDpuMxPXONfT-EXyKmwvxQ6PNaeRtAGRcm-sy5i-SEBd1vG-t2rDQxsLDpTKJEtxnfvZBbwhnEhGodoPv2_8zOp3f4p19LwvnVlHeRhxTiyH4eWujenXBDTtVRauKcWvhtkPmRT1FzKLET2bys5NYF9yAbMj6rMCBx1AIKMF-h4Opr_iSAvz3jjRuJPUEdS0TgPqc_TdRm-8cuJbTb0wtzuonY5yjhLb89PkBLSAx9QrOvAQbFNgM-STWt3RECnpAHsy9TJF5xzCpo",
            "items": []
        },
        "performing_arts_festivals": {
            "displayTitle": "Performing Arts & Festivals",
            "displayDescription": "Experience the vibrancy of performing arts and cultural festivals.",
            "mainCardImage": "https://lh3.googleusercontent.com/aida-public/AB6AXuBT1vXNLjkUVsqDjZ_2P11e9jNpcjXOKEfUBourg4kcneojSAoRTLoHUGsGALsquCtr4gwRTdo2f4HeFWf7e0t5Garf34wGjfSjsr3vk_cePSXuJZUUnPD39NXfkU9uo0hFg7IPDvQpoyNkT2Mxn86dqWug2blBZc_XMUbObSZo9_dvprg2zemb6as_U4LsIOTjLyIVELGpPvJnOPTUtQJs-gqamG7cZWxgvrVvDA2LkV-yBu_OfWnVrKHguNzV1PN3ZxvHav6cT4k",
            "items": []
        },
        "artists": {
            "displayTitle": "Artists",
            "displayDescription": "Learn about the lives and works of famous artists.",
            "mainCardImage": "https://lh3.googleusercontent.com/aida-public/AB6AXuCQJIhb-r1gfLguzlLyVcf11L9NjhJ8lq_fU9VtFTVsScOOpF3CezgwqAGOD1kxgRphKcxbKBJZbdpxuRiPvFKbmhyPiryIq3R3VD57G8oA9p6RSTPLD1-a0Bf9g2a-xs6lyVguxQVDJ8iVed3AcJw6rDMDU_NTPenjscWpJCOU5SipjAHC6VY3VvduTva-G8tBMWi35OtuAXeVUHioIYnRJigkGAeLhoTQkflNYUoSlJHjYztyoIurLCXwtY9gu7JgeDduJOyA9c",
            "items": []
        }
    }

    app_data.update(initial_categories)

    if not os.path.exists(data_folder_path):
        st.error(f"Data folder not found at: {data_folder_path}")
        return None

    # Walk through the DATA_ROOT directory
    for category_id in initial_categories.keys():
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
                        # Append the full item data
                        app_data[category_id]["items"].append(item_data)
                        # print(f"Loaded: {json_file_path}") # Can print to console for debugging

                    except json.JSONDecodeError:
                        st.warning(f"Error: Invalid JSON in {json_file_path}")
                    except Exception as e:
                        st.warning(f"Error loading {json_file_path}: {e}")
    return app_data

# --- Streamlit App Layout ---

st.set_page_config(layout="wide") # Use wide layout

# Load data
app_data = load_all_data_streamlit()

if app_data is None:
    st.stop() # Stop if data folder is not found

# Initialize session state for navigation if not already set
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

# --- Navigation Header (Simplified) ---
# Streamlit doesn't have a traditional header like Flask HTML,
# but we can simulate navigation with buttons or sidebar
# For simplicity, we'll use a "Back" button and rely on the view state

# --- Main Content Area ---

# Display Home View
if st.session_state.view == 'home':
    st.title("Art & Culture")
    st.header("Categories")

    # Simulate a grid layout for category cards using columns
    categories = app_data.keys()
    cols = st.columns(len(categories)) # Create a column for each category

    for i, category_id in enumerate(categories):
        category_info = app_data[category_id]
        with cols[i]: # Place content in the respective column
            # Simulate card appearance with container and markdown/image
            with st.container(border=True): # Use st.container with border for card look
                st.image(category_info["mainCardImage"], use_container_width=True)
                st.subheader(category_info["displayTitle"])
                st.write(category_info["displayDescription"])
                # Add a button to navigate to category detail
                if st.button(f"Explore {category_info['displayTitle']}", key=f"explore_cat_{category_id}"):
                    st.session_state.view = 'category_detail'
                    st.session_state.selected_category = category_id
                    st.rerun()

# Display Category Detail View
elif st.session_state.view == 'category_detail':
    selected_category_id = st.session_state.selected_category
    category_info = app_data.get(selected_category_id)

    if st.button("← Back to Categories"):
        st.session_state.view = 'home'
        st.session_state.selected_category = None
        st.session_state.selected_item = None # Clear selected item too
        st.rerun()

    if category_info:
        st.header(category_info["displayTitle"])

        items = category_info.get("items", [])
        if not items:
            st.info(f"No items found for {category_info['displayTitle']}.")
        else:
            # Simulate a grid layout for item cards
            item_cols = st.columns(4) # You can adjust the number of columns
            col_index = 0
            for i, item in enumerate(items):
                with item_cols[col_index]:
                    # Simulate item card
                    with st.container(border=True):
                        # Use the first image from the 'images' array, or a placeholder
                        image_url = (item.get("images") and len(item["images"]) > 0) \
                                    and item["images"][0] or 'https://via.placeholder.com/150?text=No+Image'
                        st.image(image_url, use_container_width=True)
                        st.subheader(item.get("title", "Untitled Item"))
                        # Add a button to view item details
                        if st.button("View Details", key=f"view_item_{selected_category_id}_{i}"):
                            st.session_state.view = 'item_detail'
                            st.session_state.selected_item = item # Store the full item data
                            st.rerun()
                col_index = (col_index + 1) % 4 # Move to the next column, wrap around

# Display Item Detail View
elif st.session_state.view == 'item_detail':
    selected_item = st.session_state.selected_item

    if st.button("← Back to Category"):
        st.session_state.view = 'category_detail'
        # Keep selected_category to go back to the correct category
        st.session_state.selected_item = None # Clear selected item
        st.rerun()

    if selected_item:
        # Display images at the top
        images = selected_item.get("images", [])
        if images and len(images) > 0:
             st.subheader("IMAGES")
             # Display images in columns
             image_cols = st.columns(min(len(images), 4)) # Up to 4 images per row
             for i, image_url in enumerate(images):
                 with image_cols[i % 4]:
                     st.image(image_url, use_container_width=True)

        # Display the main title
        st.title(selected_item.get("title", "Untitled Item"))

        # Display all other key-value pairs and lists
        excluded_keys = ['images', 'title', 'generated_at', 'last_modified', 'references']
        for key, value in selected_item.items():
            if key not in excluded_keys:
                st.subheader(key.replace('_', ' ').upper())
                if isinstance(value, list):
                    if value:
                        for item in value:
                            st.write(f"- {item}") # Display list items with bullet points
                    else:
                         st.write("No items available.")
                elif isinstance(value, dict):
                    st.json(value) # Display nested objects as expandable JSON
                else:
                    st.write(value) # Display other types as text

# You can add more views here following the same pattern