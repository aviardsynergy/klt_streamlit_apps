import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Pred Nvle Prod.csv')

df['date'] = pd.to_datetime(df['PERJOU'])
df['mois'] = df['date'].dt.to_period('M').astype(str)

mois_disponibles = df['mois'].unique()
mois_selectionnes = st.sidebar.multiselect('Sélectionnez les mois', mois_disponibles, default=[])

if mois_selectionnes:
    df_filtre = df[df['mois'].isin(mois_selectionnes)]
else:
    df_filtre = df 

fig, ax = plt.subplots()
ax.plot(df_filtre['date'], df_filtre['REEL_NPROD'], label='N Prod')
ax.plot(df_filtre['date'], df_filtre['PRED_NPROD'], label='Pred NProd')
ax.set_xlabel('Date')
ax.set_ylabel('Nouvelle Prod')
ax.set_title('Nouvelle Prod Réelle et Prédite')

ax.set_xticklabels(ax.get_xticks(), rotation=45)
ax.legend()
st.pyplot(fig)
