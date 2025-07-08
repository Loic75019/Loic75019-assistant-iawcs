import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document

class EnhancedMemoryManager:
    def __init__(self, memory_file: str = "conversation_memory.json"):
        self.memory_file = memory_file
        self.conversations = self._load_memory()
        self.embeddings = OpenAIEmbeddings()
        self.memory_index = None
        self._build_memory_index()
    
    def add_message(self, role: str, content: str):
        """
        Ajoute un message à la mémoire
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "session_id": self._get_current_session()
        }
        
        self.conversations.append(message)
        self._save_memory()
        self._update_memory_index(message)
    
    def search_memory(self, query: str, k: int = 3) -> str:
        """
        Recherche dans l'historique des conversations
        """
        if not self.memory_index:
            return "Aucun historique disponible pour la recherche."
        
        try:
            # Recherche de similarité
            results = self.memory_index.similarity_search(query, k=k)
            
            if not results:
                return f"Aucun résultat trouvé pour : {query}"
            
            response = f"🧠 Recherche dans la mémoire pour '{query}':\n\n"
            
            for i, doc in enumerate(results, 1):
                metadata = doc.metadata
                response += f"{i}. **{metadata.get('role', 'Unknown')}** "
                response += f"({metadata.get('timestamp', 'Date inconnue')})\n"
                response += f"   {doc.page_content[:200]}...\n\n"
            
            return response
            
        except Exception as e:
            return f"Erreur lors de la recherche en mémoire : {str(e)}"
    
    def get_recent_messages(self, limit: int = 10) -> List[Dict]:
        """
        Récupère les messages récents
        """
        return self.conversations[-limit:] if self.conversations else []
    
    def clear_memory(self):
        """
        Efface toute la mémoire
        """
        self.conversations = []
        self.memory_index = None
        if os.path.exists(self.memory_file):
            os.remove(self.memory_file)
    
    def _build_memory_index(self):
        """
        Construit l'index vectoriel de la mémoire
        """
        if not self.conversations:
            return
        
        try:
            documents = []
            for msg in self.conversations:
                doc = Document(
                    page_content=msg["content"],
                    metadata={
                        "role": msg["role"],
                        "timestamp": msg["timestamp"],
                        "session_id": msg.get("session_id", "unknown")
                    }
                )
                documents.append(doc)
            
            if documents:
                self.memory_index = FAISS.from_documents(documents, self.embeddings)
        
        except Exception as e:
            print(f"Erreur lors de la construction de l'index mémoire : {e}")
    
    def _update_memory_index(self, message: Dict):
        """
        Met à jour l'index avec un nouveau message
        """
        try:
            doc = Document(
                page_content=message["content"],
                metadata={
                    "role": message["role"],
                    "timestamp": message["timestamp"],
                    "session_id": message.get("session_id", "unknown")
                }
            )
            
            if self.memory_index:
                # Ajouter le document à l'index existant
                self.memory_index.add_documents([doc])
            else:
                # Créer un nouvel index
                self.memory_index = FAISS.from_documents([doc], self.embeddings)
        
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'index : {e}")
    
    def _load_memory(self) -> List[Dict]:
        """
        Charge la mémoire depuis le fichier
        """
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_memory(self):
        """
        Sauvegarde la mémoire dans le fichier
        """
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversations, f, ensure_ascii=False, indent=2)
    
    def _get_current_session(self) -> str:
        """
        Génère un ID de session basé sur la date
        """
        return datetime.now().strftime("%Y%m%d_%H")