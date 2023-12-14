import streamlit as st
import pandas as pd

df = pd.read_csv('visu_3D_1.csv')

def normalize(column, new_min=0.5, new_max=1.5):
    old_min = column.min()
    old_max = column.max()
    return new_min + ((column - old_min) / (old_max - old_min)) * (new_max - new_min)

df['REEL_NPROD'] = normalize(df['REEL_NPROD'])
df['CA_SERVICES'] = normalize(df['CA_SERVICES'])
df['COEF_NF'] = normalize(df['COEF_NF'])

print(df)