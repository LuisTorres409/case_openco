import streamlit as st
from utils import load_data, calculate_metrics

st.title("Questão 1: Métricas Gerais")

df = load_data()
ticket_medio, taxa_media, prazo_medio = calculate_metrics(df)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Ticket Médio", value=f"R$ {ticket_medio:,.2f}")
with col2:
    st.metric(label="Taxa Média", value=f"{taxa_media:.4f}%")
with col3:
    st.metric(label="Prazo Médio", value=f"{prazo_medio:.2f} anos")
