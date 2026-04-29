#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para limpiar y reiniciar la base de datos, luego insertar datos correctos
"""

from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

from app import app, db
from modelos.base_datos import (
    Usuario, Profesor, Estudiante, Asignatura,
    Calificacion, Asistencia, EvaluacionEmocional,
    Intervencion, MensajeChat, Recomendacion, KPI
)

def limpiar_bd():
    """Elimina todos los datos de la BD"""
    print("Limpiando base de datos...")
    with app.app_context():
        db.drop_all()
        db.create_all()
    print("✓ Base de datos limpiada\n")

def insertar_datos():
    """Inserta datos de prueba correctos"""
    with app.app_context():
        print("Insertando datos de prueba...\n")
        
        # ======================== USUARIOS ========================
        print("1. Creando usuarios...")
        
        # Profesores
        prof1 = Usuario(
            email='juan.perez@universidad.edu',
            nombre='Juan',
            apellido='Pérez García',
            rol='profesor',
            institucion='Universidad Técnica del Centro'
        )
        prof1.set_password('profesor123')
        
        prof2 = Usuario(
            email='maria.lopez@universidad.edu',
            nombre='María',
            apellido='López Martínez',
            rol='profesor',
            institucion='Universidad Técnica del Centro'
        )
        prof2.set_password('profesor123')
        
        prof3 = Usuario(
            email='carlos.ruiz@universidad.edu',
            nombre='Carlos',
            apellido='Ruiz Sánchez',
            rol='profesor',
            institucion='Universidad Técnica del Centro'
        )
        prof3.set_password('profesor123')
        
        # Estudiantes
        est1 = Usuario(
            email='ana.garcia@estudiante.edu',
            nombre='Ana',
            apellido='García Rodríguez',
            rol='alumno',
            institucion='Universidad Técnica del Centro'
        )
        est1.set_password('estudiante123')
        
        est2 = Usuario(
            email='luis.martinez@estudiante.edu',
            nombre='Luis',
            apellido='Martínez Flores',
            rol='alumno',
            institucion='Universidad Técnica del Centro'
        )
        est2.set_password('estudiante123')
        
        est3 = Usuario(
            email='sofia.diaz@estudiante.edu',
            nombre='Sofía',
            apellido='Díaz López',
            rol='alumno',
            institucion='Universidad Técnica del Centro'
        )
        est3.set_password('estudiante123')
        
        est4 = Usuario(
            email='diego.torres@estudiante.edu',
            nombre='Diego',
            apellido='Torres Gómez',
            rol='alumno',
            institucion='Universidad Técnica del Centro'
        )
        est4.set_password('estudiante123')
        
        est5 = Usuario(
            email='laura.sanchez@estudiante.edu',
            nombre='Laura',
            apellido='Sánchez Vargas',
            rol='alumno',
            institucion='Universidad Técnica del Centro'
        )
        est5.set_password('estudiante123')
        
        usuarios = [prof1, prof2, prof3, est1, est2, est3, est4, est5]
        db.session.add_all(usuarios)
        db.session.commit()
        print(f"   ✓ {len(usuarios)} usuarios creados\n")
        
        # ======================== PROFESORES ========================
        print("2. Creando profesores...")
        
        p1 = Profesor(usuario_id=prof1.id, departamento='Ciencias Exactas', especialidad='Matemáticas', telefono='+34 912 345 678')
        p2 = Profesor(usuario_id=prof2.id, departamento='Tecnología', especialidad='Ingeniería de Sistemas', telefono='+34 912 345 679')
        p3 = Profesor(usuario_id=prof3.id, departamento='Ciencias Exactas', especialidad='Física', telefono='+34 912 345 680')
        
        profesores = [p1, p2, p3]
        db.session.add_all(profesores)
        db.session.commit()
        print(f"   ✓ {len(profesores)} profesores creados\n")
        
        # ======================== ESTUDIANTES ========================
        print("3. Creando estudiantes...")
        
        s1 = Estudiante(usuario_id=est1.id, carrera='Ingeniería Informática', semestre=4, grupo='A', matricula='MAT20240001', promedio_academico=3.8, nivel_riesgo='bajo', asistencia_porcentaje=95.0)
        s2 = Estudiante(usuario_id=est2.id, carrera='Ingeniería Informática', semestre=4, grupo='A', matricula='MAT20240002', promedio_academico=3.2, nivel_riesgo='medio', razon_riesgo='Bajo desempeño en matemáticas', asistencia_porcentaje=85.0)
        s3 = Estudiante(usuario_id=est3.id, carrera='Ingeniería Industrial', semestre=3, grupo='B', matricula='MAT20240003', promedio_academico=2.9, nivel_riesgo='alto', razon_riesgo='Ausencias frecuentes y bajo rendimiento', asistencia_porcentaje=70.0)
        s4 = Estudiante(usuario_id=est4.id, carrera='Ingeniería Informática', semestre=4, grupo='A', matricula='MAT20240004', promedio_academico=3.5, nivel_riesgo='bajo', asistencia_porcentaje=92.0)
        s5 = Estudiante(usuario_id=est5.id, carrera='Ingeniería Industrial', semestre=3, grupo='B', matricula='MAT20240005', promedio_academico=2.3, nivel_riesgo='critico', razon_riesgo='En riesgo de deserción', asistencia_porcentaje=45.0)
        
        estudiantes = [s1, s2, s3, s4, s5]
        db.session.add_all(estudiantes)
        db.session.commit()
        print(f"   ✓ {len(estudiantes)} estudiantes creados\n")
        
        # ======================== ASIGNATURAS ========================
        print("4. Creando asignaturas...")
        
        asig_data = [
            Asignatura(nombre='Cálculo I', codigo='MAT101', profesor_id=p1.id, carrera='Ingeniería Informática', semestre=1, creditos=4, descripcion='Introducción al cálculo'),
            Asignatura(nombre='Programación I', codigo='INF101', profesor_id=p2.id, carrera='Ingeniería Informática', semestre=1, creditos=3, descripcion='Fundamentos de programación'),
            Asignatura(nombre='Física I', codigo='FIS101', profesor_id=p3.id, carrera='Ingeniería Informática', semestre=1, creditos=4, descripcion='Mecánica clásica'),
            Asignatura(nombre='Cálculo II', codigo='MAT102', profesor_id=p1.id, carrera='Ingeniería Informática', semestre=2, creditos=4, descripcion='Cálculo avanzado'),
            Asignatura(nombre='Programación II', codigo='INF102', profesor_id=p2.id, carrera='Ingeniería Informática', semestre=2, creditos=3, descripcion='Programación OOP'),
            Asignatura(nombre='Base de Datos', codigo='INF103', profesor_id=p2.id, carrera='Ingeniería Informática', semestre=3, creditos=3, descripcion='Diseño de BD'),
            Asignatura(nombre='Ingeniería de Software', codigo='INF104', profesor_id=p2.id, carrera='Ingeniería Informática', semestre=4, creditos=3, descripcion='Metodologías'),
            Asignatura(nombre='Resistencia de Materiales', codigo='IND101', profesor_id=p1.id, carrera='Ingeniería Industrial', semestre=1, creditos=4, descripcion='Análisis de esfuerzos'),
            Asignatura(nombre='Procesos Industriales', codigo='IND102', profesor_id=p3.id, carrera='Ingeniería Industrial', semestre=2, creditos=3, descripcion='Optimización'),
        ]
        db.session.add_all(asig_data)
        db.session.commit()
        print(f"   ✓ {len(asig_data)} asignaturas creadas\n")
        
        # ======================== CALIFICACIONES ========================
        print("5. Creando calificaciones...")
        
        calif_data = [
            Calificacion(estudiante_id=s1.id, asignatura_id=asig_data[0].id, calificacion=4.5, estado='aprobada', periodo='2024-I'),
            Calificacion(estudiante_id=s1.id, asignatura_id=asig_data[1].id, calificacion=4.3, estado='aprobada', periodo='2024-I'),
            Calificacion(estudiante_id=s2.id, asignatura_id=asig_data[0].id, calificacion=3.2, estado='aprobada', periodo='2024-I'),
            Calificacion(estudiante_id=s2.id, asignatura_id=asig_data[1].id, calificacion=3.1, estado='aprobada', periodo='2024-I'),
            Calificacion(estudiante_id=s3.id, asignatura_id=asig_data[7].id, calificacion=2.5, estado='aprobada', periodo='2024-I'),
            Calificacion(estudiante_id=s4.id, asignatura_id=asig_data[0].id, calificacion=4.1, estado='aprobada', periodo='2024-I'),
            Calificacion(estudiante_id=s5.id, asignatura_id=asig_data[0].id, calificacion=2.0, estado='aprobada', periodo='2024-I'),
            Calificacion(estudiante_id=s5.id, asignatura_id=asig_data[1].id, calificacion=1.8, estado='reprobada', periodo='2024-I'),
        ]
        db.session.add_all(calif_data)
        db.session.commit()
        print(f"   ✓ {len(calif_data)} calificaciones creadas\n")
        
        # ======================== ASISTENCIAS ========================
        print("6. Creando asistencias...")
        
        fecha_base = datetime(2024, 3, 1)
        asist_count = 0
        
        for i, estudiante in enumerate(estudiantes):
            for j in range(2):
                for k in range(4):
                    fecha = fecha_base + timedelta(days=k*3)
                    presente = not (i >= 2 and k >= 2)  # Algunos con faltas
                    asistencia = Asistencia(
                        estudiante_id=estudiante.id,
                        asignatura_id=asig_data[j].id,
                        fecha=fecha.date(),
                        presente=presente,
                        periodo='2024-I'
                    )
                    db.session.add(asistencia)
                    asist_count += 1
        
        db.session.commit()
        print(f"   ✓ {asist_count} asistencias creadas\n")
        
        # ======================== EVALUACIONES EMOCIONALES ========================
        print("7. Creando evaluaciones emocionales...")
        
        eval_emo = [
            EvaluacionEmocional(estudiante_id=s1.id, sentimiento='motivación', puntuacion=0.95, contexto='Comprometido'),
            EvaluacionEmocional(estudiante_id=s2.id, sentimiento='frustración', puntuacion=0.75, contexto='Dificultades'),
            EvaluacionEmocional(estudiante_id=s3.id, sentimiento='ansiedad', puntuacion=0.85, contexto='Preocupado'),
            EvaluacionEmocional(estudiante_id=s4.id, sentimiento='confianza', puntuacion=0.92, contexto='Seguro'),
            EvaluacionEmocional(estudiante_id=s5.id, sentimiento='depresión', puntuacion=0.70, contexto='Económico'),
        ]
        db.session.add_all(eval_emo)
        db.session.commit()
        print(f"   ✓ {len(eval_emo)} evaluaciones creadas\n")
        
        # ======================== INTERVENCIONES ========================
        print("8. Creando intervenciones...")
        
        fecha_interv = datetime.now() - timedelta(days=10)
        intervenciones = [
            Intervencion(estudiante_id=s2.id, profesor_id=p1.id, tipo_intervencion='asesoria', descripcion='Ayuda en Cálculo', fecha_programada=fecha_interv, fecha_realizacion=fecha_interv, estado='completada', resultado='Mejora esperada'),
            Intervencion(estudiante_id=s3.id, profesor_id=p1.id, tipo_intervencion='cita', descripcion='Reunión de rendimiento', fecha_programada=fecha_interv, fecha_realizacion=fecha_interv, estado='completada', resultado='Canalizado a bienestar'),
            Intervencion(estudiante_id=s5.id, profesor_id=p2.id, tipo_intervencion='llamada', descripcion='Verificación', fecha_programada=fecha_interv, fecha_realizacion=fecha_interv, estado='completada', resultado='Dirigido a becas'),
        ]
        db.session.add_all(intervenciones)
        db.session.commit()
        print(f"   ✓ {len(intervenciones)} intervenciones creadas\n")
        
        # ======================== MENSAJES CHAT ========================
        print("9. Creando mensajes de chat...")
        
        mensajes = [
            MensajeChat(estudiante_id=s1.id, rol='estudiante', contenido='Tengo dudas sobre derivadas', sentimiento_detectado='curiosidad', puntuacion_sentimiento=0.70),
            MensajeChat(estudiante_id=s1.id, rol='ia', contenido='La derivada de sen(x) es cos(x)', sentimiento_detectado='ayuda', puntuacion_sentimiento=0.85),
            MensajeChat(estudiante_id=s2.id, rol='estudiante', contenido='No entiendo programación', sentimiento_detectado='frustración', puntuacion_sentimiento=0.85),
            MensajeChat(estudiante_id=s2.id, rol='ia', contenido='Es normal al inicio, practicemos', sentimiento_detectado='apoyo', puntuacion_sentimiento=0.80),
            MensajeChat(estudiante_id=s3.id, rol='estudiante', contenido='Tengo problemas en casa', sentimiento_detectado='ansiedad', puntuacion_sentimiento=0.80),
            MensajeChat(estudiante_id=s3.id, rol='ia', contenido='Contacta con bienestar', sentimiento_detectado='empatía', puntuacion_sentimiento=0.85),
            MensajeChat(estudiante_id=s5.id, rol='estudiante', contenido='Problemas económicos', sentimiento_detectado='estrés', puntuacion_sentimiento=0.90),
            MensajeChat(estudiante_id=s5.id, rol='ia', contenido='Contacta la oficina de becas', sentimiento_detectado='empatía', puntuacion_sentimiento=0.85),
        ]
        db.session.add_all(mensajes)
        db.session.commit()
        print(f"   ✓ {len(mensajes)} mensajes creados\n")
        
        # ======================== RECOMENDACIONES ========================
        print("10. Creando recomendaciones...")
        
        recomendaciones = [
            Recomendacion(estudiante_id=s1.id, tipo='académica', contenido='Cursos avanzados en matemáticas', prioridad='media', leida=True),
            Recomendacion(estudiante_id=s2.id, tipo='académica', contenido='Trabajar lógica de programación', prioridad='alta', leida=True),
            Recomendacion(estudiante_id=s3.id, tipo='personal', contenido='Busca apoyo en bienestar', prioridad='critica', leida=True),
            Recomendacion(estudiante_id=s4.id, tipo='liderazgo', contenido='Sé monitor de asignatura', prioridad='baja', leida=False),
            Recomendacion(estudiante_id=s5.id, tipo='económica', contenido='URGENTE: Contacta becas', prioridad='critica', leida=True),
        ]
        db.session.add_all(recomendaciones)
        db.session.commit()
        print(f"   ✓ {len(recomendaciones)} recomendaciones creadas\n")
        
        # ======================== KPIs ========================
        print("11. Creando KPIs...")
        
        kpis = [
            KPI(institucion='Universidad Técnica del Centro', fecha=datetime(2024, 3, 15).date(), alumnos_en_riesgo=2, alertas_nuevas=1, materias_criticas=1, tasa_desercion=0.02, promedio_academico_general=3.54),
            KPI(institucion='Universidad Técnica del Centro', fecha=datetime(2024, 3, 22).date(), alumnos_en_riesgo=3, alertas_nuevas=2, materias_criticas=2, tasa_desercion=0.04, promedio_academico_general=3.42),
            KPI(institucion='Universidad Técnica del Centro', fecha=datetime(2024, 3, 29).date(), alumnos_en_riesgo=2, alertas_nuevas=0, materias_criticas=1, tasa_desercion=0.02, promedio_academico_general=3.56),
        ]
        db.session.add_all(kpis)
        db.session.commit()
        print(f"   ✓ {len(kpis)} KPIs creados\n")
        
        print("="*60)
        print("✓ ¡Todos los datos insertados correctamente!")
        print("="*60)
        print("\n🔐 Credenciales de Acceso:\n")
        print("Profesor:")
        print("  Email: juan.perez@universidad.edu")
        print("  Contraseña: profesor123\n")
        print("Estudiante:")
        print("  Email: ana.garcia@estudiante.edu")
        print("  Contraseña: estudiante123\n")

def main():
    """Función principal"""
    try:
        limpiar_bd()
        insertar_datos()
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
