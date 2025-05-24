import streamlit as st
import json
from components.navigation import render_back_to_category_button


def render(app_data):
    """Render the enhanced item detail page."""
    selected_item = st.session_state.selected_item

    if selected_item:
        render_item_details(selected_item)


def render_item_details(selected_item):
    """Render detailed information about an item with enhanced styling."""

    # Image gallery section - now at the top
    render_image_gallery(selected_item)

    # Enhanced navigation - moved below image
    render_back_to_category_button()

    # Content sections in organized layout
    render_content_sections(selected_item)


def render_image_gallery(selected_item):
    """Render an enhanced image gallery with modern slider and full-screen capability."""
    images = selected_item.get("images", [])

    if images and len(images) > 0:

        # For single image, display simple view with full-screen option
        if len(images) == 1:
            st.markdown(
                """
            <div style="text-align: center; margin: -2rem -1rem 2rem -1rem; height: 100vh; display: flex; align-items: center; justify-content: center;">
            """,
                unsafe_allow_html=True,
            )
            
            # Create single image with fullscreen capability
            single_image_html = f"""
            <style>
                .single-image-container {{
                    position: relative;
                    display: inline-block;
                    cursor: pointer;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                    transition: transform 0.3s ease;
                    max-height: 90vh;
                    max-width: 100%;
                }}
                
                .single-image-container:hover {{
                    transform: scale(1.02);
                }}
                
                .single-image-container img {{
                    max-height: 90vh;
                    max-width: 100%;
                    height: auto;
                    width: auto;
                    object-fit: contain;
                }}
                
                .single-image-fullscreen-btn {{
                    position: absolute;
                    top: 15px;
                    right: 15px;
                    background: rgba(0, 0, 0, 0.8);
                    color: white;
                    border: none;
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    cursor: pointer;
                    font-size: 1.2rem;
                    transition: all 0.3s ease;
                    backdrop-filter: blur(10px);
                }}
                
                .single-image-fullscreen-btn:hover {{
                    background: rgba(0, 255, 136, 0.8);
                    transform: scale(1.1);
                }}
            </style>
            
            <div class="single-image-container" onclick="openFullscreen('{images[0]}', 'Main Image')">
                <img src="{images[0]}" alt="Main Image">
                <button class="single-image-fullscreen-btn" onclick="event.stopPropagation(); openFullscreen('{images[0]}', 'Main Image')">⛶</button>
            </div>
            """
            
            st.components.v1.html(single_image_html, height=800)
            st.markdown("</div>", unsafe_allow_html=True)
            return

        # For multiple images, create modern slider with full-screen capability
        # Prepare image data for JavaScript
        image_data = []
        for i, img_url in enumerate(images):
            image_data.append(
                {
                    "url": img_url,
                    "title": f"Image {i+1}",
                    "description": f"Gallery image {i+1} from {selected_item.get('title', 'Item')}",
                }
            )

        # Create the modern image slider with full-screen support
        slider_html = f"""
        <style>
            .streamlit-gallery-container {{
                background: rgba(30, 30, 30, 0.9);
                border-radius: 16px;
                padding: 25px;
                margin: -2rem -1rem 20px -1rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
                height: 100vh;
                max-height: 100vh;
            }}
            
            .streamlit-slider-container {{
                display: flex;
                gap: 25px;
                align-items: flex-start;
                height: calc(100vh - 50px);
                min-height: calc(100vh - 50px);
            }}
            
            .streamlit-main-image-section {{
                flex: 2;
                position: relative;
            }}
            
            .streamlit-main-image-wrapper {{
                position: relative;
                border-radius: 12px;
                overflow: hidden;
                background: rgba(0, 0, 0, 0.3);
                aspect-ratio: 16/10;
                cursor: pointer;
                transition: transform 0.3s ease;
            }}
            
            .streamlit-main-image-wrapper:hover {{
                transform: scale(1.01);
            }}
            
            .streamlit-main-image {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                transition: opacity 0.3s ease;
            }}
            
            .streamlit-image-overlay {{
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
                padding: 20px;
                color: white;
            }}
            
            .streamlit-image-number {{
                font-size: 2.5rem;
                font-weight: 900;
                color: #00ff88;
                line-height: 1;
                margin-bottom: 8px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }}
            
            .streamlit-image-title {{
                font-size: 1.2rem;
                font-weight: 600;
                margin-bottom: 5px;
            }}
            
            .streamlit-image-description {{
                font-size: 0.85rem;
                color: rgba(255, 255, 255, 0.8);
                line-height: 1.4;
            }}
            
            .streamlit-fullscreen-btn {{
                position: absolute;
                top: 15px;
                right: 15px;
                background: rgba(0, 0, 0, 0.8);
                color: white;
                border: none;
                border-radius: 50%;
                width: 45px;
                height: 45px;
                cursor: pointer;
                font-size: 1.2rem;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
                z-index: 20;
            }}
            
            .streamlit-fullscreen-btn:hover {{
                background: rgba(0, 255, 136, 0.8);
                transform: scale(1.1);
            }}
            
            .streamlit-navigation-arrows {{
                position: absolute;
                top: 50%;
                transform: translateY(-50%);
                background: rgba(0, 0, 0, 0.6);
                border: none;
                color: white;
                width: 45px;
                height: 45px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 1.1rem;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
                z-index: 10;
            }}
            
            .streamlit-navigation-arrows:hover {{
                background: rgba(0, 255, 136, 0.8);
                transform: translateY(-50%) scale(1.1);
            }}
            
            .streamlit-prev-btn {{
                left: 15px;
            }}
            
            .streamlit-next-btn {{
                right: 15px;
            }}
            
            .streamlit-thumbnails-section {{
                flex: 1;
                display: flex;
                flex-direction: column;
                gap: 15px;
            }}
            
            .streamlit-thumbnails-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
                flex-grow: 1;
            }}
            
            .streamlit-thumbnail {{
                aspect-ratio: 1;
                border-radius: 10px;
                overflow: hidden;
                cursor: pointer;
                position: relative;
                transition: all 0.3s ease;
                border: 2px solid transparent;
                background: rgba(0, 0, 0, 0.3);
            }}
            
            .streamlit-thumbnail:hover {{
                transform: scale(1.05);
                border-color: rgba(0, 255, 136, 0.5);
            }}
            
            .streamlit-thumbnail.active {{
                border-color: #00ff88;
                box-shadow: 0 0 15px rgba(0, 255, 136, 0.4);
            }}
            
            .streamlit-thumbnail img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                transition: opacity 0.3s ease;
            }}
            
            .streamlit-thumbnail:hover img {{
                opacity: 0.8;
            }}
            
            .streamlit-thumbnail-number {{
                position: absolute;
                top: 8px;
                right: 8px;
                background: rgba(0, 0, 0, 0.8);
                color: #00ff88;
                font-weight: 700;
                font-size: 0.75rem;
                padding: 3px 6px;
                border-radius: 4px;
                backdrop-filter: blur(5px);
            }}
            
            .streamlit-dots-indicator {{
                display: flex;
                justify-content: center;
                gap: 6px;
                margin-top: 15px;
            }}
            
            .streamlit-dot {{
                width: 6px;
                height: 6px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.3);
                cursor: pointer;
                transition: all 0.3s ease;
            }}
            
            .streamlit-dot.active {{
                background: #00ff88;
                transform: scale(1.2);
            }}
            
            .streamlit-dot:hover {{
                background: rgba(0, 255, 136, 0.6);
            }}
            
            /* Full-screen modal styles */
            .fullscreen-overlay {{
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: rgba(0, 0, 0, 0.95);
                z-index: 9999;
                backdrop-filter: blur(5px);
            }}
            
            .fullscreen-overlay.active {{
                display: flex;
                align-items: center;
                justify-content: center;
                animation: fadeIn 0.3s ease;
            }}
            
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            
            .fullscreen-content {{
                position: relative;
                max-width: 95vw;
                max-height: 95vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .fullscreen-image {{
                max-width: 100%;
                max-height: 100%;
                object-fit: contain;
                border-radius: 8px;
                box-shadow: 0 0 50px rgba(0, 0, 0, 0.8);
            }}
            
            .fullscreen-close {{
                position: absolute;
                top: 20px;
                right: 20px;
                background: rgba(255, 255, 255, 0.9);
                color: #000;
                border: none;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                cursor: pointer;
                font-size: 1.5rem;
                font-weight: bold;
                transition: all 0.3s ease;
                z-index: 10001;
            }}
            
            .fullscreen-close:hover {{
                background: rgba(255, 0, 0, 0.8);
                color: white;
                transform: scale(1.1);
            }}
            
            .fullscreen-nav {{
                position: absolute;
                top: 50%;
                transform: translateY(-50%);
                background: rgba(255, 255, 255, 0.9);
                color: #000;
                border: none;
                border-radius: 50%;
                width: 60px;
                height: 60px;
                cursor: pointer;
                font-size: 1.5rem;
                font-weight: bold;
                transition: all 0.3s ease;
                z-index: 10001;
            }}
            
            .fullscreen-nav:hover {{
                background: rgba(0, 255, 136, 0.9);
                color: white;
                transform: translateY(-50%) scale(1.1);
            }}
            
            .fullscreen-prev {{
                left: 30px;
            }}
            
            .fullscreen-next {{
                right: 30px;
            }}
            
            .fullscreen-info {{
                position: absolute;
                bottom: 30px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 15px 25px;
                border-radius: 25px;
                backdrop-filter: blur(10px);
                text-align: center;
                max-width: 80%;
            }}
            
            .fullscreen-info h3 {{
                margin: 0 0 5px 0;
                font-size: 1.2rem;
                color: #00ff88;
            }}
            
            .fullscreen-info p {{
                margin: 0;
                font-size: 0.9rem;
                opacity: 0.8;
            }}
            
            @media (max-width: 768px) {{
                .streamlit-slider-container {{
                    flex-direction: column;
                    gap: 15px;
                }}
                
                .streamlit-thumbnails-grid {{
                    grid-template-columns: repeat(4, 1fr);
                }}
                
                .fullscreen-nav {{
                    width: 50px;
                    height: 50px;
                    font-size: 1.2rem;
                }}
                
                .fullscreen-prev {{
                    left: 15px;
                }}
                
                .fullscreen-next {{
                    right: 15px;
                }}
                
                .fullscreen-close {{
                    top: 15px;
                    right: 15px;
                    width: 40px;
                    height: 40px;
                    font-size: 1.2rem;
                }}
            }}
        </style>
        
        <div class="streamlit-gallery-container">
            <div class="streamlit-slider-container">
                <div class="streamlit-main-image-section">
                    <div class="streamlit-main-image-wrapper" onclick="openFullscreenSlider()">
                        <img id="streamlitMainImage" class="streamlit-main-image" src="{images[0]}" alt="Main Image">
                        <div class="streamlit-image-overlay">
                            <div id="streamlitImageNumber" class="streamlit-image-number">01</div>
                            <div id="streamlitImageTitle" class="streamlit-image-title">Image 1</div>
                            <div id="streamlitImageDescription" class="streamlit-image-description">Gallery image 1 from {selected_item.get('title', 'Item')}</div>
                        </div>
                    </div>
                    <button class="streamlit-fullscreen-btn" onclick="event.stopPropagation(); openFullscreenSlider()">⛶</button>
                    <button class="streamlit-navigation-arrows streamlit-prev-btn" onclick="streamlitPreviousImage()">‹</button>
                    <button class="streamlit-navigation-arrows streamlit-next-btn" onclick="streamlitNextImage()">›</button>
                </div>
                
                <div class="streamlit-thumbnails-section">
                    <div id="streamlitThumbnailsGrid" class="streamlit-thumbnails-grid">
                        <!-- Thumbnails will be generated here -->
                    </div>
                    <div id="streamlitDotsIndicator" class="streamlit-dots-indicator">
                        <!-- Dots will be generated here -->
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Full-screen overlay -->
        <div id="fullscreenOverlay" class="fullscreen-overlay" onclick="closeFullscreen(event)">
            <div class="fullscreen-content">
                <img id="fullscreenImage" class="fullscreen-image" src="" alt="Full-screen view">
                <button class="fullscreen-close" onclick="closeFullscreen()">&times;</button>
                <button class="fullscreen-nav fullscreen-prev" onclick="fullscreenPrevious()" style="display: none;">‹</button>
                <button class="fullscreen-nav fullscreen-next" onclick="fullscreenNext()" style="display: none;">›</button>
                <div id="fullscreenInfo" class="fullscreen-info">
                    <h3>Image Title</h3>
                    <p>Image Description</p>
                </div>
            </div>
        </div>
        
        <script>
            (function() {{
                const streamlitImages = {json.dumps(image_data)};
                let streamlitCurrentIndex = 0;
                let fullscreenMode = false;

                function streamlitInitializeSlider() {{
                    if (streamlitImages.length === 0) return;
                    
                    streamlitGenerateThumbnails();
                    streamlitGenerateDots();
                    streamlitUpdateMainImage();
                }}

                function streamlitGenerateThumbnails() {{
                    const grid = document.getElementById('streamlitThumbnailsGrid');
                    if (!grid) return;
                    
                    grid.innerHTML = '';
                    
                    // Show first 4 images as thumbnails
                    const thumbnailsToShow = streamlitImages.slice(0, 4);
                    
                    thumbnailsToShow.forEach((image, index) => {{
                        const thumbnail = document.createElement('div');
                        thumbnail.className = `streamlit-thumbnail ${{index === streamlitCurrentIndex ? 'active' : ''}}`;
                        thumbnail.onclick = () => streamlitSetCurrentImage(index);
                        
                        thumbnail.innerHTML = `
                            <img src="${{image.url}}" alt="Thumbnail ${{index + 1}}" loading="lazy">
                            <div class="streamlit-thumbnail-number">${{String(index + 1).padStart(2, '0')}}</div>
                        `;
                        
                        grid.appendChild(thumbnail);
                    }});
                }}

                function streamlitGenerateDots() {{
                    const dotsContainer = document.getElementById('streamlitDotsIndicator');
                    if (!dotsContainer) return;
                    
                    dotsContainer.innerHTML = '';
                    
                    streamlitImages.forEach((_, index) => {{
                        const dot = document.createElement('div');
                        dot.className = `streamlit-dot ${{index === streamlitCurrentIndex ? 'active' : ''}}`;
                        dot.onclick = () => streamlitSetCurrentImage(index);
                        dotsContainer.appendChild(dot);
                    }});
                }}

                function streamlitUpdateMainImage() {{
                    if (streamlitImages.length === 0) return;
                    
                    const mainImage = document.getElementById('streamlitMainImage');
                    const imageNumber = document.getElementById('streamlitImageNumber');
                    const imageTitle = document.getElementById('streamlitImageTitle');
                    const imageDescription = document.getElementById('streamlitImageDescription');
                    
                    if (!mainImage) return;
                    
                    // Fade effect
                    mainImage.style.opacity = '0.7';
                    
                    setTimeout(() => {{
                        mainImage.src = streamlitImages[streamlitCurrentIndex].url;
                        if (imageNumber) imageNumber.textContent = String(streamlitCurrentIndex + 1).padStart(2, '0');
                        if (imageTitle) imageTitle.textContent = streamlitImages[streamlitCurrentIndex].title;
                        if (imageDescription) imageDescription.textContent = streamlitImages[streamlitCurrentIndex].description;
                        
                        mainImage.style.opacity = '1';
                    }}, 150);
                    
                    streamlitUpdateActiveStates();
                }}

                function streamlitUpdateActiveStates() {{
                    // Update thumbnails
                    document.querySelectorAll('.streamlit-thumbnail').forEach((thumb, index) => {{
                        thumb.classList.toggle('active', index === streamlitCurrentIndex);
                    }});
                    
                    // Update dots
                    document.querySelectorAll('.streamlit-dot').forEach((dot, index) => {{
                        dot.classList.toggle('active', index === streamlitCurrentIndex);
                    }});
                }}

                function streamlitSetCurrentImage(index) {{
                    streamlitCurrentIndex = index;
                    streamlitUpdateMainImage();
                    if (fullscreenMode) {{
                        updateFullscreenImage();
                    }}
                }}

                window.streamlitNextImage = function() {{
                    streamlitCurrentIndex = (streamlitCurrentIndex + 1) % streamlitImages.length;
                    streamlitUpdateMainImage();
                }}

                window.streamlitPreviousImage = function() {{
                    streamlitCurrentIndex = (streamlitCurrentIndex - 1 + streamlitImages.length) % streamlitImages.length;
                    streamlitUpdateMainImage();
                }}

                // Full-screen functionality
                window.openFullscreen = function(imageUrl, imageTitle) {{
                    const overlay = document.getElementById('fullscreenOverlay');
                    const image = document.getElementById('fullscreenImage');
                    const info = document.getElementById('fullscreenInfo');
                    
                    if (overlay && image) {{
                        image.src = imageUrl;
                        overlay.classList.add('active');
                        document.body.style.overflow = 'hidden';
                        fullscreenMode = true;
                        
                        if (info) {{
                            info.innerHTML = `
                                <h3>${{imageTitle}}</h3>
                                <p>Press ESC to close or click outside to exit</p>
                            `;
                        }}
                        
                        // Hide navigation for single image
                        const prevBtn = document.querySelector('.fullscreen-prev');
                        const nextBtn = document.querySelector('.fullscreen-next');
                        if (prevBtn) prevBtn.style.display = 'none';
                        if (nextBtn) nextBtn.style.display = 'none';
                    }}
                }}

                window.openFullscreenSlider = function() {{
                    const overlay = document.getElementById('fullscreenOverlay');
                    const image = document.getElementById('fullscreenImage');
                    
                    if (overlay && image && streamlitImages.length > 0) {{
                        updateFullscreenImage();
                        overlay.classList.add('active');
                        document.body.style.overflow = 'hidden';
                        fullscreenMode = true;
                        
                        // Show navigation for multiple images
                        const prevBtn = document.querySelector('.fullscreen-prev');
                        const nextBtn = document.querySelector('.fullscreen-next');
                        if (prevBtn && streamlitImages.length > 1) prevBtn.style.display = 'block';
                        if (nextBtn && streamlitImages.length > 1) nextBtn.style.display = 'block';
                    }}
                }}

                function updateFullscreenImage() {{
                    const image = document.getElementById('fullscreenImage');
                    const info = document.getElementById('fullscreenInfo');
                    
                    if (image && streamlitImages[streamlitCurrentIndex]) {{
                        image.src = streamlitImages[streamlitCurrentIndex].url;
                        
                        if (info) {{
                            info.innerHTML = `
                                <h3>${{streamlitImages[streamlitCurrentIndex].title}}</h3>
                                <p>${{streamlitImages[streamlitCurrentIndex].description}}</p>
                            `;
                        }}
                    }}
                }}

                window.closeFullscreen = function(event) {{
                    if (event && event.target !== event.currentTarget && !event.target.classList.contains('fullscreen-close')) {{
                        return;
                    }}
                    
                    const overlay = document.getElementById('fullscreenOverlay');
                    if (overlay) {{
                        overlay.classList.remove('active');
                        document.body.style.overflow = '';
                        fullscreenMode = false;
                    }}
                }}

                window.fullscreenNext = function() {{
                    streamlitCurrentIndex = (streamlitCurrentIndex + 1) % streamlitImages.length;
                    updateFullscreenImage();
                    streamlitUpdateActiveStates();
                }}

                window.fullscreenPrevious = function() {{
                    streamlitCurrentIndex = (streamlitCurrentIndex - 1 + streamlitImages.length) % streamlitImages.length;
                    updateFullscreenImage();
                    streamlitUpdateActiveStates();
                }}

                // Keyboard navigation
                document.addEventListener('keydown', function(event) {{
                    if (!fullscreenMode) return;
                    
                    switch(event.key) {{
                        case 'Escape':
                            closeFullscreen();
                            break;
                        case 'ArrowLeft':
                            if (streamlitImages.length > 1) fullscreenPrevious();
                            break;
                        case 'ArrowRight':
                            if (streamlitImages.length > 1) fullscreenNext();
                            break;
                    }}
                }});

                // Initialize when DOM is ready
                if (document.readyState === 'loading') {{
                    document.addEventListener('DOMContentLoaded', streamlitInitializeSlider);
                }} else {{
                    streamlitInitializeSlider();
                }}
            }})();
        </script>
        """

        # Render the HTML component with full viewport height
        st.components.v1.html(slider_html, height=800)


