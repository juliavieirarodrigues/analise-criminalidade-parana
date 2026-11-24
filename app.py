import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da Página do Dashboard
st.set_page_config(
    page_title="Dashboard Analítico - Criminalidade no Paraná",
    page_icon="📈",
    layout="wide"
)

# Carregamento e Tratamento dos Dados (ETL)
@st.cache_data
def carregar_e_tratar_dados():
    caminho = "Crimes_Tabela.csv"
    raw = pd.read_csv(caminho, encoding="utf-16", sep=None, engine="python")
    
    colunas = list(raw.iloc[0])
    colunas[0] = "municipio"
    colunas[1] = "regiao"
    
    df = raw.iloc[2:].copy().reset_index(drop=True)
    df.columns = colunas
    
    df_municipios = df[df["municipio"] != "Estado do Paraná"].copy().reset_index(drop=True)
    df_municipios = df_municipios.drop_duplicates()
    
    colunas_crimes = [c for c in df_municipios.columns if c not in ["municipio", "regiao"]]
    
    for col in colunas_crimes:
        df_municipios[col] = df_municipios[col].replace("-", "0")
        df_municipios[col] = df_municipios[col].astype(str).str.replace(".", "", regex=False)
        df_municipios[col] = pd.to_numeric(df_municipios[col], errors="coerce").fillna(0).astype(int)
        
    df_municipios["municipio"] = df_municipios["municipio"].astype(str).str.strip()
    df_municipios["regiao"] = df_municipios["regiao"].astype(str).str.strip()
    
    def padronizar_nome(col):
        return (
            col.lower()
            .replace(" ", "_")
            .replace("/", "_")
            .replace("ç", "c")
            .replace("ã", "a")
            .replace("õ", "o")
            .replace("á", "a")
            .replace("é", "e")
            .replace("í", "i")
        )
        
    df_municipios.columns = [padronizar_nome(c) for c in df_municipios.columns]
    
    colunas_crimes_padronizadas = [c for c in df_municipios.columns if c not in ["municipio", "regiao"]]
    
    df_long = pd.melt(
        df_municipios,
        id_vars=["municipio", "regiao"],
        value_vars=colunas_crimes_padronizadas,
        var_name="tipo_crime",
        value_name="quantidade"
    )
    
    return df_municipios, df_long, colunas_crimes_padronizadas

df_municipios, df_long, colunas_crimes = carregar_e_tratar_dados()

# Título na Página Web
st.title("Análise de Dados: Crimes no Paraná")
st.markdown("Fonte: Portal de Dados Abertos do Paraná")

st.markdown("---")

# Hipótese 1 - Gráfico de Dispersão Melhorado
st.header("Efeito Dominó da Criminalidade")
st.markdown("Municípios com maior apreensão de armas de fogo e ocorrências de tráfico de drogas apresentam taxas mais elevadas de crimes violentos e lesão corporal.")

df_f_mun = df_municipios.copy()

# Garantindo compatibilidade com o nome da coluna sem acentos gerada pelo padronizador
col_trafico = "ocorrencias_envolvendo_trafico_de_drogas" if "ocorrencias_envolvendo_trafico_de_drogas" in df_f_mun.columns else [c for c in df_f_mun.columns if "trafico" in c][0]

df_f_mun["preditores_h1"] = df_f_mun["armas_de_fogo_apreendidas"] + df_f_mun[col_trafico]
df_f_mun["violentos_h1"] = df_f_mun["crimes_de_lesao_corporal"] + df_f_mun["crimes_de_roubo"] + df_f_mun["roubos_de_veiculos"] + df_f_mun["crimes_de_estupro"]

fig_h1 = px.scatter(
    df_f_mun,
    x="preditores_h1",
    y="violentos_h1",
    hover_name="municipio",
    color="regiao",
    title="Armas/Drogas (Eixo X) VS Crimes Violentos/Lesão (Eixo Y)",
    trendline="ols",
    labels={
        "preditores_h1": "Soma de Armas Apreendidas e Tráfico de Drogas",
        "violentos_h1": "Soma de Crimes Violentos e Lesão Corporal",
        "regiao": "Região Geográfica"
    }
)

fig_h1.update_layout(
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
)

st.plotly_chart(fig_h1, use_container_width=True)

st.markdown("---")

# Hipótese 2
st.header("Volume de Infrações de Convivência VS Crimes Graves")
subset_h2_conv = df_long[df_long["tipo_crime"].isin(["perturbacao_do_sossego_tranquilidade", "crimes_de_ameaca"])]["quantidade"].sum()
subset_h2_graves = df_long[df_long["tipo_crime"].isin(["crimes_de_roubo", "roubos_de_veiculos", "crimes_de_estupro"])]["quantidade"].sum()

col_kpi1, col_kpi2 = st.columns(2)
col_kpi1.metric("Total: Convivência e Ameaça (Sossego + Ameaça)", f"{subset_h2_conv:,.0f}".replace(",", "."))
col_kpi2.metric("Total: Delitos Graves (Roubos + Estupro)", f"{subset_h2_graves:,.0f}".replace(",", "."))

df_h2_comp = pd.DataFrame({
    "Categoria de Delito": ["Convivência e Menor Potencial (Sossego/Ameaça)", "Crimes Graves (Roubos/Estupro)"],
    "Total de Ocorrências": [subset_h2_conv, subset_h2_graves]
})

fig_h2 = px.bar(
    df_h2_comp,
    x="Categoria de Delito",
    y="Total de Ocorrências",
    color="Categoria de Delito",
    title="Infrações leves e de convivência superam em muito os crimes graves em quase todo o estado.",
    text_auto=True,
    color_discrete_sequence=["#2b5c8f", "#d9534f"]
)
st.plotly_chart(fig_h2, use_container_width=True)