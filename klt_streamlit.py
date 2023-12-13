import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

def millions_formatter(x, pos):
    return f'{x / 1e6}M'

st.markdown("<h3 style='text-align: center;'>Nouvelle Prod : Comparaison Prédiction (Jour) et Réel (Mois)</h3> <br>", unsafe_allow_html=True)

df = pd.read_csv('Pred Nvle Prod.csv')

df['date'] = pd.to_datetime(df['PERJOU'])
df['mois'] = df['date'].dt.to_period('M').astype(str)

mois_disponibles = sorted(df['mois'].unique())
mois_selectionnes = st.sidebar.multiselect('Sélectionnez les mois', mois_disponibles, default=[])

if mois_selectionnes:
    df_filtre = df[df['mois'].isin(mois_selectionnes)]
else:
    df_filtre = df 

fig, ax = plt.subplots()
ax.plot(df_filtre['date'], df_filtre['REEL_NPROD'], label='Prod Réelle', color='darkblue')
ax.plot(df_filtre['date'], df_filtre['PRED_NPROD'], label='Prédiction', color='coral')
ax.set_xlabel('Date')
ax.set_ylabel('Nouvelle Prod (en Millions)')
#ax.set_title('Nouvelle Prod Réelle et Prédite')

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

ax.yaxis.set_major_formatter(FuncFormatter(millions_formatter))

plt.setp(ax.get_xticklabels(), rotation=45, ha='right') 

ax.legend()
st.pyplot(fig)
