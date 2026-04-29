#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para crear datos de prueba en Acompan-IA
Ejecutar: python crear_datos_prueba.py
"""

from app import app, db
from modelos.base_datos import (
    Usuario, Estudiante, Profesor, Asignatura, 
    Calificacion, Asistencia, EvaluacionEmocional,
    Recomendacion, KPI
)
from datetime import datetime, timedelta
import random

def crear_usuarios_prueba():
    """Crear usuarios de prueba"""
    print("📝 Creando usuarios de prueba...")
    
    # Usuario Estudiante
    usuario_est = Usuario(
        email='estudiante@institucion.edu',
        nombre='Juan',
        apellido='Pérez García',
        rol='alumno',
        institucion='Universidad Nacional',
        activo=True
    )
    usuario_est.set_password('password123')
    
    # Usuario Profesor
    usuario_prof = Usuario(
        email='profesor@institucion.edu',
        nombre='María',
        apellido='López Rodríguez',
        rol='profesor',
        institucion='Universidad Nacional',
        activo=True
    )
    usuario_prof.set_password('password123')
    
    db.session.add(usuario_est)
    db.session.add(usuario_prof)
    db.session.commit()
    
    print("✓ Usuarios creados exitosamente")
    return usuario_est, usuario_prof


def crear_estudiantes(usuario_est):
    """Crear perfil de estudiante"""
    print("📚 Creando perfil de estudiante...")
    
    estudiante = Estudiante(
        usuario_id=usuario_est.id,
        carrera='Ingeniería en Sistemas',
        semestre=4,
        grupo='A',
        matricula='2024-001-001',
        promedio_academico=3.5,
        nivel_riesgo='medio',
        razon_riesgo='académica',
        asistencia_porcentaje=85.0
    )
    
    db.session.add(estudiante)
    db.session.commit()
    
    print("✓ Perfil de estudiante creado")
    return estudiante


def crear_profesores(usuario_prof):
    """Crear perfil de profesor"""
    print("👨‍🏫 Creando perfil de profesor...")
    
    profesor = Profesor(
        usuario_id=usuario_prof.id,
        departamento='Ingeniería',
        especialidad='Sistemas y Bases de Datos',
        telefono='+57 1 2345678'
    )
    
    db.session.add(profesor)
    db.session.commit()
    
    print("✓ Perfil de profesor creado")
    return profesor


def crear_asignaturas(profesor):
    """Crear asignaturas"""
    print("📖 Creando asignaturas...")
    
    asignaturas_data = [
        ('Bases de Datos Avanzadas', 'BD-401', '4', 'Ingeniería', 4),
        ('Programación Web', 'PW-402', '3', 'Ingeniería', 4),
        ('Análisis de Sistemas', 'AS-403', '4', 'Ingeniería', 4),
        ('Gestión de Proyectos', 'GP-404', '2', 'Ingeniería', 4),
    ]
    
    asignaturas = []
    for nombre, codigo, creditos, carrera, semestre in asignaturas_data:
        asignatura = Asignatura(
            nombre=nombre,
            codigo=codigo,
            creditos=int(creditos),
            carrera=carrera,
            semestre=semestre,
            profesor_id=profesor.id
        )
        db.session.add(asignatura)
        asignaturas.append(asignatura)
    
    db.session.commit()
    print(f"✓ {len(asignaturas)} asignaturas creadas")
    return asignaturas


def crear_calificaciones(estudiante, asignaturas):
    """Crear calificaciones"""
    print("📊 Creando calificaciones...")
    
    for asignatura in asignaturas:
        calificacion = Calificacion(
            estudiante_id=estudiante.id,
            asignatura_id=asignatura.id,
            calificacion=random.uniform(2.5, 4.5),
            estado='activa',
            periodo='2024-I'
        )
        db.session.add(calificacion)
    
    db.session.commit()
    print(f"✓ {len(asignaturas)} calificaciones creadas")


def crear_asistencias(estudiante, asignaturas):
    """Crear registros de asistencia"""
    print("📋 Creando asistencias...")
    
    count = 0
    for asignatura in asignaturas:
        # Crear registros de asistencia para los últimos 30 días
        for i in range(30):
            fecha = datetime.now().date() - timedelta(days=i)
            # Skip weekends
            if fecha.weekday() < 5:
                asistencia = Asistencia(
                    estudiante_id=estudiante.id,
                    asignatura_id=asignatura.id,
                    fecha=fecha,
                    presente=random.random() > 0.15,  # 85% presencia
                    periodo='2024-I'
                )
                db.session.add(asistencia)
                count += 1
    
    db.session.commit()
    print(f"✓ {count} registros de asistencia creados")


def crear_evaluaciones_emocionales(estudiante):
    """Crear evaluaciones emocionales"""
    print("💭 Creando evaluaciones emocionales...")
    
    sentimientos = [
        ('motivación', 'Me siento motivado a continuar'),
        ('frustración', 'Tengo dificultad con los temas'),
        ('ansiedad', 'Estoy preocupado por las notas'),
        ('alegría', 'Entendí bien el tema de hoy'),
        ('confusión', 'No entiendo bien cómo hacer esto'),
        ('tristeza', 'Me siento bajo de ánimo'),
        ('motivación', 'Voy a esforzarme más'),
    ]
    
    for i, (sentimiento, contexto) in enumerate(sentimientos):
        evaluacion = EvaluacionEmocional(
            estudiante_id=estudiante.id,
            sentimiento=sentimiento,
            puntuacion=random.uniform(0.3, 0.9),
            contexto=contexto,
            fecha_evaluacion=datetime.now() - timedelta(days=i)
        )
        db.session.add(evaluacion)
    
    db.session.commit()
    print(f"✓ {len(sentimientos)} evaluaciones emocionales creadas")


def crear_recomendaciones(estudiante):
    """Crear recomendaciones"""
    print("💡 Creando recomendaciones...")
    
    recomendaciones_data = [
        ('académica', 'Te recomendamos participar en tutorías para mejorar tu desempeño', 'alta'),
        ('emocional', 'Considera hablar con el psicólogo del campus para apoyo', 'media'),
        ('académica', 'Forma grupos de estudio con tus compañeros', 'media'),
        ('financiera', 'Existen becas disponibles para estudiantes en tu situación', 'alta'),
    ]
    
    for tipo, contenido, prioridad in recomendaciones_data:
        recom = Recomendacion(
            estudiante_id=estudiante.id,
            tipo=tipo,
            contenido=contenido,
            prioridad=prioridad
        )
        db.session.add(recom)
    
    db.session.commit()
    print(f"✓ {len(recomendaciones_data)} recomendaciones creadas")


def crear_kpis():
    """Crear KPIs"""
    print("📈 Creando KPIs...")
    
    kpi = KPI(
        institucion='Universidad Nacional',
        fecha=datetime.now().date(),
        alumnos_en_riesgo=45,
        alertas_nuevas=12,
        materias_criticas=8,
        tasa_desercion=3.5,
        promedio_academico_general=3.4
    )
    
    db.session.add(kpi)
    db.session.commit()
    print("✓ KPIs creados")


def main():
    """Función principal"""
    print("\n" + "="*60)
    print("🚀 CREADOR DE DATOS DE PRUEBA - ACOMPAN-IA")
    print("="*60 + "\n")
    
    try:
        with app.app_context():
            # Verificar si ya existe el usuario
            usuario_existente = Usuario.query.filter_by(email='estudiante@institucion.edu').first()
            if usuario_existente:
                print("⚠️  Los datos de prueba ya existen.")
                print("   Si deseas recrearlos, elimina primero la base de datos: acompania.db")
                return
            
            # Crear datos
            usuario_est, usuario_prof = crear_usuarios_prueba()
            estudiante = crear_estudiantes(usuario_est)
            profesor = crear_profesores(usuario_prof)
            asignaturas = crear_asignaturas(profesor)
            crear_calificaciones(estudiante, asignaturas)
            crear_asistencias(estudiante, asignaturas)
            crear_evaluaciones_emocionales(estudiante)
            crear_recomendaciones(estudiante)
            crear_kpis()
            
            print("\n" + "="*60)
            print("✅ ¡DATOS DE PRUEBA CREADOS EXITOSAMENTE!")
            print("="*60)
            print("\n📝 CREDENCIALES DE ACCESO:\n")
            print("👨‍🎓 ESTUDIANTE:")
            print("   Email: estudiante@institucion.edu")
            print("   Contraseña: password123")
            print("\n👨‍🏫 PROFESOR:")
            print("   Email: profesor@institucion.edu")
            print("   Contraseña: password123")
            print("\n🌐 URL de acceso: http://localhost:5000/login")
            print("="*60 + "\n")
            
    except Exception as e:
        print(f"\n❌ Error al crear los datos: {str(e)}")
        print("\nSoluciones:")
        print("1. Asegúrate de que la base de datos está inicializada")
        print("2. Ejecuta: python app.py (para crear tablas)")
        print("3. Luego ejecuta este script de nuevo")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
