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

st.markdown('<strong>Janvier à Septembre : </strong> RAS', unsafe_allow_html=True)
st.markdown('<strong>Octobre : </strong> données de prédictions manquantes, le réel est bon. Je vais voir avec Ingrid dans les jours prochains pour rajouter la prédiction', unsafe_allow_html=True)
st.markdown('<strong>Novembre :</strong> RAS', unsafe_allow_html=True)
st.markdown('<strong>Décembre :</strong> Le montant mis en REEL_NPROD est l\'objectif du mois', unsafe_allow_html=True)

import requests
from io import StringIO

csv_url = "https://github.com/aviardsynergy/klt_streamlit_apps/blob/main/Pred%20Nvle%20Prod.csv"

def download_csv(url):
    response = requests.get(url)
    response.raise_for_status() 
    return StringIO(response.text)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.title("Télécharger le fichier CSV")

    # Appliquer le CSS personnalisé
    local_css("style.css")

    # Créer un bouton centré avec CSS
    col1, col2, col3 = st.columns([1,6,1])
    with col2:
        button_html = f'<a href="{csv_url}" download="data.csv"><button class="css-button">Télécharger le CSV</button></a>'
        st.markdown(button_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
