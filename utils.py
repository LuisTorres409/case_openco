import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from typing import List

@st.cache_data
def load_data() -> pd.DataFrame:
    """
    Carrega os dados da planilha Excel e remove a coluna 'id'.

    Retorna:
    - pd.DataFrame: DataFrame com os dados carregados.
    """
    df: pd.DataFrame = pd.read_excel('data/Case Open.xlsx', sheet_name='Base')
    df.drop('id', axis=1, inplace=True)
    return df

# Questão 1: Métricas Gerais
def calculate_metrics(df: pd.DataFrame) -> tuple[float, float, float]:
    """
    Calcula métricas gerais de crédito.

    Parâmetros:
    - df (pd.DataFrame): DataFrame com colunas 'valor_contrato', 'taxa' e 'prazo'.

    Retorna:
    - ticket_medio (float): Média dos valores de contrato.
    - taxa_media (float): Taxa média ponderada pelo valor do contrato.
    - prazo_medio (float): Prazo médio ponderado pelo valor do contrato.
    """
    ticket_medio: float = df['valor_contrato'].mean()
    taxa_media: float = (df['taxa'] * df['valor_contrato']).sum() / df['valor_contrato'].sum()
    prazo_medio: float = (df['prazo'] * df['valor_contrato']).sum() / df['valor_contrato'].sum()
    return ticket_medio, taxa_media, prazo_medio

