import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import timedelta

from modelos.base_datos import db, Usuario, Estudiante, Profesor
from servicios.gemini_ai import GeminiAI

# Cargar variables de entorno
load_dotenv()

# Crear aplicación Flask
app = Flask(__name__)

# ======================== CONFIGURACIÓN ========================

# Configuración de BD MySQL
db_user = os.getenv('DB_USER', 'root')
db_password = os.getenv('DB_PASSWORD', '12345')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '3306')
db_name = os.getenv('DB_NAME', 'acompania')

database_uri = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 3600,
}

# Configuración de sesión
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'tu-clave-secreta-cambiar-en-produccion')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Inicializar extensiones
db.init_app(app)
CORS(app)

# Inicializar servicios
gemini_service = GeminiAI()

# ======================== CONTEXT PROCESSORS ========================

@app.context_processor
def inject_user():
    """Inyectar usuario en contexto de templates"""
    usuario = None
    if 'usuario_id' in session:
        usuario = db.session.get(Usuario, session['usuario_id'])
    return dict(usuario=usuario)


# ======================== MIDDLEWARE ========================

@app.before_request
def verificar_sesion():
    """Verificar que la sesión sea válida"""
    session.permanent = True
    
    rutas_publicas = ['login', 'privacidad', 'static']
    
    if request.endpoint and request.endpoint.split('.')[0] not in rutas_publicas:
        if 'usuario_id' not in session:
            return redirect(url_for('login'))


# ======================== RUTAS DE AUTENTICACIÓN ========================

