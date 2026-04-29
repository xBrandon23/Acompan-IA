-- ======================== CREAR BASE DE DATOS ========================
CREATE DATABASE IF NOT EXISTS acompania CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE acompania;

-- ======================== TABLA USUARIOS ========================
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(120) NOT NULL,
    apellido VARCHAR(120) NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('alumno', 'profesor')),
    institucion VARCHAR(120) NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    INDEX idx_email (email),
    INDEX idx_rol (rol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ======================== TABLA PROFESORES ========================
CREATE TABLE IF NOT EXISTS profesores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    departamento VARCHAR(120),
    especialidad VARCHAR(120),
    telefono VARCHAR(20),
    foto_perfil VARCHAR(255),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_usuario_id (usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ======================== TABLA ESTUDIANTES ========================
CREATE TABLE IF NOT EXISTS estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    carrera VARCHAR(120) NOT NULL,
    semestre INT NOT NULL,
    grupo VARCHAR(20),
    matricula VARCHAR(50) UNIQUE NOT NULL,
    promedio_academico FLOAT DEFAULT 0.0,
    nivel_riesgo VARCHAR(20) DEFAULT 'bajo' CHECK (nivel_riesgo IN ('bajo', 'medio', 'alto', 'critico')),
    razon_riesgo VARCHAR(500),
    fecha_evaluacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    asistencia_porcentaje FLOAT DEFAULT 100.0,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_usuario_id (usuario_id),
    INDEX idx_matricula (matricula),
    INDEX idx_carrera (carrera),
    INDEX idx_nivel_riesgo (nivel_riesgo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ======================== TABLA ASIGNATURAS ========================
CREATE TABLE IF NOT EXISTS asignaturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    profesor_id INT NOT NULL,
    carrera VARCHAR(120) NOT NULL,
    semestre INT NOT NULL,
    creditos INT DEFAULT 0,
    descripcion TEXT,
    FOREIGN KEY (profesor_id) REFERENCES profesores(id) ON DELETE CASCADE,
    INDEX idx_codigo (codigo),
    INDEX idx_profesor_id (profesor_id),
    INDEX idx_carrera (carrera)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ======================== TABLA CALIFICACIONES ========================
CREATE TABLE IF NOT EXISTS calificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    asignatura_id INT NOT NULL,
    calificacion FLOAT NOT NULL,
    estado VARCHAR(20) DEFAULT 'activa' CHECK (estado IN ('activa', 'aprobada', 'reprobada', 'incompleta')),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    periodo VARCHAR(20) NOT NULL,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    FOREIGN KEY (asignatura_id) REFERENCES asignaturas(id) ON DELETE CASCADE,
    INDEX idx_estudiante_id (estudiante_id),
    INDEX idx_asignatura_id (asignatura_id),
    INDEX idx_periodo (periodo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ======================== TABLA ASISTENCIAS ========================
CREATE TABLE IF NOT EXISTS asistencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    asignatura_id INT NOT NULL,
    fecha DATE NOT NULL,
    presente BOOLEAN DEFAULT TRUE,
    periodo VARCHAR(20) NOT NULL,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    FOREIGN KEY (asignatura_id) REFERENCES asignaturas(id) ON DELETE CASCADE,
    UNIQUE KEY uq_asistencia (estudiante_id, asignatura_id, fecha),
    INDEX idx_fecha (fecha),
    INDEX idx_estudiante_id (estudiante_id),
    INDEX idx_periodo (periodo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ======================== TABLA EVALUACIONES EMOCIONALES ========================
CREATE TABLE IF NOT EXISTS evaluaciones_emocionales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    sentimiento VARCHAR(50) NOT NULL,
    puntuacion FLOAT NOT NULL,
    contexto TEXT,
    fecha_evaluacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    INDEX idx_estudiante_id (estudiante_id),
    INDEX idx_fecha_evaluacion (fecha_evaluacion),
    INDEX idx_sentimiento (sentimiento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ======================== TABLA INTERVENCIONES ========================
CREATE TABLE IF NOT EXISTS intervenciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    profesor_id INT NOT NULL,
    tipo_intervencion VARCHAR(50) NOT NULL CHECK (tipo_intervencion IN ('llamada', 'cita', 'canalizacion', 'asesoria')),
    descripcion TEXT NOT NULL,
    fecha_programada DATETIME NOT NULL,
    fecha_realizacion DATETIME,
    estado VARCHAR(20) DEFAULT 'programada' CHECK (estado IN ('programada', 'completada', 'cancelada')),
    resultado TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    FOREIGN KEY (profesor_id) REFERENCES profesores(id) ON DELETE CASCADE,
    INDEX idx_estudiante_id (estudiante_id),
    INDEX idx_profesor_id (profesor_id),
    INDEX idx_estado (estado),
    INDEX idx_fecha_programada (fecha_programada)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ======================== TABLA MENSAJES CHAT ========================
CREATE TABLE IF NOT EXISTS mensajes_chat (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('estudiante', 'ia')),
    contenido LONGTEXT NOT NULL,
    sentimiento_detectado VARCHAR(50),
    puntuacion_sentimiento FLOAT,
    fecha_mensaje DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    INDEX idx_estudiante_id (estudiante_id),
    INDEX idx_fecha_mensaje (fecha_mensaje),
    INDEX idx_rol (rol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ======================== TABLA RECOMENDACIONES ========================
CREATE TABLE IF NOT EXISTS recomendaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    contenido LONGTEXT NOT NULL,
    prioridad VARCHAR(20) DEFAULT 'media' CHECK (prioridad IN ('baja', 'media', 'alta', 'critica')),
    fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    leida BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    INDEX idx_estudiante_id (estudiante_id),
    INDEX idx_fecha_generacion (fecha_generacion),
    INDEX idx_prioridad (prioridad),
    INDEX idx_leida (leida)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ======================== TABLA KPIs ========================
CREATE TABLE IF NOT EXISTS kpis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    institucion VARCHAR(120) NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    alumnos_en_riesgo INT DEFAULT 0,
    alertas_nuevas INT DEFAULT 0,
    materias_criticas INT DEFAULT 0,
    tasa_desercion FLOAT DEFAULT 0.0,
    promedio_academico_general FLOAT DEFAULT 0.0,
    INDEX idx_institucion (institucion),
    INDEX idx_fecha (fecha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ======================== CREAR ÍNDICES ADICIONALES PARA MEJOR RENDIMIENTO ========================
ALTER TABLE usuarios ADD INDEX idx_institucion (institucion);
ALTER TABLE profesores ADD INDEX idx_departamento (departamento);
ALTER TABLE estudiantes ADD INDEX idx_semestre (semestre);
ALTER TABLE asignaturas ADD INDEX idx_semestre (semestre);
ALTER TABLE calificaciones ADD INDEX idx_estado (estado);
ALTER TABLE intervenciones ADD INDEX idx_tipo (tipo_intervencion);

-- ======================== SAMPLE DATA (OPCIONAL - COMENTADO) ========================
-- Descomenta estas líneas si quieres datos de prueba

/*
-- Usuario profesor
INSERT INTO usuarios (email, password_hash, nombre, apellido, rol, institucion, activo) 
VALUES ('profesor@example.com', 'hashed_password_here', 'Juan', 'Pérez', 'profesor', 'Universidad del Ejemplo', TRUE);

-- Usuario estudiante
INSERT INTO usuarios (email, password_hash, nombre, apellido, rol, institucion, activo) 
VALUES ('estudiante@example.com', 'hashed_password_here', 'María', 'García', 'alumno', 'Universidad del Ejemplo', TRUE);

-- Profesor
INSERT INTO profesores (usuario_id, departamento, especialidad, telefono) 
VALUES (1, 'Ciencias', 'Matemáticas', '123456789');

-- Estudiante
INSERT INTO estudiantes (usuario_id, carrera, semestre, grupo, matricula, nivel_riesgo) 
VALUES (2, 'Ingeniería', 4, 'A', 'MAT2024001', 'bajo');
*/
