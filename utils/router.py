import streamlit as st
from urllib.parse import urlencode


class StreamlitRouter:
    """Handle URL routing for Streamlit applications."""
    
    @staticmethod
    def get_query_params():
        """Get current URL query parameters."""
        return st.query_params
    
    @staticmethod
    def set_query_params(**params):
        """Set URL query parameters."""
        # Filter out None values
        clean_params = {k: v for k, v in params.items() if v is not None}
        st.query_params.update(clean_params)
    
    @staticmethod
    def clear_query_params():
        """Clear all query parameters."""
        st.query_params.clear()
    
    @staticmethod
    def navigate_to_home():
        """Navigate to home page."""
        st.query_params.clear()
        st.session_state.view = 'home'
        st.session_state.selected_category = None
        st.session_state.selected_item = None
        st.rerun()
    
    @staticmethod
    def navigate_to_category(category_id):
        """Navigate to category detail page."""
        st.query_params.update({
            "page": "category",
            "category": category_id
        })
        st.session_state.view = 'category_detail'
        st.session_state.selected_category = category_id
        st.session_state.selected_item = None
        st.rerun()
    
    @staticmethod
    def navigate_to_item(item, category_id):
        """Navigate to item detail page."""
        item_id = item.get('id') or item.get('title', '').replace(' ', '_').lower()
        st.query_params.update({
            "page": "item",
            "category": category_id,
            "item": item_id
        })
        st.session_state.view = 'item_detail'
        st.session_state.selected_category = category_id
        st.session_state.selected_item = item
        st.rerun()
    
    @staticmethod
    def back_to_category():
        """Navigate back to category detail page."""
        category_id = st.session_state.get('selected_category')
        if category_id:
            st.query_params.update({
                "page": "category",
                "category": category_id
            })
        st.session_state.view = 'category_detail'
        st.session_state.selected_item = None
        st.rerun()
    
    @staticmethod
    def sync_session_from_url(app_data):
        """Sync session state from URL parameters."""
        params = st.query_params
        
        # Get URL parameters
        page = params.get("page", "home")
        category_id = params.get("category")
        item_id = params.get("item")
        
        # Set session state based on URL
        if page == "home" or not page:
            st.session_state.view = 'home'
            st.session_state.selected_category = None
            st.session_state.selected_item = None
            
        elif page == "category" and category_id:
            if category_id in app_data:
                st.session_state.view = 'category_detail'
                st.session_state.selected_category = category_id
                st.session_state.selected_item = None
            else:
                # Invalid category, redirect to home
                StreamlitRouter.navigate_to_home()
                
        elif page == "item" and category_id and item_id:
            if category_id in app_data:
                # Find the item in the category
                items = app_data[category_id].get('items', [])
                selected_item = None
                
                for item in items:
                    # Match by ID or title
                    current_item_id = item.get('id') or item.get('title', '').replace(' ', '_').lower()
                    if current_item_id == item_id:
                        selected_item = item
                        break
                
                if selected_item:
                    st.session_state.view = 'item_detail'
                    st.session_state.selected_category = category_id
                    st.session_state.selected_item = selected_item
                else:
                    # Item not found, redirect to category
                    StreamlitRouter.navigate_to_category(category_id)
            else:
                # Invalid category, redirect to home
                StreamlitRouter.navigate_to_home()
        else:
            # Invalid page, redirect to home
            StreamlitRouter.navigate_to_home()


# Create a global router instance
router = StreamlitRouter()