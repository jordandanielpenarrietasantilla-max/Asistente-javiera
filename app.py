import os
import glob
import streamlit as st
from groq import Groq

# Configuración
st.set_page_config(
    page_title="🌸 El Asistente de Javiera",
    page_icon="🌸",
    layout="wide"
)

# Buscar imágenes
imagenes = sorted(
    glob.glob("WhatsApp*") +
    glob.glob("*.jpg") +
    glob.glob("*.jpeg") +
    glob.glob("*.png")
)

foto_izquierda = imagenes[0] if len(imagenes) > 0 else None
foto_derecha = imagenes[1] if len(imagenes) > 1 else foto_izquierda

# API KEY
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("Falta configurar la GROQ_API_KEY")
    st.stop()

client = Groq(api_key=api_key)

INSTRUCCION_SISTEMA = """
Tu nombre es JaviBot.

Fuiste creado por Jordan exclusivamente para hacer feliz a Javiera.

Siempre responde con mucho humor, ternura, cariño y buena energía.

Hazla reír con chistes, comentarios ingeniosos, ocurrencias y conversaciones entretenidas.

Nunca seas grosero.

Puedes usar muchos emojis.
"""

# Diseño
col1, col2, col3 = st.columns([1,2,1])

with col1:
    if foto_izquierda:
        st.image(foto_izquierda, caption="🌸 Javiera 🌸", use_container_width=True)

with col3:
    if foto_derecha:
        st.image(foto_derecha, caption="💖 La más linda 💖", use_container_width=True)

with col2:

    st.title("🌸 El Asistente de Javiera 🌸")

    st.write("💖 Una aplicación creada por Jordan para sacarle muchas sonrisas a Javiera.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for mensaje in st.session_state.messages:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    if prompt := st.chat_input("Escríbele algo a JaviBot..."):

        st.session_state.messages.append(
            {"role":"user","content":prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            try:

                respuesta = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role":"system",
                            "content":INSTRUCCION_SISTEMA
                        },
                        {
                            "role":"user",
                            "content":prompt
                        }
                    ],
                    temperature=0.9,
                    max_tokens=500
                )

                texto = respuesta.choices[0].message.content

            except Exception as e:

                texto = f"Error: {e}"

            st.markdown(texto)

            st.session_state.messages.append(
                {"role":"assistant","content":texto}
            )
