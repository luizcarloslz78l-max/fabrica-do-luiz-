import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    motor = genai.GenerativeModel('gemini-pro')
else:
    st.error("⚠️ GEMINI_API_KEY não configurada")
    st.stop()

st.title("🏗️ FÁBRICA DO LUIZ")
st.subheader("Orquestrador de Software com IA Nativa")
st.write("---")

# Onde você dá a ordem para a fábrica
missao = st.text_area("O que este novo aplicativo deve fazer?", 
                     placeholder="Descreva aqui o objetivo do app...")

if st.button("FABRICAR AGORA"):
    if not missao.strip():
        st.warning("Por favor, descreva a missão do app!")
    else:
        with st.spinner("Injetando IA e construindo aplicativo..."):
            try:
                # O comando que obriga a IA a já nascer dentro do código novo
                instrucao = f"""
                Crie um código Python/Streamlit completo para um novo app cuja missão é: {missao}.
                REQUISITOS OBRIGATÓRIOS:
                1. O app gerado deve ter um campo de chat.
                2. Ele deve usar a chave 'GEMINI_API_KEY' para funcionar.
                3. A IA desse app já deve nascer sabendo tudo sobre {missao}.
                Retorne apenas o código puro, sem explicações.
                """
                
                resposta = motor.generate_content(instrucao)
                
                st.success("✅ Aplicativo Fabricado com IA Nativa!")
                st.divider()
                st.write("### Código do seu Novo App:")
                st.code(resposta.text, language='python')
                
            except Exception as e:
                st.error(f"Erro no motor: {e}")