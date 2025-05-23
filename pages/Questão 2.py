import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, create_bad_column, plot_boxplot, plot_correlation_matrix, plot_scatter, plot_seaborn_histogram, analyze_categorical_features
import numpy as np
import pandas as pd

st.set_page_config(layout='wide')
st.title("Questão 2: Contratos Bons vs Ruins")

# Load data
df = load_data()
df, df_bad, df_good = create_bad_column(df)

# Container for Good vs Bad Comparison
with st.container():
    st.markdown("## Comparação: Contratos Bons vs Ruins")
    
    numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    numerical_columns.remove('Bad')
    
    good_stats = df_good[numerical_columns].describe().round(2)
    bad_stats = df_bad[numerical_columns].describe().round(2)
    
    # Plot percentage differences in means
    st.markdown("### Diferença Percentual nas Médias (Bom - Mau)")
    mean_diff = good_stats.loc['mean'] - bad_stats.loc['mean']
    percent_diff = mean_diff / bad_stats.loc['mean'] * 100
    percent_diff = percent_diff.replace([np.inf, -np.inf], 0) 
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=percent_diff.index,
            y=percent_diff.values,
            marker_color=['#00CC96' if x >= 0 else '#FF5733' for x in percent_diff.values],
            text=[f"{x:.2f}%" for x in percent_diff.values],
            textposition='auto'
        )
    )
    fig.update_layout(
        title="Diferença Percentual nas Médias entre Contratos Bons e Ruins",
        xaxis_title="Variáveis",
        yaxis_title="Diferença Percentual (Média Bom - Média Mau) / Média Mau",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# Container para Análise Numérica
with st.container():
    st.markdown("## Análise Numérica")
    numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    numerical_columns.remove('Bad')
    selected_numerical = st.multiselect("Selecione as variáveis numéricas para análise", numerical_columns, default=numerical_columns)

    # Histogramas em colunas
    st.markdown("### Histogramas")
    cols = st.columns(3)
    for i, col in enumerate(selected_numerical):
        with cols[i % 3]:
            plot_seaborn_histogram(df, col, 'Bad', f"Distribuição de {col} por Bad")

    # Boxplots
    st.markdown("### Boxplots")
    cols = st.columns(3)
    for i, col in enumerate(selected_numerical):
        with cols[i % 3]:
            plot_boxplot(df, 'Bad', col, f"Boxplot de {col} por Bad")

    # Scatter Plots
    st.markdown("### Scatter Plots para Bad")
    plot_scatter(df, 'Bad', selected_numerical)

# Container para Análise Categórica
with st.container():
    st.markdown("## Análise Categórica")
    analyze_categorical_features(df, ['estado', 'setor', 'regiao'], 'Bad')

st.markdown("""# Análise de Crédito: Perfil de Bons vs Maus Pagadores

## 📊 Análise Numérica (Variáveis Quantitativas)

**Principais diferenciadores identificados:**

Como a variável `Bad` representa maus pagadores — definidos como clientes com atraso no pagamento —, algumas correlações, como **valor em aberto** e **atraso atual**, são triviais. Esses dados são coletados **após** a concessão do crédito e, portanto, não são úteis para análise preditiva.

Nos gráficos de **boxplot**, **histograma** e **scatterplot**, é possível observar que os maus pagadores tendem a apresentar:

- **Score de crédito mais baixo**
- **Maior faturamento declarado**
- **Taxas mais elevadas**
- **Maior dívida**

A análise sugere que, apesar de apresentarem maior faturamento, esses clientes podem ter um perfil de risco elevado, reforçando a importância de considerar múltiplas variáveis na decisão de crédito.

## 📌 Panorama Geral
**Distribuição Global:**
- ✅ **Bons Pagadores (Bad=0):** 1.424 clientes (73.97%)
- ❌ **Maus Pagadores (Bad=1):** 501 clientes (26.03%)

*Inadimplência média global:* 26.03%

## Análise por Estado

### 🔴 Estados de Alto Risco (Inadimplência > Média Global)
| Estado | % Mau Pagador | Destaque |
|--------|--------------|----------|
| TO | 46.15% | **Maior risco** |
| MS | 44.44% | |
| RO | 44.44% | |
| GO | 37.18% | |
| MG | 35.17% | **Maior volume (51 casos)** |
| SC | 31.51% | |

### 🟢 Estados Exemplares (Inadimplência < 20%)
| Estado | % Mau Pagador | Destaque |
|--------|--------------|----------|
| AC | 0.00% | Perfeito |
| RR | 0.00% | Perfeito |
| SE | 12.50% | |
| PB | 14.29% | |
| CE | 16.67% | |

## Análise por Setor Econômico

### 🔴 Setores Problemáticos
| Setor | % Mau Pagador | Destaque |
|-------|--------------|----------|
| Serviços de Alojamento/Alimentação | 35.59% | **Alerta máximo** |
| Indústria da Construção | 34.04% | |
| Atacado | 30.30% | |
| Bens de Consumo | 30.68% | |

### 🟢 Setores Estáveis
| Setor | % Mau Pagador | Destaque |
|-------|--------------|----------|
| Telecomunicações | 8.70% | **Melhor desempenho** |
| Serviços de Saúde | 14.71% | |
| Eletroeletrônicos | 0.00% | Perfeito |
| Energia | 0.00% | Perfeito |

## Análise por Região
| Região | % Mau Pagador | Comparativo |
|--------|--------------|-------------|
| Centro-Oeste | 32.07% | **Acima da média** |
| Sudeste | 26.21% | Na média |
| Nordeste | 24.05% | |
| Sul | 24.40% | |
| Norte | 24.03% | |""")

# Container para Loss
with st.container():
    st.markdown("## Análise de Loss")
    df['Loss'] = df['valor_em_aberto'] / df['valor_contrato_mais_juros']
    df['Loss_cat'] = pd.cut(df['Loss'], bins=[0, 0.2, float('inf')], labels=[0, 1], include_lowest=True).astype(int)

    st.markdown("### Matriz de Correlação")
    fig_corr = plot_correlation_matrix(df, "Matriz de Correlação")
    st.plotly_chart(fig_corr)

    st.markdown("### Histogramas para Loss_cat")
    cols = st.columns(3)
    for i, col in enumerate(selected_numerical):
        with cols[i % 3]:
            plot_seaborn_histogram(df.round(2), col, 'Loss_cat', f"Distribuição de {col} por Loss_cat")

    st.markdown("### Boxplots para Loss_cat")
    cols = st.columns(3)
    for i, col in enumerate(selected_numerical):
        with cols[i % 3]:
            plot_boxplot(df, 'Loss_cat', col, f"Boxplot de {col} por Loss_cat")

    st.markdown("### Scatter Plots para Loss")
    plot_scatter(df, 'Loss', selected_numerical)

    st.markdown("### Análise Categórica para Loss_cat")
    analyze_categorical_features(df, ['estado', 'setor', 'regiao'], 'Loss_cat')

st.markdown("""
### Após as análises, podemos concluir que as métricas para bons e maus pagadores com Loss e Bad são bem parecidas, inclusive, ao separar o loss na categoria de <20% e >20%, temos uma distribuição bem parecida com a do Bad, uma vez que Bad e Loss estão fortemente relacionados.
""")