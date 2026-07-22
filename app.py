import os
import glob
import streamlit as st
from google import genai

# Configuración de página ancha
st.set_page_config(
    page_title="🌸 El Asistente de Javiera", 
    page_icon="🌸",
    layout="wide"
)

# Buscar imágenes subidas al repositorio
imagenes = sorted(
    glob.glob("WhatsApp*") + glob.glob("*.jpeg") + glob.glob("*.jpg") + glob.glob("*.png")
)

# Asignar la primera foto a la izquierda y la segunda a la derecha (si existe)
foto_izquierda = imagenes[0] if len(imagenes) > 0 else None
foto_derecha = imagenes[1] if len(imagenes) > 1 else foto_izquierda

# Conectar con la API Key
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Falta configurar la GEMINI_API_KEY en Streamlit Secrets.")
    st.stop()

# Crear cliente oficial de Gemini
client = genai.Client(api_key=api_key)

INSTRUCCION_SISTEMA = (
    "Tu nombre es 'JaviBot', un asistente súper simpático, ocurrente y gracioso. "
    "Fuiste creado por Jordan exclusivamente para hacer reír a Javiera. "
    "Tu misión principal es hacer que Javiera se ría a carcajadas con chistes cortos, "
    "comentarios cómicos, buen humor y mucha buena onda. Sé siempre muy amigable y divertido."
)

# Diseño de 3 Columnas
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
            respuesta_texto = ""
            # Lista de modelos a intentar en orden por si alguno falla
            modelos_a_probar = ['gemini-1.5-flash-8b', 'gemini-2.0-flash', 'gemini-1.5-flash']
            
            for mod in modelos_a_probar:
                try:
                    response = client.models.generate_content(
                        model=mod,
                        contents=prompt,
                        config=dict(system_instruction=INSTRUCCION_SISTEMA)
                    )
                    respuesta_texto = response.text
                    if respuesta_texto:
                        break # Si respondió bien, salimos del bucle
                except Exception:
                    continue # Si falla, intenta el siguiente modelo automáticamente

            if not respuesta_texto:
                respuesta_texto = "Ups, no se pudo conectar con la API de Google. Revisa tu API Key."

            st.markdown(respuesta_texto)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
