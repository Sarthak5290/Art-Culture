import streamlit as st
from utils.session import navigate_to_category, navigate_to_item


def render_category_card(category_id, category_info):
    """Render an enhanced category card with modern styling."""
    st.markdown(f"""
    <div class="category-card">
        <div class="card-image-container">
            <img src="{category_info['mainCardImage']}" alt="{category_info['displayTitle']}" />
        </div>
        <div class="card-content">
            <h3 class="card-title">{category_info['displayTitle']}</h3>
            <p class="card-description">{category_info['displayDescription']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Button with custom styling
    if st.button(
        f"✨ Explore {category_info['displayTitle']}", 
        key=f"explore_cat_{category_id}",
        help=f"Discover amazing {category_info['displayTitle'].lower()}"
    ):
        navigate_to_category(category_id)


def render_item_card(item, category_id, item_index):
    """Render an enhanced item card with modern styling."""
    # Get image URL with fallback
    image_url = get_item_image_url(item)
    item_title = item.get("title", "Untitled Item")
    
    # Get preview text from description or other fields
    preview_text = get_item_preview(item)
    
    st.markdown(f"""
    <div class="item-card">
        <div class="item-image-container">
            <img src="{image_url}" alt="{item_title}" />
        </div>
        <div class="card-content">
            <h4 class="card-title" style="font-size: 1.2rem;">{item_title}</h4>
            <p class="card-description" style="font-size: 0.85rem; margin-bottom: 1rem;">{preview_text}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Button with custom styling
    if st.button(
        "📖 View Details", 
        key=f"view_item_{category_id}_{item_index}",
        help=f"Learn more about {item_title}"
    ):
        navigate_to_item(item)


def get_item_image_url(item):
    """Get the first available image URL or return a styled placeholder."""
    images = item.get("images", [])
    if images and len(images) > 0:
        return images[0]
    
    # Return a more attractive placeholder
    return 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop&crop=center&auto=format&q=60'


def get_item_preview(item):
    """Extract a preview text from the item data."""
    # Try different fields for preview text
    preview_fields = ['description', 'overview', 'summary', 'details', 'information']
    
    for field in preview_fields:
        if field in item and item[field]:
            text = str(item[field])
            # Truncate to a reasonable length
            if len(text) > 120:
                return text[:120] + "..."
            return text
    
    # Try to get preview from list fields
    list_fields = ['features', 'characteristics', 'highlights', 'notable_works']
    for field in list_fields:
        if field in item and isinstance(item[field], list) and item[field]:
            first_item = str(item[field][0])
            if len(first_item) > 100:
                return first_item[:100] + "..."
            return first_item
    
    return "Click to explore more details about this fascinating item."


def render_featured_card(item, category_id, item_index, is_featured=True):
    """Render a featured item card with special styling."""
    image_url = get_item_image_url(item)
    item_title = item.get("title", "Untitled Item")
    preview_text = get_item_preview(item)
    
    featured_class = "featured-card" if is_featured else "item-card"
    
    st.markdown(f"""
    <div class="{featured_class}" style="background: linear-gradient(135deg, #FFF9E6, #FFFFFF); border: 2px solid #D4AF37;">
        <div class="item-image-container" style="height: 220px;">
            <img src="{image_url}" alt="{item_title}" />
            <div style="position: absolute; top: 10px; right: 10px; background: #4A90E2; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; font-weight: 600;">
                ⭐ Featured
            </div>
        </div>
        <div class="card-content">
            <h4 class="card-title" style="font-size: 1.3rem; color: #1E3A5F;">{item_title}</h4>
            <p class="card-description" style="font-size: 0.9rem; margin-bottom: 1.2rem; color: #444;">{preview_text}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(
        "🌟 Explore Featured Item", 
        key=f"featured_item_{category_id}_{item_index}",
        help=f"Discover this featured piece: {item_title}"
    ):
        navigate_to_item(item)


def render_compact_item_list(items, category_id, max_items=6):
    """Render a compact list view of items."""
    st.markdown("### Recent Additions")
    
    for i, item in enumerate(items[:max_items]):
        image_url = get_item_image_url(item)
        item_title = item.get("title", "Untitled Item")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.image(image_url, width=80)
        
        with col2:
            st.markdown(f"""
            <div style="padding-left: 1rem;">
                <h5 style="margin: 0; color: #1E3A5F; font-size: 1rem;">{item_title}</h5>
                <p style="margin: 0.2rem 0; color: #666; font-size: 0.85rem;">{get_item_preview(item)[:80]}...</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("View →", key=f"compact_item_{category_id}_{i}", help=f"View {item_title}"):
                navigate_to_item(item)
        
        if i < len(items[:max_items]) - 1:
            st.markdown("---")