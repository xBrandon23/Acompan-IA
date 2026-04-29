# 🚀 GUÍA DE INICIO RÁPIDO - Acompan-IA

## ¡Bienvenido! 👋

Esta guía te ayudará a configurar y ejecutar **Acompan-IA** en minutos.

---

## 📋 Paso 1: Preparar el Entorno (5 minutos)

### 1.1 Verificar que tengas Python instalado
```bash
python --version
```
Debe ser 3.8 o superior.

### 1.2 Crear entorno virtual
```bash
cd Acompan-IA
python -m venv venv
```

### 1.3 Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

Deberías ver `(venv)` al inicio de tu línea de comandos.

### 1.4 Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## 🔑 Paso 2: Configurar API de Gemini (5 minutos)

### 2.1 Obtener API Key
1. Ve a: https://makersuite.google.com/app/apikey
2. Haz clic en "Create API Key"
3. Copia la clave

### 2.2 Configurar .env
Abre el archivo `.env` en el directorio raíz y reemplaza:
```
GEMINI_API_KEY=tu-clave-aqui
```

Con tu clave real.

---

## 🎯 Paso 3: Iniciar la Aplicación (2 minutos)

```bash
python app.py
```

Deberías ver algo como:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

## 🌐 Paso 4: Acceder a la Aplicación

1. Abre tu navegador
2. Ve a: **http://localhost:5000**
3. Serás redirigido al login

---

## 👤 Paso 5: Crear Usuarios de Prueba

### IMPORTANTE: Por ahora, la aplicación no tiene registro automático.

Necesitas crear usuarios en la base de datos. Aquí hay dos opciones:

### Opción A: Crear usuario directamente (Recomendado)

Crea un archivo `crear_usuarios_prueba.py` en la raíz del proyecto:

```python
from app import app, db
from modelos.base_datos import Usuario, Estudiante, Profesor

with app.app_context():
    # Crear usuario estudiante
    usuario_est = Usuario(
        email='estudiante@institucion.edu',
        nombre='Juan',
        apellido='Pérez',
        rol='alumno',
        institucion='Universidad Ejemplo'
    )
    usuario_est.set_password('password123')
    db.session.add(usuario_est)
    db.session.commit()
    
    # Crear estudiante asociado
    estudiante = Estudiante(
        usuario_id=usuario_est.id,
        carrera='Ingeniería en Sistemas',
        semestre=4,
        grupo='A',
        matricula='2024-001-123',
        promedio_academico=3.8,
        nivel_riesgo='bajo',
        asistencia_porcentaje=95.0
    )
    db.session.add(estudiante)
    db.session.commit()
    
    # Crear usuario profesor
    usuario_prof = Usuario(
        email='profesor@institucion.edu',
        nombre='María',
        apellido='García',
        rol='profesor',
        institucion='Universidad Ejemplo'
    )
    usuario_prof.set_password('password123')
    db.session.add(usuario_prof)
    db.session.commit()
    
    # Crear profesor asociado
    profesor = Profesor(
        usuario_id=usuario_prof.id,
        departamento='Ingeniería',
        especialidad='Sistemas'
    )
    db.session.add(profesor)
    db.session.commit()
    
    print("✓ Usuarios creados exitosamente!")
    print("Estudiante: estudiante@institucion.edu / password123")
    print("Profesor: profesor@institucion.edu / password123")
```

Ejecuta:
```bash
python crear_usuarios_prueba.py
```

---

## 🔐 Credenciales de Prueba

Una vez creados los usuarios, puedes usar:

### 👨‍🎓 Estudiante
- **Email**: `estudiante@institucion.edu`
- **Contraseña**: `password123`

### 👨‍🏫 Profesor
- **Email**: `profesor@institucion.edu`
- **Contraseña**: `password123`

---

## 📊 Interfaces Disponibles

### 🎓 Vista de Estudiante
- `/alumno/dashboard` - Dashboard personal
- `/alumno/perfil` - Perfil y historial académico
- `/alumno/chat` - Chat con Tutor IA

### 👨‍🏫 Vista de Profesor
- `/profesor/dashboard` - Panel de KPIs
- `/profesor/estudiantes` - Lista de estudiantes
- `/profesor/estudiantes/<id>` - Perfil del estudiante
- `/profesor/intervenciones` - Centro de intervenciones

### 📖 Públicas
- `/login` - Página de login
- `/privacidad` - Aviso de privacidad

---

## 🧪 Pruebas Recomendadas

### 1. **Chat con IA**
- Inicia sesión como estudiante
- Ve a "Chat Tutor"
- Prueba preguntas como:
  - "¿Cómo puedo mejorar mi promedio?"
  - "Me siento estresado con las tareas"
  - "¿Qué recursos hay disponibles?"

