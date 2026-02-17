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
    
    print("\n=== Lista de Tareas ===")
    tasks = manager.get_all_tasks()
    for task in tasks:
        print(task)
    
    print(f"\n=== Eliminando tarea ID {task2.id} ===")
    manager.delete_task(task2.id)
    print("✓ Tarea eliminada")
    
    print("\n=== Lista de Tareas Actualizada ===")
    tasks = manager.get_all_tasks()
    for task in tasks:
        print(task)

if __name__ == "__main__":
    main()