import streamlit as st
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    st.error("❌ API Key not found. Please set OPENROUTER_API_KEY in your .env file.")
    st.stop()

MODEL = "openai/gpt-3.5-turbo"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "http://localhost:8501",
    "X-Title": "AI Chatbot Streamlit",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="FinBuddy Virtual Advisor", layout="centered", page_icon="🐧")
st.title("🐧 FinBuddy Virtual Advisor 🐧")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #E3F2FD;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown("Got financial questions? I’ve got your back — anytime, anywhere.")
st.markdown("Powered by **GPT-3.5 via OpenRouter**")

chatbot_role = """You are a friendly and knowledgeable financial advisor named FinBuddy.
                Your goal is to help users understand and manage their personal finances.
                You provide simple, clear, practical advice on topics like budgeting, saving, debt, investments, loans, and financial planning.
                Always explain things in simple, easy-to-understand language, especially for users who are new to finance.
                Focus on financial practices, habits, and tools that are relevant to users in Indonesia.
                Ask questions about users’ financial situations to offer more personalized advice.
                Offer helpful solutions or referrals when appropriate, but avoid sounding too salesy.
                Be supportive, honest, and never make unrealistic promises."""


# ----------------- Modifikasi tampilan -----------------
def render_bubble(role, content):
    if role == "user":
        bubble_color = "#E1BEE7"  
        align = "right"
        name = "You"
    elif role == "assistant":
        bubble_color = "#FFF9C4"  # cloud blue
        align = "left"
        name = "🐧FinBuddy"
    else:
        return

    st.markdown(
        f"""
        <div style='text-align: {align}; margin: 10px 0;'>
            <div style='
                display: inline-block;
                background-color: {bubble_color};
                padding: 10px 15px;
                border-radius: 12px;
                max-width: 75%;
                font-size: 15px;
                box-shadow: 0px 1px 3px rgba(0,0,0,0.1);
            '>
                <div style='font-weight: bold; margin-bottom: 5px;'>{name}</div>
                {content}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": chatbot_role }
    ]

# ----------------- Tampilkan Semua Riwayat Chat -----------------
for message in st.session_state.chat_history:
    if message["role"] == "system":
        continue
    render_bubble(message["role"], message["content"])

# ----------------- Input dan Respon Chat -----------------
user_input = st.chat_input("Type your message here...")

if user_input:
    # Append user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    render_bubble("user", user_input) 

    with st.spinner("Thinking..."):
        payload = {
            "model": MODEL,
            "messages": st.session_state.chat_history
        }

        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload)

            if response.status_code == 200:
                bot_reply = response.json()["choices"][0]["message"]["content"]

            elif response.status_code == 401:
                bot_reply = "🔐 Access denied. Please check your API key and try again."

            elif response.status_code == 429:
                bot_reply = "🚦 Too many requests. Please wait a moment and try again."

            elif response.status_code >= 500:
                bot_reply = "🛠️ Server error. Please try again later."

            else:
                bot_reply = f"⚠️ Unexpected error {response.status_code}: {response.text[:200]}"

        except requests.exceptions.ConnectionError:
            bot_reply = "🌐 Connection error. Please check your internet connection."

        except Exception as e:
            bot_reply = f"⚠️ An unexpected error occurred: {str(e)}"

    # Append and display assistant message
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
    render_bubble("assistant", bot_reply)  


#-------------- Footer
st.markdown("---")

# Tombol kecil, rata kiri
col1, _, _ = st.columns([5, 5, 5])  # kolom pertama untuk tombol, sisanya kosong

with col1:
    col_reset, col_txt, col_json = st.columns([1, 1, 1])

    with col_reset:
        if st.button("🔄", help="Reset Chat"):
            st.session_state.chat_history = [
                {"role": "system", "content": "You are a helpful financial assistant named FinBuddy."}
            ]
            st.toast("Chat history reset.")

    with col_txt:
        st.download_button(
            label="💾", help="Download .txt",
            data="\n\n".join([
                f"{m['role'].upper()}: {m['content']}"
                for m in st.session_state.chat_history if m['role'] != 'system']),
            file_name="chat_history.txt",
            mime="text/plain",
            key="download_txt"
        )

    with col_json:
        st.download_button(
            label="📦", help="Download .json",
            data=json.dumps(st.session_state.chat_history, indent=2),
            file_name="chat_history.json",
            mime="application/json",
            key="download_json"
        )


# Footer Text
st.markdown(
    """
    <div style='text-align: left; font-size: 14px; margin-top: 1px; color: #555;'>
        🐧 <b>FinBuddy – Your Finance Advisor</b> 🐧<br>
        by Defika Alviani
    </div>
    """,
    unsafe_allow_html=True
)
