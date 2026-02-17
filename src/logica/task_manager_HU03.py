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
    
    def get_completed_tasks(self):
        query = "SELECT * FROM tasks WHERE completed = 1 ORDER BY created_at DESC"
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
    
    def get_pending_tasks(self):
        query = "SELECT * FROM tasks WHERE completed = 0 ORDER BY created_at DESC"
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
