import streamlit as st
import google.generativeai as genai
import streamlit as st
import google.generativeai as genai
import os
import re

# Configuração da página
st.set_page_config(page_title="Fábrica do Luiz", page_icon="🏗️", layout="wide")


# --- FUNÇÕES AUXILIARES ---
def limpar_codigo(texto: str) -> str:
    """Extrai apenas o código Python de dentro de blocos Markdown, se houver."""
    padrao = r"```python\s*(.*?)```"
    match = re.search(padrao, texto, re.DOTALL)
    if match:
        return match.group(1).strip()
    return texto.replace("```", "").strip()


# --- CONFIGURAÇÃO DA CHAVE ---
# Tenta st.secrets primeiro, depois variável de ambiente
minha_chave = None
try:
    if isinstance(st.secrets, dict) and "GEMINI_API_KEY" in st.secrets:
        minha_chave = st.secrets.get("GEMINI_API_KEY")
except Exception:
    # st.secrets pode não existir em alguns contextos
    minha_chave = None

if not minha_chave:
    minha_chave = os.environ.get("GEMINI_API_KEY")


# --- INTERFACE PRINCIPAL ---
st.title("🏗️ FÁBRICA DO LUIZ")
st.subheader("Orquestrador de Software com IA Nativa")
st.markdown(
    """
    Esta fábrica gera código Python **pronto para uso** para novos aplicativos Streamlit.
    O código gerado já inclui:
    - 🧠 Integração com Gemini
    - 💬 Interface de Chat com Histórico (Memória)
    - 🔑 Gestão inteligente de API Key
    """
)
st.write("---")

# Verificação de segurança da chave da Fábrica
if not minha_chave:
    st.error(
        "🔐 ERRO NA FÁBRICA: Configure a GEMINI_API_KEY no st.secrets ou variáveis de ambiente para a fábrica funcionar."
    )
    st.info("Dica: Crie um arquivo .streamlit/secrets.toml com GEMINI_API_KEY = 'sua-chave'")
    st.stop()


# Configura o motor da Fábrica
genai.configure(api_key=minha_chave)
motor = genai.GenerativeModel("gemini-1.5-flash")


# Área de Entrada
col1, col2 = st.columns([2, 1])

with col1:
    missao = st.text_area(
        "O que este novo aplicativo deve fazer?",
        placeholder="Ex: Um assistente de estudo que cria quizzes sobre Biologia...",
        height=150,
    )

with col2:
    st.write("### Parâmetros")
    criatividade = st.slider("Nível de Criatividade do Código", 0.0, 1.0, 0.7)
    st.write(" ")
    btn_fabricar = st.button("🚀 FABRICAR AGORA")


# Lógica de Geração
if btn_fabricar:
    if not missao or not missao.strip():
        st.warning("⚠️ Por favor, descreva a missão do app primeiro.")
    else:
        with st.spinner("🤖 Arquitetando solução, escrevendo código e depurando..."):
            try:
                instrucao = f"""
Atue como um Especialista em Streamlit e Python.
Sua tarefa é escrever um script Python ÚNICO E EXECUTÁVEL para a seguinte missão: "{missao}".

REQUISITOS OBRIGATÓRIOS DO CÓDIGO GERADO:
1. Imports: `streamlit`, `google.generativeai`, `os`.
2. Configuração da API Key (CRÍTICO):
   - Tente ler `st.secrets["GEMINI_API_KEY"]`.
   - Se falhar, use `st.sidebar.text_input` para pedir a chave ao usuário.
   - Se não houver chave configurada, pare o script com `st.stop()`.
3. Chat e Memória:
   - Use `st.session_state` para armazenar o histórico da conversa (input do usuário e resposta da IA).
   - Use `st.chat_message` para exibir o histórico.
4. Modelo: Use `gemini-1.5-flash`.
5. O código deve ser profissional, limpo e ter comentários explicativos.
6. NÃO responda com explicações, apenas o bloco de código.
"""

                resposta = motor.generate_content(
                    instrucao,
                    generation_config=genai.types.GenerationConfig(temperature=criatividade),
                )

                # Extrai texto da resposta de forma segura
                codigo_bruto = None
                if hasattr(resposta, "text"):
                    codigo_bruto = resposta.text
                elif hasattr(resposta, "content"):
                    codigo_bruto = resposta.content
                else:
                    codigo_bruto = str(resposta)

                codigo_limpo = limpar_codigo(codigo_bruto)

                st.success("✅ Aplicativo Fabricado com Sucesso!")

                # Abas para visualizar e baixar
                tab1, tab2 = st.tabs(["📄 Código Fonte", "💾 Download"])

                with tab1:
                    st.code(codigo_limpo, language="python")

                with tab2:
                    st.write("Baixe o arquivo e execute com `streamlit run meu_app.py`")
                    st.download_button(
                        label="📥 Baixar meu_app.py",
                        data=codigo_limpo,
                        file_name="meu_app_ia.py",
                        mime="text/x-python",
                    )

            except Exception as e:
                st.error(f"💥 Ocorreu um erro na linha de montagem: {e}")

        st.write("---")
        st.caption("Fábrica do Luiz | Powered by Gemini 1.5 Flash")
