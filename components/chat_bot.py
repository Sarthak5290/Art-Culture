import streamlit as st
import uuid


def render_chat_bot():
    """Render the chat bot widget with Streamlit-compatible styling and custom icon."""

    # Generate unique IDs to avoid conflicts
    unique_id = str(uuid.uuid4()).replace("-", "")[:8]

    # Inject CSS styles
    st.markdown(
        f"""
        <style>
        /* Chat Widget Styles */
        .chat-widget-{unique_id} {{
            position: fixed !important;
            bottom: 20px !important;
            right: 20px !important;
            z-index: 999999 !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}

        /* Chat Toggle Button */
        .chat-toggle-{unique_id} {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: #2563eb;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .chat-toggle-{unique_id}:hover {{
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6);
        }}

        .chat-toggle-{unique_id} img {{
            width: 32px;
            height: 32px;
        }}

        /* Close Icon */
        .close-icon-{unique_id} {{
            position: absolute;
            font-size: 24px;
            color: white;
            opacity: 0;
            transition: opacity 0.3s ease;
            font-weight: bold;
        }}

        .chat-toggle-{unique_id}.active .chatbot-icon-{unique_id} {{
            opacity: 0;
        }}

        .chat-toggle-{unique_id}.active .close-icon-{unique_id} {{
            opacity: 1;
        }}

        /* Chat Window */
        .chat-window-{unique_id} {{
            position: absolute;
            bottom: 80px;
            right: 0;
            width: 350px;
            height: 500px;
            background: #1f2937;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            transform: translateY(20px) scale(0.95);
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            overflow: hidden;
        }}

        .chat-window-{unique_id}.active {{
            transform: translateY(0) scale(1);
            opacity: 1;
            visibility: visible;
        }}

        /* Chat Header */
        .chat-header-{unique_id} {{
            background: #1f2937;
            padding: 16px 20px;
            border-bottom: 1px solid #374151;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .chat-header-content-{unique_id} {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .chat-avatar-{unique_id} {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: #2563eb;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }}

        .chat-info-{unique_id} h3 {{
            color: white;
            font-size: 16px;
            font-weight: 600;
            margin: 0;
        }}

        .chat-info-{unique_id} p {{
            color: #9ca3af;
            font-size: 12px;
            margin: 0;
        }}

        .close-btn-{unique_id} {{
            background: none;
            border: none;
            color: #9ca3af;
            font-size: 20px;
            cursor: pointer;
            padding: 4px;
            border-radius: 4px;
            transition: color 0.2s ease;
            font-weight: bold;
        }}

        .close-btn-{unique_id}:hover {{
            color: white;
        }}

        /* Chat Messages */
        .chat-messages-{unique_id} {{
            height: 350px;
            overflow-y: auto;
            padding: 20px;
            background: #111827;
        }}

        .welcome-message-{unique_id} {{
            background: #374151;
            border-radius: 16px 16px 16px 4px;
            padding: 16px;
            margin-bottom: 16px;
            position: relative;
        }}

        .welcome-message-{unique_id}::before {{
            content: '';
            position: absolute;
            left: -8px;
            top: 12px;
            width: 0;
            height: 0;
            border-top: 8px solid transparent;
            border-bottom: 8px solid transparent;
            border-right: 8px solid #374151;
        }}

        .message-icon-{unique_id} {{
            font-size: 16px;
            margin-bottom: 8px;
            display: block;
        }}

        .message-text-{unique_id} {{
            color: #e5e7eb;
            font-size: 14px;
            line-height: 1.5;
            margin: 0;
        }}

        /* Chat Input */
        .chat-input-container-{unique_id} {{
            padding: 16px 20px;
            background: #1f2937;
            border-top: 1px solid #374151;
        }}

        .chat-input-wrapper-{unique_id} {{
            display: flex;
            gap: 8px;
            align-items: flex-end;
        }}

        .chat-input-{unique_id} {{
            flex: 1;
            background: #374151;
            border: 1px solid #4b5563;
            border-radius: 20px;
            padding: 12px 16px;
            color: white;
            font-size: 14px;
            resize: none;
            outline: none;
            transition: border-color 0.2s ease;
            min-height: 44px;
            max-height: 100px;
            font-family: inherit;
        }}

        .chat-input-{unique_id}:focus {{
            border-color: #2563eb;
        }}

        .chat-input-{unique_id}::placeholder {{
            color: #9ca3af;
        }}

        .send-btn-{unique_id} {{
            width: 44px;
            height: 44px;
            background: #2563eb;
            border: none;
            border-radius: 50%;
            color: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background-color 0.2s ease;
            flex-shrink: 0;
        }}

        .send-btn-{unique_id}:hover {{
            background: #1d4ed8;
        }}

        .send-btn-{unique_id}:disabled {{
            background: #4b5563;
            cursor: not-allowed;
        }}

        /* Scrollbar Styling */
        .chat-messages-{unique_id}::-webkit-scrollbar {{
            width: 4px;
        }}

        .chat-messages-{unique_id}::-webkit-scrollbar-track {{
            background: #1f2937;
        }}

        .chat-messages-{unique_id}::-webkit-scrollbar-thumb {{
            background: #4b5563;
            border-radius: 2px;
        }}

        .chat-messages-{unique_id}::-webkit-scrollbar-thumb:hover {{
            background: #6b7280;
        }}

        /* Responsive Design */
        @media (max-width: 480px) {{
            .chat-window-{unique_id} {{
                width: calc(100vw - 40px);
                right: 20px;
                left: 20px;
                height: 80vh;
                bottom: 80px;
            }}
            
            .chat-messages-{unique_id} {{
                height: calc(80vh - 140px);
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Inject HTML without inline event handlers
    st.markdown(
        f"""
        <div class="chat-widget-{unique_id}">
            <button class="chat-toggle-{unique_id}" id="chatToggle-{unique_id}">
                <div class="chatbot-icon-{unique_id}">
                    <!-- Using a fallback emoji if GIF doesn't load -->
                    <span style="font-size: 32px;">🤖</span>
                </div>
                <div class="close-icon-{unique_id}">×</div>
            </button>
            <div class="chat-window-{unique_id}" id="chatWindow-{unique_id}">
                <div class="chat-header-{unique_id}">
                    <div class="chat-header-content-{unique_id}">
                        <div class="chat-avatar-{unique_id}">💬</div>
                        <div class="chat-info-{unique_id}">
                            <h3>Chat Assistant</h3>
                            <p>Always here to help</p>
                        </div>
                    </div>
                    <button class="close-btn-{unique_id}" id="closeBtn-{unique_id}">×</button>
                </div>
                <div class="chat-messages-{unique_id}" id="chatMessages-{unique_id}">
                    <div class="welcome-message-{unique_id}">
                        <span class="message-icon-{unique_id}">👋</span>
                        <p class="message-text-{unique_id}">Hi! I'm your AI assistant. Ask me anything about Sarthak's skills, experience, or projects!</p>
                    </div>
                </div>
                <div class="chat-input-container-{unique_id}">
                    <div class="chat-input-wrapper-{unique_id}">
                        <textarea class="chat-input-{unique_id}" id="chatInput-{unique_id}" placeholder="Ask about skills, projects, or experience..." rows="1"></textarea>
                        <button class="send-btn-{unique_id}" id="sendBtn-{unique_id}">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="m22 2-7 20-4-9-9-4z"/>
                                <path d="M22 2 11 13"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Inject JavaScript with event listeners only
    st.markdown(
        f"""
        <script>
            (function() {{
                // Define functions in closure to avoid global pollution
                let chatInitialized_{unique_id} = false;
                
                function toggleChat_{unique_id}() {{
                    const chatToggle = document.getElementById('chatToggle-{unique_id}');
                    const chatWindow = document.getElementById('chatWindow-{unique_id}');
                    
                    if (!chatToggle || !chatWindow) {{
                        console.error('Chat elements not found for {unique_id}');
                        return;
                    }}
                    
                    const isActive = chatWindow.classList.contains('active');
                    
                    if (isActive) {{
                        chatWindow.classList.remove('active');
                        chatToggle.classList.remove('active');
                        console.log('Chat closed');
                    }} else {{
                        chatWindow.classList.add('active');
                        chatToggle.classList.add('active');
                        console.log('Chat opened');
                        setTimeout(() => {{
                            const chatInput = document.getElementById('chatInput-{unique_id}');
                            if (chatInput) chatInput.focus();
                        }}, 300);
                    }}
                }}

                function sendMessage_{unique_id}() {{
                    const chatInput = document.getElementById('chatInput-{unique_id}');
                    if (!chatInput) return;
                    
                    const message = chatInput.value.trim();
                    
                    if (message) {{
                        console.log('Message to send:', message);
                        chatInput.value = '';
                        chatInput.style.height = 'auto';
                    }}
                }}

                function handleKeyPress_{unique_id}(event) {{
                    if (event.key === 'Enter' && !event.shiftKey) {{
                        event.preventDefault();
                        sendMessage_{unique_id}();
                    }}
                }}

                function autoResize_{unique_id}(element) {{
                    element.style.height = 'auto';
                    element.style.height = Math.min(element.scrollHeight, 100) + 'px';
                }}

                function initializeChatbot_{unique_id}() {{
                    if (chatInitialized_{unique_id}) return;
                    
                    console.log('Initializing chatbot {unique_id}');
                    
                    const chatToggle = document.getElementById('chatToggle-{unique_id}');
                    const closeBtn = document.getElementById('closeBtn-{unique_id}');
                    const chatInput = document.getElementById('chatInput-{unique_id}');
                    const sendBtn = document.getElementById('sendBtn-{unique_id}');
                    
                    if (!chatToggle || !closeBtn || !chatInput || !sendBtn) {{
                        console.log('Some chat elements not found yet, retrying...');
                        return false;
                    }}
                    
                    // Add event listeners
                    chatToggle.addEventListener('click', toggleChat_{unique_id});
                    closeBtn.addEventListener('click', toggleChat_{unique_id});
                    sendBtn.addEventListener('click', sendMessage_{unique_id});
                    
                    chatInput.addEventListener('keydown', handleKeyPress_{unique_id});
                    chatInput.addEventListener('input', function() {{
                        autoResize_{unique_id}(this);
                    }});
                    
                    // Close chat when clicking outside
                    document.addEventListener('click', function(event) {{
                        const chatWidget = document.querySelector('.chat-widget-{unique_id}');
                        const chatWindow = document.getElementById('chatWindow-{unique_id}');
                        
                        if (chatWidget && !chatWidget.contains(event.target)) {{
                            if (chatWindow && chatWindow.classList.contains('active')) {{
                                const chatToggle = document.getElementById('chatToggle-{unique_id}');
                                chatWindow.classList.remove('active');
                                if (chatToggle) chatToggle.classList.remove('active');
                            }}
                        }}
                    }});
                    
                    chatInitialized_{unique_id} = true;
                    console.log('Chatbot {unique_id} initialized successfully');
                    return true;
                }}
                
                // Try initialization multiple times
                function attemptInit() {{
                    if (!chatInitialized_{unique_id}) {{
                        initializeChatbot_{unique_id}();
                    }}
                }}
                
                // Multiple initialization attempts
                if (document.readyState === 'loading') {{
                    document.addEventListener('DOMContentLoaded', attemptInit);
                }} else {{
                    attemptInit();
                }}
                
                // Delayed attempts for Streamlit
                setTimeout(attemptInit, 100);
                setTimeout(attemptInit, 500);
                setTimeout(attemptInit, 1000);
                setTimeout(attemptInit, 2000);
                
                // MutationObserver for when Streamlit re-renders
                const observer = new MutationObserver(function(mutations) {{
                    let shouldReinit = false;
                    mutations.forEach(function(mutation) {{
                        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {{
                            for (let node of mutation.addedNodes) {{
                                if (node.nodeType === 1 && (
                                    node.querySelector && node.querySelector('.chat-widget-{unique_id}') ||
                                    node.classList && node.classList.contains('chat-widget-{unique_id}')
                                )) {{
                                    shouldReinit = true;
                                    break;
                                }}
                            }}
                        }}
                    }});
                    
                    if (shouldReinit) {{
                        chatInitialized_{unique_id} = false;
                        setTimeout(attemptInit, 100);
                    }}
                }});
                
                observer.observe(document.body, {{
                    childList: true,
                    subtree: true
                }});
            }})();
        </script>
        """,
        unsafe_allow_html=True,
    )
