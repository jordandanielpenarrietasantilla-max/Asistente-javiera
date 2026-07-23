import streamlit as st
import google.generativeai as genai

# API KEY
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Modelo que funciona con esta versión
model = genai.GenerativeModel("gemini-pro")

st.title("🌸 El Asistente de Javiera 💖")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Escríbele algo...")

if user_input:
    st.session_state.chat.append(("Tú", user_input))

    try:
        response = model.generate_content(user_input)
        reply = response.text
    except Exception as e:
        reply = f"Error: {e}"

    st.session_state.chat.append(("Javiera 💕", reply))

for role, msg in st.session_state.chat:
    st.write(f"**{role}:** {msg}")
