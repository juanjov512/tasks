INSERT INTO users (email, username, created_at, updated_at) VALUES
('user1@example.com', 'johndoe', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('user2@example.com', 'janedoe', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO categories (name, color, created_at) VALUES
('Trabajo', '#3b82f6', CURRENT_TIMESTAMP),
('Personal', '#10b981', CURRENT_TIMESTAMP),
('Estudio', '#f59e0b', CURRENT_TIMESTAMP);

INSERT INTO labels (name, color, created_at) VALUES
('Urgente', '#ef4444', CURRENT_TIMESTAMP),
('Importante', '#f97316', CURRENT_TIMESTAMP),
('Proyecto', '#8b5cf6', CURRENT_TIMESTAMP);

INSERT INTO tasks (user_id, category_id, title, content, due_date, status, priority, created_at, updated_at)
VALUES (
  (SELECT id FROM users WHERE email = 'user1@example.com'),
  (SELECT id FROM categories WHERE name = 'Trabajo'),
  'Terminar informe mensual',
  'Completar las gráficas y conclusiones',
  '2023-12-15T18:00:00',
  'in_progress',
  'high',
  CURRENT_TIMESTAMP,
  CURRENT_TIMESTAMP
),
(
  (SELECT id FROM users WHERE email = 'user2@example.com'),
  (SELECT id FROM categories WHERE name = 'Personal'),
  'Comprar regalos navideños',
  'Libro para papá, perfume para mamá',
  '2023-12-20T14:00:00',
  'pending',
  'medium',
  CURRENT_TIMESTAMP,
  CURRENT_TIMESTAMP
);

INSERT INTO task_labels (task_id, label_id)
VALUES (
  (SELECT id FROM tasks WHERE title = 'Terminar informe mensual'),
  (SELECT id FROM labels WHERE name = 'Urgente')
),
(
  (SELECT id FROM tasks WHERE title = 'Terminar informe mensual'),
  (SELECT id FROM labels WHERE name = 'Importante')
),
(
  (SELECT id FROM tasks WHERE title = 'Comprar regalos navideños'),
  (SELECT id FROM labels WHERE name = 'Importante')
);
