#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para insertar datos de prueba realistas en AcompañIA
Crea usuarios, estudiantes, profesores, calificaciones, mensajes de chat, etc.
"""

import os
from datetime import datetime, timedelta
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


class InsertorDatos:
    """Clase para insertar datos de prueba en la BD"""
    
    def __init__(self):
        self.contador = {
            'usuarios': 0,
            'profesores': 0,
            'estudiantes': 0,
            'asignaturas': 0,
            'calificaciones': 0,
            'asistencias': 0,
            'evaluaciones': 0,
            'intervenciones': 0,
            'mensajes': 0,
            'recomendaciones': 0,
            'kpis': 0
        }
    
    def crear_usuarios(self):
        """Crear usuarios de prueba"""
        print("Creando usuarios...")
        
        # Profesores
        profesores_data = [
            {
                'email': 'juan.perez@universidad.edu',
                'nombre': 'Juan',
                'apellido': 'Pérez García',
                'rol': 'profesor',
                'institucion': 'Universidad Técnica del Centro',
                'password': 'profesor123'
            },
            {
                'email': 'maria.lopez@universidad.edu',
                'nombre': 'María',
                'apellido': 'López Martínez',
                'rol': 'profesor',
                'institucion': 'Universidad Técnica del Centro',
                'password': 'profesor123'
            },
            {
                'email': 'carlos.ruiz@universidad.edu',
                'nombre': 'Carlos',
                'apellido': 'Ruiz Sánchez',
                'rol': 'profesor',
                'institucion': 'Universidad Técnica del Centro',
                'password': 'profesor123'
            }
        ]
        
        # Estudiantes
        estudiantes_data = [
            {
                'email': 'ana.garcia@estudiante.edu',
                'nombre': 'Ana',
                'apellido': 'García Rodríguez',
                'rol': 'alumno',
                'institucion': 'Universidad Técnica del Centro',
                'password': 'estudiante123'
            },
            {
                'email': 'luis.martinez@estudiante.edu',
                'nombre': 'Luis',
                'apellido': 'Martínez Flores',
                'rol': 'alumno',
                'institucion': 'Universidad Técnica del Centro',
                'password': 'estudiante123'
            },
            {
                'email': 'sofia.diaz@estudiante.edu',
                'nombre': 'Sofía',
                'apellido': 'Díaz López',
                'rol': 'alumno',
                'institucion': 'Universidad Técnica del Centro',
                'password': 'estudiante123'
            },
            {
                'email': 'diego.torres@estudiante.edu',
                'nombre': 'Diego',
                'apellido': 'Torres Gómez',
                'rol': 'alumno',
                'institucion': 'Universidad Técnica del Centro',
                'password': 'estudiante123'
            },
            {
                'email': 'laura.sanchez@estudiante.edu',
                'nombre': 'Laura',
                'apellido': 'Sánchez Vargas',
                'rol': 'alumno',
                'institucion': 'Universidad Técnica del Centro',
                'password': 'estudiante123'
            }
        ]
        
        usuarios_creados = []
        
        # Crear profesores
        for prof in profesores_data:
            usuario = Usuario(
                email=prof['email'],
                nombre=prof['nombre'],
                apellido=prof['apellido'],
                rol=prof['rol'],
                institucion=prof['institucion']
            )
            usuario.set_password(prof['password'])
            db.session.add(usuario)
            usuarios_creados.append(usuario)
            self.contador['usuarios'] += 1
        
        # Crear estudiantes
        for est in estudiantes_data:
            usuario = Usuario(
                email=est['email'],
                nombre=est['nombre'],
                apellido=est['apellido'],
                rol=est['rol'],
                institucion=est['institucion']
            )
            usuario.set_password(est['password'])
            db.session.add(usuario)
            usuarios_creados.append(usuario)
            self.contador['usuarios'] += 1
        
        db.session.commit()
        print(f"  ✓ {self.contador['usuarios']} usuarios creados\n")
        return usuarios_creados
    
    def crear_profesores(self, usuarios):
        """Crear registros de profesores"""
        print("Creando profesores...")
        
        profesor_data = [
            {
                'usuario_id': usuarios[0].id,
                'departamento': 'Ciencias Exactas',
                'especialidad': 'Matemáticas',
                'telefono': '+34 912 345 678'
            },
            {
                'usuario_id': usuarios[1].id,
                'departamento': 'Tecnología',
                'especialidad': 'Ingeniería de Sistemas',
                'telefono': '+34 912 345 679'
            },
            {
                'usuario_id': usuarios[2].id,
                'departamento': 'Ciencias Exactas',
                'especialidad': 'Física',
                'telefono': '+34 912 345 680'
            }
        ]
        
        profesores = []
        for prof in profesor_data:
            p = Profesor(**prof)
            db.session.add(p)
            profesores.append(p)
            self.contador['profesores'] += 1
        
        db.session.commit()
        print(f"  ✓ {self.contador['profesores']} profesores creados\n")
        return profesores
    
    def crear_estudiantes(self, usuarios):
        """Crear registros de estudiantes"""
        print("Creando estudiantes...")
        
        estudiante_data = [
            {
                'usuario_id': usuarios[3].id,
                'carrera': 'Ingeniería Informática',
                'semestre': 4,
                'grupo': 'A',
                'matricula': 'MAT20240001',
                'promedio_academico': 3.8,
                'nivel_riesgo': 'bajo',
                'asistencia_porcentaje': 95.0
            },
            {
                'usuario_id': usuarios[4].id,
                'carrera': 'Ingeniería Informática',
                'semestre': 4,
                'grupo': 'A',
                'matricula': 'MAT20240002',
                'promedio_academico': 3.2,
                'nivel_riesgo': 'medio',
                'razon_riesgo': 'Bajo desempeño en matemáticas',
                'asistencia_porcentaje': 85.0
            },
            {
                'usuario_id': usuarios[5].id,
                'carrera': 'Ingeniería Industrial',
                'semestre': 3,
                'grupo': 'B',
                'matricula': 'MAT20240003',
                'promedio_academico': 2.9,
                'nivel_riesgo': 'alto',
                'razon_riesgo': 'Ausencias frecuentes y bajo rendimiento',
                'asistencia_porcentaje': 70.0
            },
            {
                'usuario_id': usuarios[6].id,
                'carrera': 'Ingeniería Informática',
                'semestre': 4,
                'grupo': 'A',
                'matricula': 'MAT20240004',
                'promedio_academico': 3.5,
                'nivel_riesgo': 'bajo',
                'asistencia_porcentaje': 92.0
            },
            {
                'usuario_id': usuarios[7].id,
                'carrera': 'Ingeniería Industrial',
                'semestre': 3,
                'grupo': 'B',
                'matricula': 'MAT20240005',
                'promedio_academico': 2.3,
                'nivel_riesgo': 'critico',
                'razon_riesgo': 'En riesgo de deserción',
                'asistencia_porcentaje': 45.0
            }
        ]
        
        estudiantes = []
        for est in estudiante_data:
            e = Estudiante(**est)
            db.session.add(e)
            estudiantes.append(e)
            self.contador['estudiantes'] += 1
        
        db.session.commit()
        print(f"  ✓ {self.contador['estudiantes']} estudiantes creados\n")
        return estudiantes
    
    def crear_asignaturas(self, profesores):
        """Crear asignaturas"""
        print("Creando asignaturas...")
        
        asignatura_data = [
            {
                'nombre': 'Cálculo I',
                'codigo': 'MAT101',
                'profesor_id': profesores[0].id,
                'carrera': 'Ingeniería Informática',
                'semestre': 1,
                'creditos': 4,
                'descripcion': 'Introducción al cálculo diferencial e integral'
            },
            {
                'nombre': 'Programación I',
                'codigo': 'INF101',
                'profesor_id': profesores[1].id,
                'carrera': 'Ingeniería Informática',
                'semestre': 1,
                'creditos': 3,
                'descripcion': 'Fundamentos de programación en Python'
            },
            {
                'nombre': 'Física I',
                'codigo': 'FIS101',
                'profesor_id': profesores[2].id,
                'carrera': 'Ingeniería Informática',
                'semestre': 1,
                'creditos': 4,
                'descripcion': 'Mecánica clásica y termodinámica'
            },
            {
                'nombre': 'Cálculo II',
                'codigo': 'MAT102',
                'profesor_id': profesores[0].id,
                'carrera': 'Ingeniería Informática',
                'semestre': 2,
                'creditos': 4,
                'descripcion': 'Cálculo avanzado y aplicaciones'
            },
            {
                'nombre': 'Programación II',
                'codigo': 'INF102',
                'profesor_id': profesores[1].id,
                'carrera': 'Ingeniería Informática',
                'semestre': 2,
                'creditos': 3,
                'descripcion': 'Programación orientada a objetos'
            },
            {
                'nombre': 'Base de Datos',
                'codigo': 'INF103',
                'profesor_id': profesores[1].id,
                'carrera': 'Ingeniería Informática',
                'semestre': 3,
                'creditos': 3,
                'descripcion': 'Diseño e implementación de bases de datos'
            },
            {
                'nombre': 'Ingeniería de Software',
                'codigo': 'INF104',
                'profesor_id': profesores[1].id,
                'carrera': 'Ingeniería Informática',
                'semestre': 4,
                'creditos': 3,
                'descripcion': 'Metodologías y prácticas en desarrollo'
            },
            {
                'nombre': 'Resistencia de Materiales',
                'codigo': 'IND101',
                'profesor_id': profesores[0].id,
                'carrera': 'Ingeniería Industrial',
                'semestre': 1,
                'creditos': 4,
                'descripcion': 'Análisis de esfuerzos en materiales'
            },
            {
                'nombre': 'Procesos Industriales',
                'codigo': 'IND102',
                'profesor_id': profesores[2].id,
                'carrera': 'Ingeniería Industrial',
                'semestre': 2,
                'creditos': 3,
                'descripcion': 'Optimización de procesos'
            }
        ]
        
        asignaturas = []
        for asig in asignatura_data:
            a = Asignatura(**asig)
            db.session.add(a)
            asignaturas.append(a)
            self.contador['asignaturas'] += 1
        
        db.session.commit()
        print(f"  ✓ {self.contador['asignaturas']} asignaturas creadas\n")
        return asignaturas
    
    def crear_calificaciones(self, estudiantes, asignaturas):
        """Crear calificaciones"""
        print("Creando calificaciones...")
        
        # Calificaciones por estudiante
        calificaciones_data = [
            # Ana García - Buenas notas
            {'est_idx': 0, 'asig_idx': 0, 'nota': 4.5, 'estado': 'aprobada'},
            {'est_idx': 0, 'asig_idx': 1, 'nota': 4.3, 'estado': 'aprobada'},
            {'est_idx': 0, 'asig_idx': 2, 'nota': 4.6, 'estado': 'aprobada'},
            {'est_idx': 0, 'asig_idx': 3, 'nota': 4.2, 'estado': 'aprobada'},
            {'est_idx': 0, 'asig_idx': 4, 'nota': 4.4, 'estado': 'aprobada'},
            
            # Luis Martínez - Promedio
            {'est_idx': 1, 'asig_idx': 0, 'nota': 3.2, 'estado': 'aprobada'},
            {'est_idx': 1, 'asig_idx': 1, 'nota': 3.1, 'estado': 'aprobada'},
            {'est_idx': 1, 'asig_idx': 2, 'nota': 2.8, 'estado': 'aprobada'},
            {'est_idx': 1, 'asig_idx': 3, 'nota': 2.9, 'estado': 'aprobada'},
            {'est_idx': 1, 'asig_idx': 4, 'nota': 3.5, 'estado': 'aprobada'},
            
            # Sofía Díaz - Bajo rendimiento
            {'est_idx': 2, 'asig_idx': 7, 'nota': 2.5, 'estado': 'aprobada'},
            {'est_idx': 2, 'asig_idx': 8, 'nota': 2.0, 'estado': 'aprobada'},
            
            # Diego Torres - Excelente
            {'est_idx': 3, 'asig_idx': 0, 'nota': 4.1, 'estado': 'aprobada'},
            {'est_idx': 3, 'asig_idx': 1, 'nota': 3.9, 'estado': 'aprobada'},
            {'est_idx': 3, 'asig_idx': 2, 'nota': 4.3, 'estado': 'aprobada'},
            {'est_idx': 3, 'asig_idx': 3, 'nota': 4.0, 'estado': 'aprobada'},
            {'est_idx': 3, 'asig_idx': 4, 'nota': 4.1, 'estado': 'aprobada'},
            
            # Laura Sánchez - En riesgo
            {'est_idx': 4, 'asig_idx': 0, 'nota': 2.0, 'estado': 'aprobada'},
            {'est_idx': 4, 'asig_idx': 1, 'nota': 1.8, 'estado': 'reprobada'},
            {'est_idx': 4, 'asig_idx': 2, 'nota': 1.5, 'estado': 'reprobada'},
        ]
        
        for cal in calificaciones_data:
            calificacion = Calificacion(
                estudiante_id=estudiantes[cal['est_idx']].id,
                asignatura_id=asignaturas[cal['asig_idx']].id,
                calificacion=cal['nota'],
                estado=cal['estado'],
                periodo='2024-I'
            )
            db.session.add(calificacion)
            self.contador['calificaciones'] += 1
        
        db.session.commit()
        print(f"  ✓ {self.contador['calificaciones']} calificaciones creadas\n")
    
    def crear_asistencias(self, estudiantes, asignaturas):
        """Crear registros de asistencia"""
        print("Creando asistencias...")
        
        fecha_base = datetime(2024, 3, 1)
        
        # Patrones de asistencia
        patrones = [
            # Ana - Perfecta asistencia
            [True, True, True, True],
            # Luis - Algunas faltas
            [True, False, True, False],
            # Sofía - Muchas faltas
            [False, False, True, False],
            # Diego - Excelente
            [True, True, True, True],
            # Laura - Muy pocas asistencias
            [False, False, True, False]
        ]
        
        for est_idx, estudiante in enumerate(estudiantes):
            for asig_idx in range(min(2, len(asignaturas))):
                patron = patrones[est_idx]
                for i, presente in enumerate(patron):
                    fecha = fecha_base + timedelta(days=i*3)
                    asistencia = Asistencia(
                        estudiante_id=estudiante.id,
                        asignatura_id=asignaturas[asig_idx].id,
                        fecha=fecha.date(),
                        presente=presente,
                        periodo='2024-I'
                    )
                    db.session.add(asistencia)
                    self.contador['asistencias'] += 1
        
        db.session.commit()
        print(f"  ✓ {self.contador['asistencias']} asistencias creadas\n")
    
    def crear_evaluaciones_emocionales(self, estudiantes):
        """Crear evaluaciones emocionales"""
        print("Creando evaluaciones emocionales...")
        
        emociones = [
            # Ana - Positivo
            [
                {'sentimiento': 'motivación', 'puntuacion': 0.95, 'contexto': 'Estudiante muy comprometido'},
                {'sentimiento': 'confianza', 'puntuacion': 0.90, 'contexto': 'Resolvió problema difícil'}
            ],
            # Luis - Frustración
            [
                {'sentimiento': 'frustración', 'puntuacion': 0.75, 'contexto': 'Dificultades con programación'},
                {'sentimiento': 'incertidumbre', 'puntuacion': 0.65, 'contexto': 'No entiende la base de datos'}
            ],
            # Sofía - Ansiedad
            [
                {'sentimiento': 'ansiedad', 'puntuacion': 0.85, 'contexto': 'Preocupado por calificaciones'},
                {'sentimiento': 'desánimo', 'puntuacion': 0.80, 'contexto': 'Ausencias frecuentes'}
            ],
            # Diego - Confianza
            [
                {'sentimiento': 'confianza', 'puntuacion': 0.92, 'contexto': 'Muy seguro de sus habilidades'},
                {'sentimiento': 'motivación', 'puntuacion': 0.88, 'contexto': 'Participa activamente'}
            ],
            # Laura - Depresión
            [
                {'sentimiento': 'depresión', 'puntuacion': 0.70, 'contexto': 'Situación económica difícil'},
                {'sentimiento': 'desesperación', 'puntuacion': 0.75, 'contexto': 'En riesgo de abandonar'}
            ]
        ]
        
        for est_idx, estudiante in enumerate(estudiantes):
            for emo in emociones[est_idx]:
                evaluacion = EvaluacionEmocional(
                    estudiante_id=estudiante.id,
                    sentimiento=emo['sentimiento'],
                    puntuacion=emo['puntuacion'],
                    contexto=emo['contexto']
                )
                db.session.add(evaluacion)
                self.contador['evaluaciones'] += 1
        
        db.session.commit()
        print(f"  ✓ {self.contador['evaluaciones']} evaluaciones emocionales creadas\n")
    
    def crear_intervenciones(self, estudiantes, profesores):
        """Crear intervenciones"""
        print("Creando intervenciones...")
        
        intervenciones_data = [
            {
                'est_idx': 0,
                'prof_idx': 0,
                'tipo': 'asesoria',
                'descripcion': 'Asesoría sobre técnicas de estudio',
                'resultado': 'Estudiante motivado, no requiere'
            },
            {
                'est_idx': 1,
                'prof_idx': 0,
                'tipo': 'asesoria',
                'descripcion': 'Ayuda con dificultades en Cálculo',
                'resultado': 'Explicados conceptos básicos'
            },
            {
                'est_idx': 2,
                'prof_idx': 0,
                'tipo': 'cita',
                'descripcion': 'Reunión por bajo rendimiento',
                'resultado': 'Canalizado a bienestar'
            },
            {
                'est_idx': 4,
                'prof_idx': 1,
                'tipo': 'llamada',
                'descripcion': 'Verificación de situación',
                'resultado': 'Dirigido a becas'
            }
        ]
        
        for interv in intervenciones_data:
            fecha = datetime.now() - timedelta(days=10)
            intervencion = Intervencion(
                estudiante_id=estudiantes[interv['est_idx']].id,
                profesor_id=profesores[interv['prof_idx']].id,
                tipo_intervencion=interv['tipo'],
                descripcion=interv['descripcion'],
                fecha_programada=fecha,
                fecha_realizacion=fecha,
                estado='completada',
                resultado=interv['resultado']
            )
            db.session.add(intervencion)
            self.contador['intervenciones'] += 1
        
        db.session.commit()
        print(f"  ✓ {self.contador['intervenciones']} intervenciones creadas\n")
    
    def crear_mensajes_chat(self, estudiantes):
        """Crear mensajes de chat"""
        print("Creando mensajes de chat...")
        
        mensajes_data = [
            # Ana - Positivo
            [
                {'rol': 'estudiante', 'contenido': 'Tengo dudas sobre derivadas trigonométricas', 'sentimiento': 'curiosidad', 'puntuacion': 0.70},
                {'rol': 'ia', 'contenido': 'La derivada de sen(x) es cos(x)', 'sentimiento': 'ayuda', 'puntuacion': 0.85},
            ],
            # Luis - Frustración
            [
                {'rol': 'estudiante', 'contenido': 'No entiendo nada de programación', 'sentimiento': 'frustración', 'puntuacion': 0.85},
                {'rol': 'ia', 'contenido': 'Eso es normal, practicemos juntos', 'sentimiento': 'apoyo', 'puntuacion': 0.80},
            ],
            # Sofía - Ansiedad
            [
                {'rol': 'estudiante', 'contenido': 'Tengo problemas en casa', 'sentimiento': 'ansiedad', 'puntuacion': 0.80},
                {'rol': 'ia', 'contenido': 'Contacta con bienestar estudiantil', 'sentimiento': 'apoyo', 'puntuacion': 0.85},
            ],
            # Diego - Confianza
            [
                {'rol': 'estudiante', 'contenido': 'Entendí bien este tema', 'sentimiento': 'confianza', 'puntuacion': 0.90},
                {'rol': 'ia', 'contenido': 'Excelente progreso, continuemos', 'sentimiento': 'felicitación', 'puntuacion': 0.95},
            ],
            # Laura - Estrés
            [
                {'rol': 'estudiante', 'contenido': 'Tengo problemas económicos', 'sentimiento': 'estrés', 'puntuacion': 0.90},
                {'rol': 'ia', 'contenido': 'Contacta oficina de becas', 'sentimiento': 'empatía', 'puntuacion': 0.85},
            ]
        ]
        
        for est_idx, estudiante in enumerate(estudiantes):
            for msg in mensajes_data[est_idx]:
                mensaje = MensajeChat(
                    estudiante_id=estudiante.id,
                    rol=msg['rol'],
                    contenido=msg['contenido'],
                    sentimiento_detectado=msg['sentimiento'],
                    puntuacion_sentimiento=msg['puntuacion']
                )
                db.session.add(mensaje)
                self.contador['mensajes'] += 1
        
        db.session.commit()
        print(f"  ✓ {self.contador['mensajes']} mensajes de chat creados\n")
    
    def crear_recomendaciones(self, estudiantes):
        """Crear recomendaciones"""
        print("Creando recomendaciones...")
        
        recomendaciones_data = [
            # Ana
            [
                {'tipo': 'académica', 'contenido': 'Considera cursos avanzados en matemáticas', 'prioridad': 'media'},
                {'tipo': 'oportunidad', 'contenido': 'Participa en programa de tutorías', 'prioridad': 'baja'}
            ],
            # Luis
            [
                {'tipo': 'académica', 'contenido': 'Trabaja en lógica de programación', 'prioridad': 'alta'},
                {'tipo': 'apoyo', 'contenido': 'Busca grupo de estudio', 'prioridad': 'alta'}
            ],
            # Sofía
            [
                {'tipo': 'personal', 'contenido': 'Busca apoyo en bienestar estudiantil', 'prioridad': 'critica'},
                {'tipo': 'económica', 'contenido': 'Investiga opciones de becas', 'prioridad': 'critica'}
            ],
            # Diego
            [
                {'tipo': 'académica', 'contenido': 'Tu desempeño es excelente', 'prioridad': 'media'},
                {'tipo': 'liderazgo', 'contenido': 'Considera ser monitor', 'prioridad': 'baja'}
            ],
            # Laura
            [
                {'tipo': 'económica', 'contenido': 'URGENTE: Contacta oficina de becas', 'prioridad': 'critica'},
                {'tipo': 'personal', 'contenido': 'Habla con un consejero', 'prioridad': 'critica'},
                {'tipo': 'académica', 'contenido': 'Reprogramar cursos es opción', 'prioridad': 'alta'}
            ]
        ]
        
        for est_idx, estudiante in enumerate(estudiantes):
            for rec in recomendaciones_data[est_idx]:
                recomendacion = Recomendacion(
                    estudiante_id=estudiante.id,
                    tipo=rec['tipo'],
                    contenido=rec['contenido'],
                    prioridad=rec['prioridad'],
                    leida=est_idx < 3  # Primeros 3 ya las leyeron
                )
                db.session.add(recomendacion)
                self.contador['recomendaciones'] += 1
        
        db.session.commit()
        print(f"  ✓ {self.contador['recomendaciones']} recomendaciones creadas\n")
    
    def crear_kpis(self):
        """Crear KPIs"""
        print("Creando KPIs...")
        
        kpis_data = [
            {'fecha': datetime(2024, 3, 15).date(), 'riesgo': 2, 'alertas': 1, 'criticas': 1, 'desercion': 0.02, 'promedio': 3.54},
            {'fecha': datetime(2024, 3, 22).date(), 'riesgo': 3, 'alertas': 2, 'criticas': 2, 'desercion': 0.04, 'promedio': 3.42},
            {'fecha': datetime(2024, 3, 29).date(), 'riesgo': 2, 'alertas': 0, 'criticas': 1, 'desercion': 0.02, 'promedio': 3.56},
            {'fecha': datetime(2024, 4, 5).date(), 'riesgo': 2, 'alertas': 1, 'criticas': 1, 'desercion': 0.02, 'promedio': 3.58}
        ]
        
        for kpi_data in kpis_data:
            kpi = KPI(
                institucion='Universidad Técnica del Centro',
                fecha=kpi_data['fecha'],
                alumnos_en_riesgo=kpi_data['riesgo'],
                alertas_nuevas=kpi_data['alertas'],
                materias_criticas=kpi_data['criticas'],
                tasa_desercion=kpi_data['desercion'],
                promedio_academico_general=kpi_data['promedio']
            )
            db.session.add(kpi)
            self.contador['kpis'] += 1
        
        db.session.commit()
        print(f"  ✓ {self.contador['kpis']} KPIs creados\n")
    
    def ejecutar(self):
        """Ejecutar todo el proceso"""
        with app.app_context():
            try:
                print("\n" + "="*60)
                print("INSERTAR DATOS DE PRUEBA - AcompañIA")
                print("="*60 + "\n")
                
                usuarios = self.crear_usuarios()
                profesores = self.crear_profesores(usuarios[:3])
                estudiantes = self.crear_estudiantes(usuarios)
                asignaturas = self.crear_asignaturas(profesores)
                
                self.crear_calificaciones(estudiantes, asignaturas)
                self.crear_asistencias(estudiantes, asignaturas)
                self.crear_evaluaciones_emocionales(estudiantes)
                self.crear_intervenciones(estudiantes, profesores)
                self.crear_mensajes_chat(estudiantes)
                self.crear_recomendaciones(estudiantes)
                self.crear_kpis()
                
                print("="*60)
                print("RESUMEN DE DATOS INSERTADOS")
                print("="*60)
                for clave, valor in self.contador.items():
                    print(f"  {clave.replace('_', ' ').title()}: {valor}")
                
                print("\n✓ ¡Datos de prueba insertados exitosamente!\n")
                print("Credenciales para acceder:")
                print("  Profesor: juan.perez@universidad.edu / profesor123")
                print("  Estudiante: ana.garcia@estudiante.edu / estudiante123")
                print("  (También hay 2 profesores y 4 estudiantes más)\n")
                
            except Exception as e:
                print(f"\n✗ Error al insertar datos: {e}")
                db.session.rollback()
                return False
        
        return True


def main():
    """Función principal"""
    insertor = InsertorDatos()
    insertor.ejecutar()


if __name__ == '__main__':
    main()
