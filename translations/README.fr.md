<div align="center">

<img src="/docs/logo.webp" alt="NeoVideoLingo Logo" height="140">

# Connecter chaque frame du monde

<a href="https://trendshift.io/repositories/12200" target="_blank"><img src="https://trendshift.io/api/badge/repositories/12200" alt="Huanshere%2FVideoLingo | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[**English**](/translations/README.en.md)｜[**简体中文**](/README.md)｜[**繁體中文**](/translations/README.zh-TW.md)｜[**日本語**](/translations/README.ja.md)｜[**Español**](/translations/README.es.md)｜[**Русский**](/translations/README.ru.md)｜[**Français**](/translations/README.fr.md)

</div>

Version basée sur le développement secondaire de [Huanshere/VideoLingo](https://github.com/Huanshere/VideoLingo).  
Pour les fonctionnalités et la documentation complètes de la version originale, veuillez consulter [le dépôt original](https://github.com/Huanshere/VideoLingo).

## Introduction
NeoVideoLingo : Outil de localisation vidéo tout-en-un de haute qualité

🎥 Traitement intelligent : Intégration de yt-dlp pour le téléchargement, reconnaissance par WhisperX / Parakeet, segmentation précise des sous-titres via algorithmes NLP.

📝 Traduction parfaite : Adopte un processus en trois étapes "traduction littérale-réflexion-traduction libre", combiné à une base de terminologie personnalisée, pour éviter toute sensation de traduction automatique.

✅ Expérience visuelle : Application stricte des normes de sous-titres Netflix, garantissant que chaque phrase soit affichée sur une seule ligne, sans effort de lecture.

🗣️ Synthèse vocale : Support indextts2.0 bientôt disponible.

🚀 Opération pratique : Interface Streamlit avec lancement en un clic, journalisation complète du processus, support de l'interruption et de la reprise à tout moment.

## Prise en charge des langues
Prise en charge des langues d'entrée :

🇨🇳 Chinois | 🇺🇸 Anglais | 🇷🇺 Russe | 🇫🇷 Français | 🇩🇪 Allemand | 🇮🇹 Italien | 🇪🇸 Espagnol | 🇯🇵 Japonais | 🇧🇬 Bulgare | 🇭🇷 Croate | 🇨🇿 Tchèque | 🇩🇰 Danois | 🇳🇱 Néerlandais | 🇪🇪 Estonien | 🇫🇮 Finnois | 🇬🇷 Grec | 🇭🇺 Hongrois | 🇱🇻 Letton | 🇱🇹 Lituanien | 🇲🇹 Maltais | 🇵🇱 Polonais | 🇵🇹 Portugais | 🇷🇴 Roumain | 🇸🇰 Slovaque | 🇸🇮 Slovène | 🇸🇪 Suédois | 🇺🇦 Ukrainien

## Mises à jour récentes

Janvier 2026
- Mise à jour des dépendances - y compris l'ancienne version d'av qui causait des erreurs
- Optimisation du script d'installation automatique des dépendances
- Mise à jour de la méthode de réglage de la largeur Streamlit/nouvelle largeur d'icône
- Ajout de la fonctionnalité pour obtenir les modèles disponibles
- Maintenance automatique des fichiers de traduction
- Modification de la couleur de police des boutons
- Interrupteur RoFormer dans la barre latérale
- Mise à jour vers la dernière version de WhisperX
- Remplacement de Demucs par BS-RoFormer

Décembre 2025
- Masquage de la barre de progression du téléchargement YouTube
- Correction des erreurs de chemin

Novembre 2025
- Correction des erreurs de chemin
- Correction des erreurs de séparation par deux-points
- Correction de l'image de couverture
- Activation du mode headless

Octobre 2025
- Correction du problème d'échec d'alignement
- Prise en charge de la transcription Parakeet
**https://github.com/lost0427/parakeet-api-vl**

Septembre 2025
- Correction de l'archivage vers history
- Mise à jour des paramètres WhisperX
- Mise à jour des mots-clés forts
- Proxy de l'image de couverture
- Affichage des formats standard et maximum de l'image de couverture
- Correction du problème de couleur d'arrière-plan des métadonnées
- Traitement des shorts YouTube
- Script de service Windows
- Paramètres VAD personnalisés
- Conversion des heures de publication
- Modifications du style des images et du texte
- Bouton de téléchargement vidéo
- Prise en charge de youtu.be
- Nettoyage des liens YouTube
- Mise à jour des traductions des options
- Interrupteur d'affichage des informations vidéo YouTube
- Interrupteur optionnel pour le téléchargement h264 (mp4)
- Affichage des informations et de l'image de couverture de la vidéo YouTube
- Interdiction d'exécuter plusieurs instances WhisperX simultanément
- Interdiction des erreurs dues à l'exécution simultanée de plusieurs instances demucs
- Fichier de configuration exemple pour l'authentification multi-utilisateurs
- Ajout d'un système de connexion utilisateur, prise en charge multi-utilisateurs initialement terminée

## Remarque

Ce dépôt ne maintient pas la partie doublage

## Méthode d'installation

```
conda create -n videolingo python==3.11.13
conda activate videolingo
python ./install.py
```