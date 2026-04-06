import streamlit as st
import time
from ollama import callOLLAMA

# --- Page Config ---
st.set_page_config(page_title="AI Chat Pro", layout="wide")

# --- Zero-White-Space CSS ---
st.markdown("""
<style>
    /* 1. Global Blackout (Force every possible layer to black) */
    .stApp, header, [data-testid="stHeader"], [data-testid="stFooter"] {
        background-color: #000000 !important;
    }

    /* 2. Hide Streamlit's Default Input Container (The white strip source) */
    .stChatInputContainer, [data-testid="stChatInput"] {
        display: none !important;
    }

    /* 3. Custom Bottom Input Bar (Floating) */
    .fixed-input-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #000000 !important;
        padding: 20px 60px;
        z-index: 1000;
        border-top: 1px solid #222;
    }

    /* 4. High-Visibility Input Box (Letters fixed to White) */
    input[type="text"] {
        background-color: #000000 !important;
        color: #ffffff !important; /* Pure White text while typing */
        border: 2px solid #ff4b4b !important; /* Neon Red Border */
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 16px !important;
    }

    /* Visible Light Grey Placeholder */
    input[type="text"]::placeholder {
        color: #888888 !important;
    }

    /* 5. Chat Bubbles & Sidebar */
    [data-testid="stChatMessage"] { background-color: #111111 !important; color: white !important; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #222; }
    
    /* 6. Settings & Status (Red Highlights) */
    div.stButton > button {
        background-color: #ff4b4b !important;
        color: white !important;
        border-radius: 8px !important;
    }
    .status-tag {
        border: 1px solid #ff4b4b;
        padding: 8px;
        border-radius: 8px;
        color: white;
        text-align: center;
        background-color: #1a0000;
    }

    /* General Text */
    h1, p, span, .stMarkdown { color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- Session State Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Logic to clear input after Enter
def process_message():
    prompt = st.session_state.user_box
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        # AI Response
        response = callOLLAMA(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.user_box = "" # Reset box

# --- Sidebar ---
with st.sidebar:
    st.markdown("## Settings")
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown('<div class="status-tag">Phi-3: Online</div>', unsafe_allow_html=True)

# --- Main Page ---
st.title("AI Chat Assistant")

# Messages Display (Added bottom padding to avoid footer overlap)
msg_container = st.container()
with msg_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    st.markdown("<div style='height: 150px;'></div>", unsafe_allow_html=True)

# --- The "Fixed" Black Keyboard Section ---
st.markdown('<div class="fixed-input-bar">', unsafe_allow_html=True)
st.text_input(
    label="chat_input", 
    label_visibility="collapsed", 
    placeholder="Type here and press Enter...", 
    key="user_box",
    on_change=process_message
)
st.markdown('</div>', unsafe_allow_html=True)