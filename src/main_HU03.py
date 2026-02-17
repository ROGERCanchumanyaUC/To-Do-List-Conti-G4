from src.logica.task_manager import TaskManager

def main():
    manager = TaskManager()
    
    print("=== OOPRA - Gestor de Tareas ===\n")
    
    print("Creando tareas...")
    task1 = manager.create_task("Completar proyecto OOPRA", "Implementar todas las HU")
    task2 = manager.create_task("Estudiar para examen", "Repasar SO y Redes")
    task3 = manager.create_task("Hacer ejercicio", "30 min de cardio")
    
    print(f"✓ Tarea creada: {task1}")
    print(f"✓ Tarea creada: {task2}")
    print(f"✓ Tarea creada: {task3}")
    
    print("\n=== Todas las Tareas ===")
    all_tasks = manager.get_all_tasks()
    for task in all_tasks:
        print(task)
    
    query = "UPDATE tasks SET completed = 1 WHERE id = ?"
    manager.db.execute_query(query, (task1.id,))
    
    print("\n=== Tareas Completadas ===")
    completed_tasks = manager.get_completed_tasks()
    for task in completed_tasks:
        print(task)
    
    print("\n=== Tareas Pendientes ===")
    pending_tasks = manager.get_pending_tasks()
    for task in pending_tasks:
        print(task)

if __name__ == "__main__":
    main()
