import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import io

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Auditor HRSJC 2025", page_icon="🏥", layout="wide")

# --- BARRA LATERAL (CONFIGURAÇÃO) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=100) # Ícone Hospital
    st.title("Painel de Controle")
    api_key = st.text_input("Cole sua Google API Key:", type="password")
    st.info("Obtenha sua chave em: aistudio.google.com")
    
    st.divider()
    st.write("Desenvolvido para o Hospital Regional de SJC")

# --- PROMPT DO SISTEMA (AQUELE QUE CRIAMOS) ---
SYSTEM_PROMPT = """
VOCÊ É O AUDITOR DE COMUNICAÇÃO INSTITUCIONAL HRSJC (Versão Elite).
[COLE AQUI TODO O PROMPT OTIMIZADO QUE FIZEMOS ANTERIORMENTE]
...
IMPORTANTE: Analise os textos fornecidos abaixo (separados por mês) e gere o RELATÓRIO ANUAL FINAL.
"""

# --- FUNÇÃO PARA LER PDFS ---
def get_pdf_text(uploaded_files):
    text_data = ""
    for pdf_file in uploaded_files:
        reader = PdfReader(pdf_file)
        text_data += f"\n\n--- INICIO DO ARQUIVO: {pdf_file.name} ---\n"
        for page in reader.pages:
            text_data += page.extract_text() or ""
        text_data += f"\n--- FIM DO ARQUIVO: {pdf_file.name} ---\n"
    return text_data

# --- INTERFACE PRINCIPAL ---
st.title("🏥 Auditoria de Comunicação & Valuation - HRSJC")
st.markdown("### Sistema Inteligente de Compilação de Relatórios Anuais")

st.warning("⚠️ Atenção: Por segurança (LGPD), este sistema processa apenas texto. Imagens dentro dos PDFs não são analisadas visualmente, apenas o conteúdo escrito.")

# Área de Upload
uploaded_files = st.file_uploader(
    "Faça o upload dos Relatórios Mensais (PDFs de Jan a Dez)", 
    type=["pdf"], 
    accept_multiple_files=True
)

if st.button("GERAR RELATÓRIO ANUAL DE INTELIGÊNCIA", type="primary"):
    if not api_key:
        st.error("Por favor, insira a API Key na barra lateral.")
    elif not uploaded_files:
        st.error("Por favor, faça o upload de pelo menos um arquivo PDF.")
    else:
        try:
            with st.spinner('⏳ O Auditor está lendo os arquivos e processando o Valuation... Isso pode levar alguns instantes.'):
                # 1. Configurar o Modelo
                genai.configure(api_key=api_key)
               model = genai.GenerativeModel('gemini-1.5-pro')
                
                # 2. Extrair texto dos PDFs
                raw_text = get_pdf_text(uploaded_files)
                
                # 3. Montar o comando final
                final_prompt = f"{SYSTEM_PROMPT}\n\nDADOS PARA ANÁLISE:\n{raw_text}"
                
                # 4. Chamar a IA
                response = model.generate_content(final_prompt)
                
                # 5. Exibir Resultado
                st.success("✅ Relatório Gerado com Sucesso!")
                st.markdown("---")
                st.markdown(response.text)
                
                # Botão de Download
                st.download_button(
                    label="📥 Baixar Relatório (.md)",
                    data=response.text,
                    file_name="Relatorio_Anual_HRSJC.md",
                    mime="text/markdown"
                )
                
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
