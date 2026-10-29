def moyenne_ponderee(valeurs, poids):
    """Moyenne de taux pondérée par un effectif (ex. circulations prévues)."""
    total_poids = sum(poids)
    if total_poids == 0:
        # Liaison sans circulation : aucun taux calculable
        return None
    return sum(v * p for v, p in zip(valeurs, poids)) / total_poids