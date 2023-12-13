import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

# Chargement des données
df = pd.read_csv('chemin_de_votre_fichier.csv')
df['date'] = pd.to_datetime(df['date'])
df['mois'] = df['date'].dt.strftime('%Y-%m')  # Formatage en chaîne de caractères pour une meilleure cohérence

# Tri des mois disponibles en ordre croissant avant de les passer au multiselect
all_months = sorted(df['mois'].unique())

# Widget multiselect dans la barre latérale avec tous les mois disponibles
mois_selectionnes = st.sidebar.multiselect('Sélectionnez les mois', all_months, default=all_months)

# Filtrer les données en fonction de la sélection
df_filtre = df[df['mois'].isin(mois_selectionnes)] if mois_selectionnes else df

# Graphique ligne
fig, ax = plt.subplots()
ax.plot(df_filtre['date'], df_filtre['REEL_NPROD'], label='CA Réel (REEL_NPROD)', color='darkblue')
ax.plot(df_filtre['date'], df_filtre['PRED_NPROD'], label='CA Estimé (PRED_NPROD)', color='orange')
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x / 1e6:.1f}M'))
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_xlabel('Date')
ax.set_ylabel('Valeurs (en Millions)')
ax.set_title('Nouvelle Prod Réelle et Prédite')
ax.legend()
st.pyplot(fig)

# Préparation des données pour le graphique radar
categories = all_months  # Utilisez all_months ici pour vous assurer que tous sont inclus
N = len(categories)

# Vérification de la présence de données avant de créer le graphique radar
if N > 0:
    # Calcul des valeurs moyennes pour chaque mois
    avg_reel = df.groupby('mois')['REEL_NPROD'].mean().reindex(all_months, fill_value=0)
    avg_pred = df.groupby('mois')['PRED_NPROD'].mean().reindex(all_months, fill_value=0)

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
else:
    st.write("Aucun mois sélectionné ou aucune donnée disponible pour les mois sélectionnés.")
