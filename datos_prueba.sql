-- ======================== DATOS DE PRUEBA PARA ACOMPAÑIA ========================
-- Script para insertar datos de prueba realistas en la BD

USE acompania;

-- ======================== INSERTAR USUARIOS PROFESORES ========================
INSERT INTO usuarios (email, password_hash, nombre, apellido, rol, institucion, activo) VALUES
('juan.perez@universidad.edu', '$2b$12$5nGlMcMSw7YJpvZpWxAa2eKlZqZ3q1K8N5x9c2b3d4e5f6g7h8i9j0k1', 'Juan', 'Pérez García', 'profesor', 'Universidad Técnica del Centro', TRUE),
('maria.lopez@universidad.edu', '$2b$12$5nGlMcMSw7YJpvZpWxAa2eKlZqZ3q1K8N5x9c2b3d4e5f6g7h8i9j0k1', 'María', 'López Martínez', 'profesor', 'Universidad Técnica del Centro', TRUE),
('carlos.ruiz@universidad.edu', '$2b$12$5nGlMcMSw7YJpvZpWxAa2eKlZqZ3q1K8N5x9c2b3d4e5f6g7h8i9j0k1', 'Carlos', 'Ruiz Sánchez', 'profesor', 'Universidad Técnica del Centro', TRUE);

-- ======================== INSERTAR USUARIOS ESTUDIANTES ========================
INSERT INTO usuarios (email, password_hash, nombre, apellido, rol, institucion, activo) VALUES
('ana.garcia@estudiante.edu', '$2b$12$5nGlMcMSw7YJpvZpWxAa2eKlZqZ3q1K8N5x9c2b3d4e5f6g7h8i9j0k1', 'Ana', 'García Rodríguez', 'alumno', 'Universidad Técnica del Centro', TRUE),
('luis.martinez@estudiante.edu', '$2b$12$5nGlMcMSw7YJpvZpWxAa2eKlZqZ3q1K8N5x9c2b3d4e5f6g7h8i9j0k1', 'Luis', 'Martínez Flores', 'alumno', 'Universidad Técnica del Centro', TRUE),
('sofia.diaz@estudiante.edu', '$2b$12$5nGlMcMSw7YJpvZpWxAa2eKlZqZ3q1K8N5x9c2b3d4e5f6g7h8i9j0k1', 'Sofía', 'Díaz López', 'alumno', 'Universidad Técnica del Centro', TRUE),
('diego.torres@estudiante.edu', '$2b$12$5nGlMcMSw7YJpvZpWxAa2eKlZqZ3q1K8N5x9c2b3d4e5f6g7h8i9j0k1', 'Diego', 'Torres Gómez', 'alumno', 'Universidad Técnica del Centro', TRUE),
('laura.sanchez@estudiante.edu', '$2b$12$5nGlMcMSw7YJpvZpWxAa2eKlZqZ3q1K8N5x9c2b3d4e5f6g7h8i9j0k1', 'Laura', 'Sánchez Vargas', 'alumno', 'Universidad Técnica del Centro', TRUE);

-- ======================== INSERTAR PROFESORES ========================
INSERT INTO profesores (usuario_id, departamento, especialidad, telefono, foto_perfil) VALUES
(1, 'Ciencias Exactas', 'Matemáticas', '+34 912 345 678', '/static/fotos/juan_perez.jpg'),
(2, 'Tecnología', 'Ingeniería de Sistemas', '+34 912 345 679', '/static/fotos/maria_lopez.jpg'),
(3, 'Ciencias Exactas', 'Física', '+34 912 345 680', '/static/fotos/carlos_ruiz.jpg');

-- ======================== INSERTAR ESTUDIANTES ========================
INSERT INTO estudiantes (usuario_id, carrera, semestre, grupo, matricula, promedio_academico, nivel_riesgo, razon_riesgo, asistencia_porcentaje) VALUES
(4, 'Ingeniería Informática', 4, 'A', 'MAT20240001', 3.8, 'bajo', NULL, 95.0),
(5, 'Ingeniería Informática', 4, 'A', 'MAT20240002', 3.2, 'medio', 'Bajo desempeño en matemáticas', 85.0),
(6, 'Ingeniería Industrial', 3, 'B', 'MAT20240003', 2.9, 'alto', 'Ausencias frecuentes y bajo rendimiento', 70.0),
(7, 'Ingeniería Informática', 4, 'A', 'MAT20240004', 3.5, 'bajo', NULL, 92.0),
(8, 'Ingeniería Industrial', 3, 'B', 'MAT20240005', 2.3, 'critico', 'En riesgo de deserción', 45.0);

