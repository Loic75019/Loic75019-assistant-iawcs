import os
import shlex
import pdfplumber
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

class DocumentReaderTool:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.vectorstore = None
        self.current_doc = None
        self.llm = ChatOpenAI(temperature=0.3)

    def read_document(self, query: str) -> str:
        """
        Lit un document PDF et répond aux questions dessus.
        Format attendu : "file:chemin/vers/fichier.pdf question optionnelle"
        """
        try:
            # Parsing plus robuste
            file_path, question = self._parse_query(query)
            
            if not file_path:
                return "❌ Format attendu : 'file:chemin/vers/fichier.pdf question optionnelle'"

            # Vérification de l'existence du fichier
            if not os.path.exists(file_path):
                return f"❌ Fichier non trouvé : {file_path}"

            # Vérification de l'extension
            if not file_path.lower().endswith('.pdf'):
                return "❌ Seuls les fichiers PDF sont supportés."

            # Extraction du texte
            text_content = self._extract_pdf_text(file_path)
            if not text_content.strip():
                return "❌ Le texte du PDF est vide ou non lisible."

            # Création de la base vectorielle
            documents = self._create_documents(text_content, file_path)
            self.vectorstore = FAISS.from_documents(documents, self.embeddings)
            self.current_doc = file_path

            # Génération de la réponse
            response = self._generate_response(question, os.path.basename(file_path))
            return response

        except Exception as e:
            return f"❌ Erreur lors de l'analyse du document : {str(e)}"

    def _parse_query(self, query: str) -> tuple[Optional[str], str]:
        """
        Parse la requête pour extraire le chemin du fichier et la question
        """
        try:
            if not query.startswith("file:"):
                return None, ""
            
            # Supprime le préfixe "file:"
            query_without_prefix = query[5:]
            
            # Utilise shlex pour gérer les espaces dans les chemins
            parts = shlex.split(query_without_prefix)
            
            if not parts:
                return None, ""
            
            file_path = parts[0]
            question = " ".join(parts[1:]) if len(parts) > 1 else "Fais un résumé détaillé de ce document"
            
            return file_path, question
            
        except Exception:
            # Si shlex échoue, essaie un parsing simple
            query_without_prefix = query[5:].strip()
            if ' ' in query_without_prefix:
                # Trouve le premier espace après l'extension .pdf
                pdf_end = query_without_prefix.find('.pdf')
                if pdf_end != -1:
                    pdf_end += 4  # Ajoute la longueur de '.pdf'
                    file_path = query_without_prefix[:pdf_end]
                    question = query_without_prefix[pdf_end:].strip()
                    return file_path, question if question else "Fais un résumé détaillé de ce document"
            
            return query_without_prefix, "Fais un résumé détaillé de ce document"

    def _extract_pdf_text(self, file_path: str) -> str:
        """
        Extraction du texte d'un PDF via pdfplumber
        """
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num} ---\n{page_text}\n"
                    except Exception as e:
                        print(f"Erreur sur la page {page_num}: {e}")
                        continue
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction PDF : {str(e)}")

    def _create_documents(self, text: str, source: str) -> List[Document]:
        """
        Divise le texte en chunks pour la vectorisation
        """
        chunks = self.text_splitter.split_text(text)
        documents = []
        
        for i, chunk in enumerate(chunks):
            if chunk.strip():  # Ignore les chunks vides
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "source": source,
                        "chunk": i,
                        "total_chunks": len(chunks)
                    }
                )
                documents.append(doc)
        
        return documents

    def _generate_response(self, question: str, filename: str) -> str:
        """
        Génère une réponse contextuelle basée sur le document
        """
        try:
            # Utilise RetrievalQA pour une réponse plus intelligente
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": 4}),
                return_source_documents=True
            )
            
            # Améliore la question pour un meilleur contexte
            enhanced_question = f"""
            Basé sur le document '{filename}', réponds à la question suivante de manière détaillée et structurée.
            
            Question: {question}
            
            Assure-toi de:
            1. Donner une réponse complète et précise
            2. Utiliser des exemples du document si pertinents
            3. Structurer ta réponse clairement
            4. Mentionner si certaines informations ne sont pas disponibles dans le document
            """
            
            result = qa_chain({"query": enhanced_question})
            
            response = f"📄 **Analyse du document :** *{filename}*\n\n"
            response += f"**Question posée :** {question}\n\n"
            response += f"**Réponse :**\n\n{result['result']}\n\n"
            
            # Ajoute des informations sur les sources si disponibles
            if 'source_documents' in result and result['source_documents']:
                response += f"**Sources utilisées :** {len(result['source_documents'])} sections du document\n"
            
            return response
            
        except Exception as e:
            # Fallback sur la méthode simple si RetrievalQA échoue
            return self._simple_response(question, filename)

    def _simple_response(self, question: str, filename: str) -> str:
        """
        Méthode de fallback pour générer une réponse simple
        """
        try:
            # Recherche de similarité simple
            relevant_docs = self.vectorstore.similarity_search(question, k=3)
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            response = f"📄 **Analyse du document :** *{filename}*\n\n"
            response += f"**Question posée :** {question}\n\n"
            response += f"**Contenu pertinent trouvé :**\n\n{context[:2000]}"
            
            if len(context) > 2000:
                response += "\n\n... (contenu tronqué)"
            
            return response
            
        except Exception as e:
            return f"❌ Erreur lors de la génération de la réponse : {str(e)}"

    def get_document_info(self) -> str:
        """
        Retourne des informations sur le document actuellement chargé
        """
        if not self.current_doc:
            return "Aucun document chargé."
        
        return f"Document actuel : {os.path.basename(self.current_doc)}"