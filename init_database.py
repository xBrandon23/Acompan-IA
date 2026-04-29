#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para inicializar la base de datos MySQL para AcompañIA

Uso:
    python init_database.py          # Crea todas las tablas
    python init_database.py --reset  # Borra y recrea las tablas
    python init_database.py --test   # Agrega datos de prueba
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar la app y modelos
from app import app, db
from modelos.base_datos import (
    Usuario, Profesor, Estudiante, Asignatura,
    Calificacion, Asistencia, EvaluacionEmocional,
    Intervencion, MensajeChat, Recomendacion, KPI
)


def crear_tablas():
    """Crea todas las tablas en la base de datos"""
    print("=" * 60)
    print("Creando tablas en la base de datos MySQL...")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Crear todas las tablas
            db.create_all()
            print("\n✓ Tablas creadas exitosamente")
            
            # Verificar conexión
            db.session.execute('SELECT 1')
            print("✓ Conexión a MySQL verificada")
            
            return True
        except Exception as e:
            print(f"\n✗ Error al crear tablas: {e}")
            print("\nVerifica:")
            print(f"  - DB_USER: {os.getenv('DB_USER')}")
            print(f"  - DB_HOST: {os.getenv('DB_HOST')}")
            print(f"  - DB_PORT: {os.getenv('DB_PORT')}")
            print(f"  - DB_NAME: {os.getenv('DB_NAME')}")
            return False


def eliminar_tablas():
    """Elimina todas las tablas de la base de datos"""
    print("=" * 60)
    print("ADVERTENCIA: Esto eliminará TODAS las tablas")
    print("=" * 60)
    
    confirmacion = input("\n¿Estás seguro? Escribe 'sí' para continuar: ").strip().lower()
    
    if confirmacion != 'sí':
        print("Operación cancelada.")
        return False
    
    with app.app_context():
        try:
            db.drop_all()
            print("\n✓ Todas las tablas han sido eliminadas")
            return True
        except Exception as e:
            print(f"\n✗ Error al eliminar tablas: {e}")
            return False


def crear_datos_prueba():
    """Crea datos de prueba para desarrollar"""
    print("=" * 60)
    print("Creando datos de prueba...")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Verificar si ya existen datos
            if Usuario.query.first():
                print("\n✗ La base de datos ya contiene datos. Abortando...")
                return False
            
            # Crear usuarios profesores
            print("\n1. Creando profesores...")
            profesor1_user = Usuario(
                email='profesor1@ejemplo.com',
                nombre='Juan',
                apellido='Pérez García',
                rol='profesor',
                institucion='Universidad del Ejemplo'
            )
            profesor1_user.set_password('profesor123')
            
            profesor2_user = Usuario(
                email='profesor2@ejemplo.com',
                nombre='María',
                apellido='López Martínez',
                rol='profesor',
                institucion='Universidad del Ejemplo'
            )
            profesor2_user.set_password('profesor123')
            
            db.session.add(profesor1_user)
            db.session.add(profesor2_user)
            db.session.commit()
            
            print(f"   ✓ {Usuario.query.filter_by(rol='profesor').count()} profesores creados")
            
            # Crear profesores
            prof1 = Profesor(
                usuario_id=profesor1_user.id,
                departamento='Ciencias Exactas',
                especialidad='Matemáticas',
                telefono='+34 123 456 789'
            )
            prof2 = Profesor(
                usuario_id=profesor2_user.id,
                departamento='Letras',
                especialidad='Literatura',
                telefono='+34 987 654 321'
            )
            
            db.session.add(prof1)
            db.session.add(prof2)
            db.session.commit()
            
            # Crear asignaturas
            print("2. Creando asignaturas...")
            asig1 = Asignatura(
                nombre='Cálculo I',
                codigo='MAT101',
                profesor_id=prof1.id,
                carrera='Ingeniería Informática',
                semestre=1,
                creditos=4,
                descripcion='Introducción al cálculo diferencial e integral'
            )
            asig2 = Asignatura(
                nombre='Programación I',
                codigo='INF101',
                profesor_id=prof1.id,
                carrera='Ingeniería Informática',
                semestre=1,
                creditos=3,
                descripcion='Fundamentos de programación'
            )
            asig3 = Asignatura(
                nombre='Literatura Universal',
                codigo='LIT201',
                profesor_id=prof2.id,
                carrera='Humanidades',
                semestre=2,
                creditos=3,
                descripcion='Historia de la literatura mundial'
            )
            
            db.session.add_all([asig1, asig2, asig3])
            db.session.commit()
            
            print(f"   ✓ {Asignatura.query.count()} asignaturas creadas")
            
            # Crear estudiantes
            print("3. Creando estudiantes...")
            estudiantes_data = [
                {
                    'email': 'estudiante1@ejemplo.com',
                    'nombre': 'Carlos',
                    'apellido': 'Rodríguez',
                    'carrera': 'Ingeniería Informática',
                    'matricula': 'MAT2024001',
                    'semestre': 1,
                    'grupo': 'A'
                },
                {
                    'email': 'estudiante2@ejemplo.com',
                    'nombre': 'Ana',
                    'apellido': 'Martínez',
                    'carrera': 'Ingeniería Informática',
                    'matricula': 'MAT2024002',
                    'semestre': 1,
                    'grupo': 'A'
                },
                {
                    'email': 'estudiante3@ejemplo.com',
                    'nombre': 'Luis',
                    'apellido': 'González',
                    'carrera': 'Humanidades',
                    'matricula': 'HUM2024001',
                    'semestre': 2,
                    'grupo': 'B'
                },
            ]
            
            for data in estudiantes_data:
                usuario = Usuario(
                    email=data['email'],
                    nombre=data['nombre'],
                    apellido=data['apellido'],
                    rol='alumno',
                    institucion='Universidad del Ejemplo'
                )
                usuario.set_password('estudiante123')
                db.session.add(usuario)
                db.session.commit()
                
                estudiante = Estudiante(
                    usuario_id=usuario.id,
                    carrera=data['carrera'],
                    matricula=data['matricula'],
                    semestre=data['semestre'],
                    grupo=data['grupo'],
                    nivel_riesgo='bajo',
                    promedio_academico=3.5
                )
                db.session.add(estudiante)
            
            db.session.commit()
            print(f"   ✓ {Estudiante.query.count()} estudiantes creados")
            
            # Crear calificaciones
            print("4. Creando calificaciones...")
            estudiantes = Estudiante.query.all()
            asignaturas_list = Asignatura.query.all()
            
            for estudiante in estudiantes:
                for asig in asignaturas_list[:2]:  # Primeras 2 asignaturas
                    calif = Calificacion(
                        estudiante_id=estudiante.id,
                        asignatura_id=asig.id,
                        calificacion=3.5 + (estudiante.id % 2) * 0.5,
                        estado='activa',
                        periodo='2024-I'
                    )
                    db.session.add(calif)
            
            db.session.commit()
            print(f"   ✓ {Calificacion.query.count()} calificaciones creadas")
            
            # Crear KPIs
            print("5. Creando KPIs...")
            kpi = KPI(
                institucion='Universidad del Ejemplo',
                alumnos_en_riesgo=1,
                alertas_nuevas=0,
                materias_criticas=0,
                tasa_desercion=0.02,
                promedio_academico_general=3.5
            )
            db.session.add(kpi)
            db.session.commit()
            
            print(f"   ✓ {KPI.query.count()} KPIs creados")
            
            print("\n" + "=" * 60)
            print("✓ Datos de prueba creados exitosamente")
            print("=" * 60)
            print("\nCredenciales de acceso:")
            print("  Profesor: profesor1@ejemplo.com / profesor123")
            print("  Estudiante: estudiante1@ejemplo.com / estudiante123")
            
            return True
            
        except Exception as e:
            print(f"\n✗ Error al crear datos de prueba: {e}")
            db.session.rollback()
            return False


