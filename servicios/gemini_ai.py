import os
import google.generativeai as genai
import json
import re
from datetime import datetime

class GeminiAI:
    """Servicio para integrar Gemini AI como tutor"""
    
    def __init__(self):
        """Inicializar el servicio de Gemini"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY no está configurada en variables de entorno")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.chat_history = {}
    
    def obtener_respuesta(self, mensaje, estudiante):
        """
        Obtener respuesta personalizada del tutor IA
        
        Args:
            mensaje: Mensaje del estudiante
            estudiante: Objeto Estudiante
            
        Returns:
            dict: {'respuesta': str, 'sentimiento': str, 'puntuacion': float}
        """
        
        # Preparar contexto del estudiante
        contexto = self._preparar_contexto(estudiante)
        
        # Crear prompt del sistema
        prompt_sistema = self._crear_prompt_sistema(contexto)
        
        # Construir mensaje completo
        mensaje_completo = f"{prompt_sistema}\n\nMensaje del estudiante: {mensaje}"
        
        try:
            # Obtener respuesta de Gemini
            respuesta = self.model.generate_content(mensaje_completo)
            texto_respuesta = respuesta.text
            
            # Analizar sentimiento
            sentimiento, puntuacion = self._analizar_sentimiento(mensaje)
            
            return {
                'respuesta': texto_respuesta,
                'sentimiento': sentimiento,
                'puntuacion': puntuacion
            }
        
        except Exception as e:
            print(f"Error en Gemini: {e}")
            return {
                'respuesta': "Disculpa, estoy experimentando dificultades técnicas. Por favor, intenta de nuevo.",
                'sentimiento': 'error',
                'puntuacion': 0.0
            }
    
    def _preparar_contexto(self, estudiante):
        """Preparar contexto del estudiante para el tutor"""
        from modelos.base_datos import Calificacion, EvaluacionEmocional
        
        # Obtener últimas calificaciones
        calificaciones = Calificacion.query.filter_by(
            estudiante_id=estudiante.id
        ).order_by(Calificacion.fecha_registro.desc()).limit(5).all()
        
        # Obtener evaluaciones emocionales recientes
        emociones = EvaluacionEmocional.query.filter_by(
            estudiante_id=estudiante.id
        ).order_by(EvaluacionEmocional.fecha_evaluacion.desc()).limit(3).all()
        
        contexto = {
            'nombre': estudiante.usuario_est.nombre,
            'carrera': estudiante.carrera,
            'semestre': estudiante.semestre,
            'promedio': estudiante.promedio_academico,
            'nivel_riesgo': estudiante.nivel_riesgo,
            'razon_riesgo': estudiante.razon_riesgo,
            'asistencia': estudiante.asistencia_porcentaje,
            'calificaciones_recientes': [
                {
                    'asignatura': c.asignatura.nombre,
                    'calificacion': c.calificacion,
                    'estado': c.estado,
                    'periodo': c.periodo
                }
                for c in calificaciones
            ],
            'emociones_recientes': [
                {
                    'sentimiento': e.sentimiento,
                    'puntuacion': e.puntuacion,
                    'fecha': e.fecha_evaluacion.isoformat()
                }
                for e in emociones
            ]
        }
        
        return contexto
    
    def _crear_prompt_sistema(self, contexto):
        """Crear prompt del sistema para el tutor"""
        
        prompt = f"""Eres un Tutor de Inteligencia Artificial compasivo y experto en orientación educativa y bienestar estudiantil.

INFORMACIÓN DEL ESTUDIANTE:
- Nombre: {contexto['nombre']}
- Carrera: {contexto['carrera']}
- Semestre: {contexto['semestre']}
- Promedio Académico: {contexto['promedio']:.2f}
- Nivel de Riesgo: {contexto['nivel_riesgo']}
- Razón del Riesgo: {contexto['razon_riesgo'] or 'No especificada'}
- Asistencia: {contexto['asistencia']:.1f}%

CALIFICACIONES RECIENTES:"""
        
        for cal in contexto['calificaciones_recientes']:
            prompt += f"\n  - {cal['asignatura']}: {cal['calificacion']:.1f} ({cal['estado']})"
        
        prompt += "\n\nESTADO EMOCIONAL RECIENTE:"
        for emo in contexto['emociones_recientes']:
            prompt += f"\n  - {emo['sentimiento']} (intensidad: {emo['puntuacion']:.2f})"
        
        prompt += """

INSTRUCCIONES:
1. Proporciona respuestas empáticas y motivacionales
2. Ofrece recomendaciones académicas personalizadas basadas en el contexto
3. Si detectas señales de deserción, sugiere recursos de apoyo
4. Sé conciso pero completo (máximo 3-4 párrafos)
5. Mantén un tono profesional pero cálido
6. Si necesita ayuda profesional (psicológica, financiera), recomiéndalo
7. Proporciona recursos específicos cuando sea posible

