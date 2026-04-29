# Guía de Configuración de MySQL para AcompañIA

## Paso 1: Instalar MySQL Server

### Windows
1. Descargar desde: https://dev.mysql.com/downloads/mysql/
2. Ejecutar el instalador
3. Seguir los pasos del instalador
4. Recordar la contraseña de root que configures

### Mac
```bash
brew install mysql
brew services start mysql
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install mysql-server
sudo mysql_secure_installation
```

---

## Paso 2: Configurar Variables de Entorno

Editar el archivo `.env` en la raíz del proyecto:

```env
# ======================== CONFIGURACIÓN DE BASE DE DATOS MYSQL ========================
DB_USER=root
DB_PASSWORD=tu_contraseña_mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=acompania

# ======================== CONFIGURACIÓN DE LA APLICACIÓN ========================
SECRET_KEY=tu-clave-secreta-cambiar-en-produccion
FLASK_ENV=development

# ======================== CONFIGURACIÓN DE GEMINI AI ========================
GOOGLE_API_KEY=tu_api_key_de_google
```

**Reemplaza los valores con tus datos reales.**

---

## Paso 3: Crear la Base de Datos

### Opción A: Usando MySQL CLI

1. Abre una terminal/cmd y conéctate a MySQL:
```bash
mysql -u root -p
```
Ingresa tu contraseña de MySQL

2. Ejecuta el script SQL:
```bash
source acompania_database.sql
```

O copia y pega todo el contenido del archivo `acompania_database.sql` en la terminal MySQL.

### Opción B: Usando MySQL Workbench o herramienta gráfica

1. Abre MySQL Workbench
2. Conecta con tus credenciales
3. Abre el archivo `acompania_database.sql`
4. Haz clic en "Execute All" (ejecutar todo)

### Opción C: Usando Python (desde la app)

```bash
# Instala las dependencias
pip install -r requirements.txt

# En la terminal de Python
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
```

---

## Paso 4: Instalar Dependencias de Python

```bash
pip install -r requirements.txt
```

Esto instalará:
- Flask 3.0.3
- Flask-SQLAlchemy 3.1.1
- PyMySQL 1.1.0
- cryptography 41.0.7
- Y otras dependencias

---

## Paso 5: Crear Usuarios de Prueba (Opcional)

Puedes descomentar las líneas al final del archivo `acompania_database.sql` para agregar datos de prueba.

O desde Python:

```python
from app import app, db
from modelos.base_datos import Usuario, Profesor, Estudiante

with app.app_context():
    # Crear usuario profesor
    profesor_user = Usuario(
        email='profesor@example.com',
        nombre='Juan',
        apellido='Pérez',
        rol='profesor',
        institucion='Universidad del Ejemplo'
    )
    profesor_user.set_password('password123')
    
    # Crear usuario estudiante
    student_user = Usuario(
        email='estudiante@example.com',
        nombre='María',
        apellido='García',
        rol='alumno',
        institucion='Universidad del Ejemplo'
    )
    student_user.set_password('password123')
    
    db.session.add(profesor_user)
    db.session.add(student_user)
    db.session.commit()
    
    # Crear profesores y estudiantes
    prof = Profesor(usuario_id=profesor_user.id, departamento='Ciencias')
    estudiante = Estudiante(
        usuario_id=student_user.id,
        carrera='Ingeniería',
        semestre=4,
        matricula='MAT2024001'
    )
    
    db.session.add(prof)
    db.session.add(estudiante)
    db.session.commit()
    
    print("Usuarios de prueba creados exitosamente")
```

---

## Paso 6: Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: http://localhost:5000

---

## Verificar la Conexión

Para verificar que la conexión a MySQL está funcionando:

```python
from app import app, db

with app.app_context():
    try:
        db.session.execute('SELECT 1')
        print("✓ Conexión a MySQL exitosa")
    except Exception as e:
        print(f"✗ Error de conexión: {e}")
```

---

## Cambios Realizados

1. **requirements.txt**: Agregadas dependencias de MySQL
   - `PyMySQL==1.1.0` - Driver MySQL para Python
   - `cryptography==41.0.7` - Cifrado para conexiones seguras

2. **app.py**: 
   - Reemplazado SQLite por MySQL
   - Configuración dinámica desde variables de entorno
   - Pool de conexiones optimizado

3. **.env**: Archivo de configuración (crear/editar con tus valores)

4. **acompania_database.sql**: Script SQL con:
   - Todas las tablas necesarias
   - Índices para optimizar queries
   - Constraints y relaciones
   - Comentarios en español

---

## Troubleshooting

### Error: "No module named 'pymysql'"
```bash
pip install PyMySQL
```

### Error: "Connection refused"
- Verifica que MySQL está ejecutándose
- Comprueba las credenciales en `.env`
- Verifica el puerto (default: 3306)

### Error: "Access denied for user 'root'"
- Revisa la contraseña en `.env`
- Prueba conectar directamente: `mysql -u root -p`

### Error: "Unknown database 'acompania'"
- Asegúrate de haber ejecutado el script SQL: `acompania_database.sql`
- Verifica el nombre de la BD en `.env` (default: acompania)

---

## Estructura de la Base de Datos

```
USUARIOS
├── PROFESORES
│   └── ASIGNATURAS
│       ├── CALIFICACIONES
│       └── ASISTENCIAS
│
└── ESTUDIANTES
    ├── CALIFICACIONES
    ├── ASISTENCIAS
    ├── EVALUACIONES_EMOCIONALES
    ├── INTERVENCIONES
    ├── MENSAJES_CHAT
    └── RECOMENDACIONES

KPIs (independiente)
```

---

## Variables de Entorno Disponibles

| Variable | Default | Descripción |
|----------|---------|-------------|
| DB_USER | root | Usuario de MySQL |
| DB_PASSWORD | (vacío) | Contraseña de MySQL |
| DB_HOST | localhost | Host de MySQL |
| DB_PORT | 3306 | Puerto de MySQL |
| DB_NAME | acompania | Nombre de la base de datos |
| SECRET_KEY | (requerido) | Clave para sesiones Flask |
| GOOGLE_API_KEY | (requerido) | API Key de Google Gemini |
| FLASK_ENV | development | Entorno (development/production) |

---

¡Listo! Tu aplicación ahora está configurada para usar MySQL en lugar de SQLite.
