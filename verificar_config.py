#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de verificación de configuración MySQL para AcompañIA

Verifica que todo esté correctamente configurado antes de ejecutar la aplicación
"""

import os
import sys
from dotenv import load_dotenv

# Colores para la terminal
class Colores:
    VERDE = '\033[92m'
    ROJO = '\033[91m'
    AMARILLO = '\033[93m'
    AZUL = '\033[94m'
    FIN = '\033[0m'
    NEGRITA = '\033[1m'

def verificar_archivo(ruta, nombre="Archivo"):
    """Verifica si un archivo existe"""
    if os.path.exists(ruta):
        print(f"  {Colores.VERDE}✓{Colores.FIN} {nombre} encontrado")
        return True
    else:
        print(f"  {Colores.ROJO}✗{Colores.FIN} {nombre} NO encontrado")
        return False

def verificar_env():
    """Verifica las variables de entorno"""
    print(f"\n{Colores.NEGRITA}Verificando variables de entorno...{Colores.FIN}")
    
    load_dotenv()
    
    variables = {
        'DB_USER': 'Usuario de MySQL',
        'DB_PASSWORD': 'Contraseña de MySQL',
        'DB_HOST': 'Host de MySQL',
        'DB_PORT': 'Puerto de MySQL',
        'DB_NAME': 'Nombre de la BD'
    }
    
    todas_ok = True
    for var, descripcion in variables.items():
        valor = os.getenv(var)
        if valor:
            print(f"  {Colores.VERDE}✓{Colores.FIN} {var}: {valor}")
        else:
            print(f"  {Colores.ROJO}✗{Colores.FIN} {var}: NO CONFIGURADO")
            todas_ok = False
    
    return todas_ok

def verificar_dependencias():
    """Verifica las dependencias de Python"""
    print(f"\n{Colores.NEGRITA}Verificando dependencias de Python...{Colores.FIN}")
    
    dependencias = {
        'flask': 'Flask',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'flask_cors': 'Flask-CORS',
        'pymysql': 'PyMySQL',
        'google.generativeai': 'Google Generative AI',
        'dotenv': 'python-dotenv'
    }
    
    todas_ok = True
    for modulo, nombre in dependencias.items():
        try:
            __import__(modulo)
            print(f"  {Colores.VERDE}✓{Colores.FIN} {nombre} instalado")
        except ImportError:
            print(f"  {Colores.ROJO}✗{Colores.FIN} {nombre} NO instalado")
            todas_ok = False
    
    return todas_ok

def verificar_conexion_mysql():
    """Verifica la conexión a MySQL"""
    print(f"\n{Colores.NEGRITA}Verificando conexión a MySQL...{Colores.FIN}")
    
    try:
        import pymysql
        
        db_user = os.getenv('DB_USER', 'root')
        db_password = os.getenv('DB_PASSWORD', '')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = int(os.getenv('DB_PORT', '3306'))
        db_name = os.getenv('DB_NAME', 'acompania')
        
        try:
            # Intentar conectar a MySQL
            conexion = pymysql.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                port=db_port,
                charset='utf8mb4'
            )
            print(f"  {Colores.VERDE}✓{Colores.FIN} Conexión a MySQL exitosa")
            
            # Verificar si la BD existe
            cursor = conexion.cursor()
            cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
            resultado = cursor.fetchone()
            
            if resultado:
                print(f"  {Colores.VERDE}✓{Colores.FIN} Base de datos '{db_name}' existe")
                
                # Verificar tablas
                cursor.execute(f"USE {db_name}")
                cursor.execute("SHOW TABLES")
                tablas = cursor.fetchall()
                
                if tablas:
                    print(f"  {Colores.VERDE}✓{Colores.FIN} Se encontraron {len(tablas)} tablas")
                    for tabla in tablas:
                        print(f"      - {tabla[0]}")
                else:
                    print(f"  {Colores.AMARILLO}⚠{Colores.FIN} La BD existe pero no tiene tablas")
                    print(f"      Ejecuta: {Colores.AZUL}python init_database.py{Colores.FIN}")
            else:
                print(f"  {Colores.AMARILLO}⚠{Colores.FIN} Base de datos '{db_name}' NO existe")
                print(f"      Ejecuta: {Colores.AZUL}python init_database.py{Colores.FIN}")
            
            cursor.close()
            conexion.close()
            return True
            
        except pymysql.Error as e:
            print(f"  {Colores.ROJO}✗{Colores.FIN} Error de conexión: {e}")
            print(f"      Verifica las credenciales en .env")
            return False
    
    except Exception as e:
        print(f"  {Colores.ROJO}✗{Colores.FIN} Error inesperado: {e}")
        return False

def verificar_aplicacion():
    """Verifica que la aplicación se puede importar"""
    print(f"\n{Colores.NEGRITA}Verificando aplicación...{Colores.FIN}")
    
    try:
        from app import app, db
        from modelos.base_datos import Usuario
        
        print(f"  {Colores.VERDE}✓{Colores.FIN} Aplicación Flask importada correctamente")
        print(f"  {Colores.VERDE}✓{Colores.FIN} Base de datos inicializada correctamente")
        print(f"  {Colores.VERDE}✓{Colores.FIN} Modelos importados correctamente")
        
        return True
    except Exception as e:
        print(f"  {Colores.ROJO}✗{Colores.FIN} Error al importar: {e}")
        return False

def mostrar_resumen(resultados):
    """Muestra un resumen de la verificación"""
    print(f"\n{Colores.NEGRITA}{'='*60}{Colores.FIN}")
    print(f"{Colores.NEGRITA}RESUMEN DE VERIFICACIÓN{Colores.FIN}")
    print(f"{Colores.NEGRITA}{'='*60}{Colores.FIN}\n")
    
    todas_ok = all(resultados.values())
    
    for verificacion, resultado in resultados.items():
        if resultado:
            print(f"  {Colores.VERDE}✓{Colores.FIN} {verificacion}")
        else:
            print(f"  {Colores.ROJO}✗{Colores.FIN} {verificacion}")
    
    print(f"\n{Colores.NEGRITA}{'='*60}{Colores.FIN}")
    
    if todas_ok:
        print(f"{Colores.VERDE}{Colores.NEGRITA}✓ ¡LISTO PARA EJECUTAR!{Colores.FIN}")
        print(f"Ejecuta: {Colores.AZUL}python app.py{Colores.FIN}\n")
        return 0
    else:
        print(f"{Colores.ROJO}{Colores.NEGRITA}✗ Hay problemas de configuración{Colores.FIN}")
        print(f"Consulta {Colores.AZUL}SETUP_MYSQL.md{Colores.FIN} para más ayuda\n")
        return 1

def main():
    """Función principal"""
    print(f"\n{Colores.AZUL}{Colores.NEGRITA}")
    print("╔════════════════════════════════════════════════╗")
    print("║  VERIFICADOR DE CONFIGURACIÓN - AcompañIA     ║")
    print("╚════════════════════════════════════════════════╝")
    print(f"{Colores.FIN}\n")
    
    resultados = {}
    
    # Ejecutar verificaciones
    print(f"{Colores.NEGRITA}Archivos principales:{Colores.FIN}")
    verificar_archivo('.env', 'Archivo .env')
    verificar_archivo('requirements.txt', 'requirements.txt')
    verificar_archivo('app.py', 'app.py')
    verificar_archivo('modelos/base_datos.py', 'Base de datos (modelos)')
    
    resultados['Variables de entorno'] = verificar_env()
    resultados['Dependencias de Python'] = verificar_dependencias()
    resultados['Conexión a MySQL'] = verificar_conexion_mysql()
    resultados['Aplicación'] = verificar_aplicacion()
    
    # Mostrar resumen
    return mostrar_resumen(resultados)

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
