
# COMPARAISON DES MODÈLES

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.metrics import (confusion_matrix, roc_curve,
                              roc_auc_score, accuracy_score)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style import inject_css, footer, divider

st.set_page_config(page_title="Modèles ML", page_icon="🤖", layout="wide")
inject_css(st)

st.markdown("# Comparaison des Modèles de Machine Learning")
st.markdown("---")

# --- Chargement ---
@st.cache_data
def load_data():
    return pd.read_csv('data/heart_disease_uci.csv')

@st.cache_resource
def load_models():
    noms = {
        'Logistic Regression'   : 'logistic_regression',
        'K-Nearest Neighbors'   : 'k_nearest_neighbors',
        'Support Vector Machine': 'support_vector_machine',
        'Decision Tree'         : 'decision_tree',
        'Random Forest'         : 'random_forest',
        'AdaBoost'              : 'adaboost'
    }
    models = {}
    for nom, fichier in noms.items():
        try:
            with open(f'data/models/{fichier}.pkl', 'rb') as f:
                models[nom] = pickle.load(f)
        except:
            st.error(f"Modèle {nom} introuvable.")
    with open('data/models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return models, scaler

df = load_data()
modeles, scaler = load_models()

# Reconstruction train/test
from sklearn.model_selection import train_test_split
X = df.drop('target', axis=1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
X_test_scaled = scaler.transform(X_test)

# --- Résultats ---
try:
    df_res = pd.read_csv('data/resultats_modeles.csv', index_col=0)
except:
    st.error("Fichier resultats_modeles.csv introuvable.")
    st.stop()

# ========================
# SECTION 1 : TABLEAU
# ========================
st.markdown("## Tableau Comparatif des Performances")

df_display = df_res.copy()
df_display = df_display.sort_values('AUC-ROC', ascending=False)

# Mise en forme
def color_max(s):
    is_max = s == s.max()
    return ['background-color: #d5f5e3; font-weight:bold'
            if v else '' for v in is_max]

st.dataframe(
    df_display.style.apply(color_max).format("{:.4f}"),
    use_container_width=True
)

meilleur = df_display['AUC-ROC'].idxmax()
st.success(f"**Meilleur modèle (AUC-ROC) : {meilleur}** "
           f"→ AUC-ROC = {df_display.loc[meilleur,'AUC-ROC']:.4f} | "
           f"Accuracy = {df_display.loc[meilleur,'Accuracy']:.4f}")

# ========================
# SECTION 2 : GRAPHIQUE
# ========================
st.markdown("---")
st.markdown("## Graphique Comparatif — Toutes Métriques")

metriques = ['Accuracy','Précision','Rappel','F1-Score','AUC-ROC']
colors_m  = ['#3498db','#e74c3c','#2ecc71','#f39c12','#9b59b6']
x         = np.arange(len(df_display))
width     = 0.15

fig, ax = plt.subplots(figsize=(14, 6))
for i, (met, col) in enumerate(zip(metriques, colors_m)):
    ax.bar(x + i*width, df_display[met], width,
           label=met, color=col, alpha=0.85,
           edgecolor='black', linewidth=0.5)

ax.set_xticks(x + width*2)
ax.set_xticklabels(df_display.index, rotation=12, ha='right', fontsize=10)
ax.set_ylabel('Score')
ax.set_ylim(0.4, 1.08)
ax.set_title('Comparaison des 6 Algorithmes — Toutes Métriques',
             fontsize=13, fontweight='bold')
ax.legend(fontsize=9)
ax.axhline(0.8, color='red', linestyle='--', alpha=0.5, lw=1.5)
ax.text(len(x)-0.3, 0.81, 'Seuil 80%', color='red', fontsize=8)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
st.pyplot(fig)
plt.close()

# ========================
# SECTION 3 : RADAR CHART
# ========================
st.markdown("---")
st.markdown("## Radar Chart — Vue globale des modèles")

from matplotlib.patches import FancyArrowPatch
import matplotlib.patches as mpatches

categories = metriques
N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8),
                       subplot_kw=dict(polar=True))
colors_radar = ['#3498db','#e74c3c','#2ecc71',
                '#f39c12','#9b59b6','#1abc9c']

for (nom, row), color in zip(df_display.iterrows(), colors_radar):
    vals = row[metriques].tolist()
    vals += vals[:1]
    ax.plot(angles, vals, 'o-', linewidth=2,
            label=nom, color=color)
    ax.fill(angles, vals, alpha=0.07, color=color)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=11)
ax.set_ylim(0.5, 1.0)
ax.set_title('Radar Chart — Performances globales',
             fontsize=13, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.15), fontsize=9)
plt.tight_layout()
st.pyplot(fig)
plt.close()

# ========================
# SECTION 4 : MATRICES
# ========================
st.markdown("---")
st.markdown("## Matrices de Confusion")

fig, axes = plt.subplots(2, 3, figsize=(15, 9))
axes = axes.flatten()

for idx, (nom, modele) in enumerate(modeles.items()):
    y_pred = modele.predict(X_test_scaled)
    cm     = confusion_matrix(y_test, y_pred)
    acc    = accuracy_score(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Pas maladie','Maladie'],
                yticklabels=['Pas maladie','Maladie'],
                ax=axes[idx], linewidths=1, cbar=False)
    axes[idx].set_title(f'{nom}\n(Accuracy: {acc:.3f})',
                        fontsize=10, fontweight='bold')
    axes[idx].set_xlabel('Prédit')
    axes[idx].set_ylabel('Réel')

plt.suptitle('Matrices de Confusion — 6 Modèles',
             fontsize=14, fontweight='bold')
plt.tight_layout()
st.pyplot(fig)
plt.close()

# ========================
# SECTION 5 : ROC
# ========================
st.markdown("---")
st.markdown("## Courbes ROC")

colors_roc = ['#3498db','#e74c3c','#2ecc71',
              '#f39c12','#9b59b6','#1abc9c']
fig, ax = plt.subplots(figsize=(9, 7))

for (nom, modele), color in zip(modeles.items(), colors_roc):
    y_proba     = modele.predict_proba(X_test_scaled)[:, 1]
    fpr,tpr,_   = roc_curve(y_test, y_proba)
    auc         = roc_auc_score(y_test, y_proba)
    ax.plot(fpr, tpr, color=color, lw=2.5,
            label=f'{nom} (AUC={auc:.3f})')

ax.plot([0,1],[0,1],'k--', lw=1.5, label='Aléatoire (AUC=0.500)')
ax.set_xlim([0,1])
ax.set_ylim([0,1.05])
ax.set_xlabel('Taux Faux Positifs (FPR)', fontsize=12)
ax.set_ylabel('Taux Vrais Positifs (TPR)', fontsize=12)
ax.set_title('Courbes ROC — Comparaison des Modèles',
             fontsize=13, fontweight='bold')
ax.legend(loc='lower right', fontsize=9)
ax.grid(alpha=0.3)
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#7f8c8d;font-size:0.9em;'>
Heart Disease Predictor | IFOAD — MILLOGO Maré Augustin & OUEDRAOGO Abdoul Koudous | Dataset: UCI Heart Disease
</div>
""", unsafe_allow_html=True)