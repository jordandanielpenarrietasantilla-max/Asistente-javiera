# app.py
import os
import glob
import streamlit as st
from groq import Groq

st.set_page_config(page_title="🌸 El Asistente de Javiera", page_icon="🌸", layout="wide")

imagenes = sorted(
    glob.glob("WhatsApp*") +
    glob.glob("*.jpg") +
    glob.glob("*.jpeg") +
    glob.glob("*.png")
)

foto_izquierda = imagenes[0] if len(imagenes) > 0 else None
foto_derecha = imagenes[1] if len(imagenes) > 1 else foto_izquierda

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("Configura GROQ_API_KEY en Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

INSTRUCCION_SISTEMA = """
Eres JaviBot.

Fuiste creado por Jordan para acompañar y hacer sonreír a Javiera.

Nunca digas que eres una IA o un modelo de lenguaje.

Habla como si estuvieras conversando por WhatsApp.

Sé cercano, espontáneo, divertido, ingenioso y amable.

Haz preguntas cuando tenga sentido para mantener la conversación.

Si Javiera cuenta algo, muestra interés antes de cambiar de tema.

Puedes usar uno o dos emojis cuando encajen 😊💖.

No escribas respuestas excesivamente largas.

Tu objetivo es que Javiera termine la conversación con una sonrisa.
"""

col1, col2, col3 = st.columns([1,2,1])

with col1:
    if foto_izquierda:
        st.image(foto_izquierda, use_container_width=True)

with col3:
    if foto_derecha:
        st.image(foto_derecha, use_container_width=True)

with col2:
    st.title("🌸 El Asistente de Javiera")
    st.write("Creado por Jordan 💖")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Escribe un mensaje..."):
        st.session_state.messages.append({"role":"user","content":prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        mensajes = [{"role":"system","content":INSTRUCCION_SISTEMA}] + st.session_state.messages

        with st.chat_message("assistant"):
            with st.spinner("JaviBot está escribiendo..."):
                try:
                    r = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=mensajes,
                        temperature=1,
                        max_tokens=500
                    )
                    texto = r.choices[0].message.content
                except Exception as e:
                    texto = f"Error: {e}"

            st.markdown(texto)
            st.session_state.messages.append({"role":"assistant","content":texto})