Responde en el mismo idioma del estudiante y adapta tu lenguaje a su nivel académico.
"""
        
        return prompt
    
    def _analizar_sentimiento(self, texto):
        """
        Analizar el sentimiento del texto del estudiante
        
        Returns:
            tuple: (sentimiento: str, puntuacion: float 0-1)
        """
        
        # Palabras clave para detectar sentimientos
        sentimientos_palabras = {
            'alegría': ['feliz', 'contento', 'entusiasmado', 'emocionado', 'excelente', 'genial', 'fantástico'],
            'tristeza': ['triste', 'deprimido', 'desanimado', 'desgraciado', 'infeliz', 'angustia'],
            'frustración': ['frustrado', 'enojado', 'irritado', 'enfadado', 'molesto', 'furioso'],
            'ansiedad': ['ansioso', 'nervioso', 'preocupado', 'estresado', 'asustado', 'tenso'],
            'motivación': ['motivado', 'inspirado', 'decidido', 'comprometido', 'determinado'],
            'desesperanza': ['desesperado', 'sin esperanza', 'abandonado', 'perdido', 'derrotado'],
            'confusión': ['confundido', 'desoriented', 'perdido', 'sin claro', 'dudoso']
        }
        
        texto_lower = texto.lower()
        
        # Detectar sentimientos
        puntuaciones = {}
        for sentimiento, palabras in sentimientos_palabras.items():
            count = sum(1 for palabra in palabras if palabra in texto_lower)
            puntuaciones[sentimiento] = count
        
        # Obtener sentimiento dominante
        if not any(puntuaciones.values()):
            sentimiento_dominante = 'neutro'
            puntuacion = 0.5
        else:
            sentimiento_dominante = max(puntuaciones, key=puntuaciones.get)
            # Normalizar puntuación
            total_palabras = sum(puntuaciones.values())
            puntuacion = min(puntuaciones[sentimiento_dominante] / total_palabras, 1.0)
        
        return sentimiento_dominante, puntuacion
    
    def generar_recomendaciones(self, estudiante):
        """
        Generar recomendaciones automáticas para el estudiante
        
        Returns:
            list: Lista de recomendaciones
        """
        from modelos.base_datos import Recomendacion, Calificacion
        
        recomendaciones = []
        
        # 1. Recomendaciones académicas basadas en calificaciones
        calificaciones = Calificacion.query.filter_by(
            estudiante_id=estudiante.id
        ).all()
        
        materias_bajas = [c for c in calificaciones if c.calificacion < 3.0]
        
        if materias_bajas:
            recomendacion = Recomendacion(
                estudiante_id=estudiante.id,
                tipo='académica',
                contenido=f"Detectamos que tienes dificultades en {len(materias_bajas)} asignatura(s). Te recomendamos participar en tutorías o grupos de estudio.",
                prioridad='alta'
            )
            recomendaciones.append(recomendacion)
        
        # 2. Recomendaciones por asistencia
        if estudiante.asistencia_porcentaje < 80:
            recomendacion = Recomendacion(
                estudiante_id=estudiante.id,
                tipo='académica',
                contenido=f"Tu asistencia es del {estudiante.asistencia_porcentaje:.1f}%. Intenta aumentarla para mejorar tu desempeño.",
                prioridad='alta'
            )
            recomendaciones.append(recomendacion)
        
        # 3. Recomendaciones por nivel de riesgo
        if estudiante.nivel_riesgo == 'crítico':
            recomendacion = Recomendacion(
                estudiante_id=estudiante.id,
                tipo='emocional',
                contenido="Tu situación requiere atención inmediata. Te contactaremos para ofrecer apoyo especializado.",
                prioridad='crítica'
            )
            recomendaciones.append(recomendacion)
        
        # 4. Recomendaciones financieras
        if estudiante.razon_riesgo and 'económica' in estudiante.razon_riesgo.lower():
            recomendacion = Recomendacion(
                estudiante_id=estudiante.id,
                tipo='financiera',
                contenido="Existen programas de apoyo financiero disponibles. Contacta a la oficina de bienestar estudiantil.",
                prioridad='alta'
            )
            recomendaciones.append(recomendacion)
        
        # Guardar recomendaciones
        for rec in recomendaciones:
            db.session.add(rec)
        
        if recomendaciones:
            db.session.commit()
        
        return recomendaciones
    
    def evaluar_riesgo_desercion(self, estudiante):
        """
        Evaluar el riesgo de deserción del estudiante
        
        Returns:
            dict: {'nivel': str, 'razon': str, 'puntuacion': float}
        """
        from modelos.base_datos import Calificacion, Asistencia, EvaluacionEmocional
        
        puntuacion_riesgo = 0
        factores = []
        
        # Factor: Calificaciones
        calificaciones = Calificacion.query.filter_by(
            estudiante_id=estudiante.id
        ).all()
        
        if calificaciones:
            promedio = sum(c.calificacion for c in calificaciones) / len(calificaciones)
            if promedio < 2.0:
                puntuacion_riesgo += 40
                factores.append('académica')
            elif promedio < 2.5:
                puntuacion_riesgo += 20
        
        # Factor: Asistencia
        if estudiante.asistencia_porcentaje < 50:
            puntuacion_riesgo += 35
            factores.append('asistencia')
        elif estudiante.asistencia_porcentaje < 75:
            puntuacion_riesgo += 15
        
        # Factor: Emocional
        emociones_negativas = EvaluacionEmocional.query.filter_by(
            estudiante_id=estudiante.id
        ).filter(
            EvaluacionEmocional.sentimiento.in_(['tristeza', 'frustración', 'ansiedad', 'desesperanza'])
        ).all()
        
        if emociones_negativas:
            if len(emociones_negativas) > 5:
                puntuacion_riesgo += 25
                factores.append('emocional')
            else:
                puntuacion_riesgo += 10
        
        # Determinar nivel
        if puntuacion_riesgo >= 70:
            nivel = 'crítico'
        elif puntuacion_riesgo >= 50:
            nivel = 'alto'
        elif puntuacion_riesgo >= 25:
            nivel = 'medio'
        else:
            nivel = 'bajo'
        
        razon = ', '.join(factores) if factores else 'Sin factores detectados'
        
        return {
            'nivel': nivel,
            'razon': razon,
            'puntuacion': puntuacion_riesgo / 100
        }
