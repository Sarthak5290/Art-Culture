import streamlit as st
import json


def render_image_gallery(selected_item):
    """Render an enhanced image gallery with modern slider and full-screen capability."""
    images = selected_item.get("images", [])

    if not images or len(images) == 0:
        return

    # For single image, display simple view with full-screen option
    if len(images) == 1:
        render_single_image(images[0])
        return

    # For multiple images, create modern slider with full-screen capability
    render_image_slider(images, selected_item)


def render_single_image(image_url):
    """Render a single image with fullscreen capability."""
    st.markdown(
        """
        <div style="text-align: center; margin: 2rem 0;">
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
            box-shadow: 0 8px 32px var(--shadow-light);
            transition: transform 0.3s ease;
            border: 2px solid var(--border-color);
        }}
        
        .single-image-container:hover {{
            transform: scale(1.02);
            box-shadow: 0 12px 40px var(--shadow-medium);
            border-color: var(--primary-blue);
        }}
        
        .single-image-fullscreen-btn {{
            position: absolute;
            top: 15px;
            right: 15px;
            background: var(--primary-blue);
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            cursor: pointer;
            font-size: 1.2rem;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 8px var(--shadow-light);
        }}
        
        .single-image-fullscreen-btn:hover {{
            background: var(--secondary-blue);
            transform: scale(1.1);
            box-shadow: 0 4px 12px var(--shadow-medium);
        }}
    </style>
    
    <div class="single-image-container" onclick="openFullscreen('{image_url}', 'Main Image')">
        <img src="{image_url}" style="max-width: 100%; height: auto; display: block;" alt="Main Image">
        <button class="single-image-fullscreen-btn" onclick="event.stopPropagation(); openFullscreen('{image_url}', 'Main Image')">⛶</button>
    </div>
    """

    st.components.v1.html(single_image_html, height=400)
    st.markdown("</div>", unsafe_allow_html=True)


def render_image_slider(images, selected_item):
    """Render a multi-image slider with full-screen capability."""
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
    {get_slider_styles()}
    
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
    
    {get_fullscreen_overlay()}
    
    <script>
        {get_slider_javascript(image_data)}
    </script>
    """

    # Render the HTML component with increased height for better viewing
    st.components.v1.html(slider_html, height=600)


def get_slider_styles():
    """Return CSS styles for the image slider."""
    return """
    <style>
        .streamlit-gallery-container {
            background: var(--card-bg);
            border-radius: 16px;
            padding: 25px;
            margin: 20px 0;
            border: 2px solid var(--border-color);
            box-shadow: 0 8px 32px var(--shadow-light);
        }
        
        .streamlit-slider-container {
            display: flex;
            gap: 25px;
            align-items: flex-start;
            min-height: 400px;
        }
        
        .streamlit-main-image-section {
            flex: 2;
            position: relative;
        }
        
        .streamlit-main-image-wrapper {
            position: relative;
            border-radius: 12px;
            overflow: hidden;
            background: var(--surface-bg);
            aspect-ratio: 16/10;
            cursor: pointer;
            transition: transform 0.3s ease;
            border: 2px solid var(--border-color);
        }
        
        .streamlit-main-image-wrapper:hover {
            transform: scale(1.01);
            border-color: var(--primary-blue);
            box-shadow: 0 4px 16px var(--shadow-light);
        }
        
        .streamlit-main-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: opacity 0.3s ease;
        }
        
        .streamlit-image-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(transparent, rgba(30, 136, 229, 0.9));
            padding: 20px;
            color: white;
        }
        
        .streamlit-image-number {
            font-size: 2.5rem;
            font-weight: 900;
            color: var(--highlight-color);
            line-height: 1;
            margin-bottom: 8px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        
        .streamlit-image-title {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .streamlit-image-description {
            font-size: 0.85rem;
            color: rgba(255, 255, 255, 0.9);
            line-height: 1.4;
        }
        
        .streamlit-fullscreen-btn {
            position: absolute;
            top: 15px;
            right: 15px;
            background: var(--primary-blue);
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
            box-shadow: 0 2px 8px var(--shadow-light);
        }
        
        .streamlit-fullscreen-btn:hover {
            background: var(--secondary-blue);
            transform: scale(1.1);
            box-shadow: 0 4px 12px var(--shadow-medium);
        }
        
        .streamlit-navigation-arrows {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: var(--primary-blue);
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
            box-shadow: 0 2px 8px var(--shadow-light);
        }
        
        .streamlit-navigation-arrows:hover {
            background: var(--secondary-blue);
            transform: translateY(-50%) scale(1.1);
            box-shadow: 0 4px 12px var(--shadow-medium);
        }
        
        .streamlit-prev-btn {
            left: 15px;
        }
        
        .streamlit-next-btn {
            right: 15px;
        }
        
        .streamlit-thumbnails-section {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .streamlit-thumbnails-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            flex-grow: 1;
        }
        
        .streamlit-thumbnail {
            aspect-ratio: 1;
            border-radius: 10px;
            overflow: hidden;
            cursor: pointer;
            position: relative;
            transition: all 0.3s ease;
            border: 2px solid var(--border-color);
            background: var(--surface-bg);
            box-shadow: 0 2px 8px var(--shadow-light);
        }
        
        .streamlit-thumbnail:hover {
            transform: scale(1.05);
            border-color: var(--primary-blue);
            box-shadow: 0 4px 12px var(--shadow-medium);
        }
        
        .streamlit-thumbnail.active {
            border-color: var(--highlight-color);
            box-shadow: 0 0 15px rgba(255, 152, 0, 0.4);
        }
        
        .streamlit-thumbnail img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: opacity 0.3s ease;
        }
        
        .streamlit-thumbnail:hover img {
            opacity: 0.8;
        }
        
        .streamlit-thumbnail-number {
            position: absolute;
            top: 8px;
            right: 8px;
            background: var(--primary-blue);
            color: white;
            font-weight: 700;
            font-size: 0.75rem;
            padding: 3px 6px;
            border-radius: 4px;
            backdrop-filter: blur(5px);
            box-shadow: 0 1px 3px var(--shadow-light);
        }
        
        .streamlit-dots-indicator {
            display: flex;
            justify-content: center;
            gap: 6px;
            margin-top: 15px;
        }
        
        .streamlit-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--border-color);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .streamlit-dot.active {
            background: var(--primary-blue);
            transform: scale(1.2);
        }
        
        .streamlit-dot:hover {
            background: var(--secondary-blue);
        }
        
        @media (max-width: 768px) {
            .streamlit-slider-container {
                flex-direction: column;
                gap: 15px;
            }
            
            .streamlit-thumbnails-grid {
                grid-template-columns: repeat(4, 1fr);
            }
            
            .streamlit-gallery-container {
                padding: 15px;
            }
        }
    </style>
    """


def get_fullscreen_overlay():
    """Return HTML for the fullscreen overlay."""
    return """
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
    
    <style>
        /* Full-screen modal styles - Light Blue Theme */
        .fullscreen-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(30, 136, 229, 0.95);
            z-index: 9999;
            backdrop-filter: blur(5px);
        }
        
        .fullscreen-overlay.active {
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .fullscreen-content {
            position: relative;
            max-width: 95vw;
            max-height: 95vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .fullscreen-image {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            border-radius: 8px;
            box-shadow: 0 0 50px rgba(0, 0, 0, 0.3);
            border: 2px solid var(--border-color);
        }
        
        .fullscreen-close {
            position: absolute;
            top: 20px;
            right: 20px;
            background: var(--card-bg);
            color: var(--text-primary);
            border: 2px solid var(--border-color);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            cursor: pointer;
            font-size: 1.5rem;
            font-weight: bold;
            transition: all 0.3s ease;
            z-index: 10001;
            box-shadow: 0 4px 12px var(--shadow-medium);
        }
        
        .fullscreen-close:hover {
            background: #dc3545;
            color: white;
            border-color: #dc3545;
            transform: scale(1.1);
        }
        
        .fullscreen-nav {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: var(--card-bg);
            color: var(--text-primary);
            border: 2px solid var(--border-color);
            border-radius: 50%;
            width: 60px;
            height: 60px;
            cursor: pointer;
            font-size: 1.5rem;
            font-weight: bold;
            transition: all 0.3s ease;
            z-index: 10001;
            box-shadow: 0 4px 12px var(--shadow-medium);
        }
        
        .fullscreen-nav:hover {
            background: var(--primary-blue);
            color: white;
            border-color: var(--primary-blue);
            transform: translateY(-50%) scale(1.1);
        }
        
        .fullscreen-prev {
            left: 30px;
        }
        
        .fullscreen-next {
            right: 30px;
        }
        
        .fullscreen-info {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--card-bg);
            color: var(--text-primary);
            padding: 15px 25px;
            border-radius: 25px;
            backdrop-filter: blur(10px);
            text-align: center;
            max-width: 80%;
            border: 2px solid var(--border-color);
            box-shadow: 0 4px 16px var(--shadow-medium);
        }
        
        .fullscreen-info h3 {
            margin: 0 0 5px 0;
            font-size: 1.2rem;
            color: var(--primary-blue);
        }
        
        .fullscreen-info p {
            margin: 0;
            font-size: 0.9rem;
            color: var(--text-secondary);
        }
        
        @media (max-width: 768px) {
            .fullscreen-nav {
                width: 50px;
                height: 50px;
                font-size: 1.2rem;
            }
            
            .fullscreen-prev {
                left: 15px;
            }
            
            .fullscreen-next {
                right: 15px;
            }
            
            .fullscreen-close {
                top: 15px;
                right: 15px;
                width: 40px;
                height: 40px;
                font-size: 1.2rem;
            }
            
            .fullscreen-info {
                bottom: 20px;
                padding: 10px 20px;
                max-width: 90%;
            }
        }
    </style>
    """


def get_slider_javascript(image_data):
    """Return JavaScript code for the image slider functionality."""
    return f"""
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
    """
