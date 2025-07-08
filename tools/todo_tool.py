import json
import os
from datetime import datetime
from typing import List, Dict

class TodoTool:
    def __init__(self, storage_file: str = "todo_list.json"):
        self.storage_file = storage_file
        self.todos = self._load_todos()
    
    def manage_todo(self, command: str) -> str:
        """
        Gère la liste de tâches
        Commandes:
        - add:Tâche à ajouter
        - list (affiche toutes les tâches)
        - done:ID (marque comme terminé)
        - remove:ID (supprime)
        """
        try:
            if command.startswith("add:"):
                task = command[4:].strip()
                return self._add_task(task)
            
            elif command == "list":
                return self._list_tasks()
            
            elif command.startswith("done:"):
                task_id = int(command[5:].strip())
                return self._mark_done(task_id)
            
            elif command.startswith("remove:"):
                task_id = int(command[7:].strip())
                return self._remove_task(task_id)
            
            else:
                return ("Commandes disponibles:\n"
                       "- add:Votre tâche\n"
                       "- list\n" 
                       "- done:ID\n"
                       "- remove:ID")
        
        except Exception as e:
            return f"Erreur dans la gestion des tâches : {str(e)}"
    
    def _add_task(self, task: str) -> str:
        new_task = {
            "id": len(self.todos) + 1,
            "task": task,
            "created": datetime.now().isoformat(),
            "completed": False
        }
        self.todos.append(new_task)
        self._save_todos()
        return f"✅ Tâche ajoutée : '{task}' (ID: {new_task['id']})"
    
    def _list_tasks(self) -> str:
        if not self.todos:
            return "📝 Aucune tâche dans votre liste."
        
        active_tasks = [t for t in self.todos if not t['completed']]
        completed_tasks = [t for t in self.todos if t['completed']]
        
        result = "📝 **Vos tâches:**\n\n"
        
        if active_tasks:
            result += "**À faire:**\n"
            for task in active_tasks:
                result += f"• [{task['id']}] {task['task']}\n"
        
        if completed_tasks:
            result += "\n**Terminées:**\n"
            for task in completed_tasks:
                result += f"• ✓ [{task['id']}] {task['task']}\n"
        
        return result
    
    def _mark_done(self, task_id: int) -> str:
        task = next((t for t in self.todos if t['id'] == task_id), None)
        if task:
            task['completed'] = True
            task['completed_date'] = datetime.now().isoformat()
            self._save_todos()
            return f"✅ Tâche {task_id} marquée comme terminée : '{task['task']}'"
        return f"❌ Tâche {task_id} non trouvée"
    
    def _remove_task(self, task_id: int) -> str:
        task = next((t for t in self.todos if t['id'] == task_id), None)
        if task:
            self.todos.remove(task)
            self._save_todos()
            return f"🗑️ Tâche supprimée : '{task['task']}'"
        return f"❌ Tâche {task_id} non trouvée"
    
    def _load_todos(self) -> List[Dict]:
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_todos(self):
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.todos, f, ensure_ascii=False, indent=2)