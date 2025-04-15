import streamlit as st # Biblioteca para criar interfaces
import base64 # Módulo para codificar e decodificar dados em formato Base64.
import pandas as pd # Biblioteca essencial para manipulação de dados.
import altair as alt # Biblioteca para visualização de dados baseada em gráficos declarativos.
import numpy as np # Biblioteca usada para cálculos matemáticos e manipulação de arrays.
import matplotlib.pyplot as plt # Biblioteca para criar gráficos e visualizações em 2D.
from io import BytesIO # Módulo para manipular fluxos de dados em memória.
from fpdf import FPDF # Biblioteca utilizada para gerar arquivos PDF. Ideal para criar relatórios.

st.set_page_config(page_title="DATANExT", layout="wide")

st.markdown("""
<style>
/* Corrige o fundo e a borda do multiselect */
section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] {
    background-color: #2980b9 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 2px !important;
}

/* Corrige cor do texto no placeholder e itens */
section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] * {
    color: white !important;
}

/* Corrige o fundo e o texto do item selecionado ("tag") */
section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {
    background-color: #2980b9 !important;
    color: white !important;
    border: none !important;
    border-radius: 5px !important;
}

/* Corrige a cor do botão "x" do item selecionado */
section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] svg {
    color: white !important;
}

/* Corrige o fundo do dropdown */
section[data-testid="stSidebar"] .stMultiSelect div[role="listbox"] {
    background-color: #2980b9 !important;
    color: white !important;
}

/* Corrige a cor dos itens do dropdown */
section[data-testid="stSidebar"] .stMultiSelect div[role="option"] {
    background-color: #2980b9 !important;
    color: white !important;
}

    /* Corrige foco e hover */
    section[data-testid="stSidebar"] .stMultiSelect div[role="option"]:hover {
    background-color: #2980b9 !important;
}
</style>
""", 
unsafe_allow_html=True)

st.markdown("""
<style>
    /* Linha ativa do slider */
    div[data-baseweb="slider"] > div > div:nth-child(1) {
    background: #2980b9 !important;
    height: 4px !important;
}


    /* Bolinhas (thumbs) */
    div[data-baseweb="slider"] [role="slider"] {
    background: #2980b9 !important;
    border: none !important;
}

    /* Tooltip acima da bolinha */
    div[data-baseweb="slider"] [data-testid="stTooltipLabel"] {
    background: #2980b9 !important;
    height: 4px !important;
}

    /* Labels embaixo */
    div[data-baseweb="slider"] [data-testid="stTickBar"] span {
    font-weight: bold !important;
}
</style>
""", 
unsafe_allow_html=True)

def imagem_base64(caminho_imagem):
    import base64
    with open(caminho_imagem, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Função para gerar o PDF
def gerar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Dashboard DataNExT", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Nome da Empresa: {st.session_state.get('empresa', 'Sem empresa definida')}", ln=True, align="L")
    pdf.cell(200, 10, txt="Relatório gerado a partir do dashboard.", ln=True, align="L")
    pdf_output = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output

# Utiliza o nome da empresa, logomarca e base de dados da sessão
empresa = st.session_state.get('empresa', 'Sem empresa definida')
logo = st.session_state.get('logo', None)
data = st.session_state.get('data', None)

logo_datanext = "logo_azul2.png"
base_logo_DN = imagem_base64(logo_datanext)
st.sidebar.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{base_logo_DN}" width="150" style="margin-right:10px;">
        <span style="font-size: 20px; font-weight: bold; color:#2980b9;"></span>
    </div>
    <hr style="margin-top: 10;">
    """,
    unsafe_allow_html=True
)

# Gera o PDF e codifica em Base64 para uso no href
pdf_file = gerar_pdf()
pdf_base64 = base64.b64encode(pdf_file.getvalue()).decode('latin1')

# Caminho para o ícone PDF
logo_pdf = "pdf.png"
base_logo_pdf = imagem_base64(logo_pdf)

# Adicionando o ícone no lado direito da página
st.markdown(
    f"""
    <style>
    .pdf-icon-container {{
        display: flex;
        justify-content: flex-end;  /* Alinha o ícone à direita */
        margin-top: 10px;
    }}
    .pdf-icon {{
        width: 40px;  /* Tamanho do ícone */
        cursor: pointer;  /* Estilo do cursor ao passar o mouse */
    }}
    </style>
    <div class="pdf-icon-container">
        <a download="dashboard.pdf" href="data:application/pdf;base64,{pdf_base64}">
            <img src="data:image/png;base64,{base_logo_pdf}" class="pdf-icon" alt="PDF Icon">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

