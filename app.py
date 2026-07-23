import streamlit as st
import google.generativeai as genai

# Configurar API KEY desde secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Usar modelo actualizado
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Configuración de la página
st.set_page_config(
    page_title="🌸 El Asistente de Javiera",
    layout="wide"
)

# Título bonito
st.markdown("<h1 style='text-align: center;'>🌸 El Asistente de Javiera 💖</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Un bot hecho con amor 💕</p>", unsafe_allow_html=True)

# Estado del chat
if "chat" not in st.session_state:
    st.session_state.chat = []

# Input del usuario
user_input = st.text_input("Escríbele algo...")

# Cuando el usuario escribe
if user_input:
    st.session_state.chat.append(("Tú", user_input))

    try:
        prompt = f"""
        Eres Javiera 💖, una novia:
        - Muy cariñosa
        - Coqueta 😏
        - Dulce
        - Divertida

        Responde de forma natural, como una pareja real.

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
    st.markdown(f"**{role}:** {msg}")
