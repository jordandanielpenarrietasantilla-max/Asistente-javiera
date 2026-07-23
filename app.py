import streamlit as st
import google.generativeai as genai

# API KEY
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ⚠️ IMPORTANTE: usar modelo correcto con método correcto
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

st.title("🌸 El Asistente de Javiera 💖")

# historial
if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Escríbele algo...")

if user_input:
    st.session_state.chat.append(("Tú", user_input))

    try:
        # 🔥 MÉTODO CORRECTO
        response = model.generate_content(
            user_input,
            generation_config={
                "temperature": 0.9,
                "top_p": 1,
                "max_output_tokens": 200,
            }
        )

        reply = response.text

    except Exception as e:
        reply = f"Error: {e}"

    st.session_state.chat.append(("Javiera 💕", reply))

for role, msg in st.session_state.chat:
    st.write(f"**{role}:** {msg}")
