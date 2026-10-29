import pytest

from src.indicators import moyenne_ponderee


def test_les_grosses_liaisons_pesent_plus():
    # 10 trains à 50 % et 1000 trains à 10 % : la vraie valeur est proche de 10 %
    assert moyenne_ponderee([50, 10], [10, 1000]) == pytest.approx(10.4, abs=0.05)


def test_poids_egaux_donnent_la_moyenne_simple():
    assert moyenne_ponderee([20, 40], [5, 5]) == pytest.approx(30)


def test_sans_circulation_renvoie_none():
    assert moyenne_ponderee([0, 0], [0, 0]) is None