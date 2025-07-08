import os
import time
import requests
from dotenv import load_dotenv
from typing import Any
from duckduckgo_search import DDGS

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

class WebSearchTool:
    def __init__(self):
        self.ddgs = DDGS()

    def search(self, query: str) -> str:
        """
        Tente une recherche avec DuckDuckGo. Si échec, fallback sur Serper API (Google).
        """
        try:
            time.sleep(1.5)  # pour limiter les requêtes trop fréquentes
            results = list(self.ddgs.text(query, max_results=5))
            if not results:
                raise Exception("Aucun résultat DuckDuckGo.")
            return self._format_duckduckgo_results(query, results)
        
        except Exception as e:
            fallback_result = self._fallback_serper(query)
            return fallback_result or f"Erreur lors des recherches web : {e}"

    def _format_duckduckgo_results(self, query: str, results: list[dict]) -> str:
        output = f"🔍 Résultats DuckDuckGo pour '{query}' :\n\n"
        for i, res in enumerate(results, 1):
            title = res.get("title", "Sans titre")
            snippet = res.get("body", "Pas de description.")
            link = res.get("href", "#")
            output += f"{i}. **{title}**\n   {snippet}\n   🔗 {link}\n\n"
        return output

    def _fallback_serper(self, query: str) -> str:
        """
        Recherche via Serper (https://serper.dev) si DuckDuckGo échoue.
        """
        if not SERPER_API_KEY:
            return "❌ Serper API Key non trouvée dans l'environnement."

        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            results = data.get("organic", [])

            if not results:
                return "Aucun résultat trouvé via Serper."

            output = f"🔍 Résultats Serper (Google) pour '{query}' :\n\n"
            for i, res in enumerate(results[:5], 1):
                title = res.get("title", "Sans titre")
                snippet = res.get("snippet", "Pas de description.")
                link = res.get("link", "#")
                output += f"{i}. **{title}**\n   {snippet}\n   🔗 {link}\n\n"
            return output

        except Exception as e:
            return f"❌ Erreur Serper API : {str(e)}"
