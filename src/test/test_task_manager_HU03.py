import unittest
import os
from src.logica.task_manager import TaskManager
from src.modelo.modelo import Database

class TestTaskManager(unittest.TestCase):
    
    def setUp(self):
        self.test_db = "test_DB.sqlite"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.db = Database(self.test_db)
        self.manager = TaskManager()
        self.manager.db = self.db
    
    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_create_task_success(self):
        task = self.manager.create_task("Estudiar Python", "Repasar POO")
        self.assertIsNotNone(task.id)
        self.assertEqual(task.title, "Estudiar Python")
    
    def test_get_all_tasks_empty(self):
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 0)
    
    def test_get_all_tasks_multiple(self):
        self.manager.create_task("Tarea 1", "Desc 1")
        self.manager.create_task("Tarea 2", "Desc 2")
        self.manager.create_task("Tarea 3", "Desc 3")
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 3)
    
    def test_get_completed_tasks(self):
        task1 = self.manager.create_task("Tarea completada")
        task2 = self.manager.create_task("Tarea pendiente")
        
        query = "UPDATE tasks SET completed = 1 WHERE id = ?"
        self.db.execute_query(query, (task1.id,))
        
        completed = self.manager.get_completed_tasks()
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0].id, task1.id)
    
    def test_get_pending_tasks(self):
        task1 = self.manager.create_task("Tarea completada")
        task2 = self.manager.create_task("Tarea pendiente")
        
        query = "UPDATE tasks SET completed = 1 WHERE id = ?"
        self.db.execute_query(query, (task1.id,))
        
        pending = self.manager.get_pending_tasks()
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].id, task2.id)
    
    def test_get_task_by_id(self):
        task = self.manager.create_task("Tarea específica")
        found = self.manager.get_task_by_id(task.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.title, "Tarea específica")
    
    def test_tasks_ordered_by_date(self):
        self.manager.create_task("Primera")
        self.manager.create_task("Segunda")
        self.manager.create_task("Tercera")
        tasks = self.manager.get_all_tasks()
        self.assertEqual(tasks[0].title, "Tercera")
        self.assertEqual(tasks[2].title, "Primera")

if __name__ == '__main__':
    unittest.main()
