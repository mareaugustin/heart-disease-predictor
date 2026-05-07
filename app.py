# ============================================================
# APP.PY — PAGE D'ACCUEIL
# ============================================================

import streamlit as st
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from style import inject_css,footer, section_header, divider

st.set_page_config(
    page_title="Heart Disease Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css(st)

# ========== HERO SECTION ==========
st.markdown("""
<div style="text-align:center; padding: 40px 20px 20px 20px;">
    <div class="main-title">Heart Disease Predictor</div>
    <div class="sub-title">
        Projet de Machine Learning — IFOAD<br>
        Intelligence Artificielle et Apprentissage Automatique<br>
        <strong>MILLOGO Maré Augustin & OUEDRAOGO Abdoul Koudous</strong>
    </div>
    <div style="margin-top:15px;">
        <span class="badge badge-red">
            <i class="fa-solid fa-brain"></i> Machine Learning
        </span>
        <span class="badge badge-blue">
            <i class="fa-solid fa-database"></i> UCI Dataset
        </span>
        <span class="badge badge-green">
            <i class="fa-solid fa-chart-line"></i> 6 Algorithmes
        </span>
        <span class="badge badge-orange">
            <i class="fa-solid fa-flask"></i> Classification
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

divider(st)

# ========== STATS DU DATASET ==========
try:
    df = pd.read_csv('data/heart_disease_uci.csv')

    st.markdown("""
    <div class="section-header">
        <i class="fa-solid fa-chart-bar" style="color:#e74c3c;font-size:1.4em;"></i>
        <h2 style="margin:0;font-size:1.5em;font-weight:700;color:#2c3e50;">
            Dataset en chiffres
        </h2>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    stats = [
        (c1, "fa-users",       "#3498db", str(df.shape[0]),
         "Patients"),
        (c2, "fa-microscope",  "#9b59b6", str(df.shape[1]-1),
         "Features"),
        (c3, "fa-heart-pulse", "#e74c3c", str(int(df['target'].sum())),
         "Malades"),
        (c4, "fa-shield-heart","#2ecc71", str(int((df['target']==0).sum())),
         "Sains"),
        (c5, "fa-calendar",    "#f39c12", f"{df['age'].mean():.0f} ans",
         "Âge moyen"),
        (c6, "fa-venus-mars",  "#1abc9c", f"{df['sex'].mean()*100:.0f}%",
         "Hommes"),
    ]
    for col, icon, color, val, label in stats:
        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">
                <i class="fa-solid {icon}" style="color:{color};"></i>
            </div>
            <div class="metric-value" style="color:{color};">{val}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.warning(f"Dataset non trouvé : {e}")

divider(st)

# ========== DESCRIPTION + OBJECTIF ==========
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("""
    <div class="section-header">
        <i class="fa-solid fa-bullseye" style="color:#e74c3c;font-size:1.4em;"></i>
        <h2 style="margin:0;font-size:1.5em;font-weight:700;color:#2c3e50;">
            Objectif du Projet
        </h2>
    </div>
    <div class="info-box">
        <i class="fa-solid fa-circle-info" style="color:#3498db;"></i>
        Ce projet applique des techniques de <b>Machine Learning</b> pour 
        prédire la présence d'une <b>maladie cardiaque</b> chez un patient 
        à partir de ses données médicales.<br><br>
        Il utilise le dataset officiel 
        <b><a href="https://archive.ics.uci.edu/dataset/45/heart+disease" 
        target="_blank" style="color:#3498db;">Heart Disease UCI</a></b> 
        (303 patients, 13 caractéristiques).
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="margin-top:15px;">
        <b><i class="fa-solid fa-list-check" style="color:#e74c3c;"></i> 
        Ce que fait cette application :</b>
        <ul style="margin-top:12px; line-height:2;">
            <li>
                <i class="fa-solid fa-magnifying-glass-chart" 
                   style="color:#3498db; width:20px;"></i>
                <b>Explorer</b> le dataset et répondre à 6 questions analytiques
            </li>
            <li>
                <i class="fa-solid fa-robot" 
                   style="color:#9b59b6; width:20px;"></i>
                <b>Comparer</b> 6 algorithmes de classification
            </li>
            <li>
                <i class="fa-solid fa-wand-magic-sparkles" 
                   style="color:#e74c3c; width:20px;"></i>
                <b>Prédire</b> si un patient est à risque
            </li>
            <li>
                <i class="fa-solid fa-chart-pie" 
                   style="color:#2ecc71; width:20px;"></i>
                <b>Visualiser</b> les résultats de manière interactive
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div class="section-header">
        <i class="fa-solid fa-stethoscope" style="color:#e74c3c;font-size:1.4em;"></i>
        <h2 style="margin:0;font-size:1.5em;font-weight:700;color:#2c3e50;">
            Variables Clés
        </h2>
    </div>
    <div class="card">
        <table style="width:100%; font-size:0.88em; border-collapse:collapse;">
            <tr style="border-bottom:2px solid #f0f0f0;">
                <th style="padding:8px;text-align:left;color:#7f8c8d;">Variable</th>
                <th style="padding:8px;text-align:left;color:#7f8c8d;">Description</th>
            </tr>
            <tr style="border-bottom:1px solid #f8f8f8;">
                <td style="padding:8px;">
                    <span class="badge badge-red">age</span>
                </td>
                <td style="padding:8px;color:#555;">Âge (années)</td>
            </tr>
            <tr style="border-bottom:1px solid #f8f8f8;">
                <td style="padding:8px;">
                    <span class="badge badge-blue">cp</span>
                </td>
                <td style="padding:8px;color:#555;">Type douleur thoracique</td>
            </tr>
            <tr style="border-bottom:1px solid #f8f8f8;">
                <td style="padding:8px;">
                    <span class="badge badge-green">thalach</span>
                </td>
                <td style="padding:8px;color:#555;">Fréq. cardiaque max</td>
            </tr>
            <tr style="border-bottom:1px solid #f8f8f8;">
                <td style="padding:8px;">
                    <span class="badge badge-orange">chol</span>
                </td>
                <td style="padding:8px;color:#555;">Cholestérol (mg/dl)</td>
            </tr>
            <tr style="border-bottom:1px solid #f8f8f8;">
                <td style="padding:8px;">
                    <span class="badge badge-purple">exang</span>
                </td>
                <td style="padding:8px;color:#555;">Angine à l'effort</td>
            </tr>
            <tr>
                <td style="padding:8px;">
                    <span class="badge badge-red">target</span>
                </td>
                <td style="padding:8px;color:#555;">
                    <b>Maladie cardiaque</b> ✓
                </td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

divider(st)

# ========== LES 6 ALGORITHMES ==========
st.markdown("""
<div class="section-header">
    <i class="fa-solid fa-robot" style="color:#e74c3c;font-size:1.4em;"></i>
    <h2 style="margin:0;font-size:1.5em;font-weight:700;color:#2c3e50;">
        Les 6 Algorithmes de Classification
    </h2>
</div>
""", unsafe_allow_html=True)

algos = [
    ("01", "fa-chart-line",       "#3498db",
     "Logistic Regression",
     "Modèle statistique linéaire, simple et très interprétable."),
    ("02", "fa-circle-nodes",     "#e74c3c",
     "K-Nearest Neighbors",
     "Classe selon les K voisins les plus proches dans l'espace."),
    ("03", "fa-vector-square",    "#9b59b6",
     "Support Vector Machine",
     "Trouve la meilleure frontière (hyperplan) entre les classes."),
    ("04", "fa-sitemap",          "#f39c12",
     "Decision Tree",
     "Arbre de décision basé sur des règles if/else successives."),
    ("05", "fa-tree",             "#2ecc71",
     "Random Forest",
     "Ensemble d'arbres de décision pour + de robustesse."),
    ("06", "fa-layer-group",      "#1abc9c",
     "AdaBoost",
     "Combine plusieurs modèles faibles en un modèle fort."),
]

cols = st.columns(3)
for i, (num, icon, color, nom, desc) in enumerate(algos):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="algo-card">
            <div style="display:flex; align-items:center; gap:12px; 
                        margin-bottom:8px;">
                <i class="fa-solid {icon}" 
                   style="font-size:1.6em; color:{color};"></i>
                <div>
                    <div class="algo-number" style="color:{color}; 
                                font-size:0.85em; font-weight:700;">
                        #{num}
                    </div>
                    <div class="algo-name">{nom}</div>
                </div>
            </div>
            <div class="algo-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

divider(st)

# ========== NAVIGATION ==========
st.markdown("""
<div class="section-header">
    <i class="fa-solid fa-map-signs" style="color:#e74c3c;font-size:1.4em;"></i>
    <h2 style="margin:0;font-size:1.5em;font-weight:700;color:#2c3e50;">
        Navigation
    </h2>
</div>
<div class="info-box">
    <i class="fa-solid fa-hand-point-left" style="color:#3498db;"></i>
    <b>Utilise le menu à gauche</b> pour naviguer entre les pages :
    <ul style="margin-top:12px; line-height:2.2;">
        <li>
            <i class="fa-solid fa-magnifying-glass-chart" 
               style="color:#3498db;width:20px;"></i>
            <b>Exploration</b> → Analyse du dataset et réponses aux 6 questions
        </li>
        <li>
            <i class="fa-solid fa-robot" 
               style="color:#9b59b6;width:20px;"></i>
            <b>Modèles</b> → Comparaison des algorithmes et métriques
        </li>
        <li>
            <i class="fa-solid fa-wand-magic-sparkles" 
               style="color:#e74c3c;width:20px;"></i>
            <b>Prédiction</b> → Teste avec tes propres données patient
        </li>
        <li>
            <i class="fa-solid fa-chart-pie" 
               style="color:#2ecc71;width:20px;"></i>
            <b>Visualisations</b> → Graphiques interactifs Plotly
        </li>
    </ul>
</div>
""", unsafe_allow_html=True)

footer(st)