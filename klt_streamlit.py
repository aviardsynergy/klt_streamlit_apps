import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Pred Nvle Prod.csv')

df['date'] = pd.to_datetime(df['PERJOU'])
df['mois'] = df['date'].dt.to_period('M')

mois_choisi = st.sidebar.selectbox('Choisissez un mois', df['mois'].unique())

df_filtre = df[df['mois'] == mois_choisi]

fig, ax = plt.subplots()
ax.plot(df_filtre['date'], df_filtre['REEL_NPROD'], label='N Prod')
ax.plot(df_filtre['date'], df_filtre['PRED_NPROD'], label='Pred NProd')
ax.set_xlabel('Date')
ax.set_ylabel('Nouvelle Prod')
ax.set_title(f'Nouvelle Prod Réelle et Prédite pour {mois_choisi}')
ax.legend()

st.pyplot(fig)
