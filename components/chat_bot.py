import streamlit as st
import uuid


def render_chat_bot():
    """Render an enhanced rounded chat bot toggle button with modern UI and Google redirect."""
    unique_id = str(uuid.uuid4()).replace("-", "")[:8]

    # Inject enhanced CSS for modern rounded UI
    st.markdown(
        f"""
        <style>
        .chat-toggle-{unique_id} {{
            position: fixed !important;
            bottom: 30px;
            right: 30px;
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            cursor: pointer;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            font-size: 28px;
            color: white;
            outline: none;
            overflow: hidden;
        }}
        
        .chat-toggle-{unique_id}::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
            border-radius: 50%;
        }}
        
        .chat-toggle-{unique_id}:hover {{
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
        }}
        
        .chat-toggle-{unique_id}:hover::before {{
            opacity: 1;
        }}
        
        .chat-toggle-{unique_id}:active {{
            transform: translateY(-1px) scale(1.02);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
        }}
        
        .chat-icon-{unique_id} {{
            position: relative;
            z-index: 2;
            animation: float-{unique_id} 3s ease-in-out infinite;
        }}
        
        @keyframes float-{unique_id} {{
            0%, 100% {{
                transform: translateY(0px);
            }}
            50% {{
                transform: translateY(-3px);
            }}
        }}
        
        /* Pulse animation for attention */
        .chat-toggle-{unique_id}::after {{
            content: '';
            position: absolute;
            top: -5px;
            left: -5px;
            right: -5px;
            bottom: -5px;
            border: 2px solid rgba(102, 126, 234, 0.3);
            border-radius: 50%;
            animation: pulse-{unique_id} 2s infinite;
        }}
        
        @keyframes pulse-{unique_id} {{
            0% {{
                transform: scale(1);
                opacity: 1;
            }}
            100% {{
                transform: scale(1.2);
                opacity: 0;
            }}
        }}
        
        /* Tooltip */
        .chat-toggle-{unique_id}:hover .tooltip-{unique_id} {{
            opacity: 1;
            visibility: visible;
            transform: translateX(-50%) translateY(-10px);
        }}
        
        .tooltip-{unique_id} {{
            position: absolute;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%) translateY(0px);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 12px;
            white-space: nowrap;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
            z-index: 1001;
        }}
        
        .tooltip-{unique_id}::after {{
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 5px solid transparent;
            border-top-color: rgba(0, 0, 0, 0.8);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Inject enhanced HTML with tooltip
    st.markdown(
        f"""
        <button class="chat-toggle-{unique_id}" id="chatToggle-{unique_id}">
            <span class="chat-icon-{unique_id}">🤖</span>
            <div class="tooltip-{unique_id}">Click to search Google</div>
        </button>
        """,
        unsafe_allow_html=True,
    )

    # Enhanced JS with Google redirect - multiple fallback methods
    st.markdown(
        f"""
        <script>
        document.getElementById('chatToggle-{unique_id}').addEventListener('click', function(e) {{
            console.log('Chat toggle clicked - redirecting to Google');
            
            // Method 1: Try window.open with immediate execution
            try {{
                var newWindow = window.open('https://www.google.com', '_blank');
                if (newWindow) {{
                    newWindow.focus();
                    return;
                }}
            }} catch (error) {{
                console.log('Method 1 failed:', error);
            }}
            
            // Method 2: Try with setTimeout to avoid popup blockers
            try {{
                setTimeout(function() {{
                    window.open('https://www.google.com', '_blank');
                }}, 100);
                return;
            }} catch (error) {{
                console.log('Method 2 failed:', error);
            }}
            
            // Method 3: Direct navigation as fallback
            try {{
                window.location.href = 'https://www.google.com';
            }} catch (error) {{
                console.log('Method 3 failed:', error);
            }}
            
            // Method 4: Create a temporary link and click it
            try {{
                var link = document.createElement('a');
                link.href = 'https://www.google.com';
                link.target = '_blank';
                link.rel = 'noopener noreferrer';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }} catch (error) {{
                console.log('All methods failed:', error);
            }}
        }});
        </script>
        """,
        unsafe_allow_html=True,
    )
