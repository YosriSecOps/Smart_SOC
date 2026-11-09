# 🛡️ Smart SOC : Architecture Hybride, Multi-Agents et IA

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Wazuh](https://img.shields.io/badge/Wazuh-007AFF?style=for-the-badge&logo=wazuh&logoColor=white)
![Suricata](https://img.shields.io/badge/Suricata-EF3B2D?style=for-the-badge&logo=suricata&logoColor=white)
![Llama3](https://img.shields.io/badge/Llama3-0466C8?style=for-the-badge&logo=meta&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

Un Security Operations Center (SOC) autonome de nouvelle génération visant à éliminer l'"alert fatigue". Ce projet intègre une architecture XDR (Wazuh + Suricata), un pipeline SOAR en Python, et un agent IA interactif pilotable via Telegram.

## 🎯 Problématique & Solution
Les SOC traditionnels font face à une surcharge cognitive (ratio de 20:1) entraînant une latence de réponse critique. 
**Notre solution :** Un pipeline événementiel qui ingère, enrichit via un LLM (Ollama), et bloque automatiquement les menaces critiques en moins de 10 secondes sans intervention humaine.

## 🏗️ Topologie de l'Infrastructure
Le laboratoire est déployé sur VMware avec une segmentation réseau stricte (`Host-Only` isolé sur `192.168.56.0/24`) :
* **Serveur SOC (192.168.56.10) :** Wazuh Manager, Pipeline Python SOAR, LLM Agent (Llama3).
* **Machine Cible (192.168.56.20) :** Ubuntu Server surveillé par l'Agent Wazuh et Suricata IDS en mode haute performance `af-packet`.
* **Machine Attaquant (192.168.56.30) :** Kali Linux pour la simulation d'attaques (Nmap, brute-force Hydra).

## ✨ Fonctionnalités Principales
* **Collecte Asynchrone :** Lecture en flux continu des alertes SIEM avec haute tolérance aux pannes.
* **Réponse Automatique (SOAR) :** Isolation réseau (`iptables`) instantanée avec système de liste blanche (Whitelist).
* **Agent IA Contextuel :** Interrogation du SOC en langage naturel avec des commandes sécurisées (`ALLOWED_COMMANDS`) pour prévenir les hallucinations et l'injection.
* **Bot Telegram :** Notifications enrichies en temps réel et pilotage du SOC à distance 24/7.

## 📂 Structure du Projet

```text
Smart_SOC/
├── .env                  # Token de l'API Telegram (à configurer en local)
├── .gitignore            # Fichiers exclus de Git (cache, .env, venv)
├── README.md             # Documentation du projet
├── requirements.txt      # Dépendances Python isolées
├── src/                  # Code source du pipeline SOAR
│   ├── analyzer.py       # Parsing et Prompt Engineering
│   ├── collector.py      # Collecteur asynchrone d'alertes
│   ├── main.py           # Orchestrateur principal
│   ├── notifier.py       # Notifications Telegram
│   ├── responder.py      # Réponse active (iptables)
│   ├── soc_agent.py      # Agent IA interactif (Ollama)
│   ├── telegram_agent.py # Interface conversationnelle Telegram
└── configs/              # Configurations des capteurs et de l'infrastructure
    ├── ubuntu_target/    # [192.168.56.20]
    │   ├── ossec.conf    # Paramétrage de l'Agent Wazuh
    │   └── suricata.yaml # Paramétrage du NIDS Suricata
    └── soc_server/       # [192.168.56.10]
        ├── ossec.conf    # Paramétrage du Manager Wazuh
        └── smart-soc.service # Daemon systemd du pipeline Python
'''
## 🚀 Installation & Exécution

1. **Cloner le dépôt :**
   ```bash
   git clone [https://github.com/YosriSecOps/Smart_SOC.git](https://github.com/YosriSecOps/Smart_SOC.git)
   cd Smart_SOC
   ```

2. **Configurer l'environnement virtuel et installer les dépendances :**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configurer la sécurité (Token) :**
   Créer un fichier `.env` à la racine pour sécuriser les identifiants :
   ```env
   TELEGRAM_TOKEN="VOTRE_TOKEN_TELEGRAM_ICI"
   ```

4. **Lancer l'orchestrateur (en environnement virtuel) :**
   ```bash
   python src/main.py
   ```

## 👥 Équipe du Projet
Ce travail a été réalisé par le futur ingénieur dans le cadre d'un Projet de Fin d'Année à **TEK-UP University** (Année Académique 2024-2025) :
* **Hamdouni Yosri**
Yosri Hamdouni ([@YosriSecOps](https://github.com/YosriSecOps)) 

