import streamlit as st
import pandas as pd
import yfinance as yf

# Função para carregar tickers da B3 direto do site
@st.cache_data
def listar_acoes_b3():
    dados = [
        ("Petrobras PN", "PETR4.SA"),
        ("Vale ON", "VALE3.SA"),
        ("Itaú Unibanco PN", "ITUB4.SA"),
        ("Bradesco PN", "BBDC4.SA"),
        ("Magazine Luiza ON", "MGLU3.SA"),
        ("Banco do Brasil ON", "BBAS3.SA"),
        ("Ambev ON", "ABEV3.SA"),
        ("WEG ON", "WEGE3.SA"),
        ("Localiza ON", "RENT3.SA"),
        ("Suzano ON", "SUZB3.SA"),
        ("Gerdau PN", "GGBR4.SA"),
        ("Eletrobras ON", "ELET3.SA"),
        ("Santander BR PN", "SANB11.SA"),
    ]
    
    df = pd.DataFrame(dados, columns=["Nome Comercial", "Código"])
    return df


# Função para baixar os dados das ações
@st.cache_data
def carregar_dados(tickers):
    dados = yf.download(tickers, start="2020-01-01", end="2025-01-01")["Close"]
    return dados

# Interface do Streamlit
st.title("📈 Análise da Bolsa de Valores Brasileira (B3)")
st.write("""  ## Gráfico das Ações Brasileiras Mais Ativas
         """)

# Carrega lista de empresas
empresas_b3 = listar_acoes_b3()

# Monta dicionário Nome -> Código
mapa_empresas = dict(zip(empresas_b3["Nome Comercial"], empresas_b3["Código"]))

# Multiselect com nome da empresa, mas pega código no fundo
selecionadas_nomes = st.multiselect("Selecione as ações:", list(mapa_empresas.keys()), default=["Petrobras PN"])
selecionadas_codigos = [mapa_empresas[nome] for nome in selecionadas_nomes]

# Se há ações selecionadas
if selecionadas_codigos:
    # Baixa os dados das ações
    dados = carregar_dados(selecionadas_codigos)

    # Se for apenas uma ação, mostra o gráfico de linha dessa única ação
    if len(selecionadas_codigos) == 1:
        if isinstance(dados, pd.Series):
            dados = dados.to_frame()
            dados.columns = [selecionadas_nomes[0]]  # Nome da coluna como o nome da ação
        st.subheader(f"Gráfico de {selecionadas_nomes[0]}")
        st.line_chart(dados)
        st.dataframe(dados.tail())
    
    # Se houver mais de uma ação, mostra o gráfico comparativo
    elif len(selecionadas_codigos) > 1:
        st.subheader("Comparação entre as ações selecionadas")
        st.line_chart(dados)
        st.dataframe(dados.tail())
else:
    st.info("Por favor, selecione pelo menos uma ação.")
