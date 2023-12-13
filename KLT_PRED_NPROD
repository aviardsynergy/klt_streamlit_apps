import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Pred Nvle Prod.csv')

df['date'] = pd.to_datetime(df['PERJOU'])
df['mois'] = df['date'].dt.to_period('M')

mois_choisi = st.sidebar.selectbox('Choisissez un mois', df['mois'].unique())

df_filtre = df[df['mois'] == mois_choisi]

fig, ax = plt.subplots()
ax.plot(df_filtre['date'], df_filtre['CA_reel'], label='CA Réel')
ax.plot(df_filtre['date'], df_filtre['CA_estime'], label='CA Estimé')
ax.set_xlabel('Date')
ax.set_ylabel('Chiffre d\'Affaires')
ax.set_title(f'CA Réel et Estimé pour {mois_choisi}')
ax.legend()

st.pyplot(fig)
