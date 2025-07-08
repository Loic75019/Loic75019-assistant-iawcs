Voici un exemple complet de **README.md** en français, parfaitement adapté à ton projet de chatbot IA personnel avec LangChain, Streamlit, mémoire conversationnelle, et outils intégrés :

---

# 🤖 Agent IA Personnel avec LangChain & Streamlit

Un assistant conversationnel intelligent, **amical** et **contextuel**, capable de :

* 💬 Mener une conversation fluide et personnalisée
* 🧠 Se souvenir du prénom et des infos de l'utilisateur
* 📄 Lire et analyser des fichiers PDF
* 🔍 Rechercher des infos sur Internet
* ✅ Gérer une liste de tâches
* 🧮 Faire des calculs

---

## 🚀 Démo rapide

```bash
streamlit run app.py
```

---

## 📦 Fonctionnalités

| Fonction                         | Description                                                      |
| -------------------------------- | ---------------------------------------------------------------- |
| 💬 **Chat contextuel**           | Conversation fluide avec mémoire (prénom, intentions, etc.)      |
| 🧠 **Mémoire conversationnelle** | Conservation des échanges récents et recherche dans l'historique |
| 📄 **Lecture de PDF**            | Posez des questions sur le contenu d’un fichier PDF              |
| 🔍 **Recherche Web**             | Utilisation de DuckDuckGo pour chercher des infos en direct      |
| ✅ **TODO list**                  | Ajouter, lister, supprimer ou terminer des tâches                |
| 🧮 **Calculatrice**              | Évaluation sécurisée d'expressions mathématiques                 |
| 🔁 **Commande `/reset`**         | Réinitialise mémoire et contexte utilisateur                     |

---

## 🧱 Stack technique

* [LangChain](https://www.langchain.com/) – orchestration LLM et mémoire
* [OpenAI GPT-3.5 / GPT-4](https://platform.openai.com/docs) – modèle de langage
* [Streamlit](https://streamlit.io/) – interface web légère
* [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/) – recherche web ou SERPER API
* [FAISS](https://github.com/facebookresearch/faiss) – indexation vectorielle pour la mémoire avancée
* [ChromaDB (optionnel)](https://www.trychroma.com/) – support vector stores

---

## 🛠️ Installation

### 1. Cloner le repo

```bash
git clone https://github.com/votre-utilisateur/agent-ia-personnel.git
cd agent-ia-personnel
```

### 2. Installer les dépendances

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sous Windows

pip install -r requirements.txt
```

### 3. Configurer l’API OpenAI

Créer un fichier `.env` :

```ini
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

---

## 🧪 Exemple de scénario

> Utilisateur : Salut, je m'appelle Loic
> Assistant : Enchanté Loic ! Comment puis-je t'aider aujourd'hui ?
> Utilisateur : J’aimerais apprendre à coder
> Assistant : Super Loic ! Python, ça te tente pour débuter ? 😊

---

## 📂 Structure du projet

```
.
├── app.py                         # Interface Streamlit
├── agent.py                       # Agent principal avec mémoire + outils
├── tools/                         # Tous les outils (PDF, TODO, calcul, recherche)
├── memory/                        # Mémoire avancée + gestion index FAISS
├── chat_history.json       # Historique sauvegardé
├── requirements.txt               # Dépendances
└── .env                           # Clé API OpenAI
```

---

## 🧠 Mémoire intégrée

* **ConversationBufferWindowMemory** : mémoire courte (10 derniers échanges)
* **Historique JSON** : sauvegarde complète de toutes les conversations
* **Recherche vectorielle** (FAISS) : permet à l'IA de "se rappeler" des infos passées

---

## ✨ Bonus possibles

* 🎭 Personnaliser le style du bot (formel, expert, humoristique…)
* 📝 Télécharger l’historique complet au format `.json`
* 🔗 Connecter à des sources de données personnelles (Notion, fichiers, etc.)
* 🎙️ Interface vocale avec `speech_recognition`

---

## 📜 Licence

MIT – libre à usage personnel ou pédagogique.

---

## 🙌 Remerciements

Ce projet a été réalisé dans le cadre d’un challenge LangChain pour développer un assistant IA intelligent, avec mémoire conversationnelle et fonctionnalités utiles.

---