def render_content_sections(selected_item):
    """Render content sections in an organized, visually appealing layout."""

    # Define excluded keys and section priorities
    excluded_keys = {"images", "title", "generated_at", "last_modified", "references"}

    # Priority sections that should appear first
    priority_sections = [
        "description",
        "overview",
        "summary",
        "history",
        "significance",
    ]

    # Categorize sections
    main_sections = {}
    list_sections = {}
    other_sections = {}

    for key, value in selected_item.items():
        if key not in excluded_keys and value:  # Only include non-empty values
            if isinstance(value, list):
                list_sections[key] = value
            elif key in priority_sections:
                main_sections[key] = value
            else:
                other_sections[key] = value

    # Render priority/main content sections first
    if main_sections:
        st.markdown('<div class="item-detail-container">', unsafe_allow_html=True)

        for key in priority_sections:
            if key in main_sections:
                render_content_section(key, main_sections[key], is_priority=True)

        # Render other main sections
        for key, value in main_sections.items():
            if key not in priority_sections:
                render_content_section(key, value, is_priority=False)

        st.markdown("</div>", unsafe_allow_html=True)

    # Render list sections in a separate container
    if list_sections:
        st.markdown(
            '<div class="item-detail-container" style="margin-top: 2rem;">',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<h3 class="item-section-title" style="color: var(--text-light);">📋 Additional Information</h3>',
            unsafe_allow_html=True,
        )

        # Create columns for list sections
        list_keys = list(list_sections.keys())
        if len(list_keys) <= 2:
            cols = st.columns(len(list_keys))
        else:
            cols = st.columns(2)

        for i, (key, value) in enumerate(list_sections.items()):
            with cols[i % len(cols)]:
                render_list_section(key, value)

        st.markdown("</div>", unsafe_allow_html=True)

    # Render other sections
    if other_sections:
        st.markdown(
            '<div class="item-detail-container" style="margin-top: 2rem;">',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<h3 class="item-section-title" style="color: var(--text-light);">🔍 Detailed Information</h3>',
            unsafe_allow_html=True,
        )

        for key, value in other_sections.items():
            render_content_section(key, value, is_priority=False)

        st.markdown("</div>", unsafe_allow_html=True)


