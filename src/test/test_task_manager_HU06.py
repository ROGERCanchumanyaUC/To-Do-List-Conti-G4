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
    
    def test_mark_as_completed_success(self):
        task = self.manager.create_task("Tarea a completar")
        self.assertFalse(task.completed)
        
        completed_task = self.manager.mark_as_completed(task.id)
        self.assertTrue(completed_task.completed)
        
        found_task = self.manager.get_task_by_id(task.id)
        self.assertTrue(found_task.completed)
    
    def test_mark_as_completed_invalid_id(self):
        with self.assertRaises(ValueError):
            self.manager.mark_as_completed(0)
    
    def test_mark_as_completed_null_id(self):
        with self.assertRaises(ValueError):
            self.manager.mark_as_completed(None)
    
    def test_mark_as_completed_nonexistent(self):
        with self.assertRaises(ValueError):
            self.manager.mark_as_completed(9999)
    
    def test_mark_as_completed_already_completed(self):
        task = self.manager.create_task("Tarea")
        self.manager.mark_as_completed(task.id)
        
        with self.assertRaises(ValueError):
            self.manager.mark_as_completed(task.id)
    
    def test_get_all_tasks(self):
        task1 = self.manager.create_task("Tarea 1")
        task2 = self.manager.create_task("Tarea 2")
        self.manager.mark_as_completed(task1.id)
        
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        
        completed_count = sum(1 for t in tasks if t.completed)
        self.assertEqual(completed_count, 1)

if __name__ == '__main__':
    unittest.main()
