# ============================================================
# TÉLÉCHARGEMENT OFFICIEL DU DATASET UCI HEART DISEASE
# Source: https://archive.ics.uci.edu/dataset/45/heart+disease
# ============================================================

import pandas as pd
import os
from ucimlrepo import fetch_ucirepo

# Création du dossier data s'il n'existe pas
os.makedirs('data', exist_ok=True)

print("Téléchargement du dataset officiel UCI Heart Disease...")
print("   Source: https://archive.ics.uci.edu/dataset/45/heart+disease\n")

# Téléchargement officiel via ucimlrepo (id=45 = Heart Disease)
heart_disease = fetch_ucirepo(id=45)

# Récupération des features et de la cible
X = heart_disease.data.features
y = heart_disease.data.targets

print("Dataset téléchargé avec succès!")
print(f"\n Features (X) : {X.shape[0]} lignes x {X.shape[1]} colonnes")
print(f"Target  (y) : {y.shape[0]} lignes x {y.shape[1]} colonnes")

# ---------------------------------------------------------
# NETTOYAGE IMPORTANT
# La variable cible 'num' dans UCI prend les valeurs 0,1,2,3,4
# Le projet demande une classification binaire :
#   0 = pas de maladie
#   1 = maladie cardiaque (toute valeur > 0 devient 1)
# ---------------------------------------------------------
print("\n Valeurs originales de la cible 'num':")
print(y['num'].value_counts().sort_index())

y_binary = (y['num'] > 0).astype(int)
y_binary.name = 'target'

print("\n Après conversion binaire (0=sain, 1=malade):")
print(y_binary.value_counts().sort_index())

# ---------------------------------------------------------
# FUSION EN UN SEUL DATAFRAME
# ---------------------------------------------------------
df = pd.concat([X, y_binary], axis=1)

# ---------------------------------------------------------
# GESTION DES VALEURS MANQUANTES
# UCI Heart Disease a quelques valeurs manquantes
# On les remplace par la médiane (robuste aux outliers)
# ---------------------------------------------------------
print(f"\n Valeurs manquantes avant nettoyage:")
print(df.isnull().sum())

for col in df.columns:
    if df[col].isnull().sum() > 0:
        mediane = df[col].median()
        df[col].fillna(mediane, inplace=True)
        print(f"   Colonne '{col}' : valeurs manquantes remplacées par médiane ({mediane})")

print(f"\n Valeurs manquantes après nettoyage: {df.isnull().sum().sum()}")

# ---------------------------------------------------------
# SAUVEGARDE LOCALE
# ---------------------------------------------------------
df.to_csv('data/heart_disease_uci.csv', index=False)

print(f"\n Dataset sauvegardé dans 'data/heart_disease_uci.csv'")
print(f" Dimensions finales : {df.shape[0]} lignes x {df.shape[1]} colonnes")
print(f"\n Colonnes disponibles:")
for col in df.columns:
    print(f"   • {col}")

print(f"\n Aperçu des premières lignes:")
print(df.head())

print(f"\n Statistiques descriptives:")
print(df.describe().round(2))
