# ============================================================
# PAGE 4 : VISUALISATIONS INTERACTIVES
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style import inject_css,  footer, divider

st.set_page_config(page_title="Visualisations", page_icon="📈", layout="wide")
inject_css(st)

st.markdown("# Visualisations Interactives")
st.markdown("Explore les données de manière interactive.")
st.markdown("---")

@st.cache_data
def load_data():
    return pd.read_csv('data/heart_disease_uci.csv')

df = load_data()

# Noms lisibles
df['Statut'] = df['target'].map({0: 'Sain', 1: 'Malade'})
df['Sexe']   = df['sex'].map({0: 'Femme', 1: 'Homme'})

# ========================
# VIZ 1 : Distribution âge
# ========================
st.markdown("## 1. Distribution de l'âge")
fig = px.histogram(df, x='age', color='Statut',
                   barmode='overlay',
                   color_discrete_map={'Sain':'#2ecc71','Malade':'#e74c3c'},
                   nbins=30,
                   title="Distribution de l'âge selon le statut cardiaque",
                   labels={'age': 'Âge', 'count': 'Nombre de patients'},
                   opacity=0.75)
fig.update_layout(bargap=0.1)
st.plotly_chart(fig, use_container_width=True)

# ========================
# VIZ 2 : Scatter plot
# ========================
st.markdown("---")
st.markdown("## 2. Relation entre les variables (Scatter Plot)")

col1, col2 = st.columns(2)
with col1:
    x_var = st.selectbox("Variable axe X",
                         ['age','trestbps','chol','thalach','oldpeak'],
                         index=0)
with col2:
    y_var = st.selectbox("Variable axe Y",
                         ['thalach','chol','trestbps','age','oldpeak'],
                         index=0)

fig = px.scatter(df, x=x_var, y=y_var,
                 color='Statut', symbol='Sexe',
                 color_discrete_map={'Sain':'#2ecc71','Malade':'#e74c3c'},
                 title=f'Relation entre {x_var} et {y_var}',
                 hover_data=['age','sex','cp','target'],
                 opacity=0.8, size_max=10)
st.plotly_chart(fig, use_container_width=True)

# ========================
# VIZ 3 : Box plots
# ========================
st.markdown("---")
st.markdown("## 3. Distribution des variables numériques")

var_box = st.selectbox("Choisir une variable",
                       ['age','trestbps','chol','thalach','oldpeak'])
fig = px.box(df, x='Statut', y=var_box,
             color='Statut',
             color_discrete_map={'Sain':'#2ecc71','Malade':'#e74c3c'},
             points='all',
             title=f'Distribution de {var_box} selon le statut cardiaque',
             notched=True)
st.plotly_chart(fig, use_container_width=True)

# ========================
# VIZ 4 : Heatmap corrélation
# ========================
st.markdown("---")
st.markdown("## 4. Heatmap de Corrélation Interactive")

corr = df.drop(columns=['Statut','Sexe']).corr().round(2)
fig  = px.imshow(corr,
                 text_auto=True,
                 color_continuous_scale='RdBu_r',
                 zmin=-1, zmax=1,
                 title='Matrice de Corrélation Interactive',
                 aspect='auto')
fig.update_layout(width=750, height=650)
st.plotly_chart(fig, use_container_width=True)

# ========================
# VIZ 5 : Radar chart
# ========================
st.markdown("---")
st.markdown("## 5. Comparaison des Modèles — Radar Chart Interactif")

try:
    df_res = pd.read_csv('data/resultats_modeles.csv', index_col=0)
    metriques = ['Accuracy','Précision','Rappel','F1-Score','AUC-ROC']
    colors_r  = ['#3498db','#e74c3c','#2ecc71','#f39c12','#9b59b6','#1abc9c']

    fig = go.Figure()
    for (nom, row), color in zip(df_res.iterrows(), colors_r):
        vals = row[metriques].tolist()
        vals += vals[:1]
        cats = metriques + [metriques[0]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=cats,
            fill='toself', name=nom,
            line_color=color, opacity=0.7
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0.5, 1.0])),
        showlegend=True,
        title='Radar Chart — Comparaison des 6 Algorithmes',
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.warning(f"Résultats non disponibles : {e}")

# ========================
# VIZ 6 : Barplot métriques
# ========================
st.markdown("---")
st.markdown("## 6. Comparaison des Métriques par Algorithme")

try:
    metrique_choisie = st.selectbox(
        "Choisir une métrique",
        ['Accuracy','Précision','Rappel','F1-Score','AUC-ROC']
    )
    df_sorted = df_res.sort_values(metrique_choisie, ascending=False)
    fig = px.bar(df_sorted.reset_index(),
                 x='index', y=metrique_choisie,
                 color=metrique_choisie,
                 color_continuous_scale='RdYlGn',
                 text=df_sorted[metrique_choisie].round(4).values,
                 title=f'Classement des modèles — {metrique_choisie}',
                 labels={'index': 'Algorithme'})
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, yaxis_range=[0.5, 1.05])
    fig.add_hline(y=0.8, line_dash='dash',
                  line_color='red', annotation_text='Seuil 80%')
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.warning(f"Résultats non disponibles : {e}")

st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#7f8c8d;font-size:0.9em;'>
Heart Disease Predictor | IFOAD — MILLOGO Maré Augustin & OUEDRAOGO Abdoul Koudous | Dataset: UCI Heart Disease
</div>
""", unsafe_allow_html=True)