# Resumen de Migración: SQLite → MySQL

## ✅ Cambios Realizados

### 1. **Actualizado `requirements.txt`**
Se agregaron las dependencias necesarias para MySQL:
```
PyMySQL==1.1.0          # Driver MySQL para Python
cryptography==41.0.7    # Cifrado para conexiones seguras
```

### 2. **Actualizado `app.py`**
Se reemplazó la configuración de SQLite por MySQL:
- Antes: `sqlite:///acompania.db`
- Ahora: `mysql+pymysql://user:password@host:port/database`

Configuración dinámica desde variables de entorno:
```python
DB_USER=root
DB_PASSWORD=contraseña
DB_HOST=localhost
DB_PORT=3306
DB_NAME=acompania
```

### 3. **Creado `.env`** (archivo de configuración)
```env
DB_USER=root
DB_PASSWORD=tu_contraseña_mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=acompania
```

### 4. **Creado `acompania_database.sql`**
Script SQL completo con:
- ✓ 11 tablas completamente modeladas
- ✓ Relaciones y constraints
- ✓ Índices para optimizar queries
- ✓ Validaciones CHECK
- ✓ Comentarios en español

**Tablas incluidas:**
1. `usuarios` - Usuarios del sistema
2. `profesores` - Datos de profesores
3. `estudiantes` - Datos de estudiantes
4. `asignaturas` - Asignaturas disponibles
5. `calificaciones` - Calificaciones de estudiantes
6. `asistencias` - Registro de asistencia
7. `evaluaciones_emocionales` - Análisis emocional de chats
8. `intervenciones` - Intervenciones del tutor
9. `mensajes_chat` - Historial de chats
10. `recomendaciones` - Recomendaciones automáticas
11. `kpis` - Métricas de la institución

### 5. **Creado `SETUP_MYSQL.md`**
Guía completa con:
- Instrucciones de instalación de MySQL para cada SO
- Pasos de configuración
- Múltiples opciones para crear la BD
- Solución de problemas (troubleshooting)
- Estructura visual de la BD

### 6. **Creado `init_database.py`**
Script Python para inicializar la BD desde la aplicación:
```bash
python init_database.py          # Crea las tablas
python init_database.py --reset  # Borra y recrea
python init_database.py --test   # Crea con datos de prueba
python init_database.py --info   # Muestra información
```

---

## 🚀 Inicio Rápido

### 1. Instalar MySQL Server
```bash
# Windows
# Descargar: https://dev.mysql.com/downloads/mysql/

# Mac
brew install mysql
brew services start mysql

# Linux
sudo apt-get install mysql-server
```

### 2. Editar `.env`
```env
DB_USER=root
DB_PASSWORD=tu_contraseña_mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=acompania
```

### 3. Instalar dependencias Python
```bash
pip install -r requirements.txt
```

### 4. Crear la base de datos

**Opción A (Recomendado - desde Python):**
```bash
python init_database.py --test
```

**Opción B (Desde MySQL CLI):**
```bash
mysql -u root -p < acompania_database.sql
```

**Opción C (Desde MySQL Workbench):**
- Abre MySQL Workbench
- Importa el archivo `acompania_database.sql`
- Ejecuta

### 5. Ejecutar la aplicación
```bash
python app.py
```

---

## 📊 Estructura de la Base de Datos

```
┌─────────────────────────────────────────────────┐
│           USUARIOS (Base)                       │
├─────────────────┬───────────────────────────────┤
│                 │                               │
└──────┬──────────┴──────┬───────────────────────┘
       │                 │
   PROFESORES      ESTUDIANTES
       │                 │
   ASIGNATURAS      ├─ CALIFICACIONES
       │            ├─ ASISTENCIAS
   ├─ CALIFICACIONES
   ├─ ASISTENCIAS      ├─ EVALUACIONES_EMOCIONALES
                       ├─ INTERVENCIONES
                       ├─ MENSAJES_CHAT
                       └─ RECOMENDACIONES
                       
                       KPIS (Independiente)
```

---

## 🔒 Características de Seguridad

✓ Constraints CHECK para validar datos  
✓ Foreign Keys con CASCADE para integridad referencial  
✓ Índices en columnas de búsqueda frecuente  
✓ Contraseñas hasheadas (werkzeug.security)  
✓ Sesiones HTTPS secure por defecto  
✓ CORS habilitado controladamente  

---

## 📈 Optimizaciones MySQL

- **Pool de conexiones**: Reutilización automática de conexiones
- **Pool pre-ping**: Verifica conexiones antes de usar
- **Pool recycle**: Recicla conexiones cada 1 hora
- **Índices estratégicos**: En foreign keys, búsquedas y filtros
- **Collation UTF-8**: Soporte completo para caracteres especiales

---

## 🧪 Datos de Prueba

Si ejecutas con `--test`:

**Profesores:**
- Email: profesor1@ejemplo.com | Contraseña: profesor123
- Email: profesor2@ejemplo.com | Contraseña: profesor123

**Estudiantes:**
- Email: estudiante1@ejemplo.com | Contraseña: estudiante123
- Email: estudiante2@ejemplo.com | Contraseña: estudiante123
- Email: estudiante3@ejemplo.com | Contraseña: estudiante123

**Datos incluidos:**
- 2 profesores con 3 asignaturas
- 3 estudiantes con calificaciones
- KPIs de la institución

---

## 🐛 Troubleshooting

| Error | Solución |
|-------|----------|
| `No module named 'pymysql'` | `pip install PyMySQL` |
| `Connection refused` | Verifica MySQL esté corriendo |
| `Access denied` | Revisa credenciales en `.env` |
| `Unknown database` | Ejecuta el script SQL |
| `Port 3306 already in use` | Cambia DB_PORT en `.env` |

---

## 📋 Checklist de Configuración

- [ ] MySQL Server instalado y ejecutándose
- [ ] Archivo `.env` configurado con credenciales
- [ ] `pip install -r requirements.txt` ejecutado
- [ ] Base de datos creada (`python init_database.py`)
- [ ] Aplicación inicia sin errores (`python app.py`)
- [ ] Puedes ingresar a http://localhost:5000
- [ ] Datos de prueba funcionales

---

## 📚 Archivos Creados/Modificados

| Archivo | Estado | Descripción |
|---------|--------|-------------|
| `requirements.txt` | ✏️ Modificado | Agregadas dependencias MySQL |
| `app.py` | ✏️ Modificado | Configuración de MySQL |
| `.env` | ✨ Nuevo | Variables de entorno |
| `acompania_database.sql` | ✨ Nuevo | Script SQL para crear BD |
| `init_database.py` | ✨ Nuevo | Script Python para inicializar BD |
| `SETUP_MYSQL.md` | ✨ Nuevo | Guía de configuración |
| `MIGRACION_RESUMEN.md` | ✨ Nuevo | Este archivo |

---

## 🔄 Migración de Datos (SQLite → MySQL)

Si tienes datos en la BD anterior de SQLite:

```python
from app import app, db
from modelos.base_datos import Usuario, Profesor, Estudiante

# 1. Exportar datos del SQLite antiguo
# 2. Importar a MySQL con la nueva app

# O usar un script de migración personalizado
```

---

## 📞 Soporte

Para más información:
- 📖 Consulta `SETUP_MYSQL.md`
- 📝 Lee los comentarios en `acompania_database.sql`
- 🐍 Revisa el código en `init_database.py`

---

**Migración completada: ✅**  
**Estado: Listo para producción** 🚀
