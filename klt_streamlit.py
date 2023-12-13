import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import altair as alt



def millions_formatter(x, pos):
    return f'{x / 1e6}M'

st.markdown("<h3 style='text-align: center;'>Nouvelle Prod : Comparaison Prédiction (Jour) et Réel (Mois)</h3> <br>", unsafe_allow_html=True)

df = pd.read_csv('Pred Nvle Prod.csv')

df['date'] = pd.to_datetime(df['PERJOU'])
df['mois'] = df['date'].dt.to_period('M').astype(str)

mois_disponibles = sorted(df['mois'].unique())
mois_selectionnes = st.sidebar.multiselect('Sélectionnez les mois', mois_disponibles, default=[])

df_filtre = df[df['mois'].isin(mois_selectionnes)] if mois_selectionnes else df
#if mois_selectionnes:
 #   df_filtre = df[df['mois'].isin(mois_selectionnes)]
#else:
 #   df_filtre = df 

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

df['REEL_NPROD'] = df['REEL_NPROD'] / 1e6
df['PRED_NPROD'] = df['PRED_NPROD'] / 1e6


line_chart = alt.Chart(df_filtre).mark_line().encode(
    x='date:T',  # Format de date pour l'axe des abscisses
    y=alt.Y('REEL_NPROD:Q', title='CA Réel (Millions €)'),  # Quantitative scale
    color=alt.value('blue'),  # Couleur de la première série
    tooltip=['date:T', alt.Tooltip('REEL_NPROD:Q', title='CA Réel', format='.2f')]  # Tooltip pour la date et la valeur
).properties(
    width=800,
    height=400
) + alt.Chart(df_filtre).mark_line().encode(
    x='date:T',  # Format de date pour l'axe des abscisses
    y=alt.Y('PRED_NPROD:Q', title='CA Prévu (Millions €)'),  # Quantitative scale
    color=alt.value('orange'),  # Couleur de la seconde série
    tooltip=['date:T', alt.Tooltip('PRED_NPROD:Q', title='CA Prévu', format='.2f')]  # Tooltip pour la date et la valeur
)

st.altair_chart(line_chart, use_container_width=True)