### 2. **Ver Estudiantes (Profesor)**
- Inicia sesión como profesor
- Ve a "Estudiantes"
- Prueba los filtros (carrera, semestre, riesgo)

### 3. **Crear Intervención**
- Como profesor, ve a "Estudiantes"
- Haz clic en "+" en una fila
- Crea una intervención de prueba

### 4. **Ver Dashboards**
- Explora ambos dashboards
- Revisa los gráficos y KPIs

---

## 🐛 Solución de Problemas

### ❌ Error: "ModuleNotFoundError: No module named 'flask'"
**Solución:**
```bash
# Asegúrate de haber activado el entorno virtual
# Luego reinstala:
pip install -r requirements.txt
```

### ❌ Error: "No such table: usuarios"
**Solución:**
```bash
# Reinicia la aplicación (creará las tablas automáticamente)
python app.py
```

### ❌ Error: "GEMINI_API_KEY not configured"
**Solución:**
1. Verifica que `.env` exista en la raíz
2. Verifica que tengas `GEMINI_API_KEY=tu-clave` en `.env`
3. Reinicia la aplicación

### ❌ Error: Puerto 5000 en uso
**Solución:**
```bash
# Cambia el puerto en app.py:
# app.run(debug=DEBUG, host='0.0.0.0', port=5001)

# O mata el proceso:
# Windows: netstat -ano | findstr :5000
# Linux/Mac: lsof -i :5000
```

---

## 📁 Estructura Base Creada

```
Acompan-IA/
├── app.py ........................... Aplicación principal
├── requirements.txt ................. Dependencias
├── .env ............................ Variables de entorno
├── .env.example ................... Ejemplo de .env
├── README.md ....................... Documentación principal
├── QUICK_START.md .................. Esta guía
│
├── modelos/
│   └── base_datos.py .............. 11 modelos SQLAlchemy
│
├── servicios/
│   └── gemini_ai.py ............... Integración IA
│
├── templates/
│   ├── base.html .................. Template base
│   ├── login.html ................. Login
│   ├── privacidad.html ............ Privacidad
│   ├── alumno/ .................... 3 templates
│   ├── profesor/ .................. 4 templates
│   └── errores/ ................... 2 templates
│
└── static/
    ├── css/
    │   └── styles.css ............ 400+ líneas CSS
    └── js/
        └── main.js ............... 400+ líneas JS
```

---

## ⚙️ Configuración Personalizada

### Cambiar Puerto
En `app.py`, línea final:
```python
app.run(debug=DEBUG, host='0.0.0.0', port=5001)  # Cambiar 5000 a 5001
```

### Cambiar Base de Datos
En `.env`:
```
# SQLite (actual)
DATABASE_URL=sqlite:///acompania.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/acompania

# MySQL
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/acompania
```

---

## 🎨 Personalizar la Aplicación

### Cambiar Colores
En `static/css/styles.css`:
```css
:root {
    --primary-color: #667eea;      /* Cambiar estos valores */
    --secondary-color: #764ba2;
    --success-color: #27ae60;
    --danger-color: #e74c3c;
    --warning-color: #f39c12;
    --info-color: #3498db;
}
```

### Agregar Logo
1. Guarda tu logo en `static/images/logo.png`
2. En `templates/base.html`, busca el navbar:
```html
<a class="navbar-brand" href="/">
    <img src="{{ url_for('static', filename='images/logo.png') }}" height="30">
    Acompan-IA
</a>
```

---

## 📞 Próximos Pasos

1. ✅ **Explora la interfaz** - Familiarízate con todas las vistas
2. 🔧 **Personaliza** - Adapta colores, textos, logo
3. 📊 **Agrega datos** - Crea más usuarios y datos de prueba
4. 🚀 **Deploya** - Sube a un servidor (Heroku, AWS, Digital Ocean)
5. 🔐 **Asegura** - Cambia claves secretas, configura HTTPS

---

## 📚 Recursos Útiles

- [Documentación Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Google Gemini API](https://ai.google.dev/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.0/)

---

## 💡 Tips Avanzados

### 1. Modo Debug
```python
# En app.py
DEBUG = os.getenv('FLASK_ENV') == 'development'
```

### 2. Logs
Agrega en app.py:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 3. Shell Interactivo
```bash
flask shell
>>> from modelos.base_datos import *
>>> Usuario.query.all()
```

---

## 🎉 ¡Listo!

Tu aplicación **Acompan-IA** está lista para usar. 

Si encuentras problemas, revisa:
1. El archivo `.env`
2. Los logs de la aplicación
3. La sección de Troubleshooting

**¡Que disfrutes desarrollando! 🚀**

---

**Última actualización:** Abril 2024
**Versión:** 1.0.0
