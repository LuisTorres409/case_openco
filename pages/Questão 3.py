import streamlit as st
from utils import load_data, create_new_features, plot_seaborn_histogram, plot_boxplot, plot_scatter,create_bad_column
import pandas as pd

st.set_page_config(layout="wide")
st.title("Questão 3: Novas Métricas")

df = load_data()
df, df_bad, df_good = create_bad_column(df)
df['Loss'] = df['valor_em_aberto'] / df['valor_contrato_mais_juros']
df['Loss_cat'] = pd.cut(df['Loss'], bins=[0, 0.2, float('inf')], labels=[0, 1], include_lowest=True).astype(int)

st.markdown("""
# Novas Métricas para Análise de Crédito

Para criarmos novas métricas, podemos observar que qualquer tipo de **score que levar em consideração o atraso ou o valor atrasado** será extremamente correlacionado com **Bad** e **Loss**, uma vez que essas variáveis são intimamente ligadas. 

Por isso, irei tentar encontrar métricas que, assim como o score, possam ser avaliadas **no momento da concessão do crédito**.

---

### Exemplos de Métricas Propostas:

- **Razão Valor_contrato / Faturamento:**  
Essa métrica avalia o quanto o valor do contrato é relevante em relação ao faturamento declarado da empresa. Dessa forma, podemos estimar o impacto do contrato e de eventual inadimplência para a empresa.

- **Razão valor_aberto / prazo** e **Razão atraso / prazo:**  
Ambas as métricas têm o objetivo de mostrar que qualquer métrica que considere **valor** e **atraso** tende a performar bem na análise.

---
""")
new_metrics_df = create_new_features(df)

new_cols = ['ratio_contrato_faturamento','score','ratio_valor_prazo','ratio_atraso_prazo','ratio_contrato_faturamento_cat','score_cat']

st.markdown("### Histogramas para Novas Métricas por Bad")
cols = st.columns(3)
for i, col in enumerate(new_cols):
    with cols[i % 3]:
        plot_seaborn_histogram(new_metrics_df, col, 'Bad', f"Distribuição de {col} por Bad")

st.markdown("### Scatter Plots para Novas Métricas por Bad")
plot_scatter(new_metrics_df,'Bad',new_cols)

st.markdown("### Histogramas para Novas Métricas por Loss categórico")
cols = st.columns(3)
for i, col in enumerate(new_cols):
    with cols[i % 3]:
        plot_seaborn_histogram(new_metrics_df, col, 'Loss_cat', f"Distribuição de {col} por Loss")

st.markdown("### Scatter Plots para Novas Métricas por Loss")
plot_scatter(new_metrics_df,'Loss',new_cols)

st.markdown("""
## Conclusões

Conforme mencionado anteriormente, métricas baseadas em atraso e valor devido apresentam bons resultados e alta correlação tanto com a variável **Bad** quanto com **Loss**. 
A métrica que utiliza a razão entre o valor do contrato e o faturamento se aproxima do desempenho do score tradicional, conseguindo separar razoavelmente bem bons e maus pagadores.
Essa abordagem reforça a importância de criar métricas que capturem características financeiras relevantes no momento da concessão do crédito, possibilitando uma análise mais eficaz e antecipada do risco.
""")
