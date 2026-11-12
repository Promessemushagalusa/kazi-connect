# KAZI Connect

Bot WhatsApp qui connecte travailleurs et employeurs, en français, swahili et lingala.
Projet en cours de développement, à Lubumbashi (RDC).

## Fonctionnalités
- Choix de la langue (français, Kiswahili, Lingala)
- Mémoire de la langue choisie par chaque utilisateur
- Webhook WhatsApp Cloud API avec Flask

## À venir
- Inscription des travailleurs (nom, métier, ville)
- Recherche pour les employeurs
- Base de données

## Prérequis
- Python 3
- Un compte Meta for Developers avec WhatsApp Cloud API

## Installation
```
py -m pip install flask requests python-dotenv
```
Copie `.env.example` en `.env` et remplis tes valeurs.

## Lancer
```
py app.py
```