-- ======================== INSERTAR ASIGNATURAS ========================
INSERT INTO asignaturas (nombre, codigo, profesor_id, carrera, semestre, creditos, descripcion) VALUES
('Cálculo I', 'MAT101', 1, 'Ingeniería Informática', 1, 4, 'Introducción al cálculo diferencial e integral'),
('Programación I', 'INF101', 2, 'Ingeniería Informática', 1, 3, 'Fundamentos de programación en Python'),
('Física I', 'FIS101', 3, 'Ingeniería Informática', 1, 4, 'Mecánica clásica y termodinámica'),
('Cálculo II', 'MAT102', 1, 'Ingeniería Informática', 2, 4, 'Cálculo avanzado y aplicaciones'),
('Programación II', 'INF102', 2, 'Ingeniería Informática', 2, 3, 'Programación orientada a objetos'),
('Base de Datos', 'INF103', 2, 'Ingeniería Informática', 3, 3, 'Diseño e implementación de bases de datos'),
('Ingeniería de Software', 'INF104', 2, 'Ingeniería Informática', 4, 3, 'Metodologías y prácticas en desarrollo'),
('Resistencia de Materiales', 'IND101', 1, 'Ingeniería Industrial', 1, 4, 'Análisis de esfuerzos en materiales'),
('Procesos Industriales', 'IND102', 3, 'Ingeniería Industrial', 2, 3, 'Optimización de procesos');

-- ======================== INSERTAR CALIFICACIONES ========================
INSERT INTO calificaciones (estudiante_id, asignatura_id, calificacion, estado, periodo) VALUES
-- Ana García (estudiante con buenas notas)
(1, 1, 4.5, 'aprobada', '2024-I'),
(1, 2, 4.3, 'aprobada', '2024-I'),
(1, 3, 4.6, 'aprobada', '2024-I'),
(1, 4, 4.2, 'aprobada', '2024-II'),
(1, 5, 4.4, 'aprobada', '2024-II'),

-- Luis Martínez (estudiante promedio)
(2, 1, 3.2, 'aprobada', '2024-I'),
(2, 2, 3.1, 'aprobada', '2024-I'),
(2, 3, 2.8, 'aprobada', '2024-I'),
(2, 4, 2.9, 'aprobada', '2024-II'),
(2, 5, 3.5, 'aprobada', '2024-II'),

-- Sofía Díaz (estudiante con bajo rendimiento)
(3, 8, 2.5, 'aprobada', '2024-I'),
(3, 9, 2.0, 'aprobada', '2024-II'),

-- Diego Torres (estudiante bueno)
(4, 1, 4.1, 'aprobada', '2024-I'),
(4, 2, 3.9, 'aprobada', '2024-I'),
(4, 3, 4.3, 'aprobada', '2024-I'),
(4, 4, 4.0, 'aprobada', '2024-II'),
(4, 5, 4.1, 'aprobada', '2024-II'),

-- Laura Sánchez (estudiante en riesgo)
(5, 1, 2.0, 'aprobada', '2024-I'),
(5, 2, 1.8, 'reprobada', '2024-I'),
(5, 3, 1.5, 'reprobada', '2024-I');

-- ======================== INSERTAR ASISTENCIAS ========================
INSERT INTO asistencias (estudiante_id, asignatura_id, fecha, presente, periodo) VALUES
-- Ana García - Asistencias regulares
(1, 1, '2024-03-01', TRUE, '2024-I'),
(1, 1, '2024-03-04', TRUE, '2024-I'),
(1, 1, '2024-03-08', TRUE, '2024-I'),
(1, 1, '2024-03-11', TRUE, '2024-I'),
(1, 2, '2024-03-02', TRUE, '2024-I'),
(1, 2, '2024-03-05', TRUE, '2024-I'),

-- Luis Martínez - Algunas inasistencias
(2, 1, '2024-03-01', TRUE, '2024-I'),
(2, 1, '2024-03-04', FALSE, '2024-I'),
(2, 1, '2024-03-08', TRUE, '2024-I'),
(2, 1, '2024-03-11', FALSE, '2024-I'),
(2, 2, '2024-03-02', TRUE, '2024-I'),
(2, 2, '2024-03-05', TRUE, '2024-I'),

-- Sofía Díaz - Muchas inasistencias
(3, 8, '2024-03-01', FALSE, '2024-I'),
(3, 8, '2024-03-04', FALSE, '2024-I'),
(3, 8, '2024-03-08', TRUE, '2024-I'),
(3, 8, '2024-03-11', FALSE, '2024-I'),
(3, 9, '2024-04-05', FALSE, '2024-II'),
(3, 9, '2024-04-12', FALSE, '2024-II'),