def render_content_section(key, value, is_priority=False):
    """Render a single content section with appropriate styling."""
    display_title = format_section_title(key)

    if is_priority:
        st.markdown(
            f'<h4 class="item-section-title" style="font-size: 1.4rem; color: var(--text-light);">✨ {display_title}</h4>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<h5 style="color: var(--text-light); margin: 1.5rem 0 0.8rem 0; font-size: 1.1rem;">📌 {display_title}</h5>',
            unsafe_allow_html=True,
        )

    if isinstance(value, dict):
        render_dict_content(value)
    else:
        content = str(value)
        if len(content) > 500:
            # For long content, add expandable section
            with st.expander(
                f"Read full {display_title.lower()}", expanded=is_priority
            ):
                st.markdown(
                    f'<div class="item-content" style="color: var(--text-secondary);">{content}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                f'<div class="item-content" style="color: var(--text-secondary);">{content}</div>',
                unsafe_allow_html=True,
            )


def render_list_section(key, value_list):
    """Render a list section with enhanced styling."""
    display_title = format_section_title(key)

    st.markdown(
        f"""
    <div style="background: var(--surface-bg); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid var(--highlight-color); border: 1px solid var(--border-color);">
        <h5 style="color: var(--text-light); margin: 0 0 1rem 0; font-size: 1.1rem;">📋 {display_title}</h5>
    """,
        unsafe_allow_html=True,
    )

    if value_list:
        for i, item in enumerate(value_list, 1):
            st.markdown(
                f"""
            <div style="margin-bottom: 0.5rem; padding: 0.5rem 0; border-bottom: 1px solid var(--border-color);">
                <span style="color: var(--highlight-color); font-weight: 600;">{i}.</span>
                <span style="color: var(--text-secondary); margin-left: 0.5rem;">{item}</span>
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<p style="color: var(--text-muted); font-style: italic; margin: 0;">No items available.</p>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def render_dict_content(dict_value):
    """Render dictionary content in an organized way."""
    st.markdown(
        """
    <div style="background: var(--surface-bg); padding: 1rem; border-radius: 8px; margin: 1rem 0; border: 1px solid var(--border-color);">
    """,
        unsafe_allow_html=True,
    )

    for sub_key, sub_value in dict_value.items():
        display_key = format_section_title(sub_key)
        st.markdown(
            f"""
        <div style="margin-bottom: 0.8rem;">
            <strong style="color: var(--text-light);">{display_key}:</strong>
            <span style="color: var(--text-secondary); margin-left: 0.5rem;">{sub_value}</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def format_section_title(key):
    """Format section keys into readable titles."""
    # Handle special cases
    title_mappings = {
        "notable_works": "Notable Works",
        "art_style": "Art Style",
        "time_period": "Time Period",
        "birth_date": "Birth Date",
        "death_date": "Death Date",
        "birth_place": "Birth Place",
        "architectural_style": "Architectural Style",
        "construction_period": "Construction Period",
        "cultural_significance": "Cultural Significance",
    }

    if key in title_mappings:
        return title_mappings[key]

    # Default formatting: replace underscores with spaces and capitalize
    return key.replace("_", " ").title()