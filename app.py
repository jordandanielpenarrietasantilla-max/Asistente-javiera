import streamlit as st
import google.generativeai as genai

# Configurar API KEY
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ MODELO NUEVO (IMPORTANTE)
model = genai.GenerativeModel("gemini-1.5-flash")

# Configuración
st.set_page_config(page_title="🌸 Javiera 💖")

st.title("🌸 El Asistente de Javiera 💖")

# Historial
if "chat" not in st.session_state:
    st.session_state.chat = []

# Input
user_input = st.text_input("Escríbele algo...")

if user_input:
    st.session_state.chat.append(("Tú", user_input))

    try:
        prompt = f"""
        Eres Javiera 💖, una novia:
        - Cariñosa
        - Coqueta 😏
        - Dulce
        - Divertida

        Responde como una pareja real.

        Mensaje:
        {user_input}
        """

        response = model.generate_content(prompt)
        reply = response.text

    except Exception as e:
        reply = f"Error: {e}"

    st.session_state.chat.append(("Javiera 💕", reply))

# Mostrar chat
for role, msg in st.session_state.chat:
    st.write(f"**{role}:** {msg}")
