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
    
    print("\n=== Lista de Tareas (Todas Pendientes) ===")
    tasks = manager.get_all_tasks()
    for task in tasks:
        print(task)
    
    print(f"\n=== Marcando tarea ID {task2.id} como completada ===")
    completed_task = manager.mark_as_completed(task2.id)
    print(f"✓ Tarea completada: {completed_task}")
    
    print("\n=== Lista de Tareas Actualizada ===")
    tasks = manager.get_all_tasks()
    for task in tasks:
        print(task)

if __name__ == "__main__":
    main()
