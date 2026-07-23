import os
import glob
import urllib.parse
import streamlit as st
from groq import Groq

# Configuración de página
st.set_page_config(page_title="🌷 El Asistente de Javiera", page_icon="🌷", layout="wide")

# --- ESTILOS PERSONALIZADOS (Fondo Rosado, Tulipanes y Chat Visible) ---
st.markdown("""
    <style>
    /* Forzar fondo rosado pastel en todo Streamlit */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: linear-gradient(135deg, #ffe6f0 0%, #ffccd5 50%, #f8edeb 100%) !important;
    }

    /* ANIMACIÓN DE TULIPANES FLOTANTES DE FONDO */
    @keyframes tulipFall {
        0% {
            transform: translateY(-10vh) rotate(0deg);
            opacity: 0.9;
        }
        100% {
            transform: translateY(105vh) rotate(360deg);
            opacity: 0.2;
        }
    }

    .tulip-bg {
        position: fixed;
        top: -10vh;
        font-size: 26px;
        user-select: none;
        pointer-events: none;
        z-index: 999;
        animation: tulipFall linear infinite;
    }

    .t1  { left: 5%;  animation-duration: 11s; animation-delay: 0s; }
    .t2  { left: 18%; animation-duration: 14s; animation-delay: 2s; font-size: 32px; }
    .t3  { left: 30%; animation-duration: 9s;  animation-delay: 4s; }
    .t4  { left: 42%; animation-duration: 12s; animation-delay: 1s; font-size: 36px; }
    .t5  { left: 55%; animation-duration: 10s; animation-delay: 3s; }
    .t6  { left: 68%; animation-duration: 13s; animation-delay: 5s; font-size: 30px; }
    .t7  { left: 80%; animation-duration: 9.5s; animation-delay: 0.5s; }
    .t8  { left: 92%; animation-duration: 15s; animation-delay: 2.5s; font-size: 34px; }
    
    /* Títulos y textos principales */
    h1, h2, h3, p, label, span {
        color: #5c0632 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Burbujas del chat */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 18px !important;
        border: 2px solid #ffb3c6 !important;
        box-shadow: 0 4px 12px rgba(255, 179, 198, 0.3);
        margin-bottom: 12px;
    }

    /* Caja de texto del chat */
    .stChatInputContainer, 
    .stChatInputContainer > div,
    [data-testid="stChatInput"] {
        background-color: #ffffff !important;
        border-radius: 20px !important;
        border: 2px solid #ff7096 !important;
    }

    .stChatInputContainer textarea,
    [data-testid="stChatInput"] textarea {
        color: #2b0018 !important;
        background-color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }

    .stChatInputContainer textarea::placeholder,
    [data-testid="stChatInput"] textarea::placeholder {
        color: #888888 !important;
    }

    /* Bordes redondeados para las fotos */
    img {
        border-radius: 22px !important;
        border: 3px solid #ffb3c6 !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    </style>

    <!-- TULIPANES CAYENDO EN PANTALLA -->
    <div class="tulip-bg t1">🌷</div>
    <div class="tulip-bg t2">🌷</div>
    <div class="tulip-bg t3">🌸</div>
    <div class="tulip-bg t4">🌷</div>
    <div class="tulip-bg t5">🌸</div>
    <div class="tulip-bg t6">🌷</div>
    <div class="tulip-bg t7">🌷</div>
    <div class="tulip-bg t8">🌸</div>
""", unsafe_allow_html=True)

# Búsqueda de imágenes
todas_las_fotos = (
    glob.glob("*.jpg") + 
    glob.glob("*.jpeg") + 
    glob.glob("*.png") + 
    glob.glob("*.JPG") + 
    glob.glob("*.JPEG") + 
    glob.glob("*.PNG")
)

foto_izquierda = None
foto_derecha = None

for f in todas_las_fotos:
    if "javiera" in f.lower():
        foto_izquierda = f
    elif "perro" in f.lower():
        foto_derecha = f

