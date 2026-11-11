# 🧬 Jumeau Numérique de Bioréacteur (Bioreactor Digital Twin)

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![Dash](https://img.shields.io/badge/Dash-2.14%2B-008080?logo=dash)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?logo=plotly)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green)

Plateforme d'ingénierie des bioprocédés pour le **suivi dynamique en temps réel**, la **simulation cinétique** (modèle de Monod / systèmes EDO) et la **visualisation 3D interactive** d'un bioréacteur de culture cellulaire.

---

## 📸 Aperçu de l'Interface

* **Schéma Réacteur 3D Vectoriel (SVG/CSS)** : Baie vitrée cylindrique en verre feuilleté avec dégradés de reflets spéculaires, graduations gravées, surface fluide sinusoïdale animée par effet de vague et rotation dynamique des pales de la turbine selon le régime RPM.
* **Panneau d'Analyse Cinétique Temps Réel** : Graphiques Plotly haute performance intégrant le lissage `uirevision` pour un suivi continu sans sauts d'image ni clignotements.
* **Pupitre de Commande Opérationnelle** : Ajustement à la volée des régimes d'agitation, du débit d'alimentation du substrat (*Fed-Batch*) et des concentrations entrantes.

---

## ✨ Fonctionnalités Principales

### 🔬 1. Moteur de Simulation Cinétique & Modélisation (ODE Engine)
* **Modèle de Monod étendu** pour le calcul de la croissance cellulaire, la consommation de substrat et la formation de produit biopharmaceutique.
* **Bilan d'oxygène dissous (DO)** dépendant du coefficient de transfert de matière $k_L a$ (couplé au régime d'agitation RPM).
* **Modes de conduite opératoire** :
  * **Batch (Cuvée)** : Évolution cinétique en système clos.
  * **Fed-Batch (Semi-continu)** : Maintien de la croissance par apport d'alimentation $F_{in}(t)$ et substrat $S_{in}$.
* **Résolution numérique des équations différentielles (ODE)** via le module `core/twin_engine.py`.

### 🎨 2. Représentation Graphique 3D & Animation SVG
* **Baie vitrée cylindrique photoréaliste** générée dynamiquement en HTML/SVG.
* **Animation de vague sinusoïdale (CSS Keyframes)** simulant l'agitation de surface et les mouvements de fluide sans surcharger le DOM.
* **Modulation visuelle de l'état du milieu** :
  * Variation du niveau de liquide $(1\text{L} \rightarrow 5\text{L})$ en direct.
  * Indicateur visuel d'hypoxie/normoxie (changement de couleur du milieu selon la saturation en $DO$).
  * Mobile d'agitation (turbine de Rushton / hélice) animé en fréquence d'images fluide.

### 📊 3. Logging & Analytics Temps Réel
* Historisation dynamique de la simulation (`services/logger.py`) transformée en structures de données Pandas.
* Maintien du contexte visuel Plotly pour l'inspection interactive des courbes sans réinitialisation des axes.

### 🐳 4. Conteneurisation & Prêt pour la Production
* Configuration multi-stage **Docker** et orchestration **Docker Compose**.
* Exécution possible via serveur WSGI **Gunicorn** pour les déploiements industriels.

---

## 📐 Modélisation Mathématique

Le comportement biologique et physico-chimique du réacteur repose sur le système d'équations différentielles ordinaires (EDO) suivant :

### 1. Vitesse Spécifique de Croissance (Monod)
$$\mu(S) = \mu_{max} \cdot \frac{S}{K_S + S}$$

### 2. Bilans de Matière (Régime Fed-Batch)

$$\frac{dX}{dt} = \mu(S) \cdot X - \left(\frac{F_{in}}{V}\right) X$$

$$\frac{dS}{dt} = -\frac{1}{Y_{X/S}} \cdot \mu(S) \cdot X + \left(\frac{F_{in}}{V}\right) (S_{in} - S)$$

$$\frac{dP}{dt} = q_P \cdot X - \left(\frac{F_{in}}{V}\right) P$$

$$\frac{dV}{dt} = F_{in}$$

### 3. Transfert d'Oxygène Dissous ($DO$)

$$\frac{d(DO)}{dt} = k_L a(RPM) \cdot (DO^* - DO) - q_{O_2} \cdot X$$

---

## 🏗️ Architecture du Projet

Le projet adopte une structure modulaire respectant la séparation des responsabilités (SOC) :

```text
Bioreacteur/
├── core/
│   ├── __init__.py
│   └── twin_engine.py       # Moteur cinétique (Solveur EDO, équations de Monod)
├── services/
│   ├── __init__.py
│   └── logger.py            # Enregistrement et conversion des séries temporelles (Pandas)
├── ui/
│   ├── __init__.py
│   └── svg_bioreactor.py    # Générateur SVG 3D (Baie vitrée, vagues CSS, turbine)
├── app.py                   # Application principale Dash & Callbacks temps réel
├── requirements.txt         # Dépendances Python
├── Dockerfile               # Configuration de conteneurisation
├── docker-compose.yml       # Orchestration des services
└── README.md                # Documentation globale du projet