-- Diego Torres - Muy puntual
(4, 1, '2024-03-01', TRUE, '2024-I'),
(4, 1, '2024-03-04', TRUE, '2024-I'),
(4, 1, '2024-03-08', TRUE, '2024-I'),
(4, 1, '2024-03-11', TRUE, '2024-I'),
(4, 2, '2024-03-02', TRUE, '2024-I'),
(4, 2, '2024-03-05', TRUE, '2024-I'),

-- Laura Sánchez - Inasistencias críticas
(5, 1, '2024-03-01', FALSE, '2024-I'),
(5, 1, '2024-03-04', FALSE, '2024-I'),
(5, 1, '2024-03-08', FALSE, '2024-I'),
(5, 1, '2024-03-11', TRUE, '2024-I'),
(5, 2, '2024-03-02', FALSE, '2024-I'),
(5, 2, '2024-03-05', FALSE, '2024-I');

-- ======================== INSERTAR EVALUACIONES EMOCIONALES ========================
INSERT INTO evaluaciones_emocionales (estudiante_id, sentimiento, puntuacion, contexto) VALUES
(1, 'motivación', 0.95, 'Estudiante muy comprometido con sus estudios'),
(1, 'confianza', 0.90, 'Resolvió problema difícil sin ayuda'),
(2, 'frustración', 0.75, 'Dificultades con conceptos de programación'),
(2, 'incertidumbre', 0.65, 'No entiende bien la base de datos'),
(3, 'ansiedad', 0.85, 'Preocupado por sus calificaciones'),
(3, 'desánimo', 0.80, 'Ausencias frecuentes indican problema personal'),
(4, 'confianza', 0.92, 'Muy seguro de sus habilidades'),
(4, 'motivación', 0.88, 'Participa activamente en clase'),
(5, 'depresión', 0.70, 'Situación económica difícil'),
(5, 'desesperación', 0.75, 'En riesgo de abandonar la carrera');

-- ======================== INSERTAR INTERVENCIONES ========================
INSERT INTO intervenciones (estudiante_id, profesor_id, tipo_intervencion, descripcion, fecha_programada, fecha_realizacion, estado, resultado) VALUES
(1, 1, 'asesoria', 'Asesoría sobre técnicas de estudio avanzadas', '2024-03-15 14:00:00', '2024-03-15 14:30:00', 'completada', 'Estudiante muy motivado, no requiere intervención.'),
(2, 1, 'asesoria', 'Ayuda con dificultades en Cálculo', '2024-03-18 10:00:00', '2024-03-18 10:45:00', 'completada', 'Se explicaron conceptos básicos. Mejora esperada.'),
(3, 1, 'cita', 'Reunión para discutir bajo rendimiento', '2024-03-20 09:00:00', '2024-03-20 09:30:00', 'completada', 'Estudiante con problemas personales. Se canaliza a bienestar.'),
(3, 1, 'canalizacion', 'Derivación a departamento de bienestar estudiantil', '2024-03-22 16:00:00', '2024-03-22 16:00:00', 'completada', 'Contactado departamento de bienestar.'),
(5, 2, 'llamada', 'Llamada para verificar situación del estudiante', '2024-03-25 15:00:00', '2024-03-25 15:15:00', 'completada', 'Estudiante con problemas financieros. Dirigido a becas.'),
(5, 2, 'canalizacion', 'Derivación a oficina de becas y ayudas', '2024-03-26 10:00:00', '2024-03-26 10:00:00', 'completada', 'Solicitado análisis de elegibilidad para beca de emergencia.');

-- ======================== INSERTAR MENSAJES CHAT ========================
INSERT INTO mensajes_chat (estudiante_id, rol, contenido, sentimiento_detectado, puntuacion_sentimiento) VALUES
(1, 'estudiante', 'Hola, tengo dudas sobre la derivada de funciones trigonométricas', 'curiosidad', 0.70),
(1, 'ia', 'Claro, con gusto te ayudo. La derivada de sen(x) es cos(x), y la de cos(x) es -sen(x). ¿Necesitas ver ejemplos?', 'asistencia', 0.85),
(1, 'estudiante', 'Sí, por favor. Me ayudaría mucho ver ejemplos prácticos', 'motivación', 0.80),
(1, 'ia', 'Perfecto. Aquí están: [ejemplos]. ¿Qué otros tipos de derivadas necesitas practicar?', 'ayuda', 0.85),