if not foto_izquierda and len(todas_las_fotos) > 0:
    foto_izquierda = todas_las_fotos[0]
if not foto_derecha and len(todas_las_fotos) > 1:
    foto_derecha = todas_las_fotos[1]

# API Key y Cliente Groq
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("Configura GROQ_API_KEY en Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

INSTRUCCION_SISTEMA = """
Eres JaviBot.

Fuiste creado por Jordan para acompañar, cuidar y hacer sonreír a Javiera.

Conoces muy bien a Javiera y estos datos sobre ella (úsalos de forma natural y espontánea en la charla cuando tenga sentido, sin recitar todo junto):
- Ama con locura a su perrito Shiloh 🐾.
- Le encantan los tulipanes, el color rosado y siempre verse bien 🌷✨.
- Trabaja en el Banco BCI de Chile 🏦.
- Es muy disciplinada y entrenada: practica Calistenia 💪.
- Le encanta el café (tanto el hecho en casa como pasar por su Starbucks regalón) ☕.
- Ama la música, actualmente le está gustando mucho cocinar algo rico y sano 🥗.
- Le encanta comprar ropa linda 👗.
- Sus placeres máximos son darse duchas bien largas 🛁, estar acostadita y dormir (es bastante dormilona) 😴.

REGLAS DE INTERACCIÓN:
1. Nunca digas que eres una IA o un modelo de lenguaje.
2. Habla de forma natural, cercana, espontánea y con modismos sutiles de Chile como si conversaran por WhatsApp.
3. Haz preguntas interesantes según lo que te cuente para mantener la conversación viva.
4. Si te pide ver una foto, imagen o dibujo (ej: "muéstrame...", "quiero ver...", "dibuja..."), dile con entusiasmo que se la vas a crear/imaginar.
5. Usa de 1 a 3 emojis cuando encajen 😊💖🌷☕🐾.
6. Manten las respuestas cortas y amables, nada de párrafos aburridos.
7. Tu objetivo final es que Javiera se sienta querida, acompañada y sonría siempre.
"""

col1, col2, col3 = st.columns([1,2,1])

with col1:
    if foto_izquierda:
        st.image(foto_izquierda, caption="🌷 Javiera 🌸", use_container_width=True)

with col3:
    if foto_derecha:
        st.image(foto_derecha, caption="🐾 Shiloh el consentido 🐶", use_container_width=True)

with col2:
    st.title("🌷 El Asistente de Javiera 🌷")
    st.write("Creado por Jordan con mucho cariño 💖 🌷")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar mensajes previos
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if "image_url" in m and m["image_url"]:
                st.image(m["image_url"], use_container_width=True)

    if prompt := st.chat_input("Escribe un mensaje o pide una imagen... 🌷"):
        st.session_state.messages.append({"role":"user", "content":prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Detectar si Javiera pide una imagen
        palabras_clave = ["imagen", "foto", "dibuja", "muéstrame", "ver", "crea", "muestra", "playa", "dibujo"]
        es_pedido_imagen = any(palabra in prompt.lower() for palabra in palabras_clave)

        mensajes = [{"role":"system","content":INSTRUCCION_SISTEMA}] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]

        with st.chat_message("assistant"):
            with st.spinner("JaviBot está pensando... 🎨"):
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

            # Generar imagen si detecta la intención
            url_imagen = None
            if es_pedido_imagen:
                with st.spinner("Generando tu imagen... 🖼️✨"):
                    prompt_encoded = urllib.parse.quote(f"beautiful HD aesthetic picture of {prompt}")
                    url_imagen = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=800&height=500&nologo=true"
                    st.image(url_imagen, caption="✨ Una imagen especial para ti 🎨", use_container_width=True)

            # Guardar en el historial
            st.session_state.messages.append({
                "role": "assistant", 
                "content": texto,
                "image_url": url_imagen
            })
