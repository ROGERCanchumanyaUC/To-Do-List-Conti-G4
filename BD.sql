PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- Usuarios (HU01)
INSERT OR IGNORE INTO usuarios (username, password_hash)
VALUES
  ('admin', 'hash_demo_admin'),
  ('usuario1', 'hash_demo_usuario1');

-- Tareas (HU02–HU06) - completada 0/1
INSERT OR IGNORE INTO tareas (id_usuario, titulo, descripcion, completada)
VALUES
  (
    (SELECT id_usuario FROM usuarios WHERE username = 'admin'),
    'Comprar pan',
    'Ir a la tienda y comprar pan',
    0
  ),
  (
    (SELECT id_usuario FROM usuarios WHERE username = 'admin'),
    'Estudiar Python',
    'Repasar unittest y TDD',
    0
  ),
  (
    (SELECT id_usuario FROM usuarios WHERE username = 'admin'),
    'Hacer ejercicio',
    'Caminar 30 minutos',
    1
  );

COMMIT;
