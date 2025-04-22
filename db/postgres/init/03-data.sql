INSERT INTO roles (name, created_at) VALUES
('admin', CURRENT_TIMESTAMP),
('user', CURRENT_TIMESTAMP);

INSERT INTO users (email, username, password_hash, role_id, created_at, updated_at) VALUES
('user1@example.com', 'johndoe', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', (SELECT id FROM roles WHERE name = 'admin'), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('user2@example.com', 'janedoe', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', (SELECT id FROM roles WHERE name = 'user'), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO categories (name, created_at) VALUES
('Trabajo', CURRENT_TIMESTAMP),
('Personal', CURRENT_TIMESTAMP),
('Estudio', CURRENT_TIMESTAMP);

INSERT INTO labels (user_id, name, color, created_at) VALUES
((SELECT id FROM users WHERE email = 'user1@example.com'), 'Urgente', '#ef4444', CURRENT_TIMESTAMP),
((SELECT id FROM users WHERE email = 'user1@example.com'), 'Importante', '#f97316', CURRENT_TIMESTAMP),
((SELECT id FROM users WHERE email = 'user2@example.com'), 'Proyecto', '#8b5cf6', CURRENT_TIMESTAMP);

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
  (SELECT id FROM labels WHERE name = 'Urgente' AND user_id = (SELECT id FROM users WHERE email = 'user1@example.com'))
),
(
  (SELECT id FROM tasks WHERE title = 'Terminar informe mensual'),
  (SELECT id FROM labels WHERE name = 'Importante' AND user_id = (SELECT id FROM users WHERE email = 'user1@example.com'))
),
(
  (SELECT id FROM tasks WHERE title = 'Comprar regalos navideños'),
  (SELECT id FROM labels WHERE name = 'Proyecto' AND user_id = (SELECT id FROM users WHERE email = 'user2@example.com'))
);
