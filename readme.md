# 🤖 Assistant IA Personnel – LangChain + Streamlit + FastAPI

Un assistant conversationnel intelligent et polyvalent, capable de :

- 💬 Mener une conversation fluide et personnalisée
- 🧠 Mémoriser le prénom et le contexte utilisateur
- 📄 Lire et analyser des fichiers PDF
- 🔍 Rechercher des infos sur Internet
- ✅ Gérer une TODO-list
- 🧮 Faire des calculs
- 🌐 Répondre à distance via une API REST sécurisée

---

## 🚀 Démo publique

- Interface utilisateur (Streamlit) :  
  👉 http://15.237.160.172:8501

- API REST FastAPI :  
  👉 http://15.237.160.172:8000/docs (Swagger)

---

## 📦 Fonctionnalités

| Fonction               | Description |
|------------------------|-------------|
| 💬 Chat contextuel     | Mémoire de conversation et prénom |
| 🧠 Mémoire conversationnelle | Historique, FAISS, contexte |
| 📄 Lecture de PDF       | Posez des questions sur un PDF |
| 🔍 Recherche Web       | Recherche via DuckDuckGo |
| ✅ Liste de tâches     | Ajouter/supprimer des TODOs |
| 🧮 Calculatrice        | Calculs mathématiques |
| 🔐 API sécurisée par token | Accès REST protégé par `Authorization: Bearer` |

---

## 🛠️ Stack technique

- LangChain (agent, outils, mémoire)
- OpenAI GPT-3.5 / GPT-4
- Streamlit (interface utilisateur)
- FastAPI + Uvicorn (serveur API)
- DuckDuckGo Search API
- FAISS pour l’indexation vectorielle
- tmux pour garder le serveur actif après déconnexion

---

## 🧱 Déploiement sur une instance EC2 (Ubuntu)

### 1. 🧑‍💻 Cloner le projet

```bash
git clone https://github.com/Loic75019/Loic75019-assistant-iawcs.git
cd Loic75019-assistant-iawcs
```

### 2. 🐍 Créer un environnement Python

```bash
sudo apt update && sudo apt install python3.10-venv git curl tmux -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 🔐 Configurer les clés

Créer un fichier `.env` :

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxx
HUGGINGFACEHUB_API_TOKEN=hf_yyyyyyyyyyyyyy
API_TOKEN=xxx
```

> ⚠️ Ne jamais versionner ce fichier dans GitHub !

---

## 🌐 Lancer l'application

### Interface utilisateur (Streamlit)

```bash
tmux new -s streamlit
source venv/bin/activate
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Puis détacher avec `Ctrl + B`, puis `D`.

➡️ Accessible sur : `http://<IP>:8501`

---

### API REST (FastAPI)

```bash
tmux new -s api
source venv/bin/activate
uvicorn api:app --host 0.0.0.0 --port 8000
```

➡️ Accessible sur : `http://<IP>:8000/docs`

---

## 🧪 Tester l’API avec `curl`

```bash
curl -X POST http://<IP>:8000/ask \
  -H "Authorization: Bearer cle_secrete_api_assitant_wcs" \
  -H "Content-Type: application/json" \
  -d '{"question": "Quelle est la capitale de la France ?"}'
```

---

## 📂 Structure du projet

.
├── app.py                   # Interface Streamlit
├── api.py                   # API FastAPI sécurisée
├── agent.py                 # Agent principal avec outils
├── memory/                  # Mémoire FAISS et historique
├── tools/                   # Modules outils (PDF, web, calc, todo)
├── retriever/               # Gestion d’index vectoriel
├── requirements.txt         # Dépendances Python
├── .env.example             # Exemple de configuration
└── readme.md

---

## 🧠 Mémoire IA

- `ConversationBufferWindowMemory` : mémoire de chat courte
- `FAISS` : recherche vectorielle locale
- `conversation_memory.json` : historique JSON sauvegardé

---

## ✨ Bonus possibles

- 🔒 Ajouter authentification OAuth
- 🎤 Ajout interface vocale (speech recognition)
- 🧾 Export des conversations
- 🌍 Ajout d’un nom de domaine + HTTPS via nginx + certbot

---

## 📌 Arrêt / redémarrage EC2

- **Stop instance** : via AWS Console → Instances > Arrêter
- **Reprise** :

```bash
ssh -i aiwcs.pem ubuntu@<new_ip>
tmux attach -t streamlit   # Interface
tmux attach -t api         # API REST
```

---

## 📜 Licence

Projet open-source sous licence MIT – usage personnel ou pédagogique.
