# Journal des anomalies

Jeu de données : Régularité mensuelle TGV par liaisons (SNCF Voyageurs), 12 907 lignes, 26 colonnes, 105 mois consécutifs depuis janvier 2018.
Principe : aucune ligne n'est supprimée ou corrigée sans trace écrite dans ce journal.

## ANO-01 : dates stockées en texte
- **Colonne(s)** : `Date`
- **Description** : stockée en texte au format AAAA-MM (exemple : `2018-01`)
- **Ampleur** : 12 907 lignes (100 %)
- **Cause probable** : format texte du fichier source
- **Traitement retenu** : converti en date lors du nettoyage (`src/cleaning.py`)
- **Impact sur l'analyse** : aucun après conversion

## ANO-02 : colonnes de commentaires entièrement vides
- **Colonne(s)** : `Commentaire annulations`, `Commentaire retards au départ`
- **Description** : colonnes sans aucune valeur (lues comme des nombres décimaux parce qu'elles sont vides)
- **Ampleur** : 0 ligne remplie sur 12 907 pour chacune des deux colonnes (100 % vides)
- **Cause probable** : champs de commentaire jamais remplis par le producteur
- **Traitement retenu** : exclues de l'analyse
- **Impact sur l'analyse** : aucun

## ANO-03 : texte libre à valeurs multiples
- **Colonne(s)** : `Commentaire retards à l'arrivée`
- **Description** : une même case décrit plusieurs incidents, avec le jour, le lieu, le nombre de TGV et les minutes de retard
- **Ampleur** : 698 lignes remplies sur 12 907 (5,4 %)
- **Cause probable** : champ saisi à la main
- **Traitement retenu** : signalé, non exploité dans les calculs
- **Impact sur l'analyse** : les causes de retard sont lues dans les colonnes de pourcentages

## ANO-04 : liaisons sans circulation prévue
- **Colonne(s)** : `Nombre de circulations prévues`, `Durée moyenne du trajet`
- **Description** : circulations prévues égales à 0 et durée égale ou inférieure à 0
- **Ampleur** : 73 lignes sur 12 907 (0,57 %), toutes en 2020 : avril (50), mai (9), juin (4), puis 2 par mois d'août à décembre
- **Cause probable** : suspension de liaisons en 2020, vraisemblablement liée à la crise sanitaire (à confirmer)
- **Traitement retenu** : exclues des taux (division par zéro), conservées dans les données brutes
- **Impact sur l'analyse** : 2020 est une période atypique, à signaler dans les limites et dans l'étude des tendances

## ANO-05 : annulations supérieures aux circulations prévues
- **Colonne(s)** : `Nombre de trains annulés`, `Nombre de circulations prévues`
- **Description** : plus de trains annulés que de trains prévus
- **Ampleur** : 63 lignes sur 12 907 (0,49 %), toutes comprises dans les 73 lignes de l'ANO-04
- **Cause probable** : annulations enregistrées sur des liaisons à 0 circulation prévue
- **Traitement retenu** : exclues avec l'ANO-04
- **Impact sur l'analyse** : aucun hors de ces lignes ; aucune ligne avec des circulations prévues supérieures à 0 n'a plus d'annulations que de circulations

## ANO-06 : valeur manquante déguisée en -1
- **Colonne(s)** : `Nombre trains en retard > 30min`
- **Description** : valeur -1 alors qu'un nombre de trains ne peut pas être négatif
- **Ampleur** : 16 lignes sur 12 907 (0,12 %) : janvier 2025 (9), février 2025 (3), mars 2025 (4)
- **Cause probable** : code « non renseigné » du producteur
- **Traitement retenu** : remplacé par une valeur manquante
- **Impact sur l'analyse** : ces lignes sont ignorées pour les retards de plus de 30 minutes

## ANO-07 : valeurs hors écart interquartile
- **Colonne(s)** : toutes les colonnes numériques de comptage, de retard et de causes
- **Description** : valeurs au-delà de 1,5 fois l'écart interquartile (méthode de repérage explicite)
- **Ampleur** : de 249 lignes (causes de retard liées à la gestion du trafic) à 1 382 lignes (trains annulés) selon la colonne, soit de 2 % à 11 % des lignes
- **Cause probable** : grandes liaisons, qui ont naturellement plus de trains, et événements réels (grèves, tempêtes, travaux)
- **Traitement retenu** : conservées et signalées, non supprimées
- **Impact sur l'analyse** : privilégier la médiane et les taux plutôt que les valeurs brutes

## ANO-08 : liaisons incomplètes dans le temps
- **Colonne(s)** : `Gare de départ`, `Gare d'arrivée`, `Date`
- **Description** : certaines liaisons n'apparaissent pas sur les 105 mois
- **Ampleur** : 16 liaisons sur 130 : 7 observées seulement 12 ou 13 mois, 2 observées 45 mois, 7 observées de 101 à 104 mois ; 114 liaisons sont complètes
- **Cause probable** : liaisons créées, supprimées ou suspendues au fil des années
- **Traitement retenu** : conservées ; les évolutions dans le temps sont comparées sur les 114 liaisons complètes
- **Impact sur l'analyse** : un classement sur toute la période mélange des liaisons observées plus ou moins longtemps

## ANO-09 : seuils de retard incohérents en 2025
- **Colonne(s)** : `Nombre trains en retard > 15min`, `> 30min`, `> 60min`
- **Description** : « > 60 min » supérieur à « > 30 min » dans 338 lignes (2,6 %), et « > 30 min » supérieur à « > 15 min » dans 3 lignes, alors qu'un seuil plus haut devrait compter moins de trains
- **Ampleur** : les 338 lignes sont toutes datées de 2025 ; la part des trains en retard de plus de 60 minutes parmi ceux en retard de plus de 30 minutes vaut entre 32 % et 41 % chaque année, sauf 66 % en 2025 (13 167 sur 19 944)
- **Cause probable** : erreur ou changement de définition dans la source en 2025, non expliqué dans la documentation du producteur (à vérifier auprès du producteur)
- **Traitement retenu** : signalé ; ces trois colonnes ne servent pas à comparer 2025 avec les autres années ; les retards sont mesurés avec `Nombre de trains en retard à l'arrivée`
- **Impact sur l'analyse** : les retards de plus de 60 minutes de 2025 ne sont pas comparables aux autres années ; les valeurs -1 de l'ANO-06 sont aussi datées de 2025

## ANO-10 : causes de retard qui ne totalisent pas 100 %
- **Colonne(s)** : les 6 colonnes `Prct retard pour cause ...`
- **Description** : somme des causes éloignée de 100 de plus d'un point alors qu'il y a des trains en retard à l'arrivée
- **Ampleur** : 89 lignes sur 12 907 (0,69 %) : 80 lignes ont toutes leurs causes à 0, les 9 autres ont une somme non nulle inférieure à 98,6
- **Cause probable** : causes non renseignées par le producteur
- **Traitement retenu** : conservées ; la répartition des causes est calculée sur les lignes dont la somme est proche de 100
- **Impact sur l'analyse** : la répartition des causes porte sur un sous-ensemble de lignes

## Contrôles réalisés sans anomalie
- Doublons exacts : 0
- Doublons fonctionnels (même mois, même liaison) : 0
- Dates illisibles : 0
- Mois absents entre le premier et le dernier mois : 0
- Trains en retard à l'arrivée supérieurs aux circulations prévues : 0
- Pourcentages de causes hors de [0 ; 100] : 0
- Gares de départ ou d'arrivée notées `0` ou vides : 0