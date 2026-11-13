import math
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from asistencia.models import Personal, Maquina, Asistencia, Incidencia

def calcular_distancia(lat1, lon1, lat2, lon2):
    rad = math.pi / 180
    dlat = (lat2 - lat1) * rad
    dlon = (lon2 - lon1) * rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1 * rad) * math.cos(lat2 * rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371000 * c  # Retorna la distancia en metros

@csrf_exempt
def registrar_marcado_tiempo_real(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

    try:
        huella_recibida = request.POST.get('huella')
        serie_enviada = request.POST.get('serie_dispositivo')
        lat_capturada = float(request.POST.get('latitud', 0))
        lon_capturada = float(request.POST.get('longitud', 0))
        imagen_foto = request.FILES.get('ubicacion_imagen')

        # Sincronización exacta con el huso horario local de Lima (UTC-5)
        ahora_lima = timezone.localtime(timezone.now())
        hoy_lima = ahora_lima.date()

        # PASO 1: BÚSQUEDA POR HUELLA Y CAPTURA DE IDENTIDADES
        empleado = Personal.objects.filter(huella_indice=huella_recibida, condicion=True).first() or \
                   Personal.objects.filter(huella_pulgar=huella_recibida, condicion=True).first()

        if not empleado:
            return JsonResponse({'status': 'invalid', 'message': 'Huella no reconocida o personal inactivo.'}, status=401)

        id_personal = empleado.id
        institucion_empleado = empleado.institucion

        # PASO 2: FILTRADO POR MÁQUINA AUTORIZADA
        maquina_valida = Maquina.objects.filter(serie_dispositivo=serie_enviada, institucion=institucion_empleado).exists()
        if not maquina_valida:
            Incidencia.objects.create(
                personal=empleado,
                serie_dispositivo=serie_enviada,
                latitud=lat_capturada,
                longitud=lon_capturada,
                ubicacion_imagen=imagen_foto,
                motivo_incidencia='MAQUINA',
                detalles=f'Dispositivo no autorizado. Pertenece a la I.E. "{institucion_empleado.nombre}" (Serie: {serie_enviada}).'
            )
            return JsonResponse({'status': 'invalid', 'message': 'Dispositivo no autorizado para registrar asistencia en su institución.'}, status=401)

        # PASO 3: FILTRADO POR RANGO GEOGRÁFICO GPS (MAX 50M)
        distancia = calcular_distancia(
            float(institucion_empleado.latitud), float(institucion_empleado.longitud),
            lat_capturada, lon_capturada
        )

        if distancia > 50:
            Incidencia.objects.create(
                personal=empleado,
                serie_dispositivo=serie_enviada,
                latitud=lat_capturada,
                longitud=lon_capturada,
                ubicacion_imagen=imagen_foto,
                motivo_incidencia='GEOLOCALIZACION',
                detalles=f'Usuario fuera de rango permitido. Distancia calculada: {round(distancia, 2)} metros.'
            )
            return JsonResponse({'status': 'invalid', 'message': f'Fuera del rango geográfico permitido ({round(distancia, 2)}m).'}, status=401)

        # PASO 4: REGISTRO O ACTUALIZACIÓN DE ASISTENCIA DIARIA
        asistencia_diaria, created = Asistencia.objects.get_or_create(
            personal_id=id_personal,
            fecha=hoy_lima,
            defaults={'justificado': False}
        )

        if not asistencia_diaria.h_entrada:
            asistencia_diaria.h_entrada = ahora_lima.time()
            asistencia_diaria.save()
            return JsonResponse({'status': 'success', 'message': f'Entrada registrada con éxito para: {empleado.apellidos}, {empleado.nombres}'})
        elif not asistencia_diaria.h_salida:
            asistencia_diaria.h_salida = ahora_lima.time()
            asistencia_diaria.save()
            return JsonResponse({'status': 'success', 'message': f'Salida registrada con éxito para: {empleado.apellidos}, {empleado.nombres}'})
        else:
            return JsonResponse({'status': 'warning', 'message': 'El personal ya cuenta con sus registros completos (Entrada y Salida) para el día de hoy.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error interno en procesamiento: {str(e)}'}, status=500)
    