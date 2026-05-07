# ============================================================
# PAGE 3 : PRÉDICTION
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from style import inject_css,  footer, divider

st.set_page_config(page_title="Prédiction", page_icon="🔮", layout="wide")
inject_css(st)
st.markdown("# Prédiction de Maladie Cardiaque")
st.markdown("Remplis le formulaire ci-dessous pour savoir si un patient "
            "est à risque de maladie cardiaque.")
st.markdown("---")

# --- Chargement modèles ---
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
        with open(f'data/models/{fichier}.pkl', 'rb') as f:
            models[nom] = pickle.load(f)
    with open('data/models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return models, scaler

modeles, scaler = load_models()

# ========================
# FORMULAIRE
# ========================
st.markdown("## Données du Patient")

with st.form("formulaire_patient"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Informations personnelles")
        age = st.slider("Âge (années)", 20, 80, 50)
        sex = st.selectbox("Sexe", [0, 1],
                           format_func=lambda x: "Femme" if x == 0 else "Homme")
        cp  = st.selectbox("Type de douleur thoracique (cp)",
                           [0, 1, 2, 3],
                           format_func=lambda x: {
                               0: "0 — Angine typique",
                               1: "1 — Angine atypique",
                               2: "2 — Douleur non-angineuse",
                               3: "3 — Asymptomatique"
                           }[x])

    with col2:
        st.markdown("### Mesures cliniques")
        trestbps = st.slider("Pression artérielle au repos (mm Hg)", 80, 200, 120)
        chol     = st.slider("Cholestérol sérique (mg/dl)", 100, 600, 240)
        thalach  = st.slider("Fréquence cardiaque maximale (bpm)", 60, 220, 150)
        oldpeak  = st.slider("Dépression ST (oldpeak)", 0.0, 7.0, 1.0, 0.1)

    with col3:
        st.markdown("### Résultats d'examens")
        fbs     = st.selectbox("Glycémie à jeun > 120 mg/dl (fbs)",
                               [0, 1],
                               format_func=lambda x: "Non (0)" if x == 0 else "Oui (1)")
        restecg = st.selectbox("Résultats ECG au repos (restecg)",
                               [0, 1, 2],
                               format_func=lambda x: {
                                   0: "0 — Normal",
                                   1: "1 — Anomalie ST-T",
                                   2: "2 — Hypertrophie ventriculaire"
                               }[x])
        exang   = st.selectbox("Angine à l'effort (exang)",
                               [0, 1],
                               format_func=lambda x: "Non (0)" if x == 0 else "Oui (1)")
        slope   = st.selectbox("Pente segment ST (slope)",
                               [0, 1, 2],
                               format_func=lambda x: {
                                   0: "0 — Montante",
                                   1: "1 — Plate",
                                   2: "2 — Descendante"
                               }[x])
        ca      = st.selectbox("Nombre de vaisseaux colorés (ca)",
                               [0, 1, 2, 3])
        thal    = st.selectbox("Thalassémie (thal)",
                               [3, 6, 7],
                               format_func=lambda x: {
                                   3: "3 — Normal",
                                   6: "6 — Défaut fixé",
                                   7: "7 — Défaut réversible"
                               }[x])

    # Choix du modèle
    st.markdown("---")
    modele_choisi = st.selectbox(
        "Choisir l'algorithme de prédiction",
        list(modeles.keys())
    )

    submitted = st.form_submit_button(
        "Lancer la Prédiction", use_container_width=True)

# ========================
# RÉSULTAT
# ========================
if submitted:
    # Création du vecteur patient
    patient = np.array([[age, sex, cp, trestbps, chol, fbs,
                         restecg, thalach, exang, oldpeak,
                         slope, ca, thal]])

    patient_scaled = scaler.transform(patient)
    modele         = modeles[modele_choisi]
    prediction     = modele.predict(patient_scaled)[0]
    probabilite    = modele.predict_proba(patient_scaled)[0]

    st.markdown("---")
    st.markdown("## Résultat de la Prédiction")

    col1, col2, col3 = st.columns(3)
    col1.metric("Algorithme utilisé", modele_choisi)
    col2.metric("Probabilité — Sain",
                f"{probabilite[0]*100:.1f}%")
    col3.metric("Probabilité — Malade",
                f"{probabilite[1]*100:.1f}%")

    st.markdown("---")

    if prediction == 1:
        st.error(f"""
        ### Risque de Maladie Cardiaque Détecté

        Le modèle **{modele_choisi}** prédit que ce patient est 
        **à risque de maladie cardiaque** avec une probabilité de 
        **{probabilite[1]*100:.1f}%**.

        **Attention :** Cette prédiction est basée sur un modèle 
        d'apprentissage automatique et ne remplace pas un diagnostic médical professionnel.
        Consultez un médecin.
        """)
    else:
        st.success(f"""
        ### Pas de Maladie Cardiaque Détectée

        Le modèle **{modele_choisi}** prédit que ce patient 
        **n'est pas à risque de maladie cardiaque** avec une probabilité de 
        **{probabilite[0]*100:.1f}%**.

        **Note :** Cette prédiction est basée sur un modèle 
        d'apprentissage automatique et ne remplace pas un diagnostic médical professionnel.
        """)

    # Résumé des données saisies
    st.markdown("### Résumé des données saisies")
    recap = pd.DataFrame({
        'Variable' : ['age','sex','cp','trestbps','chol','fbs',
                      'restecg','thalach','exang','oldpeak',
                      'slope','ca','thal'],
        'Valeur'   : [age, sex, cp, trestbps, chol, fbs,
                      restecg, thalach, exang, oldpeak,
                      slope, ca, thal]
    })
    st.dataframe(recap, use_container_width=True)

    # Prédictions de tous les modèles
    st.markdown("### Avis de tous les modèles")
    avis = []
    for nom, mod in modeles.items():
        pred  = mod.predict(patient_scaled)[0]
        proba = mod.predict_proba(patient_scaled)[0]
        avis.append({
            'Modèle'          : nom,
            'Prédiction'      : 'Malade' if pred == 1 else 'Sain',
            'Proba Sain (%)'  : f"{proba[0]*100:.1f}",
            'Proba Malade (%)': f"{proba[1]*100:.1f}"
        })
    st.dataframe(pd.DataFrame(avis), use_container_width=True)

st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#7f8c8d;font-size:0.9em;'>
Heart Disease Predictor | IFOAD — MILLOGO Maré Augustin & OUEDRAOGO Abdoul Koudous | Dataset: UCI Heart Disease
</div>
""", unsafe_allow_html=True)