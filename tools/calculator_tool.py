import math
import re
from typing import Union

class CalculatorTool:
    def __init__(self):
        # Fonctions mathématiques sûres
        self.safe_functions = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
            'log': math.log, 'log10': math.log10, 'ln': math.log,
            'sqrt': math.sqrt, 'abs': abs, 'ceil': math.ceil,
            'floor': math.floor, 'round': round, 'pi': math.pi,
            'e': math.e, 'exp': math.exp, 'pow': pow
        }
    
    def calculate(self, expression: str) -> str:
        """
        Effectue des calculs mathématiques sécurisés
        """
        try:
            # Nettoyage de l'expression
            expression = expression.strip()
            
            # Remplacement des fonctions
            for func_name, func in self.safe_functions.items():
                if isinstance(func, (int, float)):  # Constantes
                    expression = expression.replace(func_name, str(func))
                else:  # Fonctions
                    expression = re.sub(
                        rf'\b{func_name}\s*\(',
                        f'self.safe_functions["{func_name}"](',
                        expression
                    )
            
            # Évaluation sécurisée
            # On utilise eval mais avec un environnement restreint
            allowed_names = {
                "__builtins__": {},
                "self": self,
                **self.safe_functions
            }
            
            result = eval(expression, allowed_names)
            
            return f"🧮 Calcul: {expression}\n📊 Résultat: {result}"
            
        except ZeroDivisionError:
            return "❌ Erreur: Division par zéro"
        except ValueError as e:
            return f"❌ Erreur de valeur: {str(e)}"
        except SyntaxError:
            return "❌ Erreur: Expression mathématique invalide"
        except Exception as e:
            return f"❌ Erreur de calcul: {str(e)}"