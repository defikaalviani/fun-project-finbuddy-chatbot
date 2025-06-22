import streamlit as st
import requests

#======================CONFIG API KEY ==========================#
OPENROUTER_API_KEY = "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"
MODEL = "gpt-3.5-turbo"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "http://localhost:8501",
    "Content-Type": "application/json",
    "X-title":"AI Chatbot Streamlit"
}

API_URL = f"https://openrouter.ai/api/v1/chat/completion"

#================================================================#

st.title("AI chatbot with Openrouter and Buble Style")
st.markdown(f"Powered by '[Mistral AI] (https://mistral.ai/)' and 'OpenRouter'")

#Chat History
if "Chat_history" not in st.session_state:
    st.session_state.chat_history=[]

#Input dari user
user_input = st.chat_input("Type your message here...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role":"user", "content": user_input})

    #Kirim ke API OpenRouter
    with st.spinner("Thinking..."):
        playload = {
            "model": MODEL,
            "messages": [
                {"role": "user", "content": "Your are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        }
        response = requests.post(API_URL, headers=HEADERS, json=playload)
        if response.status_code==200:
            bot_reply = response.json()["choices"][0]["message"]["content"]
        else:
            bot_reply="Maaf gagal mendapatkan respon dari AI"

    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})