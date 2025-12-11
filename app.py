import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA (Deve ser a primeira coisa) ---
st.set_page_config(
    page_title="Auditor HRSJC - Sequencial", 
    page_icon="🏥", 
    layout="wide"
)

# --- 2. GERENCIAMENTO DE ESTADO (MEMÓRIA) ---
if 'accumulated_text' not in st.session_state:
    st.session_state.accumulated_text = ""
if 'file_list' not in st.session_state:
    st.session_state.file_list = []
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0

# --- 3. PROMPT DO SISTEMA ---
SYSTEM_PROMPT = """
SYSTEM INSTRUCTIONS — Auditor Sênior de Comunicação & Estratégia HRSJC (v2.0 Elite)

ROLE:
Você é um Consultor Sênior de Comunicação Corporativa e Auditoria de Marca, especializado no ecossistema de Saúde Pública (SUS/OSS) e Acreditação Hospitalar (ONA).

CONTEXTO:
Hospital Regional de São José dos Campos (HRSJC).

=====================================================================
FASE 1: ANÁLISE DOS DADOS ACUMULADOS
=====================================================================
1. FILTRO DE SEGURANÇA (LGPD): Jamais reproduza nomes de pacientes.
2. TAXONOMIA: Classifique mentalmente cada peça por Formato, Eixo e Complexidade.
3. REGRA DE UNICIDADE: Relatórios contam como 1 peça. Desdobramentos contam separado.

=====================================================================
FASE 2: RELATÓRIO ANUAL DE INTELIGÊNCIA
=====================================================================
Gere o relatório final em Markdown:

SEÇÃO 1: DASHBOARD EXECUTIVO
- Tabela Resumo: Peças por Mês.
- Distribuição por Eixo Estratégico.
- Insight do Auditor.

SEÇÃO 2: INVENTÁRIO "JOB A JOB"
- Tabela única listando as principais entregas do ano (Mês | Título | Complexidade).

SEÇÃO 3: VALUATION ECONÔMICO (SHADOW PRICING)
- METODOLOGIA: Baixa (R$150), Média (R$400), Alta (R$1500).
- Calcule e exiba o VALOR TOTAL ECONOMIZADO (Saving).

SEÇÃO 4: CONSIDERAÇÕES FINAIS
- SWOT e Sugestões para o próximo ano.
"""

# --- 4. BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=100)
    st.title("Painel de Controle")
    
    # Verifica Secrets ou pede manual
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ API Key Conectada!")
    else:
        api_key = st.text_input("Cole sua Google API Key:", type="password")
    
    st.divider()
    
    # Botão de Reset
    if st.button("🗑️ Limpar Tudo (Reset)"):
        st.session_state.accumulated_text = ""
        st.session_state.file_list = []
        st.session_state.uploader_key += 1
        st.rerun()

# --- 5. INTERFACE PRINCIPAL ---
st.title("🏥 Auditoria Sequencial - HRSJC")
st.markdown("### Adicione os meses um por um para evitar erros de memória.")

# --- DEFINIÇÃO DAS COLUNAS (AQUI ESTAVA O ERRO ANTERIOR) ---
# Criamos as variáveis col1 e col2 explicitamente antes de usá-las
col1, col2 = st.columns(2)

# --- COLUNA 1: UPLOAD ---
with col1:
    st.subheader("1. Adicionar Arquivo")
    st.info("Faça o upload de UM mês, espere processar e repita.")
    
    # Chave dinâmica para limpar o uploader após uso
    current_key = f"uploader_{st.session_state.uploader_key}"
    
    uploaded_file = st.file_uploader(
        "Selecione o PDF do mês:", 
        type=["pdf"], 
        key=current_key
    )

    if uploaded_file is not None:
        if st.button("📥 Processar e Adicionar à Memória"):
            with st.spinner(f"Lendo {uploaded_file.name}..."):
                try:
                    reader = PdfReader(uploaded_file)
                    text_extracted = f"\n\n--- ARQUIVO: {uploaded_file.name} ---\n"
                    for page in reader.pages:
                        text_extracted += page.extract_text() or ""
                    
                    # Salva na memória
                    st.session_state.accumulated_text += text_extracted
                    st.session_state.file_list.append(uploaded_file.name)
                    
                    # Incrementa key para limpar o campo
                    st.session_state.uploader_key += 1
                    
                    st.success(f"✅ {uploaded_file.name} salvo!")
                    time.sleep(1)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Erro ao ler arquivo: {e}")

# --- COLUNA 2: LISTA DE ARQUIVOS ---
with col2:
    st.subheader("2. Arquivos na Memória")
    if not st.session_state.file_list:
        st.warning("Nenhum arquivo adicionado ainda.")
    else:
        st.success(f"📂 {len(st.session_state.file_list)} arquivos prontos.")
        for f in st.session_state.file_list:
            st.code(f, language="text")

st.divider()

# --- 6. GERAÇÃO FINAL ---
st.subheader("3. Gerar Relatório Anual")
st.markdown("Quando terminar de adicionar todos os meses, clique abaixo.")

if st.button("🚀 GERAR RELATÓRIO COMPLETO", type="primary"):
    if not api_key:
        st.error("⚠️ Falta a API Key.")
    elif not st.session_state.accumulated_text:
        st.error("⚠️ A memória está vazia. Adicione arquivos primeiro.")
    else:
        try:
            with st.spinner('🧠 O Auditor está analisando todos os meses compilados...'):
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                final_prompt = f"{SYSTEM_PROMPT}\n\nDADOS ACUMULADOS:\n{st.session_state.accumulated_text}"
                
                response = model.generate_content(final_prompt)
                
                st.markdown("## 📊 Relatório Final")
                st.write(response.text)
                
                st.download_button(
                    label="📥 Baixar Relatório (.md)",
                    data=response.text,
                    file_name="Relatorio_Anual_HRSJC_2025.md",
                    mime="text/markdown"
                )
        except Exception as e:
            st.error(f"Erro na geração: {e}")