# Questão 2: BAD e Loss
def create_bad_column(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Cria a coluna 'Bad' indicando maus pagadores e separa DataFrames de bons e maus.

    Parâmetros:
    - df (pd.DataFrame): DataFrame original com coluna 'atraso_corrente'.

    Retorna:
    - df (pd.DataFrame): DataFrame original com coluna 'Bad'.
    - df_bad (pd.DataFrame): Subset com Bad == 1.
    - df_good (pd.DataFrame): Subset com Bad == 0.
    """
    df['Bad'] = (df['atraso_corrente'] > 180).astype(int)
    df_bad: pd.DataFrame = df[df['Bad'] == 1].reset_index(drop=True)
    df_good: pd.DataFrame = df[df['Bad'] == 0].reset_index(drop=True)
    return df, df_bad, df_good


def create_loss_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria as colunas 'Loss' e 'Loss_cat' para análise de perda.

    Parâmetros:
    - df (pd.DataFrame): DataFrame com colunas 'valor_em_aberto' e 'valor_contrato_mais_juros'.

    Retorna:
    - pd.DataFrame: DataFrame com colunas 'Loss' e 'Loss_cat'.
    """
    df['Loss'] = df['valor_em_aberto'] / df['valor_contrato_mais_juros']
    df['Loss_cat'] = pd.cut(
        df['Loss'], bins=[0, 0.2, float('inf')], labels=[0, 1], include_lowest=True
    ).astype(int)
    return df

# Funções de plotagem reutilizáveis
def plot_seaborn_histogram(
    df: pd.DataFrame,
    x: str,
    hue: str,
    title: str
) -> None:
    """
    Plota histograma com Seaborn para uma coluna numérica, agrupando por categoria.

    Parâmetros:
    - df (pd.DataFrame): DataFrame com os dados.
    - x (str): Coluna numérica a ser plotada.
    - hue (str): Coluna categórica usada como 'hue'.
    - title (str): Título do gráfico.
    """
    df_hist = df.copy().round(2)
    plt.figure(figsize=(6, 4))
    sns.histplot(
        data=df_hist, x=x, hue=hue, kde=True,
        element="step", common_norm=False, stat='density'
    )
    plt.title(title, fontsize=10)
    plt.xlabel(x, fontsize=8)
    plt.ylabel("Densidade", fontsize=8)
    st.pyplot(plt)
    plt.clf()


def plot_boxplot(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str
) -> None:
    """
    Plota boxplot de coluna numérica por categoria.

    Parâmetros:
    - df (pd.DataFrame): DataFrame com os dados.
    - x (str): Coluna categórica no eixo X.
    - y (str): Coluna numérica no eixo Y.
    - title (str): Título do gráfico.
    """
    plt.figure(figsize=(6, 4))
    sns.boxplot(data=df, x=x, y=y)
    plt.title(title, fontsize=10)
    st.pyplot(plt)
    plt.clf()


def plot_scatter(
    df: pd.DataFrame,
    base: str,
    features: list[str]
) -> None:
    """
    Plota scatter plots com linha de tendência para múltiplas features.

    Parâmetros:
    - df (pd.DataFrame): DataFrame com os dados.
    - base (str): Coluna do eixo Y.
    - features (list[str]): Lista de colunas do eixo X.
    """
    plt.figure(figsize=(20, 15))
    for i, feat in enumerate(features):
        plt.subplot(4, 4, i + 1)
        sns.scatterplot(data=df, x=feat, y=base, alpha=0.6)
        sns.regplot(data=df, x=feat, y=base, scatter=False, color='red')
        plt.title(f'{base} vs {feat}')
        plt.xlabel(feat)
        plt.ylabel(base)
    plt.tight_layout()
    st.pyplot(plt)
    plt.clf()


def plot_correlation_matrix(
    df: pd.DataFrame,
    title: str
) -> None:
    """
    Gera matriz de correlação interativa com Plotly.

    Parâmetros:
    - df (pd.DataFrame): DataFrame com os dados.
    - title (str): Título da figura.

    Retorna:
    - plotly.graph_objects.Figure: Figura da matriz de correlação.
    """
    corr = df.select_dtypes(include=[np.number]).corr()
    fig = px.imshow(corr, text_auto=True, aspect='auto', title=title)
    return fig

# Questão 3: Novas Métricas
def create_new_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria novas métricas para análise de crédito disponiveis no momento da concessão.

    Parâmetros:
    - df (pd.DataFrame): DataFrame original com colunas necessárias.

    Retorna:
    - pd.DataFrame: DataFrame com métricas 'ratio_contrato_faturamento',
      'ratio_valor_prazo' e 'ratio_atraso_prazo'.
    """
    df_new = df.copy()
    df_new['ratio_contrato_faturamento'] = df_new['valor_contrato_mais_juros'] / df_new['faturamento_informado']
    df_new['ratio_contrato_faturamento_cat'] = pd.cut(df_new['ratio_contrato_faturamento'], bins=[0,0.25,float('inf')], labels=[0,1],include_lowest=True).astype(int)
    df_new['ratio_valor_prazo'] = df_new['valor_em_aberto'] / df_new['prazo']
    df_new['ratio_atraso_prazo'] = df_new['atraso_corrente'] / df_new['prazo']
    df_new['score_cat'] = pd.cut(df_new['score'], bins=[0,400,float('inf')], labels=[0,1],include_lowest=True).astype(int)
    return df_new.fillna(0)


def analyze_categorical_features(
    df: pd.DataFrame,
    categorical_columns: List[str],
    class_column: str = 'Bad'
) -> None:
    """
    Realiza análise exploratória para múltiplas variáveis categóricas em relação a uma variável de classe binária.

    Para cada variável categórica:
    - Exibe totais globais e percentuais da classe alvo
    - Mostra tabelas de frequência absoluta, proporções internas (por categoria) e proporções globais
    - Destaca categorias com risco (classe 1) e desempenho (classe 0) acima da média global + 10%
    - Plota gráfico de barras empilhadas da proporção interna usando Plotly e exibe no Streamlit

    Parâmetros:
    -----------
    df : pd.DataFrame
        DataFrame contendo os dados.
    categorical_columns : List[str]
        Lista de colunas categóricas a serem analisadas.
    class_column : str, default='Bad'
        Nome da coluna da variável binária alvo (ex: 0 = bom pagador, 1 = mau pagador).

    Retorno:
    --------
    None
        Função exibe resultados diretamente no Streamlit.
    """
    df = df.copy()
    if 'regiao' not in df.columns and 'estado' in df.columns:
        df['regiao'] = df['estado'].map({
            'AC': 'Norte', 'AP': 'Norte', 'AM': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
            'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste',
            'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
            'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste',
            'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
            'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul'
        })

    total_classe = df[class_column].value_counts()
    total_classe_percent = df[class_column].value_counts(normalize=True) * 100

    st.markdown("📌 **Totais globais:**")
    st.markdown(f"**Total Bom Pagador ({class_column} = 0):** {total_classe[0]} ({total_classe_percent[0]:.2f}%)  ")
    st.markdown(f"**Total Mau Pagador ({class_column} = 1):** {total_classe[1]} ({total_classe_percent[1]:.2f}%)")

    for col in categorical_columns:
        st.markdown(f"\n📊 **Análise categórica: {col}**")
        freq_abs = df.groupby([col, class_column]).size().unstack(fill_value=0)
        freq_prop_interna = freq_abs.div(freq_abs.sum(axis=1), axis=0) * 100
        freq_prop_global = pd.DataFrame({
            '% Global Bom Pagador': freq_abs[0] / total_classe[0] * 100,
            '% Global Mau Pagador': freq_abs[1] / total_classe[1] * 100
        })

        resumo = freq_abs.copy()
        resumo.columns = ['Total Bom Pagador', 'Total Mau Pagador']
        resumo['% Interno Bom Pagador'] = freq_prop_interna[0]
        resumo['% Interno Mau Pagador'] = freq_prop_interna[1]
        resumo['% Global Bom Pagador'] = freq_prop_global['% Global Bom Pagador']
        resumo['% Global Mau Pagador'] = freq_prop_global['% Global Mau Pagador']

        st.markdown("\n📌 **Resumo por categoria:**")
        st.write(resumo.round(2))

        limite_mau = 1.1 * total_classe_percent[1]
        limite_bom = 1.1 * total_classe_percent[0]
        alto_risco = resumo[resumo['% Interno Mau Pagador'] > limite_mau]
        alto_desempenho = resumo[resumo['% Interno Bom Pagador'] > limite_bom]

        st.markdown(f"\n⚠️ **Categorias com risco acima da média global ({limite_mau:.2f}%):**")
        st.write(alto_risco.round(2))
        st.markdown(f"\n✅ **Categorias com desempenho acima da média global ({limite_bom:.2f}%):**")
        st.write(alto_desempenho.round(2))

        fig = px.bar(freq_prop_interna, barmode='stack', title=f'Proporção (%) de Bom e Mau Pagador por "{col}"')
        st.plotly_chart(fig)
