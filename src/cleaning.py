"""Nettoyage et typage du jeu de données de régularité mensuelle TGV.

Chaque traitement renvoie à une entrée de docs/anomalies.md (ANO-xx).
"""
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
FICHIER_BRUT = (
    RACINE / "data" / "raw" / "regularite_mensuelle_tgv_par_liaisons.csv"
)
FICHIER_PROPRE = RACINE / "data" / "processed" / "regularite_tgv_propre.csv"

COL_CIRCULATIONS = "Nombre de circulations prévues"
COL_RETARD_15 = "Nombre trains en retard > 15min"
COL_RETARD_30 = "Nombre trains en retard > 30min"
COL_RETARD_60 = "Nombre trains en retard > 60min"
COLS_COMMENTAIRES_VIDES = [
    "Commentaire annulations",
    "Commentaire retards au départ",
]
PREFIXE_CAUSES = "Prct retard pour cause"


def charger_brut(chemin=FICHIER_BRUT):
    """Charge le CSV brut sans rien modifier."""
    return pd.read_csv(chemin, sep=";")


def nettoyer(brut):
    """Applique les traitements du journal des anomalies.

    Renvoie le tableau propre et un dictionnaire de comptes, pour que
    chaque ligne écartée ou signalée reste tracée.
    """
    df = brut.copy()
    rapport = {"lignes_brutes": len(df)}

    # ANO-01 : la date est un texte AAAA-MM
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m")

    # ANO-02 : colonnes de commentaires entièrement vides
    df = df.drop(columns=COLS_COMMENTAIRES_VIDES)

    # ANO-06 : -1 est un « non renseigné » déguisé, pas un nombre de trains
    retard_30 = df[COL_RETARD_30]
    rapport["valeurs_moins_un"] = int((retard_30 == -1).sum())
    df[COL_RETARD_30] = retard_30.astype("Int64").mask(retard_30 == -1)

    # ANO-09 : seuils incohérents (2025), signalés sans être modifiés
    r15, r30, r60 = df[COL_RETARD_15], df[COL_RETARD_30], df[COL_RETARD_60]
    incoherent = ((r30 > r15) | (r60 > r30) | r30.isna()).fillna(True)
    df["seuils_fiables"] = ~incoherent.astype(bool)

    # ANO-10 : les causes ne sont exploitables que si elles totalisent 100
    causes = [c for c in df.columns if c.startswith(PREFIXE_CAUSES)]
    somme_causes = df[causes].sum(axis=1)
    df["causes_exploitables"] = (somme_causes - 100).abs() <= 1

    # ANO-08 : liaisons observées sur tous les mois (calculé avant d'écarter
    # des lignes, pour ne pas fausser le nombre de mois de chaque liaison)
    df["liaison"] = df["Gare de départ"] + " -> " + df["Gare d'arrivée"]
    mois_par_liaison = df.groupby("liaison")["Date"].transform("nunique")
    df["liaison_complete"] = mois_par_liaison == df["Date"].nunique()

    # ANO-04 et ANO-05 : lignes sans circulation, taux incalculables
    sans_circulation = df[COL_CIRCULATIONS] == 0
    rapport["lignes_sans_circulation"] = int(sans_circulation.sum())
    df = df[~sans_circulation].reset_index(drop=True)

    rapport["lignes_propres"] = len(df)
    return df, rapport


def sauvegarder(propre, chemin=FICHIER_PROPRE):
    """Écrit le tableau propre dans data/processed/ (non versionné)."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    propre.to_csv(chemin, index=False)
    return chemin


if __name__ == "__main__":
    propre, rapport = nettoyer(charger_brut())
    print(rapport)
    print("Fichier écrit :", sauvegarder(propre))