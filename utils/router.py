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
    def generate_item_id(item):
        """Generate a unique ID for an item."""
        # Try to use existing ID first
        if 'id' in item and item['id']:
            return str(item['id'])
        
        # Generate from title
        title = item.get('title', 'untitled')
        # Clean the title for URL use
        item_id = title.lower().replace(' ', '_').replace('-', '_')
        # Remove special characters
        item_id = ''.join(c for c in item_id if c.isalnum() or c == '_')
        return item_id
    
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
        item_id = StreamlitRouter.generate_item_id(item)
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
        else:
            StreamlitRouter.navigate_to_home()
    
    @staticmethod
    def sync_session_from_url(app_data):
        """Sync session state from URL parameters without triggering navigation."""
        params = st.query_params
        
        # Get URL parameters
        page = params.get("page", "home")
        category_id = params.get("category")
        item_id = params.get("item")
        
        # Set session state based on URL - DO NOT call navigation methods here
        # to avoid recursion and multiple st.rerun() calls
        
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
                # Invalid category, set to home but don't navigate
                st.session_state.view = 'home'
                st.session_state.selected_category = None
                st.session_state.selected_item = None
                st.query_params.clear()
                
        elif page == "item" and category_id and item_id:
            if category_id in app_data:
                # Find the item in the category
                items = app_data[category_id].get('items', [])
                selected_item = None
                
                for item in items:
                    # Match by generated ID
                    current_item_id = StreamlitRouter.generate_item_id(item)
                    if current_item_id == item_id:
                        selected_item = item
                        break
                
                if selected_item:
                    st.session_state.view = 'item_detail'
                    st.session_state.selected_category = category_id
                    st.session_state.selected_item = selected_item
                else:
                    # Item not found, go to category
                    st.session_state.view = 'category_detail'
                    st.session_state.selected_category = category_id
                    st.session_state.selected_item = None
                    st.query_params.update({
                        "page": "category",
                        "category": category_id
                    })
            else:
                # Invalid category, go to home
                st.session_state.view = 'home'
                st.session_state.selected_category = None
                st.session_state.selected_item = None
                st.query_params.clear()
        else:
            # Invalid page, go to home
            st.session_state.view = 'home'
            st.session_state.selected_category = None
            st.session_state.selected_item = None
            st.query_params.clear()


# Create a global router instance
router = StreamlitRouter()