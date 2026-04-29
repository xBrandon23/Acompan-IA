# 🎓 Acompan-IA - Sistema de Gestión de Deserción Estudiantil

**Acompan-IA** es una aplicación web integral diseñada para detectar y prevenir la deserción estudiantil mediante análisis predictivo, tutoría de IA y seguimiento personalizado. La plataforma proporciona herramientas tanto para estudiantes como para docentes y orientadores.

## 📋 Características Principales

### Para Estudiantes
- 📊 **Dashboard Personal**: Visualización de progreso académico en tiempo real
- 🤖 **Chat Tutor IA**: Tutor virtual con análisis de sentimientos en segundo plano
- 📈 **Historial Académico**: Registro completo de calificaciones y asistencia
- 💭 **Recomendaciones Inteligentes**: Sugerencias personalizadas basadas en desempeño
- 😊 **Seguimiento Emocional**: Detección de señales de riesgo

### Para Profesores/Orientadores
- 👥 **Panel de Estudiantes**: Lista con semáforo de riesgo
- 📍 **Dashboard KPIs**: Métricas de riesgo y alertas
- 🎯 **Filtros Avanzados**: Por carrera, semestre, grupo o nivel de riesgo
- 📋 **Centro de Intervenciones**: Registro de acciones (llamadas, citas, canalizaciones)
- 📊 **Perfiles Detallados**: Análisis completo de cada alumno
- 🔔 **Alertas Automáticas**: Notificaciones de estudiantes críticos

## 🛠️ Stack Tecnológico

### Backend
- **Framework**: Flask 3.0.3
- **Base de Datos**: SQLAlchemy (soporta SQLite, PostgreSQL, MySQL)
- **IA**: Google Gemini API
- **Autenticación**: Werkzeug (hashing de contraseñas)

### Frontend
- **HTML5** & **CSS3**
- **Bootstrap 5.3**
- **JavaScript Vanilla**
- **Chart.js** (gráficos)
- **Font Awesome** (iconos)

## 📦 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/Acompan-IA.git
cd Acompan-IA
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**

**En Windows:**
```bash
venv\Scripts\activate
```

**En macOS/Linux:**
```bash
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Configurar variables de entorno**
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
# - GEMINI_API_KEY: Clave de API de Google Gemini
# - DATABASE_URL: URL de conexión a base de datos
# - SECRET_KEY: Clave secreta para Flask
```

6. **Inicializar base de datos**
```bash
python app.py
```

Esto creará la base de datos y las tablas automáticamente.

7. **Ejecutar aplicación**
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## 🚀 Uso Rápido

### Acceso a la Aplicación

1. Abre el navegador y ve a `http://localhost:5000/login`
2. Usa tus credenciales institucionales
3. Se te redirigirá según tu rol

## 📁 Estructura del Proyecto

```
Acompan-IA/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias Python
├── .env                   # Variables de entorno
├── README.md             # Este archivo
├── modelos/
│   └── base_datos.py     # Modelos SQLAlchemy
├── rutas/
│   └── api.py            # Rutas y endpoints
├── servicios/
│   └── gemini_ai.py      # Integración con Gemini AI
├── templates/
│   ├── base.html         # Template base
│   ├── login.html        # Página de login
│   ├── privacidad.html   # Aviso de privacidad
│   ├── alumno/           # Templates de estudiante
│   ├── profesor/         # Templates de profesor
│   └── errores/          # Páginas de error
└── static/
    ├── css/
    │   └── styles.css    # Estilos personalizados
    └── js/
        └── main.js       # JavaScript personalizado
```

## 🔌 Configuración de Gemini API

1. Obtén tu clave de API en [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Añade la clave al archivo `.env`:
```
GEMINI_API_KEY=tu-clave-aqui
```

## 🔐 Seguridad

- ✅ Contraseñas hasheadas con Werkzeug
- ✅ Sesiones seguras con cookies HTTPOnly
- ✅ CORS habilitado para APIs seguras
- ✅ Validación de roles en cada endpoint
- ✅ Variables de entorno para datos sensibles
- ✅ Aviso de privacidad completo

## 📝 Modelos de Datos Principales

- **Usuario**: Información base (email, contraseña, rol)
- **Estudiante**: Información académica
- **Profesor**: Información docente
- **Calificación**: Desempeño académico
- **Asistencia**: Registro de asistencias
- **EvaluacionEmocional**: Sentimientos detectados por IA
- **Intervencion**: Acciones de apoyo registradas
- **MensajeChat**: Conversaciones con Tutor IA

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "No such table: usuarios"
```bash
python app.py
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes, abre un Pull Request.

## 📞 Contacto

Para preguntas o soporte: soporte@acompania.edu

---

**Acompan-IA** - Acompañando el éxito académico con tecnología e IA 🚀
