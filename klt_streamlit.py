import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from math import pi


def millions_formatter(x, pos):
    return f'{x / 1e6}M'

st.markdown("<h3 style='text-align: center;'>Nouvelle Prod : Comparaison Prédiction (Jour) et Réel (Mois)</h3> <br>", unsafe_allow_html=True)

df = pd.read_csv('Pred Nvle Prod.csv')

df['date'] = pd.to_datetime(df['PERJOU'])
df['mois'] = df['date'].dt.to_period('M').astype(str)
df['jour'] = df['date'].dt.strftime('%Y-%m-%d')

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




categories = df_filtre['mois'].unique()
N = len(categories)

if N > 0:
    try:
        # Calcul des valeurs moyennes pour chaque mois
        avg_reel = df_filtre.groupby('mois')['REEL_NPROD'].mean().reindex(categories, fill_value=0)
        avg_pred = df_filtre.groupby('jour')['PRED_NPROD'].mean().reindex(categories, fill_value=0)

        # Préparation des angles pour le graphique radar
        angles = np.linspace(0, 2 * pi, N, endpoint=False).tolist()
        angles += angles[:1]  # Fermeture du cercle

        # Création du graphique radar
        radar_fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        ax.plot(angles, avg_reel.tolist() + avg_reel.tolist()[:1], linewidth=2, linestyle='solid', label='REEL_NPROD')
        ax.plot(angles, avg_pred.tolist() + avg_pred.tolist()[:1], linewidth=2, linestyle='solid', label='PRED_NPROD')
        ax.set_thetagrids(np.degrees(angles[:-1]), categories)
        ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

        st.pyplot(radar_fig)
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de la création du graphique radar: {e}")
else:
    st.write("Aucun mois sélectionné ou aucune donnée disponible pour les mois sélectionnés.")
