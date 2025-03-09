import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai


# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:", 
    layout="centered",  
)

GOOGLE_API_KEY = os.getenv("AIzaSyBHSEqHYw2JjxlYp-BOqqCWaLcOD8Hdb3I")

gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel(model_name="gemini-pro")



def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

if "chat_session" not in st.session_state or not st.session_state.chat_session:
    st.session_state.chat_session = model.start_chat(history=[])



st.title("🤖 Gemini Pro - ChatBot")

#chat history
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


    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

st.write("API Key:", GOOGLE_API_KEY)
