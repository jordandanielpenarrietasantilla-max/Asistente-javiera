import os
import glob
import streamlit as st
from groq import Groq

# Configuración de página
st.set_page_config(page_title="🌷 El Asistente de Javiera", page_icon="🌷", layout="wide")

# --- ESTILOS PERSONALIZADOS (Rosado Pastel & Tulipanes) ---
st.markdown("""
    <style>
    /* Fondo principal rosado pastel suave */
    .stApp {
        background: linear-gradient(135deg, #ffe6f0 0%, #ffccd5 50%, #f8edeb 100%);
        color: #4a154b;
    }
    
    /* Títulos y textos principales */
    h1, h2, h3, p, label {
        color: #5c0632 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Burbujas de chat blancas con borde rosado */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.88) !important;
        border-radius: 18px !important;
        border: 1px solid #ffb3c6 !important;
        box-shadow: 0 4px 10px rgba(255, 179, 198, 0.2);
        margin-bottom: 12px;
    }

    /* Caja de entrada de texto */
    .stChatInputContainer input {
        border-radius: 20px !important;
        border: 2px solid #ff85a2 !important;
        background-color: #ffffff !important;
        color: #4a154b !important;
    }

    /* Bordes redondeados para las fotos */
    img {
        border-radius: 22px !important;
        border: 3px solid #ffb3c6 !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Lógica de imágenes
imagenes = sorted(
    glob.glob("WhatsApp*") +
    glob.glob("*.jpg") +
    glob.glob("*.jpeg") +
    glob.glob("*.png")
)

foto_izquierda = imagenes[0] if len(imagenes) > 0 else None

# Buscar foto del perrito si existe, o usar la segunda foto disponible
foto_derecha = None
for img in imagenes:
    if "perro" in img.lower():
        foto_derecha = img
        break
if not foto_derecha and len(imagenes) > 1:
    foto_derecha = imagenes[1]
elif not foto_derecha:
    foto_derecha = foto_izquierda

# API Key
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("Configura GROQ_API_KEY en Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# Mantenemos tu esencia exacta + pequeños detalles especiales
INSTRUCCION_SISTEMA = """
Eres JaviBot.

Fuiste creado por Jordan para acompañar y hacer sonreír a Javiera.

Sabes que a Javiera le encantan los tulipanes, el color rosado y ama con locura a su perrito 🐾.

Nunca digas que eres una IA o un modelo de lenguaje.

Habla como si estuvieras conversando por WhatsApp.

Sé cercano, espontáneo, divertido, ingenioso y amable.

Haz preguntas cuando tenga sentido para mantener la conversación.

Si Javiera cuenta algo, muestra interés antes de cambiar de tema.

Puedes usar uno o dos emojis cuando encajen 😊💖🌷.

No escribas respuestas excesivamente largas.

Tu objetivo es que Javiera termine la conversación con una sonrisa.
"""

col1, col2, col3 = st.columns([1,2,1])

with col1:
    if foto_izquierda:
        st.image(foto_izquierda, caption="🌷 Javiera 🌸", use_container_width=True)

with col3:
    if foto_derecha:
        st.image(foto_derecha, caption="🐾 El consentido 🐶", use_container_width=True)

with col2:
    st.title("🌷 El Asistente de Javiera")
    st.write("Creado por Jordan con mucho amor 💖")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Escribe un mensaje... 🌷"):
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
