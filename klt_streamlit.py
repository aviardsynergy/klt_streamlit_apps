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



# Fonction pour créer le graphique radar
def create_radar_chart(df_filtre, categories):
    N = len(categories)

    # Assurez-vous que le nombre de valeurs correspond au nombre de catégories
    # Exemple: calcul de trois valeurs différentes pour les trois catégories
    values = [df_filtre['REEL_NPROD'].sum(), df_filtre['PRED_NPROD'].mean(), df_filtre['REEL_NPROD'].max()]
    
    # Fermer le cercle
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist() + [0]
    
    radar_fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.set_thetagrids(np.degrees(angles), categories)

    return radar_fig

# Catégories pour le graphique radar (à adapter selon vos besoins)
categories = ['Total CA Réel', 'Moyenne CA Prévu', 'Max CA Réel']

# Création du graphique radar
radar_fig = create_radar_chart(df_filtre, categories)

# Affichage du graphique radar dans Streamlit
st.pyplot(radar_fig)
