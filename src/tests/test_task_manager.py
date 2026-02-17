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
        self.assertEqual(task.description, "Repasar POO")
        self.assertFalse(task.completed)
    
    def test_create_task_empty_title(self):
        with self.assertRaises(ValueError):
            self.manager.create_task("")
    
    def test_create_task_whitespace_title(self):
        with self.assertRaises(ValueError):
            self.manager.create_task("   ")
    
    def test_create_task_no_description(self):
        task = self.manager.create_task("Tarea sin descripción")
        self.assertEqual(task.description, "")
    
    def test_get_all_tasks(self):
        self.manager.create_task("Tarea 1", "Desc 1")
        self.manager.create_task("Tarea 2", "Desc 2")
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 2)
    
    def test_get_task_by_id(self):
        task = self.manager.create_task("Encontrar esta tarea")
        found_task = self.manager.get_task_by_id(task.id)
        self.assertIsNotNone(found_task)
        self.assertEqual(found_task.title, "Encontrar esta tarea")

if __name__ == '__main__':
    unittest.main()