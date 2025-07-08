import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from langchain.agents import Tool, AgentExecutor, initialize_agent, AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import BaseMessage
from langchain_openai import ChatOpenAI
from langchain.callbacks import StreamlitCallbackHandler

from tools.search_tool import WebSearchTool
from tools.doc_reader import DocumentReaderTool
from tools.todo_tool import TodoTool
from tools.calculator_tool import CalculatorTool
from memory.memory_manager import EnhancedMemoryManager


load_dotenv()

class PersonalAIAgent:
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.7):
        """
        Agent IA personnel multitâche
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Gestionnaire de mémoire amélioré
        self.memory_manager = EnhancedMemoryManager()
        
        # Mémoire conversationnelle
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10  # Garde les 10 derniers échanges
        )
        
        # Initialisation des outils
        self.tools = self._initialize_tools()
        
        # Création de l'agent
        self.agent = self._create_agent()
        
    def _initialize_tools(self) -> List[Tool]:
        """
        Initialise tous les outils disponibles pour l'agent
        """
        web_search = WebSearchTool()
        doc_reader = DocumentReaderTool()
        todo_manager = TodoTool()
        calculator = CalculatorTool()
        
        tools = [
            Tool(
                name="web_search",
                description="Recherche d'informations sur internet. Utilise ce tool quand l'utilisateur demande des informations actuelles, des données spécifiques, ou des recherches web.",
                func=web_search.search
            ),
            Tool(
                name="document_reader",
                description="Lit et analyse des documents PDF. Utilise ce tool quand l'utilisateur mentionne un fichier PDF ou demande des informations sur un document.",
                func=doc_reader.read_document
            ),
            Tool(
                name="todo_manager",
                description="Gère une liste de tâches (TODO). Utilise ce tool pour ajouter, lister, marquer comme terminé ou supprimer des tâches.",
                func=todo_manager.manage_todo
            ),
            Tool(
                name="calculator",
                description="Effectue des calculs mathématiques simples ou complexes. Utilise ce tool pour tous types de calculs numériques.",
                func=calculator.calculate
            ),
            Tool(
                name="memory_search",
                description="Recherche dans l'historique des conversations précédentes. Utilise ce tool quand l'utilisateur fait référence à quelque chose mentionné précédemment.",
                func=self.memory_manager.search_memory
            )
        ]
        
        return tools
    
    def _create_agent(self) -> AgentExecutor:
        """
        Crée l'agent avec les outils et la mémoire
        """
        system_message = system_message = """Tu es un assistant IA personnel, amical et attentionné, toujours prêt à aider.

Tu te comportes comme un assistant humain bienveillant :
- Tu accueilles chaleureusement l'utilisateur
- Tu te souviens de son prénom et de ce qu'il te dit
- Tu poses des questions de suivi personnalisées
- Tu adoptes un ton convivial et empathique (ex : "Super idée !", "Génial Loic, voyons cela ensemble 😊")

Voici ce que tu peux faire :
- 📄 Lire et analyser des documents PDF
- 🔍 Rechercher des informations sur Internet
- 🧮 Effectuer des calculs
- ✅ Gérer une liste de tâches
- 💬 Converser naturellement et suivre le fil

Règles :
1. Rappelle-toi du prénom et des informations personnelles mentionnées
2. Ne répète pas tout le contexte, mais utilise-le naturellement
3. Ton style est chaleureux, engageant, jamais robotique
4. Si quelqu’un dit “je suis prof”, tu poses une question liée à ça
5. Commence souvent par le prénom de l’utilisateur si tu le connais

Exemples :
- Utilisateur : Je m'appelle Loic
- Assistant : Enchanté Loic ! Comment puis-je t'aider aujourd'hui ?
- Utilisateur : J'aimerais apprendre à coder
- Assistant : Super Loic ! Python, ça te tente pour débuter ? 😊
"""


        agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            agent_kwargs={
                "system_message": system_message
            }
        )
        
        return agent
    
    def chat(self, message: str, callback_handler=None) -> str:
        """
        Interface principale pour discuter avec l'agent
        """
        try:
            # Sauvegarde du message utilisateur
            self.memory_manager.add_message("user", message)
            
            # Traitement par l'agent
            if callback_handler:
                response = self.agent.run(input=message, callbacks=[callback_handler])
            else:
                response = self.agent.run(input=message)
            
            # Sauvegarde de la réponse
            self.memory_manager.add_message("assistant", response)
            
            return response
            
        except Exception as e:
            error_msg = f"Désolé, j'ai rencontré une erreur : {str(e)}"
            self.memory_manager.add_message("assistant", error_msg)
            return error_msg
    
    def get_conversation_history(self) -> List[Dict]:
        """
        Récupère l'historique de conversation
        """
        return self.memory_manager.get_recent_messages()
    
    def clear_memory(self):
        """
        Efface la mémoire conversationnelle
        """
        self.memory.clear()
        self.memory_manager.clear_memory()