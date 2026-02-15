import streamlit as st
import os
import re

import google.generativeai as genai

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Fábrica do Luiz", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    .stTextArea textarea {font-size: 16px;}
    div[data-testid="stMetricValue"] {font-size: 18px;}
    </style>
""", unsafe_allow_html=True)

def limpar_codigo(texto):
    padrao = r"```python(.*?)```"
    match = re.search(padrao, texto, re.DOTALL)
    if match:
        return match.group(1).strip()
    return texto.strip()

chave = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not chave:
    st.error("🔐 ERRO: Configure a GEMINI_API_KEY nos Secrets.")
    st.stop()

genai.configure(api_key=chave)
motor = genai.GenerativeModel('gemini-1.5-pro')

# --- INTERFACE ---
st.title("🏗️ FÁBRICA DO LUIZ")
st.caption("Orquestrador de Software - Monitoramento 2026")

if 'codigo_gerado' not in st.session_state:
    st.session_state.codigo_gerado = ""

col_in, col_out = st.columns([1, 1])

with col_in:
    st.subheader("1. O Pedido")
    missao = st.text_area("O que vamos fabricar hoje?", height=250)
    gerar = st.button("🚀 FABRICAR AGORA", type="primary", use_container_width=True)

with col_out:
    st.subheader("2. O Resultado")
    if gerar and missao:
        with st.spinner("🤖 Produzindo..."):
            try:
                prompt = f"Crie um código Python Streamlit completo para: {missao}"
                res = motor.generate_content(prompt)
                if res.text:
                    st.session_state.codigo_gerado = limpar_codigo(res.text)
                    st.success("✅ Sucesso!")
            except Exception as e:
                st.error(f"💥 Erro: {e}")

    if st.session_state.codigo_gerado:
        st.code(st.session_state.codigo_gerado, language='python')
        st.download_button("📥 Baixar .py", st.session_state.codigo_gerado, file_name="app.py")