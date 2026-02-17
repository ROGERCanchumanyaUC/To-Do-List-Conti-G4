from src.modelo.modelo import Database
from src.modelo.task import Task

class TaskManager:
    def __init__(self):
        self.db = Database()
    
    def create_task(self, title, description=""):
        if not title or title.strip() == "":
            raise ValueError("El título de la tarea no puede estar vacío")
        
        task = Task(title=title.strip(), description=description.strip())
        
        query = '''
            INSERT INTO tasks (title, description, completed, created_at)
            VALUES (?, ?, ?, ?)
        '''
        task_id = self.db.execute_query(
            query, 
            (task.title, task.description, int(task.completed), task.created_at)
        )
        task.id = task_id
        return task
    
    def delete_task(self, task_id):
        if task_id is None or task_id <= 0:
            raise ValueError("ID de tarea inválido")
        
        task = self.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"No existe una tarea con ID {task_id}")
        
        query = "DELETE FROM tasks WHERE id = ?"
        self.db.execute_query(query, (task_id,))
        return True
    
    def get_all_tasks(self):
        query = "SELECT * FROM tasks ORDER BY created_at DESC"
        rows = self.db.fetch_all(query)
        tasks = []
        for row in rows:
            task = Task(
                id=row['id'],
                title=row['title'],
                description=row['description'],
                completed=bool(row['completed']),
                created_at=row['created_at']
            )
            tasks.append(task)
        return tasks
    
    def get_task_by_id(self, task_id):
        query = "SELECT * FROM tasks WHERE id = ?"
        row = self.db.fetch_one(query, (task_id,))
        if row:
            return Task(
                id=row['id'],
                title=row['title'],
                description=row['description'],
                completed=bool(row['completed']),
                created_at=row['created_at']
            )
        return None