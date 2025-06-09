# 🤖 Bot Discord : Scan, Citations & Encouragements

![Python](https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

Un bot Discord multi-fonction :

- 🔍 Scanne les fichiers avec l’API **VirusTotal**
- 📖 Génère des citations inspirantes via **ZenQuotes**
- 💬 Envoie des **messages d'encouragement** en détectant certains mots
- ➕ Permet aux utilisateurs d’ajouter leurs propres messages positifs

---

## ✨ Fonctions disponibles

### 🔐 `$scan`  
Envoie un fichier à analyser avec **VirusTotal**.

> ⚠️ Si vous n’avez pas **Discord Nitro**, vous ne pouvez pas envoyer de fichiers de plus de **5 Mo**.

---

### 📖 `$inspire`  
Génère une **citation inspirante** aléatoire.

---

### 💬 `$new <message>`  
Ajoute un **nouveau message encourageant** à la base de données du bot.

---

### 💡 Réponses automatiques  
Le bot détecte des mots comme **“triste”**, **“malheureux”**, **“dépression”**, etc.  
➡️ Et répond automatiquement avec un message positif.

---

## ⚙️ Configuration

Créez un fichier `.env` à la racine du projet, basé sur `.env.example`, avec les vraies clés :

```env
TOKEN=votre_clé_discord_ici
VT_API_KEY=votre_clé_virustotal_ici
