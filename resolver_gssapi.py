#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para resolver el problema de autenticación GSSAPI en MySQL

El error 'auth_gssapi_client' ocurre cuando MySQL usa autenticación del SO
en lugar de autenticación estándar con contraseña.
"""

import os
import subprocess
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

def mostrar_menu():
    """Muestra el menú de opciones"""
    print(f"\n{Colores.AZUL}{Colores.NEGRITA}")
    print("╔════════════════════════════════════════════════╗")
    print("║  SOLUCIONAR ERROR GSSAPI EN MYSQL              ║")
    print("╚════════════════════════════════════════════════╝")
    print(f"{Colores.FIN}\n")
    
    print("El error 'auth_gssapi_client' significa que MySQL usa autenticación del SO.")
    print("Elige cómo resolverlo:\n")
    
    print(f"{Colores.AMARILLO}1.{Colores.FIN} Reiniciar MySQL sin autenticación GSSAPI (recomendado)")
    print(f"{Colores.AMARILLO}2.{Colores.FIN} Ver información de cómo configurar manualmente")
    print(f"{Colores.AMARILLO}3.{Colores.FIN} Probar conexión directa con CLI")
    print(f"{Colores.AMARILLO}4.{Colores.FIN} Ver archivo de configuración")
    print()

def opcion_1_reiniciar_mysql():
    """Opción 1: Reiniciar MySQL"""
    print(f"\n{Colores.NEGRITA}Opción 1: Reiniciar MySQL sin GSSAPI{Colores.FIN}\n")
    
    print("En Windows, MySQL se ejecuta como servicio.")
    print("Sigue estos pasos:")
    print()
    
    print(f"{Colores.AMARILLO}Paso 1: Abre Command Prompt como Administrador{Colores.FIN}")
    print(f"{Colores.AMARILLO}Paso 2: Ejecuta este comando:{Colores.FIN}")
    print(f"  {Colores.AZUL}net stop MySQL80{Colores.FIN}")
    print()
    
    print("Si MySQL tiene otro nombre, prueba:")
    print(f"  {Colores.AZUL}sc query | findstr MySQL{Colores.FIN}")
    print()
    
    print(f"{Colores.AMARILLO}Paso 3: Edita el archivo my.ini de MySQL:{Colores.FIN}")
    print("  Ubicación típica: C:\\ProgramData\\MySQL\\MySQL Server 8.0\\my.ini")
    print()
    
    print(f"{Colores.AMARILLO}Paso 4: En la sección [mysqld], agrega o modifica:{Colores.FIN}")
    print(f"  {Colores.VERDE}[mysqld]{Colores.FIN}")
    print(f"  {Colores.VERDE}default_authentication_plugin=mysql_native_password{Colores.FIN}")
    print()
    
    print(f"{Colores.AMARILLO}Paso 5: Reinicia MySQL con:{Colores.FIN}")
    print(f"  {Colores.AZUL}net start MySQL80{Colores.FIN}")
    print()
    
    print(f"{Colores.AMARILLO}Paso 6: Verifica la conexión:{Colores.FIN}")
    print(f"  {Colores.AZUL}mysql -u root -p{Colores.FIN}")
    print()

def opcion_2_info():
    """Opción 2: Información detallada"""
    print(f"\n{Colores.NEGRITA}Opción 2: Información detallada{Colores.FIN}\n")
    
    print(f"{Colores.AMARILLO}¿Qué es GSSAPI?{Colores.FIN}")
    print("GSSAPI (Generic Security Service API) es autenticación del sistema operativo.")
    print("MySQL intenta usar credenciales de Windows en lugar de la contraseña.")
    print()
    
    print(f"{Colores.AMARILLO}¿Cómo se produce?{Colores.FIN}")
    print("1. MySQL instalado con autenticación GSSAPI habilitada")
    print("2. Usuario 'root' configurado para usar GSSAPI")
    print("3. PyMySQL no soporta este método de autenticación")
    print()
    
    print(f"{Colores.AMARILLO}Soluciones (en orden de recomendación):{Colores.FIN}")
    print("1. Cambiar a mysql_native_password (contraseña simple)")
    print("2. Crear usuario específico para la app")
    print("3. Usar MySQL desde WSL2 en lugar de Windows")
    print()

def opcion_3_probar_conexion():
    """Opción 3: Probar conexión"""
    print(f"\n{Colores.NEGRITA}Opción 3: Probar conexión con CLI{Colores.FIN}\n")
    
    load_dotenv()
    
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', 'localhost')
    
    print(f"Intenta conectar directamente con:")
    print(f"  {Colores.AZUL}mysql -h {db_host} -u {db_user} -p{Colores.FIN}")
    print()
    print(f"Cuando pida contraseña, ingresa: {Colores.AMARILLO}{db_password}{Colores.FIN}")
    print()
    
    print("Si conecta exitosamente:")
    print(f"  {Colores.VERDE}mysql> CREATE DATABASE acompania;{Colores.FIN}")
    print(f"  {Colores.VERDE}mysql> SELECT VERSION();{Colores.FIN}")
    print()

def opcion_4_ver_config():
    """Opción 4: Ver configuración"""
    print(f"\n{Colores.NEGRITA}Opción 4: Configuración de MySQL{Colores.FIN}\n")
    
    print("Ubicaciones típicas del archivo my.ini en Windows:")
    print("  • C:\\ProgramData\\MySQL\\MySQL Server 8.0\\my.ini")
    print("  • C:\\Program Files\\MySQL\\MySQL Server 8.0\\my.ini")
    print()
    
    print("Para encontrarlo, ejecuta en Power Shell (como Admin):")
    print(f"  {Colores.AZUL}Get-Service | findstr MySQL{Colores.FIN}")
    print()
    
    print("Luego busca el path del ejecutable y localiza my.ini ahí.")
    print()

def crear_usuario_nueva():
    """Crear un nuevo usuario MySQL"""
    print(f"\n{Colores.NEGRITA}ALTERNATIVA: Crear usuario nuevo para la app{Colores.FIN}\n")
    
    print("Si tienes acceso a MySQL, crea un usuario específico:")
    print()
    print(f"{Colores.VERDE}mysql> CREATE USER 'acompania'@'localhost'{Colores.FIN}")
    print(f"{Colores.VERDE}        IDENTIFIED WITH mysql_native_password BY 'acompania123';{Colores.FIN}")
    print()
    print(f"{Colores.VERDE}mysql> GRANT ALL PRIVILEGES ON acompania.* TO 'acompania'@'localhost';{Colores.FIN}")
    print()
    print(f"{Colores.VERDE}mysql> FLUSH PRIVILEGES;{Colores.FIN}")
    print()
    
    print("Luego actualiza tu .env:")
    print(f"  {Colores.AZUL}DB_USER=acompania{Colores.FIN}")
    print(f"  {Colores.AZUL}DB_PASSWORD=acompania123{Colores.FIN}")
    print()

def main():
    """Función principal"""
    while True:
        mostrar_menu()
        
        opcion = input(f"{Colores.AMARILLO}Selecciona una opción (1-4) o 'q' para salir:{Colores.FIN} ").strip().lower()
        
        if opcion == 'q':
            print(f"\n{Colores.VERDE}¡Hasta luego!{Colores.FIN}\n")
            break
        elif opcion == '1':
            opcion_1_reiniciar_mysql()
        elif opcion == '2':
            opcion_2_info()
        elif opcion == '3':
            opcion_3_probar_conexion()
        elif opcion == '4':
            opcion_4_ver_config()
        else:
            print(f"{Colores.ROJO}Opción no válida{Colores.FIN}")
        
        # Preguntar si continuar
        print()
        continuar = input(f"{Colores.AMARILLO}¿Deseas ver otra opción? (s/n):{Colores.FIN} ").strip().lower()
        if continuar != 's':
            break
    
    # Mostrar alternativa
    print(f"\n{Colores.NEGRITA}═══════════════════════════════════════════════{Colores.FIN}")
    crear_usuario_nueva()
    print(f"{Colores.NEGRITA}═══════════════════════════════════════════════{Colores.FIN}\n")

if __name__ == '__main__':
    main()
