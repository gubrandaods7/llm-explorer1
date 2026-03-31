"""
app.py - Interface visual de chat com o Gemini usando Streamlit.
"""

import os

from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted
import google.generativeai as genai
import streamlit as st

load_dotenv(override=True)

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("API key não encontrada. Preencha o arquivo .env com sua GEMINI_API_KEY.")
    st.stop()

genai.configure(api_key=api_key)

st.set_page_config(page_title="LLM Explorer", page_icon="🤖")
st.title("🤖 LLM Explorer")
st.caption("Chat com Google Gemini")

MODELS = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash-lite", "gemini-2.5-pro"]
selected_model = st.sidebar.selectbox("Modelo", MODELS)

if "current_model" not in st.session_state or st.session_state.current_model != selected_model:
    model = genai.GenerativeModel(selected_model)
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []
    st.session_state.current_model = selected_model

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Pensando..."):
                response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except ResourceExhausted as e:
            st.error(f"Cota excedida! Tente trocar o modelo na barra lateral ou aguarde alguns minutos.\n\nDetalhe: {e}")
        except Exception as e:
            st.error(f"Erro: {e}")
