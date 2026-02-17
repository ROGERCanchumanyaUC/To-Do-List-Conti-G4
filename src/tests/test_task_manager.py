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
    
    def test_delete_task_success(self):
        task = self.manager.create_task("Tarea a eliminar")
        result = self.manager.delete_task(task.id)
        self.assertTrue(result)
        deleted_task = self.manager.get_task_by_id(task.id)
        self.assertIsNone(deleted_task)
    
    def test_delete_task_invalid_id(self):
        with self.assertRaises(ValueError):
            self.manager.delete_task(0)
    
    def test_delete_task_nonexistent(self):
        with self.assertRaises(ValueError):
            self.manager.delete_task(9999)
    
    def test_delete_task_null_id(self):
        with self.assertRaises(ValueError):
            self.manager.delete_task(None)
    
    def test_get_all_tasks_after_delete(self):
        task1 = self.manager.create_task("Tarea 1")
        task2 = self.manager.create_task("Tarea 2")
        task3 = self.manager.create_task("Tarea 3")
        
        self.manager.delete_task(task2.id)
        
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        task_ids = [t.id for t in tasks]
        self.assertIn(task1.id, task_ids)
        self.assertIn(task3.id, task_ids)
        self.assertNotIn(task2.id, task_ids)

if __name__ == '__main__':
    unittest.main()