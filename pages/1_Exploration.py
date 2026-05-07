# Une vue d'exploration du datatset

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style import inject_css, footer, divider

st.set_page_config(page_title="Exploration", page_icon="📊", layout="wide")
inject_css(st)

# --- CSS ---
st.markdown("""
<style>
.question-box {
    background-color: #eaf4fb;
    border-left: 5px solid #3498db;
    padding: 12px;
    border-radius: 5px;
    margin: 8px 0;
    font-weight: bold;
}
.answer-box {
    background-color: #f9f9f9;
    border-left: 5px solid #2ecc71;
    padding: 12px;
    border-radius: 5px;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)

# --- Chargement données ---
@st.cache_data
def load_data():
    return pd.read_csv('data/heart_disease_uci.csv')

df = load_data()

# --- Titre ---
st.markdown("# Exploration du Dataset")
st.markdown("**Source :** Heart Disease UCI — "
            "[archive.ics.uci.edu](https://archive.ics.uci.edu/dataset/45/heart+disease)")
st.markdown("---")

# ========================
# SECTION 1 : APERÇU
# ========================
st.markdown("## 1. Aperçu du Dataset")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total patients", df.shape[0])
col2.metric("Nombre de features", df.shape[1] - 1)
col3.metric("Patients malades", int(df['target'].sum()))
col4.metric("Patients sains", int((df['target'] == 0).sum()))

st.markdown("### Premières lignes du dataset")
st.dataframe(df.head(10), use_container_width=True)

st.markdown("### Statistiques descriptives")
st.dataframe(df.describe().round(2), use_container_width=True)

st.markdown("### Description des colonnes")
descriptions = {
    'age'     : "Âge du patient (années)",
    'sex'     : "Sexe (1=Homme, 0=Femme)",
    'cp'      : "Type de douleur thoracique (0 à 3)",
    'trestbps': "Pression artérielle au repos (mm Hg)",
    'chol'    : "Cholestérol sérique (mg/dl)",
    'fbs'     : "Glycémie à jeun > 120 mg/dl (1=Oui, 0=Non)",
    'restecg' : "Résultats ECG au repos (0, 1, 2)",
    'thalach' : "Fréquence cardiaque maximale (bpm)",
    'exang'   : "Angine à l'effort (1=Oui, 0=Non)",
    'oldpeak' : "Dépression ST à l'effort",
    'slope'   : "Pente du segment ST (0, 1, 2)",
    'ca'      : "Nombre de vaisseaux colorés (0 à 3)",
    'thal'    : "Thalassémie (3=Normal, 6=Fixe, 7=Réversible)",
    'target'  : "Maladie cardiaque (1=Oui, 0=Non)"
}
df_desc = pd.DataFrame(list(descriptions.items()),
                        columns=['Colonne', 'Description'])
st.dataframe(df_desc, use_container_width=True)

# ========================
# SECTION 2 : 6 QUESTIONS
# ========================
st.markdown("---")
st.markdown("## 2. Analyse — Réponses aux 6 Questions")

# --- Q1 ---
st.markdown("""
<div class="question-box">
Q1 : Quelle est la distribution de l'âge des individus dans le jeu de données ?
</div>
""", unsafe_allow_html=True)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].hist(df[df['target'] == 0]['age'], bins=20, alpha=0.7,
             color='#2ecc71', label='Pas de maladie', edgecolor='black')
axes[0].hist(df[df['target'] == 1]['age'], bins=20, alpha=0.7,
             color='#e74c3c', label='Maladie cardiaque', edgecolor='black')
axes[0].set_title("Distribution de l'âge", fontsize=13, fontweight='bold')
axes[0].set_xlabel("Âge (années)")
axes[0].set_ylabel("Nombre de patients")
axes[0].legend()
axes[0].axvline(df['age'].mean(), color='navy', linestyle='--', linewidth=2)
axes[0].text(df['age'].mean() + 0.5, axes[0].get_ylim()[1]*0.9,
             f"Moy: {df['age'].mean():.1f}", color='navy')

data_bp = [df[df['target'] == 0]['age'].values,
           df[df['target'] == 1]['age'].values]
bp = axes[1].boxplot(data_bp, labels=['Pas de maladie', 'Maladie'],
                     patch_artist=True)
bp['boxes'][0].set_facecolor('#2ecc71')
bp['boxes'][1].set_facecolor('#e74c3c')
axes[1].set_title("Boxplot de l'âge", fontsize=13, fontweight='bold')
axes[1].set_ylabel("Âge (années)")
axes[1].grid(axis='y', alpha=0.3)
plt.tight_layout()
st.pyplot(fig)
plt.close()

age_stats = df.groupby('target')['age'].describe().round(1)
age_stats.index = ['Pas de maladie', 'Maladie cardiaque']
st.dataframe(age_stats, use_container_width=True)

st.markdown(f"""
<div class="answer-box">
<b>Réponse Q1 :</b> Les patients ont entre <b>{int(df['age'].min())} 
et {int(df['age'].max())} ans</b>, avec une moyenne de 
<b>{df['age'].mean():.1f} ans</b>. 
Les patients <b>sans maladie</b> sont en moyenne plus jeunes 
({df[df['target']==0]['age'].mean():.1f} ans) que ceux 
<b>avec maladie</b> ({df[df['target']==1]['age'].mean():.1f} ans).
</div>
""", unsafe_allow_html=True)

# --- Q2 ---
st.markdown("---")
st.markdown("""
<div class="question-box">
Q2 : Y a-t-il une différence dans la présence de maladie cardiaque entre les sexes ?
</div>
""", unsafe_allow_html=True)

cross_sex = pd.crosstab(df['sex'], df['target'])
cross_sex.index = ['Femme', 'Homme']
cross_sex.columns = ['Pas de maladie', 'Maladie cardiaque']

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
cross_sex.plot(kind='bar', ax=axes[0], color=['#2ecc71', '#e74c3c'],
               edgecolor='black', rot=0)
axes[0].set_title('Maladie cardiaque par sexe', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Nombre de patients')
for c in axes[0].containers:
    axes[0].bar_label(c, fontweight='bold')

cross_pct = cross_sex.div(cross_sex.sum(axis=1), axis=0) * 100
cross_pct.plot(kind='bar', ax=axes[1], color=['#2ecc71', '#e74c3c'],
               edgecolor='black', rot=0)
axes[1].set_title('Pourcentage par sexe', fontsize=13, fontweight='bold')
axes[1].set_ylabel('Pourcentage (%)')
axes[1].set_ylim(0, 115)
for c in axes[1].containers:
    axes[1].bar_label(c, fmt='%.1f%%', fontweight='bold')
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown(f"""
<div class="answer-box">
<b>Réponse Q2 :</b> 
Oui, il existe une différence notable. 
Parmi les <b>femmes</b>, 
{cross_pct.loc['Femme','Maladie cardiaque']:.1f}% sont atteintes de maladie cardiaque. 
Parmi les <b>hommes</b>, ce taux est de 
{cross_pct.loc['Homme','Maladie cardiaque']:.1f}%. 
Les hommes semblent plus touchés par la maladie cardiaque dans ce dataset.
</div>
""", unsafe_allow_html=True)

# --- Q3 ---
st.markdown("---")
st.markdown("""
<div class="question-box">
Q3 : Comment le type de douleur thoracique (cp) est-il lié à la maladie cardiaque ?
</div>
""", unsafe_allow_html=True)

cp_labels = {0: 'Angine typique', 1: 'Angine atypique',
             2: 'Douleur non-angineuse', 3: 'Asymptomatique'}
df['cp_label'] = df['cp'].map(cp_labels)
cross_cp = pd.crosstab(df['cp_label'], df['target'])
cross_cp.columns = ['Pas de maladie', 'Maladie cardiaque']

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
cross_cp.plot(kind='bar', ax=axes[0], color=['#2ecc71', '#e74c3c'],
              edgecolor='black', rot=15)
axes[0].set_title('Type de douleur vs Maladie', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Nombre de patients')
for c in axes[0].containers:
    axes[0].bar_label(c, fontweight='bold')

sns.heatmap(pd.crosstab(df['cp'], df['target']),
            annot=True, fmt='d', cmap='YlOrRd',
            xticklabels=['Pas maladie', 'Maladie'],
            ax=axes[1], linewidths=1, cbar=False)
axes[1].set_title('Heatmap douleur vs maladie', fontsize=13, fontweight='bold')
plt.tight_layout()
st.pyplot(fig)
plt.close()
df.drop('cp_label', axis=1, inplace=True)

st.markdown("""
<div class="answer-box">
<b>Réponse Q3 :</b> 
Le type de douleur thoracique est fortement lié à la maladie cardiaque.
Les patients <b>asymptomatiques (cp=3)</b> présentent le plus grand nombre de cas 
de maladie cardiaque, ce qui est paradoxal mais cliniquement connu : 
l'absence de douleur n'exclut pas la maladie. 
Les patients avec une <b>angine typique (cp=0)</b> sont majoritairement sains dans ce dataset.
</div>
""", unsafe_allow_html=True)

# --- Q4 ---
st.markdown("---")
st.markdown("""
<div class="question-box">
Q4 : Valeurs moyennes de trestbps, chol et thalach selon le statut cardiaque ?
</div>
""", unsafe_allow_html=True)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
variables = ['trestbps', 'chol', 'thalach']
titres = ['Pression artérielle\nau repos (mm Hg)',
          'Cholestérol\n(mg/dl)',
          'Fréquence cardiaque\nmax (bpm)']
colors_b = [['#2ecc71','#e74c3c'],['#3498db','#e67e22'],['#9b59b6','#f39c12']]

for idx, (var, titre, cols) in enumerate(zip(variables, titres, colors_b)):
    data = [df[df['target']==0][var].values, df[df['target']==1][var].values]
    bp = axes[idx].boxplot(data, labels=['Pas maladie','Maladie'],
                           patch_artist=True)
    bp['boxes'][0].set_facecolor(cols[0])
    bp['boxes'][1].set_facecolor(cols[1])
    for med in bp['medians']:
        med.set_color('black')
        med.set_linewidth(2)
    axes[idx].set_title(titre, fontsize=12, fontweight='bold')
    axes[idx].grid(axis='y', alpha=0.3)
    for i, d in enumerate(data):
        axes[idx].text(i+1, np.mean(d), f'  {np.mean(d):.1f}',
                       va='center', fontsize=9, color='navy')
plt.tight_layout()
st.pyplot(fig)
plt.close()

moy = df.groupby('target')[['trestbps','chol','thalach']].mean().round(1)
moy.index = ['Pas de maladie','Maladie cardiaque']
st.dataframe(moy, use_container_width=True)

st.markdown(f"""
<div class="answer-box">
<b>Réponse Q4 :</b><br>
• <b>Pression artérielle (trestbps)</b> : légèrement plus élevée chez les malades 
({moy.loc['Maladie cardiaque','trestbps']} vs {moy.loc['Pas de maladie','trestbps']} mm Hg).<br>
• <b>Cholestérol (chol)</b> : valeurs similaires dans les deux groupes 
({moy.loc['Maladie cardiaque','chol']} vs {moy.loc['Pas de maladie','chol']} mg/dl).<br>
• <b>Fréquence cardiaque max (thalach)</b> : nettement plus basse chez les malades 
({moy.loc['Maladie cardiaque','thalach']} vs {moy.loc['Pas de maladie','thalach']} bpm), 
ce qui est un indicateur important.
</div>
""", unsafe_allow_html=True)

# --- Q5 ---
st.markdown("---")
st.markdown("""
<div class="question-box">
Q5 : La glycémie à jeun > 120 mg/dl (fbs) est-elle associée à la maladie cardiaque ?
</div>
""", unsafe_allow_html=True)

cross_fbs = pd.crosstab(df['fbs'], df['target'])
cross_fbs.index = ['FBS ≤ 120 mg/dl','FBS > 120 mg/dl']
cross_fbs.columns = ['Pas de maladie','Maladie cardiaque']
cross_pct_fbs = cross_fbs.div(cross_fbs.sum(axis=1), axis=0) * 100

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
cross_fbs.plot(kind='bar', ax=axes[0], color=['#2ecc71','#e74c3c'],
               edgecolor='black', rot=0)
axes[0].set_title('Glycémie à jeun vs Maladie', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Nombre de patients')
for c in axes[0].containers:
    axes[0].bar_label(c, fontweight='bold')

cross_pct_fbs.plot(kind='bar', ax=axes[1], color=['#2ecc71','#e74c3c'],
                   edgecolor='black', rot=0)
axes[1].set_title('Glycémie à jeun vs Maladie (%)', fontsize=13, fontweight='bold')
axes[1].set_ylabel('Pourcentage (%)')
axes[1].set_ylim(0, 115)
for c in axes[1].containers:
    axes[1].bar_label(c, fmt='%.1f%%', fontweight='bold')
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown(f"""
<div class="answer-box">
<b>Réponse Q5 :</b> 
La glycémie à jeun élevée (fbs=1) ne semble <b>pas fortement associée</b> 
à la maladie cardiaque dans ce dataset. 
Les taux de maladie sont comparables entre les patients avec 
FBS normal ({cross_pct_fbs.loc['FBS ≤ 120 mg/dl','Maladie cardiaque']:.1f}%) 
et ceux avec FBS élevé ({cross_pct_fbs.loc['FBS > 120 mg/dl','Maladie cardiaque']:.1f}%). 
La glycémie seule n'est donc pas un bon prédicteur isolé dans ce dataset.
</div>
""", unsafe_allow_html=True)

# --- Q6 ---
st.markdown("---")
st.markdown("""
<div class="question-box">
Q6 : Comment l'angine induite par l'exercice (exang) est-elle corrélée à la maladie ?
</div>
""", unsafe_allow_html=True)

cross_exang = pd.crosstab(df['exang'], df['target'])
cross_exang.index = ["Pas d'angine","Angine à l'effort"]
cross_exang.columns = ['Pas de maladie','Maladie cardiaque']
cross_pct_ex = cross_exang.div(cross_exang.sum(axis=1), axis=0) * 100

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
cross_exang.plot(kind='bar', ax=axes[0], color=['#2ecc71','#e74c3c'],
                 edgecolor='black', rot=0)
axes[0].set_title("Angine à l'effort vs Maladie", fontsize=13, fontweight='bold')
axes[0].set_ylabel('Nombre de patients')
for c in axes[0].containers:
    axes[0].bar_label(c, fontweight='bold')

cross_pct_ex.plot(kind='bar', ax=axes[1], color=['#2ecc71','#e74c3c'],
                  edgecolor='black', rot=0)
axes[1].set_title("Angine à l'effort vs Maladie (%)", fontsize=13, fontweight='bold')
axes[1].set_ylabel('Pourcentage (%)')
axes[1].set_ylim(0, 115)
for c in axes[1].containers:
    axes[1].bar_label(c, fmt='%.1f%%', fontweight='bold')
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown(f"""
<div class="answer-box">
<b>Réponse Q6 :</b> 
L'angine induite par l'exercice est <b>fortement corrélée</b> à la maladie cardiaque. 
Parmi les patients qui souffrent d'angine à l'effort, 
<b>{cross_pct_ex.loc["Angine à l'effort",'Maladie cardiaque']:.1f}%</b> 
ont une maladie cardiaque. 
En comparaison, seulement 
<b>{cross_pct_ex.loc["Pas d'angine",'Maladie cardiaque']:.1f}%</b> 
des patients sans angine à l'effort sont malades. 
C'est donc un <b>indicateur important</b> de la maladie.
</div>
""", unsafe_allow_html=True)

# --- Matrice de corrélation ---
st.markdown("---")
st.markdown("## 3. Matrice de Corrélation")

fig, ax = plt.subplots(figsize=(12, 9))
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
            cmap='coolwarm', center=0, square=True,
            linewidths=0.5, ax=ax)
ax.set_title('Matrice de Corrélation', fontsize=14, fontweight='bold')
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#7f8c8d; font-size:0.9em;'>
Heart Disease Predictor | IFOAD — MILLOGO Maré Augustin & OUEDRAOGO Abdoul Koudous | Dataset: UCI Heart Disease
</div>
""", unsafe_allow_html=True)