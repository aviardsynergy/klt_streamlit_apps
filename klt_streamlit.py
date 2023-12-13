import streamlit as st
import pandas as pd
import altair as alt

# Chargement des données
df = pd.read_csv('Pred Nvle Prod.csv')
df['date'] = pd.to_datetime(df['date']).dt.date  # Assurez-vous que la colonne 'date' est de type date

# Convertir les valeurs en millions d'euros pour une meilleure lisibilité
df['REEL_NPROD'] = df['REEL_NPROD'] / 1e6
df['PRED_NPROD'] = df['PRED_NPROD'] / 1e6

# Tri des mois disponibles en ordre croissant avant de les passer au multiselect
all_months = sorted(df['date'].dt.strftime('%Y-%m').unique())

# Widget multiselect dans la barre latérale avec tous les mois disponibles
mois_selectionnes = st.sidebar.multiselect('Sélectionnez les mois', all_months, default=all_months)

# Filtrer les données en fonction de la sélection des mois
df_filtre = df[df['date'].dt.strftime('%Y-%m').isin(mois_selectionnes)] if mois_selectionnes else df

# Créer le graphique linéaire avec tooltips en utilisant Altair
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
