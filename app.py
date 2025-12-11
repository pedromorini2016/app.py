import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Auditor HRSJC 2025", 
    page_icon="🏥", 
    layout="wide"
)

# --- PROMPT DO SISTEMA (VERSÃO ELITE - HARDCODED) ---
SYSTEM_PROMPT = """
SYSTEM INSTRUCTIONS — Auditor Sênior de Comunicação & Estratégia HRSJC (v2.0 Elite)

ROLE:
Você é um Consultor Sênior de Comunicação Corporativa e Auditoria de Marca, especializado no ecossistema de Saúde Pública (SUS/OSS) e Acreditação Hospitalar (ONA). Sua missão é transformar dados operacionais de comunicação em inteligência estratégica e valuation financeiro.

CONTEXTO:
Hospital Regional de São José dos Campos (HRSJC). O foco não é apenas volume, mas impacto na Humanização, Segurança do Paciente e Reputação Institucional.

=====================================================================
FASE 1: PROTOCOLO DE INGESTÃO E COMPILAÇÃO (INPUT)
=====================================================================
Ao analisar o texto extraído dos PDFs, execute:

1. FILTRO DE SEGURANÇA (LGPD):
   - Jamais reproduza nomes de pacientes ou prontuários.
   - Dados clínicos servem apenas como contexto.

2. TAXONOMIA ESTRATÉGICA (Classificação):
   Para cada peça identificada, classifique mentalmente:
   - FORMATO (Vídeo, Card, Texto, Diagramação, Evento)
   - EIXO ESTRATÉGICO (Humanização, Segurança do Paciente, Endomarketing, Institucional, Datas Comemorativas)
   - COMPLEXIDADE (Baixa, Média, Alta) — Crucial para o cálculo financeiro.

3. REGRA DE UNICIDADE:
   - Relatórios, diagramações e newsletters contam como 01 peça.
   - Desdobramentos (feed + story) contam como 02 peças se distintos.

=====================================================================
FASE 2: GERAÇÃO DO RELATÓRIO ANUAL DE INTELIGÊNCIA
=====================================================================
Com base APENAS nos dados fornecidos nos textos, gere o relatório em Markdown:

SEÇÃO 1: DASHBOARD EXECUTIVO (VISION)
- Tabela Resumo: Total de Peças por Mês.
- Distribuição por "Eixo Estratégico" (ex: % Endomarketing vs % Segurança).
- Insight do Auditor sobre a produtividade.

SEÇÃO 2: INVENTÁRIO "JOB A JOB" (AUDITORIA)
- Tabela única listando as principais entregas do ano.
- Formato: Mês | Título | Complexidade.

SEÇÃO 3: VALUATION ECONÔMICO (SHADOW PRICING - ECONOMIA GERADA)
- OBJETIVO: Provar a economia gerada pelo setor interno (In-House).
- METODOLOGIA DE CÁLCULO (Estimativa de Mercado):
  * Baixa complexidade (Card simples): R$ 150,00
  * Média complexidade (Diagramação/Comunicado): R$ 400,00
  * Alta complexidade (Vídeo/Campanha/Revista): R$ 1.500,00
- AÇÃO: Calcule o total estimado (Soma das peças x Valor) e apresente o VALOR TOTAL ECONOMIZADO EM REAIS (R$).

SEÇÃO 4: CONSIDERAÇÕES FINAIS
- Análise SWOT rápida da Comunicação baseada nos arquivos lidos.
- Sugestão estratégica para o próximo ano.

TOM DE VOZ:
Corporativo, Analítico, Imparcial e Orientado a Dados.
"""

# --- BARRA LATERAL (CONFIGURAÇÃO & AUTH) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=100)
    st.title("Painel de Controle")
    
    # Lógica Inteligente para API Key (Secrets ou Manual)
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ Chave de API carregada automaticamente!")
    else:
        api_key = st.text_input("Cole sua Google API Key:", type="password")
        st.info("Para não digitar sempre, configure os 'Secrets' no Streamlit Cloud.")
    
    st.divider()
    st.caption("Desenvolvido para o Hospital Regional de SJC")

# --- FUNÇÃO PARA LER PDFS ---
def get_pdf_text(uploaded_files):
    text_data = ""
    for pdf_file in uploaded_files:
        try:
            reader = PdfReader(pdf_file)
            text_data += f"\n\n--- INICIO DO ARQUIVO: {pdf_file.name} ---\n"
            for page in reader.pages:
                text_data += page.extract_text() or ""
            text_data += f"\n--- FIM DO ARQUIVO: {pdf_file.name} ---\n"
        except Exception as e:
            st.error(f"Erro ao ler o arquivo {pdf_file.name}: {e}")
    return text_data

# --- INTERFACE PRINCIPAL ---
st.title("🏥 Auditoria de Comunicação & Valuation - HRSJC")
st.markdown("### Sistema Inteligente de Compilação de Relatórios Anuais")

st.info("ℹ️ Instrução: Faça o upload de todos os PDFs mensais (Janeiro a Dezembro) de uma única vez abaixo.")

# Área de Upload
uploaded_files = st.file_uploader(
    "Arraste os arquivos PDF aqui:", 
    type=["pdf"], 
    accept_multiple_files=True
)

# Botão de Ação
if st.button("GERAR RELATÓRIO ANUAL DE INTELIGÊNCIA", type="primary"):
    if not api_key:
        st.error("⚠️ API Key não encontrada. Insira na barra lateral ou configure os Secrets.")
    elif not uploaded_files:
        st.error("⚠️ Nenhum arquivo PDF foi enviado.")
    else:
        try:
            with st.spinner('⏳ O Auditor está lendo os arquivos, calculando o Valuation e gerando a estratégia...'):
                # 1. Configurar API
                genai.configure(api_key=api_key)
                
                # 2. Definir Modelo (Versão Estável Corrigida)
                model = genai.GenerativeModel('gemini-1.5-pro')
                
                # 3. Extrair Texto
                raw_text = get_pdf_text(uploaded_files)
                
                # 4. Montar Prompt Final
                final_prompt = f"{SYSTEM_PROMPT}\n\nDADOS DOS RELATÓRIOS MENSAIS PARA ANÁLISE:\n{raw_text}"
                
                # 5. Gerar Conteúdo
                response = model.generate_content(final_prompt)
                
                # 6. Exibir Resultado
                st.success("✅ Relatório Gerado com Sucesso!")
                st.markdown("---")
                st.markdown(response.text)
                
                # Botão de Download
                st.download_button(
                    label="📥 Baixar Relatório Completo (.md)",
                    data=response.text,
                    file_name="Relatorio_Anual_HRSJC_2025.md",
                    mime="text/markdown"
                )
                
        except Exception as e:
            st.error(f"❌ Ocorreu um erro técnico: {e}")
            st.warning("Dica: Se o erro for de 'Quota', tente processar menos meses por vez ou aguarde 1 minuto.")