@app.route('/')
def index():
    """Página principal"""
    if 'usuario_id' in session:
        usuario = db.session.get(Usuario, session['usuario_id'])
        if usuario.rol == 'alumno':
            return redirect(url_for('dashboard_alumno'))
        else:
            return redirect(url_for('dashboard_profesor'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login institucional"""
    if request.method == 'POST':
        datos = request.get_json() if request.is_json else request.form
        email = datos.get('email')
        password = datos.get('password')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(password) and usuario.activo:
            session['usuario_id'] = usuario.id
            session['rol'] = usuario.rol
            
            if usuario.rol == 'alumno':
                return redirect(url_for('dashboard_alumno')) if not request.is_json else jsonify({'success': True, 'redirect': url_for('dashboard_alumno')})
            else:
                return redirect(url_for('dashboard_profesor')) if not request.is_json else jsonify({'success': True, 'redirect': url_for('dashboard_profesor')})
        
        return jsonify({'error': 'Credenciales inválidas'}) if request.is_json else render_template('login.html', error='Credenciales inválidas')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    return redirect(url_for('login'))


@app.route('/privacidad')
def privacidad():
    """Página de privacidad"""
    return render_template('privacidad.html')


# ======================== RUTAS DEL ALUMNO ========================

@app.route('/alumno/dashboard')
def dashboard_alumno():
    """Dashboard del alumno"""
    if session.get('rol') != 'alumno':
        return redirect(url_for('login'))
    
    usuario = db.session.get(Usuario, session['usuario_id'])
    estudiante = usuario.estudiante
    
    # Obtener recomendaciones
    from modelos.base_datos import Recomendacion
    recomendaciones = Recomendacion.query.filter_by(estudiante_id=estudiante.id).order_by(Recomendacion.fecha_generacion.desc()).limit(5).all()
    
    return render_template('alumno/dashboard.html', estudiante=estudiante, recomendaciones=recomendaciones)


@app.route('/alumno/perfil')
def perfil_alumno():
    """Perfil del alumno"""
    if session.get('rol') != 'alumno':
        return redirect(url_for('login'))
    
    usuario = db.session.get(Usuario, session['usuario_id'])
    estudiante = usuario.estudiante
    
    # Obtener historial académico
    from modelos.base_datos import Calificacion, Asistencia, EvaluacionEmocional
    calificaciones = Calificacion.query.filter_by(estudiante_id=estudiante.id).all()
    asistencias = Asistencia.query.filter_by(estudiante_id=estudiante.id).all()
    emociones = EvaluacionEmocional.query.filter_by(estudiante_id=estudiante.id).order_by(EvaluacionEmocional.fecha_evaluacion.desc()).limit(10).all()
    
    return render_template('alumno/perfil.html', 
                          estudiante=estudiante, 
                          calificaciones=calificaciones,
                          asistencias=asistencias,
                          emociones=emociones)


@app.route('/alumno/chat')
def chat_alumno():
    """Chat con tutor IA"""
    if session.get('rol') != 'alumno':
        return redirect(url_for('login'))
    
    return render_template('alumno/chat.html')


# ======================== RUTAS DEL PROFESOR ========================

@app.route('/profesor/dashboard')
def dashboard_profesor():
    """Dashboard del profesor"""
    if session.get('rol') != 'profesor':
        return redirect(url_for('login'))
    
    usuario = db.session.get(Usuario, session['usuario_id'])
    profesor = usuario.profesor
    
    # Obtener KPIs
    from modelos.base_datos import KPI
    from datetime import date
    kpi_hoy = KPI.query.filter_by(institucion=usuario.institucion).filter_by(fecha=date.today()).first()
    
    return render_template('profesor/dashboard.html', profesor=profesor, kpi=kpi_hoy)


@app.route('/profesor/estudiantes')
def estudiantes_profesor():
    """Lista de estudiantes"""
    if session.get('rol') != 'profesor':
        return redirect(url_for('login'))
    
    usuario = db.session.get(Usuario, session['usuario_id'])
    profesor = usuario.profesor
    
    # Filtros
    carrera = request.args.get('carrera')
    semestre = request.args.get('semestre')
    grupo = request.args.get('grupo')
    nivel_riesgo = request.args.get('riesgo')
    
    query = Estudiante.query
    
    if carrera:
        query = query.filter_by(carrera=carrera)
    if semestre:
        query = query.filter_by(semestre=int(semestre))
    if grupo:
        query = query.filter_by(grupo=grupo)
    if nivel_riesgo:
        query = query.filter_by(nivel_riesgo=nivel_riesgo)
    
    estudiantes = query.all()
    
    return render_template('profesor/estudiantes.html', estudiantes=estudiantes, profesor=profesor)


@app.route('/profesor/alumno/<int:estudiante_id>')
def perfil_alumno_profesor(estudiante_id):
    """Ver perfil del alumno (vista profesor)"""
    if session.get('rol') != 'profesor':
        return redirect(url_for('login'))
    
    estudiante = Estudiante.query.get_or_404(estudiante_id)
    
    from modelos.base_datos import Calificacion, Asistencia, EvaluacionEmocional, Intervencion
    calificaciones = Calificacion.query.filter_by(estudiante_id=estudiante_id).all()
    asistencias = Asistencia.query.filter_by(estudiante_id=estudiante_id).all()
    emociones = EvaluacionEmocional.query.filter_by(estudiante_id=estudiante_id).order_by(EvaluacionEmocional.fecha_evaluacion.desc()).limit(10).all()
    intervenciones = Intervencion.query.filter_by(estudiante_id=estudiante_id).order_by(Intervencion.fecha_creacion.desc()).all()
    
    return render_template('profesor/perfil_alumno.html',
                          estudiante=estudiante,
                          calificaciones=calificaciones,
                          asistencias=asistencias,
                          emociones=emociones,
                          intervenciones=intervenciones)


@app.route('/profesor/intervenciones')
def intervenciones_profesor():
    """Centro de intervenciones"""
    if session.get('rol') != 'profesor':
        return redirect(url_for('login'))
    
    usuario = db.session.get(Usuario, session['usuario_id'])
    profesor = usuario.profesor
    
    from modelos.base_datos import Intervencion
    intervenciones = Intervencion.query.filter_by(profesor_id=profesor.id).order_by(Intervencion.fecha_creacion.desc()).all()
    
    return render_template('profesor/intervenciones.html', intervenciones=intervenciones)


# ======================== API ENDPOINTS ========================

@app.route('/api/chat/enviar', methods=['POST'])
def enviar_mensaje_chat():
    """Enviar mensaje al chat IA"""
    if session.get('rol') != 'alumno':
        return jsonify({'error': 'No autorizado'}), 401
    
    usuario = db.session.get(Usuario, session['usuario_id'])
    estudiante = usuario.estudiante
    
    datos = request.get_json()
    mensaje = datos.get('mensaje')
    
    if not mensaje:
        return jsonify({'error': 'Mensaje vacío'}), 400
    
    # Guardar mensaje del estudiante
    from modelos.base_datos import MensajeChat
    msg_est = MensajeChat(
        estudiante_id=estudiante.id,
        rol='estudiante',
        contenido=mensaje
    )
    db.session.add(msg_est)
    
    # Obtener respuesta de IA
    respuesta_ia = gemini_service.obtener_respuesta(mensaje, estudiante)
    
    # Guardar respuesta de IA
    msg_ia = MensajeChat(
        estudiante_id=estudiante.id,
        rol='ia',
        contenido=respuesta_ia['respuesta'],
        sentimiento_detectado=respuesta_ia.get('sentimiento'),
        puntuacion_sentimiento=respuesta_ia.get('puntuacion')
    )
    db.session.add(msg_ia)
    db.session.commit()
    
    return jsonify({
        'respuesta': respuesta_ia['respuesta'],
        'sentimiento': respuesta_ia.get('sentimiento'),
        'puntuacion': respuesta_ia.get('puntuacion')
    })


@app.route('/api/intervenciones/crear', methods=['POST'])
def crear_intervencion():
    """Crear una nueva intervención"""
    if session.get('rol') != 'profesor':
        return jsonify({'error': 'No autorizado'}), 401
    
    usuario = db.session.get(Usuario, session['usuario_id'])
    profesor = usuario.profesor
    
    datos = request.get_json()
    
    from modelos.base_datos import Intervencion
    from datetime import datetime
    
    # Convertir el string de fecha a objeto datetime
    fecha_str = datos.get('fecha_programada')
    fecha_prog = None
    if fecha_str:
        try:
            fecha_prog = datetime.fromisoformat(fecha_str)
        except ValueError:
            # Por si el formato es solo fecha o diferente
            try:
                fecha_prog = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M")
            except:
                pass
                
    intervencion = Intervencion(
        estudiante_id=datos.get('estudiante_id'),
        profesor_id=profesor.id,
        tipo_intervencion=datos.get('tipo'),
        descripcion=datos.get('descripcion'),
        fecha_programada=fecha_prog
    )
    
    db.session.add(intervencion)
    db.session.commit()
    
    return jsonify({'success': True, 'id': intervencion.id})


@app.route('/api/kpis', methods=['GET'])
def obtener_kpis():
    """Obtener KPIs"""
    if session.get('rol') != 'profesor':
        return jsonify({'error': 'No autorizado'}), 401
    
    usuario = db.session.get(Usuario, session['usuario_id'])
    
    from modelos.base_datos import KPI
    from datetime import date
    kpi = KPI.query.filter_by(institucion=usuario.institucion).filter_by(fecha=date.today()).first()
    
    if kpi:
        return jsonify({
            'alumnos_en_riesgo': kpi.alumnos_en_riesgo,
            'alertas_nuevas': kpi.alertas_nuevas,
            'materias_criticas': kpi.materias_criticas,
            'tasa_desercion': kpi.tasa_desercion,
            'promedio_academico': kpi.promedio_academico_general
        })
    
    return jsonify({'error': 'No hay datos disponibles'}), 404


# ======================== MANEJO DE ERRORES ========================

@app.errorhandler(404)
def no_encontrado(error):
    """Página no encontrada"""
    return render_template('errores/404.html'), 404


@app.errorhandler(500)
def error_servidor(error):
    """Error del servidor"""
    return render_template('errores/500.html'), 500


# ======================== CREAR TABLAS Y EJECUTAR ========================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✓ Base de datos inicializada")
    
    # Modo debug solo en desarrollo
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
