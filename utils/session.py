import streamlit as st
from utils.router import router


def initialize_session_state():
    """Initialize session state variables if not already set."""
    if "view" not in st.session_state:
        st.session_state.view = "home"
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = None
    if "selected_item" not in st.session_state:
        st.session_state.selected_item = None


def scroll_to_top():
    """Force scroll to top of the page using JavaScript."""
    scroll_script = """
    <script>
        // Scroll to top immediately
        window.scrollTo(0, 0);
        
        // Also try document.body.scrollTop for compatibility
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
        
        // Force scroll after a small delay to ensure page is loaded
        setTimeout(function() {
            window.scrollTo(0, 0);
            document.body.scrollTop = 0;
            document.documentElement.scrollTop = 0;
        }, 100);
        
        // Additional attempt after longer delay for slower loads
        setTimeout(function() {
            window.scrollTo(0, 0);
            document.body.scrollTop = 0;
            document.documentElement.scrollTop = 0;
        }, 300);
    </script>
    """
    st.components.v1.html(scroll_script, height=0)


def navigate_to_home():
    """Navigate to home page and clear selections."""
    router.navigate_to_home()
    scroll_to_top()


def navigate_to_category(category_id):
    """Navigate to category detail page."""
    router.navigate_to_category(category_id)
    scroll_to_top()


def navigate_to_item(item):
    """Navigate to item detail page."""
    category_id = st.session_state.get("selected_category")
    if not category_id:
        # If no category is selected, we can't navigate to item
        # This shouldn't happen in normal flow, but handle gracefully
        st.error("Cannot navigate to item without selecting a category first.")
        return

    router.navigate_to_item(item, category_id)
    scroll_to_top()


def back_to_category():
    """Navigate back to category detail page."""
    router.back_to_category()
    scroll_to_top()


def get_current_view():
    """Get the current view from session state."""
    return st.session_state.get("view", "home")


def get_selected_category():
    """Get the currently selected category."""
    return st.session_state.get("selected_category")


def get_selected_item():
    """Get the currently selected item."""
    return st.session_state.get("selected_item")


def set_view(view_name):
    """Set the current view (use with caution - prefer navigation methods)."""
    st.session_state.view = view_name
    scroll_to_top()


def inject_scroll_fix_css():
    """Inject CSS to ensure smooth scrolling and proper page positioning."""
    scroll_css = """
    <style>
        /* Ensure smooth scrolling */
        html {
            scroll-behavior: smooth;
        }
        
        /* Fix any potential scroll issues */
        body {
            overflow-x: hidden;
        }
        
        /* Ensure main content starts from top */
        .main .block-container {
            padding-top: 1rem !important;
            margin-top: 0 !important;
        }
        
        /* Remove any unwanted top margins */
        .stApp > div:first-child {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        
        /* Fix for Streamlit's default spacing */
        div[data-testid="stAppViewContainer"] {
            padding-top: 0 !important;
        }
        
        /* Ensure consistent top positioning */
        .stApp {
            padding-top: 0 !important;
        }
    </style>
    """
    st.markdown(scroll_css, unsafe_allow_html=True)


def add_page_transition_effect():
    """Add a subtle page transition effect."""
    transition_css = """
    <style>
        /* Page transition effect */
        .main {
            animation: fadeIn 0.3s ease-in-out;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Smooth transitions for content */
        .block-container {
            transition: all 0.3s ease;
        }
    </style>
    """
    st.markdown(transition_css, unsafe_allow_html=True)


def enhanced_scroll_to_top():
    """Enhanced scroll to top with multiple fallback methods."""
    enhanced_scroll_script = """
    <script>
        function scrollToTop() {
            // Method 1: Standard window.scrollTo
            if (window.scrollTo) {
                window.scrollTo({
                    top: 0,
                    left: 0,
                    behavior: 'auto'
                });
            }
            
            // Method 2: Direct property setting
            if (document.documentElement) {
                document.documentElement.scrollTop = 0;
            }
            
            if (document.body) {
                document.body.scrollTop = 0;
            }
            
            // Method 3: Try to scroll parent containers
            const containers = document.querySelectorAll('.main, .stApp, [data-testid="stAppViewContainer"]');
            containers.forEach(container => {
                if (container) {
                    container.scrollTop = 0;
                }
            });
            
            // Method 4: Focus on top element to ensure position
            const topElement = document.querySelector('.main') || document.body;
            if (topElement && topElement.focus) {
                topElement.focus();
            }
        }
        
        // Execute immediately
        scrollToTop();
        
        // Execute after DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', scrollToTop);
        }
        
        // Execute after a short delay
        setTimeout(scrollToTop, 50);
        setTimeout(scrollToTop, 150);
        setTimeout(scrollToTop, 300);
        
        // Execute when page is fully loaded
        window.addEventListener('load', scrollToTop);
        
        // Also try when Streamlit finishes rendering
        const observer = new MutationObserver(function(mutations) {
            scrollToTop();
        });
        
        // Observe changes to detect when Streamlit updates
        const targetNode = document.querySelector('.main') || document.body;
        if (targetNode) {
            observer.observe(targetNode, {
                childList: true,
                subtree: false
            });
            
            // Stop observing after 1 second to avoid infinite loops
            setTimeout(() => observer.disconnect(), 1000);
        }
    </script>
    """
    st.components.v1.html(enhanced_scroll_script, height=0)


def force_page_refresh_scroll():
    """Force scroll to top using meta refresh technique as fallback."""
    # This is a more aggressive approach for stubborn cases
    st.markdown(
        """
    <script>
        // Force scroll to top using multiple techniques
        function forceScrollTop() {
            // Immediate scroll
            window.scrollTo(0, 0);
            
            // Scroll all possible containers
            const scrollableElements = [
                window,
                document.documentElement,
                document.body,
                ...document.querySelectorAll('.main'),
                ...document.querySelectorAll('.stApp'),
                ...document.querySelectorAll('[data-testid="stAppViewContainer"]'),
                ...document.querySelectorAll('.block-container')
            ];
            
            scrollableElements.forEach(element => {
                if (element && typeof element.scrollTo === 'function') {
                    element.scrollTo(0, 0);
                }
                if (element && 'scrollTop' in element) {
                    element.scrollTop = 0;
                }
            });
        }
        
        // Execute multiple times with different delays
        forceScrollTop();
        requestAnimationFrame(forceScrollTop);
        setTimeout(forceScrollTop, 0);
        setTimeout(forceScrollTop, 10);
        setTimeout(forceScrollTop, 50);
        setTimeout(forceScrollTop, 100);
    </script>
    """,
        unsafe_allow_html=True,
    )
