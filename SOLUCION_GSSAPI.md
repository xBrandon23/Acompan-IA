# ⚠️ SOLUCIÓN: Error GSSAPI en MySQL

## Problema

```
Error de conexión: (2059, "Authentication plugin 'b'auth_gssapi_client'' not configured")
```

Este error ocurre porque **MySQL está usando autenticación del sistema operativo (GSSAPI)** en lugar de autenticación estándar con contraseña. PyMySQL no soporta este método.

---

## ✅ Soluciones

### Solución Rápida (Recomendada)

Ejecuta este script interactivo:

```bash
python resolver_gssapi.py
```

Te mostrará 4 opciones con instrucciones paso a paso.

---

### Solución 1: Cambiar Autenticación de MySQL

**Paso 1: Detener MySQL (como Administrador)**

```powershell
# Abre PowerShell/CMD como Administrador

# Encuentra el nombre del servicio MySQL
sc query | findstr MySQL

# Detén el servicio (típicamente MySQL80)
net stop MySQL80
```

**Paso 2: Editar my.ini**

Abre el archivo `my.ini` (ubicado típicamente en):
```
C:\ProgramData\MySQL\MySQL Server 8.0\my.ini
```

Busca la sección `[mysqld]` y agrega:

```ini
[mysqld]
default_authentication_plugin=mysql_native_password
```

**Paso 3: Reiniciar MySQL**

```powershell
net start MySQL80
```

**Paso 4: Verificar**

```powershell
mysql -u root -p
# Ingresa contraseña: 12345
```

---

### Solución 2: Crear Usuario Nuevo

Si prefieres no cambiar la configuración global:

**Paso 1: Conecta a MySQL**

```bash
mysql -u root -p
# Contraseña: 12345
```

**Paso 2: Crear usuario para la app**

```sql
CREATE USER 'acompania'@'localhost' 
IDENTIFIED WITH mysql_native_password BY 'acompania123';

GRANT ALL PRIVILEGES ON acompania.* 
TO 'acompania'@'localhost';

FLUSH PRIVILEGES;
```

**Paso 3: Actualiza .env**

```env
DB_USER=acompania
DB_PASSWORD=acompania123
DB_HOST=localhost
DB_PORT=3306
DB_NAME=acompania
```

---

### Solución 3: Usar WSL2 (Avanzado)

Si tienes WSL2 instalado:

```bash
# En WSL2
sudo apt-get install mysql-server
sudo service mysql start
```

Luego en `.env`:
```env
DB_HOST=localhost
DB_PORT=3306
```

---

## 🔍 Diagnosticar el Problema

Ejecuta este comando para ver el método de autenticación:

```bash
mysql -u root -p
```

```sql
mysql> SELECT user, host, plugin FROM mysql.user WHERE user='root';
+------+-----------+------------------+
| user | host      | plugin           |
+------+-----------+------------------+
| root | localhost | auth_gssapi*     | ← PROBLEMA
| root | %         | auth_gssapi*     | ← PROBLEMA
+------+-----------+------------------+

# DEBE SER:
+------+-----------+----------------------+
| user | host      | plugin               |
+------+-----------+----------------------+
| root | localhost | mysql_native_password| ← CORRECTO
+------+-----------+----------------------+
```

**Para arreglarlo:**

```sql
ALTER USER 'root'@'localhost' 
IDENTIFIED WITH mysql_native_password BY '12345';

ALTER USER 'root'@'%' 
IDENTIFIED WITH mysql_native_password BY '12345';

FLUSH PRIVILEGES;
```

---

## ✅ Verificar que Funciona

Una vez hecho lo anterior:

```bash
# Verificar configuración
python verificar_config.py
```

Debería mostrar:
```
✓ Variables de entorno
✓ Conexión a MySQL
✓ Aplicación
```

---

## 📋 Checklist de Solución

- [ ] Detuve MySQL (Administrador)
- [ ] Edité my.ini agregando `default_authentication_plugin=mysql_native_password`
- [ ] Reinicié MySQL
- [ ] Probé `mysql -u root -p` con contraseña `12345`
- [ ] Ejecuté `python verificar_config.py` sin errores
- [ ] Base de datos `acompania` existe
- [ ] Puedo ejecutar `python init_database.py --test`

---

## 🆘 Si Nada Funciona

Reinstala MySQL:

```bash
# 1. Desinstala completamente MySQL
# Windows: Ir a Panel de Control → Desinstalar
# o usar Command Prompt: msiexec /x {MySQL-GUID}

# 2. Elimina carpeta de datos
# C:\ProgramData\MySQL

# 3. Descargar e instalar fresh
# https://dev.mysql.com/downloads/mysql/

# 4. En el instalador, IMPORTANTE:
#    - Usar mysql_native_password (NO GSSAPI)
#    - Configurar 'root' con contraseña: 12345
```

---

## 📞 Recursos

- [MySQL Authentication Plugins](https://dev.mysql.com/doc/refman/8.0/en/authentication-plugins.html)
- [PyMySQL Documentation](https://pymysql.readthedocs.io/)
- Script interactivo: `python resolver_gssapi.py`

---

**Última actualización:** 29 de abril de 2026  
**Estado:** Documentado y probado ✅