def imagem_base64(caminho_imagem):
    with open(caminho_imagem, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Usa a logo enviada na main_page
if logo:
    if isinstance(logo, bytes):  # Caso seja um upload de arquivo
        st.sidebar.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center;">
                <img src="data:image/png;base64,{base64.b64encode(logo).decode()}" width="150" alt="Logomarca">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:  # Caso seja uma URL
        st.sidebar.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center;">
                <img src="{logo}" width="150" alt="Logomarca enviada por URL">
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    # Usa a logo local (fallback)
    caminho_logo = "logo_01.png"
    base_logo = imagem_base64(caminho_logo)
    st.sidebar.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center;">
            <img src="data:image/png;base64,{base_logo}" width="150" alt="Logomarca local">
        </div>
        <hr style="margin-top: 10;">
        """,
        unsafe_allow_html=True
    )

st.markdown(
    f"""
    <h1 style= 'text-align:left; color: #12357c'>
    Dashboard {empresa}
    </h1>
    """,
    unsafe_allow_html=True
)

#Utiliza o arquivo csv upado 
csv_caminho = r"C:\Users\Lenovo\Documents\Next\projeto_final\gerador_relatorio_de_vendas\Base_farmacia_manipulada_2024_dashboard.csv"

# Inicializar o DataFrame
data = None

try:
    if data is not None:
        st.success("Análise Gerada com Sucesso!")
    else:
        # Carregar os dados do CSV
        data = pd.read_csv(csv_caminho)
        st.success("Base de dados carregada com sucesso!")
        
    data['Data_Venda'] = pd.to_datetime(data['Data_Venda'], errors='coerce')
    data['Quantidade_Vendida'] = pd.to_numeric(data['Quantidade_Vendida'], errors='coerce')
    data['Preço_Unitário'] = pd.to_numeric(data['Preço_Unitário'], errors='coerce')
    data['Valor_Total'] = data['Quantidade_Vendida'] * data['Preço_Unitário']
    data['AnoMes'] = data['Data_Venda'].dt.to_period('M')
    
    st.sidebar.markdown("#### FILTROS")

    categorias = st.sidebar.multiselect("Categoria do Produto", options=data['Categoria_Produto'].dropna().unique()) #dropna é remover os valores vázios e o unique é remover a duplicidade.
    if categorias:
        data = data[data['Categoria_Produto'].isin(categorias)] #isin verifica se todos os itens daquela categoria foram selecionados.

    vendedores = st.sidebar.multiselect("Vendedores", options=data['Vendedor'].dropna().unique()) 
    if vendedores:
        data = data[data['Vendedor'].isin(vendedores)] 
    
    canal = st.sidebar.multiselect("Canal de Venda", options=data['Canal_Venda'].dropna().unique()) 
    if canal:
        data = data[data['Canal_Venda'].isin(canal)] 

    data_minima = data['Data_Venda'].min().date()    
    data_maxima = data['Data_Venda'].max().date()

    intervalo_data =  st.sidebar.slider("Intervalo de Vendas",min_value=data_minima,max_value=data_maxima,value=(data_minima,data_maxima))
    data = data[(data['Data_Venda'].dt.date >= intervalo_data[0]) & (data['Data_Venda'].dt.date <=  intervalo_data[1])]
    
    vendas_por_mes = data.groupby('AnoMes')['Valor_Total'].sum()
    vendas_por_mes.index = vendas_por_mes.index.astype(str)

    vendas_categoria = data.groupby('Categoria_Produto')['Valor_Total'].sum().sort_values(ascending=False)

    vendas_vendedor = data.groupby('Vendedor')['Valor_Total'].sum().sort_values(ascending=False)

    canal_vendas = data.groupby('Canal_Venda').size().sort_values(ascending=False)

    col1, col2, col3 = st.columns([0.5, 0.5, 0.3])
    with col1:
        st.write('#### Vendas por Mês')
        fig1, ax1 = plt.subplots(figsize=(6, 3))
        vendas_por_mes.plot(kind='barh', ax=ax1, color='#2980b9')
        ax1.set_xlabel('Ano / Mês')
        ax1.set_ylabel('Valor Total')
        ax1.grid(True)
        plt.xticks(rotation=0)
        for container in ax1.containers:
            rotulo1 = [f'R$ {v:,.2f}'.replace(",","x").replace(".",",").replace("x",".") for v in container.datavalues]
            ax1.bar_label(container,labels=rotulo1, padding=5, fontsize = 10)
        st.pyplot(fig1)

    with col2:
        st.write('###### Vendas por Categoria')
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        cores = ['#2980b9', '#3498db', '#1f618d', '#2471a3','#12496e','#91c8ed']

        vendas_categoria.plot(
            kind='pie',
            ax=ax2,
            colors=cores, 
            autopct='%1.1f%%',  
            startangle=90,      
            legend=False
        )

        ax2.set_ylabel('')  
        ax2.set_xlabel('')  
        ax2.axis('equal')   
        st.pyplot(fig2)


    def borda(title, value):
        st.markdown(
        f""" 
        <div style="
            border: 2px solid;
            border-radius: 10px;
            padding:10px;
            margin-bottom:8px;
            background-color: white;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            text-align:center; 
        ">
            <h4 style="margin-bottom: 8px; color: #333; font-size:20px;">{title} </h4>
            <p style="font-size: 25px; font-weight: bold; margin: 0; color: #000;">{value} </p>
        </div>
    """,
    unsafe_allow_html=True
)

    with col3:
        qtd_vendas = data.shape[0]
        faturamento_total = data['Valor_Total'].sum()
        ticket_medio = faturamento_total / qtd_vendas if qtd_vendas != 0 else 0

        borda("Quantidade de Vendas", f"{qtd_vendas:,}".replace(",", "."))
        borda("Faturamento Total", f"R$ {faturamento_total:,.2f}".replace(",", "."))
        borda("Ticket Médio", f"R$ {ticket_medio:,.2f}".replace(",", ".").replace(".", ","))

    col4, col5 = st.columns([0.5, 0.5])
    with col4:
        st.write('#### Vendas por Vendedor')
        fig4, ax4 = plt.subplots(figsize=(6, 3))  
        ax4.plot(vendas_vendedor.index, vendas_vendedor.values, marker='o', linestyle='-', color='#2471a3')
        ax4.set_xlabel('Vendedor')
        ax4.set_ylabel('Valor Total')
        ax4.grid(True)
        plt.xticks(rotation=0, ha='right', fontsize=6)
        

        # Rótulos nos pontos
        for i, valor in enumerate(vendas_vendedor.values):
            valor_formatado = f'R$ {valor:,.0f}'.replace(',', '.') 
            ax4.annotate(valor_formatado,
                     (vendas_vendedor.index[i], vendas_vendedor.values[i]),
                     textcoords="offset points",
                     xytext=(0, 8),
                     ha='center',
                     fontsize=8)

        st.pyplot(fig4)

    with col5:
        st.write('#### Canal de vendas')
        fig5, ax5 = plt.subplots(figsize=(6, 3))
        canal_vendas.plot(kind='bar', ax=ax5)
        ax5.set_xlabel('')
        ax5.set_ylabel('')
        ax5.grid(False)
        plt.xticks(rotation=0)
        for container in ax5.containers:
            ax5.bar_label(container, fmt="%.0f",  padding=0.8, fontsize = 7)
        st.pyplot(fig5)

 # st.write("###  Total Vendido por Mês")
    # fig, ax = plt.subplots(figsize=(11, 5))
    # vendas_por_mes.plot(kind='bar', ax=ax)
    # ax.set_title("Total Vendido por Mês")
    # ax.set_xlabel('Ano-Mês')
    # ax.set_ylabel('Valor Total')
    # ax.grid(True)
    # plt.xticks(rotation=0)
    # st.pyplot(fig)

except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")

# Rodapé
st.markdown("""<hr><div style= 'text-align: center;font-size: small;'>©Todos os direitos reservados.</div>""", unsafe_allow_html=True)