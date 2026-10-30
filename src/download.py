"""Télécharge le jeu de données de régularité mensuelle TGV par liaisons."""
from datetime import date
from pathlib import Path

import requests

URL = "https://www.data.gouv.fr/api/1/datasets/r/91fe399d-cafa-4e72-8ba3-56d8717fdad4"  # noqa: E501
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
FICHIER = RAW_DIR / "regularite_mensuelle_tgv_par_liaisons.csv"


def telecharger(url=URL, destination=FICHIER):
    # Le dossier peut ne pas exister chez un collègue qui vient de cloner
    destination.parent.mkdir(parents=True, exist_ok=True)
    reponse = requests.get(url, timeout=60)
    reponse.raise_for_status()
    destination.write_bytes(reponse.content)
    return destination


if __name__ == "__main__":
    chemin = telecharger()
    print(f"Fichier téléchargé le {date.today()} : {chemin}")