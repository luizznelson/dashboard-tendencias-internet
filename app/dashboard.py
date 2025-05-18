import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Tendências de Consumo de Internet", layout="centered")

# Carrega dados
df = pd.read_csv("data/internet_usage.csv", parse_dates=["data"])
df['mm_7d'] = df['consumo_mb'].rolling(7).mean()
df['dias'] = (df['data'] - df['data'].min()).dt.days

# Modelo linear
model = LinearRegression().fit(df[['dias']], df['consumo_mb'])
df['tendencia_linear'] = model.predict(df[['dias']])

st.title("📊 Dashboard de Tendências de Uso de Internet")

st.write("""
## Evolução do Consumo Diário de Internet

Este gráfico apresenta o consumo diário de internet (linha azul clara) ao longo do ano, destacando as principais tendências e padrões de uso.

- **Consumo Diário:** Linha azul clara, mostra o valor registrado de consumo em cada dia, evidenciando as variações naturais e possíveis picos de uso.
- **Média Móvel (7 dias):** Linha vermelha, suaviza as oscilações diárias e ajuda a identificar padrões semanais e períodos de maior estabilidade ou crescimento.
- **Tendência Linear:** Linha verde, indica a direção geral do consumo ao longo do tempo, baseada em uma regressão simples.

Juntos, esses elementos permitem identificar comportamentos sazonais, eventos fora do padrão e o crescimento contínuo do consumo de internet ao longo do ano.
""")

st.subheader("Consumo Diário, Média Móvel e Tendência Linear")
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(df['data'], df['consumo_mb'], alpha=0.4, label='Consumo Diário', color='skyblue')
ax.plot(df['data'], df['mm_7d'], color='red', label='Média Móvel (7 dias)')
ax.plot(df['data'], df['tendencia_linear'], color='green', label='Tendência Linear')
ax.set_xlabel("Data")
ax.set_ylabel("Consumo (MB)")
ax.legend()
st.pyplot(fig)

st.write("""
---
## Estatísticas Gerais do Consumo

Esta tabela resume as principais estatísticas descritivas do consumo diário de internet no período analisado:

- **Média (mean):** Valor médio de consumo ao longo do ano, indicando o uso típico diário.
- **Mínimo e Máximo (min/max):** Mostram os menores e maiores valores registrados, úteis para identificar extremos.
- **Desvio Padrão (std):** Mede o quanto os valores de consumo variam em relação à média; quanto maior, maior a variabilidade do consumo diário.
- **Quartis (25%, 50%, 75%):** Apresentam a distribuição dos dados, indicando como o consumo se concentra ao longo do período.

Estas estatísticas ajudam a entender o perfil de consumo, identificar possíveis anomalias e fornecer uma visão geral dos dados, servindo como base para análises e decisões futuras.
""")

st.subheader("Estatísticas Gerais")
st.write(df[['consumo_mb', 'mm_7d', 'dias', 'tendencia_linear']].describe())

st.write("""
---
## Projeção Linear de Consumo para os Próximos 30 Dias

Este gráfico mostra uma projeção do consumo de internet para os próximos 30 dias, baseada na tendência linear identificada nos dados históricos.

- **Histórico:** Linha azul clara, mostra o histórico de consumo até o presente.
- **Projeção Linear:** Linha laranja, apresenta a estimativa de consumo futuro, assumindo que a tendência observada será mantida.

Esta previsão é útil para planejamento de capacidade, identificação de possíveis gargalos e para apoiar decisões estratégicas sobre a infraestrutura de internet, garantindo que a empresa esteja preparada para atender ao crescimento da demanda.
""")

st.subheader("Projeção Linear para os próximos 30 dias")
future_days = pd.DataFrame({
    "dias": range(df['dias'].max()+1, df['dias'].max()+31),
})
future_days['consumo_proj'] = model.predict(future_days[['dias']])
future_days['data'] = df['data'].max() + pd.to_timedelta(future_days['dias'] - df['dias'].max(), unit="D")

fig2, ax2 = plt.subplots(figsize=(10,3))
ax2.plot(df['data'], df['consumo_mb'], alpha=0.3, label="Histórico", color='skyblue')
ax2.plot(future_days['data'], future_days['consumo_proj'], color='orange', label="Projeção Linear")
ax2.set_xlabel("Data")
ax2.set_ylabel("Consumo (MB)")
ax2.legend()
st.pyplot(fig2)
