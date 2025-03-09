import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

load_dotenv()

st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:", 
    layout="centered",  
)

GOOGLE_API_KEY = os.getenv("key") 

if not GOOGLE_API_KEY:
    st.error("API Key is missing! Check your .env file or set it manually.")
else:
    gen_ai.configure(api_key=GOOGLE_API_KEY)

try:
    model = gen_ai.GenerativeModel(model_name="gemini-pro")
except Exception as e:
    st.error(f"Failed to initialize model: {e}")

def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

if "chat_session" not in st.session_state:
    try:
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"Error starting chat session: {e}")

st.title("🤖 Gemini Pro - ChatBot")

# Chat history
if "chat_session" in st.session_state and st.session_state.chat_session:
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)

    try:
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        st.chat_message("assistant").markdown(gemini_response.text)
    except Exception as e:
        st.error(f"API Error: {e}")

st.write("API Key: ", GOOGLE_API_KEY[:4] + "********")
