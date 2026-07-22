import os
import glob
import streamlit as st
from google import genai

# Configuración de página ancha (Layout Wide)
st.set_page_config(
    page_title="🌸 El Asistente de Javiera", 
    page_icon="🌸",
    layout="wide"
)

# Buscar imágenes subidas en el directorio
imagenes = sorted(glob.glob("WhatsApp*") + glob.glob("Imagen*") + glob.glob("*.jpg") + glob.glob("*.png") + glob.glob("*.jpeg"))
# Filtrar para evitar buscar otros archivos si existieran
imagenes_javiera = [img for img in imagenes if not img.startswith("app") and not img.startswith("aplicacion")]

foto_izquierda = imagenes_javiera[0] if len(imagenes_javiera) > 0 else None
foto_derecha = imagenes_javiera[1] if len(imagenes_javiera) > 1 else foto_izquierda

# Conectar con la API Key
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Falta configurar la GEMINI_API_KEY en Streamlit Secrets.")
    st.stop()

# Crear cliente de Gemini
client = genai.Client(api_key=api_key)

INSTRUCCION_SISTEMA = (
    "Tu nombre es 'JaviBot', un asistente súper simpático, ocurrente y gracioso. "
    "Fuiste creado por Jordan exclusivamente para hacer reír a Javiera. "
    "Tu misión principal es hacer que Javiera se ría a carcajadas con chistes cortos, "
    "comentarios cómicos, buen humor y mucha buena onda. Sé siempre muy amigable y divertido."
)

# Crear 3 Columnas: [Foto Izq (1), Chat Centro (2), Foto Der (1)]
col_izq, col_centro, col_der = st.columns([1, 2, 1])

# --- EXTREMO IZQUIERDO ---
with col_izq:
    if foto_izquierda:
        st.image(foto_izquierda, caption="🌸 Javiera 🌸", use_container_width=True)

# --- EXTREMO DERECHO ---
with col_der:
    if foto_derecha:
        st.image(foto_derecha, caption="💖 La más linda 💖", use_container_width=True)

# --- CENTRO: CHAT ---
with col_centro:
    st.title("🌸 El Asistente de Javiera 🌸")
    st.write("💖 Una aplicación creada por **Jordan** para sacarle risas a Javiera.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Escríbeme algo para reírnos un rato..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt,
                    config=dict(
                        system_instruction=INSTRUCCION_SISTEMA
                    )
                )
                respuesta_texto = response.text
            except Exception as e:
                respuesta_texto = f"Ups, ocurrió un error: {e}"

            st.markdown(respuesta_texto)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