(2, 'estudiante', 'No entiendo nada de programación. Creo que debería cambiarme de carrera', 'frustración', 0.85),
(2, 'ia', 'Entiendo tu frustración, pero muchos estudiantes se sienten así al inicio. ¿Qué tema específico te cuesta?', 'empatía', 0.80),
(2, 'estudiante', 'Los loops y las funciones. Es demasiado abstracto', 'confusión', 0.75),
(2, 'ia', 'Eso es normal. Te recomiendo practicar con ejercicios pequeños. ¿Quieres que te sugiera algunos recursos?', 'apoyo', 0.75),

(3, 'estudiante', 'Tengo muchos problemas en casa. No sé si pueda seguir estudiando', 'ansiedad', 0.80),
(3, 'ia', 'Lamento escuchar eso. Es importante que busques apoyo. ¿Has contactado con el departamento de bienestar?', 'preocupación', 0.80),
(3, 'estudiante', 'No, no sabía que existía', 'esperanza', 0.60),
(3, 'ia', 'Te enviaré el contacto. No estás solo en esto. El bienestar universitario puede ayudarte', 'ánimo', 0.85),

(4, 'estudiante', 'Perfecto, entendí bien este tema. ¿Cuál es el siguiente?', 'confianza', 0.90),
(4, 'ia', '¡Excelente! Tu progreso es muy bueno. El siguiente tema es control de versiones con Git', 'felicitación', 0.90),
(4, 'estudiante', 'Listo, estoy listo para aprender', 'motivación', 0.95),

(5, 'estudiante', 'No puedo concentrarme. Tengo problemas económicos y estoy muy estresado', 'estrés', 0.90),
(5, 'ia', 'Lo siento. Tu situación es importante. Te recomiendo contactar a la oficina de becas para ver opciones', 'empatía', 0.85),
(5, 'estudiante', 'Gracias por escuchar. Al menos ahora sé a dónde acudir', 'alivio', 0.70);

-- ======================== INSERTAR RECOMENDACIONES ========================
INSERT INTO recomendaciones (estudiante_id, tipo, contenido, prioridad, leida) VALUES
(1, 'académica', 'Considera tomar cursos avanzados en matemáticas. Tu desempeño lo permite.', 'media', TRUE),
(1, 'oportunidad', 'Hay un programa de tutorías para ayudar a otros estudiantes. Podrías participar.', 'baja', FALSE),

(2, 'académica', 'Te recomiendo trabajar en la lógica de programación con ejercicios prácticos.', 'alta', TRUE),
(2, 'apoyo', 'Considera buscar un grupo de estudio. Aprender con otros puede ayudarte.', 'alta', TRUE),

(3, 'personal', 'Es importante que busques apoyo en el departamento de bienestar estudiantil.', 'crítica', TRUE),
(3, 'económica', 'Investiga las opciones de becas disponibles para tu situación.', 'crítica', TRUE),

(4, 'académica', 'Tu desempeño es excelente. Considera participar en proyectos de investigación.', 'media', FALSE),
(4, 'liderazgo', 'Podrías ser monitor de alguna asignatura. Tu capacidad es excepcional.', 'baja', FALSE),

(5, 'económica', 'URGENTE: Contacta a la oficina de becas para opciones de ayuda financiera.', 'crítica', TRUE),
(5, 'personal', 'Habla con un consejero sobre tus dificultades personales y emocionales.', 'crítica', TRUE),
(5, 'académica', 'Reprogramar cursos es una opción. Consulta con académica.', 'alta', FALSE);

-- ======================== INSERTAR KPIs ========================
INSERT INTO kpis (institucion, fecha, alumnos_en_riesgo, alertas_nuevas, materias_criticas, tasa_desercion, promedio_academico_general) VALUES
('Universidad Técnica del Centro', '2024-03-15', 2, 1, 1, 0.02, 3.54),
('Universidad Técnica del Centro', '2024-03-22', 3, 2, 2, 0.04, 3.42),
('Universidad Técnica del Centro', '2024-03-29', 2, 0, 1, 0.02, 3.56),
('Universidad Técnica del Centro', '2024-04-05', 2, 1, 1, 0.02, 3.58);

-- ======================== RESUMEN ========================
-- Insertados exitosamente:
-- ✓ 8 usuarios (3 profesores + 5 estudiantes)
-- ✓ 3 profesores
-- ✓ 5 estudiantes
-- ✓ 9 asignaturas
-- ✓ 17 calificaciones
-- ✓ 26 registros de asistencia
-- ✓ 10 evaluaciones emocionales
-- ✓ 6 intervenciones
-- ✓ 16 mensajes de chat
-- ✓ 11 recomendaciones
-- ✓ 4 registros de KPI
