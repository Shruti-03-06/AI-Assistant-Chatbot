import streamlit as st
from datetime import datetime
from ollama import callOLLAMA  # local helper
from prompt import prompt       # your system prompt

# Page configuration
st.set_page_config(
    page_title='AI Chat Assistant',
    layout='centered'
)

# Custom CSS styling
st.markdown(
    """
    <style>
    body {
        background-image: url("https://img.freepik.com/premium-photo/abstract-connected-background-technology-network-concept_34629-495.jpg");
        background-size: cover;
        background-attachment: fixed;
    }

    .stApp {
        background-color: rgba(0, 0, 0, 0.7);
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }

    .stTextInput > div > div > input {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #444;
        padding: 10px;
        border-radius: 5px;
    }

    .stButton button {
        background-color: #1a73e8;
        color: white;
    }

    .stTextInput input::placeholder {
        color: #cccccc;
        font-style: italic;
    }

    .stMarkdown, .stSubheader, .stTitle {
        color: white;
        text-shadow: 0 0 3px #000000;
    }

    .stInfo, .stSuccess, .stWarning {
        border-radius: 10px;
        padding: 10px;
    }

    .stSuccess {
        background-color: rgba(0, 128, 0, 0.4);
    }

    .stInfo {
        background-color: rgba(30, 144, 255, 0.4);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, I am your smart assistant. How can I help you today?"}
    ]
if "is_typing" not in st.session_state:
    st.session_state.is_typing = False
if "full_user_message" not in st.session_state:
    st.session_state.full_user_message = ""

# Header
st.title("AI Chat Assistant")
st.markdown("Welcome to your personalized offline GPT chatbot.")
st.subheader("💬 Start Chatting")

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.info(f"🧑‍💻 {message['content']}")
    else:
        st.success(f"🤖 {message['content']}")

# Show typing spinner
if st.session_state.is_typing:
    with st.spinner("🤖 Bot is typing..."):
        pass

# Chat form
st.markdown("---")
st.subheader("Your Message")

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message", placeholder="Ask me anything...")
    send_button = st.form_submit_button("Send Message")

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.session_state.full_user_message = ""
    st.rerun()

# Handle user input
if send_button and user_input.strip():
    user_input = user_input.strip()
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.full_user_message = f"{prompt}<|>{user_input}"
    st.session_state.is_typing = True
    st.rerun()

# Generate response
if st.session_state.is_typing:
    user_message = st.session_state.full_user_message
    bot_response = callOLLAMA(user_message)  # Implemented in ollama.py
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.session_state.is_typing = False
    st.rerun()
