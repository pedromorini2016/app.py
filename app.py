import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Auditor HRSJC - Sequencial", 
    page_icon="🏥", 
    layout="wide"
)

# --- INICIALIZAÇÃO DO ESTADO (MEMÓRIA TEMPORÁRIA) ---
# Isso permite que o app lembre dos arquivos enquanto você carrega outros
if 'accumulated_text' not in st.session_state:
    st.session_state.accumulated_text = ""
if 'file_list' not in st.session_state:
    st.session_state.file_list = []
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0

# --- PROMPT DO SISTEMA ---
SYSTEM_PROMPT = """
SYSTEM INSTRUCTIONS — Auditor Sênior de Comunicação & Estratégia HRSJC (v2.0 Elite)

ROLE:
Você é um Consultor Sênior de Comunicação Corporativa e Auditoria de Marca, especializado no ecossistema de Saúde Pública (SUS/OSS) e Acreditação Hospitalar (ONA). Sua missão é transformar dados operacionais de comunicação em inteligência estratégica e valuation financeiro.

CONTEXTO:
Hospital Regional de São José dos Campos (HRSJC). O foco não é apenas volume, mas impacto na Humanização, Segurança do Paciente e Reputação Institucional.

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

TOM DE VOZ: Corporativo, Analítico e Orientado a Dados.
"""

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=100)
    st.title("Painel de Controle")
    
    # API Key
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ API Key Conectada!")
    else:
        api_key = st.text_input("Cole sua Google API Key:", type="password")
    
    st.divider()
    
    # Botão de Reset (Limpar Memória)
    if st.button("🗑️ Limpar Tudo e Começar do Zero"):
        st.session_state.accumulated_text = ""
        st.session_state.file_list = []
        st.session_state.uploader_key += 1
        st.rerun()

# --- INTERFACE PRINCIPAL ---
st.title("🏥 Auditoria Sequencial - HRSJC")
st.markdown("### Adicione os meses um por um para não sobrecarregar o sistema.")

# --- COLUNAS DE LAYOUT ---
co
