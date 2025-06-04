import streamlit as st
from groq import Groq

st.set_page_config(page_title="MI CHATBOT")
st.title("BIENVENIDO AL CHAT BOT DE MATIAS")

MODELOS = ["llama3-8b-8192","llama3-70b-8192","mixtral-8x7b-32768"]

def main():
    def configurar_pagina():
        st.title("Mi Chat IA")
        nombre = st.text_input("¿Cuál es tu nombre?")
        if st.button("Saludar"):
            st.write(f"Hola {nombre}")
        st.sidebar.title("Configuración modelos")

        modelo_elegido = st.sidebar.selectbox("Modelos",MODELOS,index=0) #nombre de selectbox, lista de elementos y el index elije el modelo predeterminado 
        return modelo_elegido

    def crear_usuario():
        clave_secreta = st.secrets["CLAVE_API"]
        return Groq(api_key=clave_secreta)

    def configurar_modelo(cliente,modelo,mensaje_entrada):
        respuesta = cliente.chat.completions.create(
            model = modelo,
            messages = [{"role" : "user", "content" : mensaje_entrada}],
            stream = False
        )
        content_ia = respuesta.choices[0].message.content
        return content_ia

    def inicializar_estado():
        if "mensajes" not in st.session_state:
            st.session_state.mensajes = []

    def actualizar_historial(rol,contenido,avatar):
        st.session_state.mensajes.append({"role" : rol, "content" : contenido, "avatar" : avatar})

    def mostrar_historial():
        for mensaje in st.session_state.mensajes:
            with st.chat_message(mensaje["role"],avatar = mensaje["avatar"]) :
                st.markdown(mensaje["content"])

    def area_chat():
        contenedor = st.container(height=400)
        with contenedor : mostrar_historial()

    usuario_groq = crear_usuario()
    inicializar_estado()
    modelo_actual = configurar_pagina()
    area_chat()
    mensaje_usuario = st.chat_input("Escibí un prompt")

    if mensaje_usuario:
        actualizar_historial("user",mensaje_usuario,"💀")
        
        respuesta_ia = configurar_modelo(usuario_groq, modelo_actual, mensaje_usuario)
        
        actualizar_historial("assistant",respuesta_ia,"🤡")
        st.rerun()


if __name__ == "__main__":
    main()

#python -m streamlit run main.py