def mostrar_info():
    """Muestra información de la base de datos"""
    print("\n" + "=" * 60)
    print("Información de la Base de Datos")
    print("=" * 60)
    
    with app.app_context():
        try:
            print(f"\nDB_USER: {os.getenv('DB_USER')}")
            print(f"DB_HOST: {os.getenv('DB_HOST')}")
            print(f"DB_PORT: {os.getenv('DB_PORT')}")
            print(f"DB_NAME: {os.getenv('DB_NAME')}")
            
            # Contar registros
            print("\nRegistros en la base de datos:")
            print(f"  - Usuarios: {Usuario.query.count()}")
            print(f"  - Profesores: {Profesor.query.count()}")
            print(f"  - Estudiantes: {Estudiante.query.count()}")
            print(f"  - Asignaturas: {Asignatura.query.count()}")
            print(f"  - Calificaciones: {Calificacion.query.count()}")
            print(f"  - Asistencias: {Asistencia.query.count()}")
            print(f"  - Evaluaciones Emocionales: {EvaluacionEmocional.query.count()}")
            print(f"  - Intervenciones: {Intervencion.query.count()}")
            print(f"  - Mensajes Chat: {MensajeChat.query.count()}")
            print(f"  - Recomendaciones: {Recomendacion.query.count()}")
            print(f"  - KPIs: {KPI.query.count()}")
            
        except Exception as e:
            print(f"Error al obtener información: {e}")


def main():
    """Función principal"""
    print("\n" + "=" * 60)
    print("Inicializador de Base de Datos - AcompañIA")
    print("=" * 60 + "\n")
    
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        
        if comando == '--reset':
            if eliminar_tablas() and crear_tablas():
                print("\n✓ Base de datos reiniciada exitosamente")
        
        elif comando == '--test':
            if crear_tablas() and crear_datos_prueba():
                mostrar_info()
        
        elif comando == '--info':
            mostrar_info()
        
        elif comando == '--help':
            print("Opciones disponibles:")
            print("  (sin argumentos)    - Crea las tablas")
            print("  --reset             - Elimina y recrea las tablas")
            print("  --test              - Crea tablas y datos de prueba")
            print("  --info              - Muestra información de la BD")
            print("  --help              - Muestra esta ayuda")
        
        else:
            print(f"Comando desconocido: {comando}")
            print("Usa --help para ver las opciones disponibles")
    
    else:
        # Por defecto, crear tablas
        if crear_tablas():
            mostrar_info()
            print("\n✓ Base de datos inicializada exitosamente")


if __name__ == '__main__':
    main()
