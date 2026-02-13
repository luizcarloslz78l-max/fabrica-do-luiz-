import streamlit as st
import google.generativeai as genai
import os
st.set_page_config(page_title="Fábrica do Luiz", layout="wide")
compiler = re.compile(r"```python(.*?)```", re.DOTALL)
st.set_page_config(page_title="Fábrica do Luiz", page_icon="🏗️", layout="wide", initial_sidebar_state="collapsed")                   
page_icon="🏗️", 
layout="wide",
initial_sidebar_state="collapsed"
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_kEY"))
st.markdown("""
<style>
.stTextArea textarea {font-size: 16px;}
div[data-testid="stMetricValue"] {font-size: 18px;}
</style>
""", unsafe_allow_html=True)
def limpar_codigo(texto):
 Extrai <apenas o código Python de blocos Markdown."")
padrao = r"```python(.*?)```"
match = re.search(padra
col_input, col_output = st.columns([1, 1])
with col_input:
st.subheader("1. O Pedido")
missao = st.text_area(
"O que vamos fabricar hoje?", 
placeholder="Ex: Crie um dashboard financeiro com gráfico de linhas usando dados fictícios...",
height=250
)
gerar = st.button("🚀 FABRICAR AGORA", type="primary", use_container_width=True)
with col_output:
st.subheader("2. O Resultado")                                                                                                                                                                               
if gerar and missao:
with st.spinner("🤖 Os robôs estão programando..."):
try:
prompt_sistema = f"""
Você é um Engenheiro de Software Sênior especialista em Python e Streamlit.
Sua tarefa é escrever o código COMPLETO para a seguinte solicitação: "{missao}".
REGRAS OBRIGATÓRIAS:
1. O código deve ser um script único e executável.
2. Inclua TODOS os imports necessários no topo (ex: import pandas as pd, import streamlit as st).
3. Se precisar de dados, gere dados fictícios dentro do código.
4. O código deve ter tratamento de erros básico.
5. Não explique o código, apenas forneça o bloco de código.
"""
resposta = motor.generate_content(prompt_sistema)
if resposta.text:
codigo_limpo = limpar_codigo(resposta.text)
st.success("✅ Aplicativo Fabricado com Sucesso!")
# Exibir código com destaque de sintaxe
st.code(codigo_limpo, language='python', line_numbers=True)
st.download_button(
label="📥 Baixar arquivo (.py)",
data=codigo_limpo,
file_name="app_gerado.py",
mime="text/x-python",
use_container_width=True
) else:
st.error("O modelo não retornou texto. Pode ter sido bloqueado por segurança.")
except Exception as e:
st.error(f"💥 Falha na linha de produção: {e}")                                                                                                                                                                                                                                                                        
elif gerar and not missao:
st.warning("Por favor, descreva o que deseja criar.")
else:
st.info("Aguardando instruções para iniciar a produção...")
st.write("---")
st.markdown("<div style='text-align: center; color: grey;'>Fábrica do Luiz © 2026 | Powered by Gemini</div>", unsafe_allow_html=True) não entendi nada não entendi é p**** nenhuma e não vou mexer com você vai dormir mais)