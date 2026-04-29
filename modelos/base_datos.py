from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ======================== MODELOS BÁSICOS ========================

class Usuario(db.Model):
    """Modelo base para usuarios del sistema"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    apellido = db.Column(db.String(120), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # 'alumno' o 'profesor'
    institucion = db.Column(db.String(120), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    estudiante = db.relationship('Estudiante', backref='usuario_est', uselist=False, cascade='all, delete-orphan')
    profesor = db.relationship('Profesor', backref='usuario_prof', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash de contraseña"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Usuario {self.email}>'


class Profesor(db.Model):
    """Modelo para profesores"""
    __tablename__ = 'profesores'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, unique=True)
    departamento = db.Column(db.String(120), nullable=True)
    especialidad = db.Column(db.String(120), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    foto_perfil = db.Column(db.String(255), nullable=True)
    
    # Relaciones
    asignaturas = db.relationship('Asignatura', backref='profesor', lazy=True)
    intervenciones = db.relationship('Intervencion', backref='profesor', lazy=True)
    
    def __repr__(self):
        return f'<Profesor {self.usuario_id}>'


class Estudiante(db.Model):
    """Modelo para estudiantes"""
    __tablename__ = 'estudiantes'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, unique=True)
    carrera = db.Column(db.String(120), nullable=False)
    semestre = db.Column(db.Integer, nullable=False)
    grupo = db.Column(db.String(20), nullable=True)
    matricula = db.Column(db.String(50), unique=True, nullable=False, index=True)
    promedio_academico = db.Column(db.Float, default=0.0)
    nivel_riesgo = db.Column(db.String(20), default='bajo')  # bajo, medio, alto, critico
    razon_riesgo = db.Column(db.String(500), nullable=True)  # económica, académica, personal, etc.
    fecha_evaluacion = db.Column(db.DateTime, default=datetime.utcnow)
    asistencia_porcentaje = db.Column(db.Float, default=100.0)
    
    # Relaciones
    calificaciones = db.relationship('Calificacion', backref='estudiante', lazy=True, cascade='all, delete-orphan')
    asistencias = db.relationship('Asistencia', backref='estudiante', lazy=True, cascade='all, delete-orphan')
    evaluaciones_emocionales = db.relationship('EvaluacionEmocional', backref='estudiante', lazy=True, cascade='all, delete-orphan')
    intervenciones = db.relationship('Intervencion', backref='estudiante', lazy=True, cascade='all, delete-orphan')
    mensajes_chat = db.relationship('MensajeChat', backref='estudiante', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Estudiante {self.matricula}>'


class Asignatura(db.Model):
    """Modelo para asignaturas"""
    __tablename__ = 'asignaturas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    codigo = db.Column(db.String(20), unique=True, nullable=False, index=True)
    profesor_id = db.Column(db.Integer, db.ForeignKey('profesores.id'), nullable=False)
    carrera = db.Column(db.String(120), nullable=False)
    semestre = db.Column(db.Integer, nullable=False)
    creditos = db.Column(db.Integer, default=0)
    descripcion = db.Column(db.Text, nullable=True)
    
    # Relaciones
    calificaciones = db.relationship('Calificacion', backref='asignatura', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Asignatura {self.nombre}>'


class Calificacion(db.Model):
    """Modelo para calificaciones de estudiantes"""
    __tablename__ = 'calificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    asignatura_id = db.Column(db.Integer, db.ForeignKey('asignaturas.id'), nullable=False)
    calificacion = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), default='activa')  # activa, aprobada, reprobada, incompleta
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    periodo = db.Column(db.String(20), nullable=False)  # 2024-I, 2024-II, etc.
    
    def __repr__(self):
        return f'<Calificacion {self.estudiante_id} - {self.asignatura_id}>'


class Asistencia(db.Model):
    """Modelo para registro de asistencia"""
    __tablename__ = 'asistencias'
    
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    asignatura_id = db.Column(db.Integer, db.ForeignKey('asignaturas.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False, index=True)
    presente = db.Column(db.Boolean, default=True)
    periodo = db.Column(db.String(20), nullable=False)
    
    __table_args__ = (db.UniqueConstraint('estudiante_id', 'asignatura_id', 'fecha', name='uq_asistencia'),)
    
    def __repr__(self):
        return f'<Asistencia {self.estudiante_id} - {self.fecha}>'


class EvaluacionEmocional(db.Model):
    """Modelo para almacenar sentimientos detectados en chats"""
    __tablename__ = 'evaluaciones_emocionales'
    
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    sentimiento = db.Column(db.String(50), nullable=False)  # alegría, tristeza, frustración, motivación, etc.
    puntuacion = db.Column(db.Float, nullable=False)  # 0-1
    contexto = db.Column(db.Text, nullable=True)  # Texto que generó la evaluación
    fecha_evaluacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EvaluacionEmocional {self.estudiante_id} - {self.sentimiento}>'


class Intervencion(db.Model):
    """Modelo para registrar intervenciones del tutor"""
    __tablename__ = 'intervenciones'
    
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    profesor_id = db.Column(db.Integer, db.ForeignKey('profesores.id'), nullable=False)
    tipo_intervencion = db.Column(db.String(50), nullable=False)  # llamada, cita, canalización, asesoría
    descripcion = db.Column(db.Text, nullable=False)
    fecha_programada = db.Column(db.DateTime, nullable=False)
    fecha_realizacion = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.String(20), default='programada')  # programada, completada, cancelada
    resultado = db.Column(db.Text, nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Intervencion {self.id} - {self.tipo_intervencion}>'


class MensajeChat(db.Model):
    """Modelo para mensajes del chat con tutor IA"""
    __tablename__ = 'mensajes_chat'
    
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # 'estudiante' o 'ia'
    contenido = db.Column(db.Text, nullable=False)
    sentimiento_detectado = db.Column(db.String(50), nullable=True)  # Detectado por IA
    puntuacion_sentimiento = db.Column(db.Float, nullable=True)  # 0-1
    fecha_mensaje = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<MensajeChat {self.id} - {self.rol}>'


class Recomendacion(db.Model):
    """Modelo para recomendaciones automáticas"""
    __tablename__ = 'recomendaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # académica, emocional, financiera, etc.
    contenido = db.Column(db.Text, nullable=False)
    prioridad = db.Column(db.String(20), default='media')  # baja, media, alta, crítica
    fecha_generacion = db.Column(db.DateTime, default=datetime.utcnow)
    leida = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Recomendacion {self.id}>'


class KPI(db.Model):
    """Modelo para almacenar métricas KPI"""
    __tablename__ = 'kpis'
    
    id = db.Column(db.Integer, primary_key=True)
    institucion = db.Column(db.String(120), nullable=False, index=True)
    fecha = db.Column(db.Date, default=datetime.utcnow, index=True)
    alumnos_en_riesgo = db.Column(db.Integer, default=0)
    alertas_nuevas = db.Column(db.Integer, default=0)
    materias_criticas = db.Column(db.Integer, default=0)
    tasa_desercion = db.Column(db.Float, default=0.0)
    promedio_academico_general = db.Column(db.Float, default=0.0)
    
    def __repr__(self):
        return f'<KPI {self.fecha}>'
