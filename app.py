import os
import streamlit as st
import google.generativeai as genai

# Configuración visual de la página
st.set_page_config(page_title="🌸 El Asistente de Javiera", page_icon="🌸")

st.title("🌸 El Asistente de Javiera 🌸")
st.write("💖 Una aplicación creada por **Jordan** para sacarle risas a Javiera.")

# Conectar con la API Key guardada en Secrets o Variables de entorno
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Falta configurar la GEMINI_API_KEY en Streamlit Secrets.")
    st.stop()

# Configurar cliente de Google Gemini
genai.configure(api_key=api_key)

INSTRUCCION_SISTEMA = (
    "Tu nombre es 'JaviBot', un asistente súper simpático, ocurrente y gracioso. "
    "Fuiste creado por Jordan exclusivamente para hacer reír a Javiera. "
    "Tu misión principal es hacer que Javiera se ría a carcajadas con chistes cortos, "
    "comentarios cómicos, buen humor y mucha buena onda. Sé siempre muy amigable y divertido."
)

# Inicializar modelo de Gemini
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=INSTRUCCION_SISTEMA
)

# Historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt := st.chat_input("Escríbeme algo para reírnos un rato..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            respuesta_texto = response.text
        except Exception as e:
            respuesta_texto = f"Ups, ocurrió un error: {e}"

        st.markdown(respuesta_texto)
        st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
