import math
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import date
from asistencia.models import Personal, Maquina, Asistencia, Incidencia, Corte

# ---------------------------------------------------------------------------
# VISTA 1: Renderizado de la Pantalla de Marcado
# ---------------------------------------------------------------------------
def mostrar_pantalla_marcado(request):
    """
    Renderiza la interfaz web alineada con el estándar corporativo.
    """
    context = {
        'titulo_seccion': 'Marcado Biométrico',
        'mantenimiento_activo': False,  # <-- OBLIGATORIO: False para NO deshabilitar el menú
    }
    return render(request, 'asistencia/marcar.html', context)

# ---------------------------------------------------------------------------
# VISTA 2: Procesamiento del Marcado en Tiempo Real (API Fetch)
# ---------------------------------------------------------------------------
def calcular_distancia(lat1, lon1, lat2, lon2):
    """Fórmula de Haversine para calcular distancia en metros entre dos puntos GPS"""
    rad = math.pi / 180
    dlat = (lat2 - lat1) * rad
    dlon = (lon2 - lon1) * rad
    a = math.sin(dlat/2)**2 + math.cos(lat1*rad) * math.cos(lat2*rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return 6371000 * c 

@csrf_exempt
def registrar_marcado_tiempo_real(request):
    """
    Recibe la huella, serie, geolocalización y foto en binario por POST.
    Realiza las validaciones de negocio e ingresa Asistencia o Incidencia.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

    try:
        huella_recibida = request.POST.get('huella')
        serie_enviada = request.POST.get('serie_dispositivo')
        lat_capturada = float(request.POST.get('latitud', 0))
        lon_capturada = float(request.POST.get('longitud', 0))
        imagen_foto = request.FILES.get('ubicacion_imagen')

        hoy = date.today()
        ahora = timezone.now()

        # Validar periodo de corte activo
        corte_actual = Corte.objects.filter(f_inicio__lte=hoy, f_final__gte=hoy, procesado=False).first()
        if not corte_actual:
            return JsonResponse({
                'status': 'error', 
                'message': 'Error de configuración: No se encuentra un periodo de corte activo para la fecha actual.'
            }, status=400)

        # VALIDACIÓN 1: Búsqueda de Personal por Huella Digital
        empleado = Personal.objects.filter(huella_indice=huella_recibida, condicion=True).first() or \
                   Personal.objects.filter(huella_pulgar=huella_recibida, condicion=True).first()

        if not empleado:
            Incidencia.objects.create(
                serie_dispositivo=serie_enviada, latitud=lat_capturada, longitud=lon_capturada,
                ubicacion_imagen=imagen_foto, motivo_incidencia='HUELLA',
                detalles='Código de huella digital no coincide con ningún personal activo.', corte=corte_actual
            )
            return JsonResponse({'status': 'invalid', 'message': 'Acceso denegado: Huella digital no reconocida.'}, status=401)

        # VALIDACIÓN 2: Verificación de la Máquina Autorizada para la Institución
        maquina_valida = Maquina.objects.filter(serie_dispositivo=serie_enviada, institucion=empleado.institucion).exists()
        if not maquina_valida:
            Incidencia.objects.create(
                personal=empleado, serie_dispositivo=serie_enviada, latitud=lat_capturada, longitud=lon_capturada,
                ubicacion_imagen=imagen_foto, motivo_incidencia='MAQUINA',
                detalles=f'Dispositivo serie {serie_enviada} no está asignado a la institución {empleado.institucion.nombre}.',
                corte=corte_actual
            )
            return JsonResponse({'status': 'invalid', 'message': 'Dispositivo no autorizado para esta institución.'}, status=401)

        # VALIDACIÓN 3: Geolocalización (Tolerancia de 50 metros)
        distancia = calcular_distancia(
            float(empleado.institucion.latitud), float(empleado.institucion.longitud),
            lat_capturada, lon_capturada
        )
        
        if distancia > 50:
            Incidencia.objects.create(
                personal=empleado, serie_dispositivo=serie_enviada, latitud=lat_capturada, longitud=lon_capturada,
                ubicacion_imagen=imagen_foto, motivo_incidencia='GEOLOCALIZACION',
                detalles=f'El usuario intentó marcar a una distancia de {round(distancia, 2)} metros de su institución.',
                corte=corte_actual
            )
            return JsonResponse({'status': 'invalid', 'message': 'Ubicación inválida: Se encuentra fuera del rango permitido.'}, status=401)

        # -------------------------------------------------------------------
        # REGISTRO DE ASISTENCIA (ÉXITO)
        # -------------------------------------------------------------------
        asistencia_diaria = Asistencia.objects.filter(personal=empleado, fecha=hoy).first()

        # Si el comando de las 00:00 no corrió o falló, se autogenera el registro base en caliente
        if not asistencia_diaria:
            asistencia_diaria = Asistencia.objects.create(personal=empleado, corte=corte_actual, fecha=hoy)

        if not asistencia_diaria.h_entrada:
            asistencia_diaria.h_entrada = ahora
            asistencia_diaria.save()
            return JsonResponse({'status': 'success', 'message': f'Entrada registrada con éxito para: {empleado.apellidos}, {empleado.nombres}'})
        
        elif not asistencia_diaria.h_salida:
            asistencia_diaria.h_salida = ahora
            asistencia_diaria.save()
            return JsonResponse({'status': 'success', 'message': f'Salida registrada con éxito para: {empleado.apellidos}, {empleado.nombres}'})
        
        else:
            return JsonResponse({'status': 'warning', 'message': 'El usuario ya cuenta con sus registros de entrada y salida completos para hoy.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error interno en el servidor: {str(e)}'}, status=500)
