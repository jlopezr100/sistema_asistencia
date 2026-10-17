import math
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import date
from asistencia.models import Personal, Maquina, Asistencia, Incidencia, Corte

def mostrar_pantalla_marcado(request):
    context = {
        'titulo_seccion': 'Marcado Biométrico',
        'mantenimiento_activo': False,
    }
    return render(request, 'asistencia/marcar.html', context)

def calcular_distancia(lat1, lon1, lat2, lon2):
    rad = math.pi / 180
    dlat = (lat2 - lat1) * rad
    dlon = (lon2 - lon1) * rad
    a = math.sin(dlat/2)**2 + math.cos(lat1*rad) * math.cos(lat2*rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return 6371000 * c 

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

        hoy = date.today()
        ahora = timezone.now()

        # Corregido a doble guion bajo estándar de Django (__lte y __gte)
        corte_actual = Corte.objects.filter(f_inicio__lte=hoy, f_final__gte=hoy, procesado=False).first()
        if not corte_actual:
            return JsonResponse({'status': 'error', 'message': 'Falta configurar el Periodo de Corte activo para la fecha de hoy.'}, status=400)

        # PASO 1 EN CASCADA: BUSQUEDA POR HUELLA
        empleado = Personal.objects.filter(huella_indice=huella_recibida, condicion=True).first() or \
                   Personal.objects.filter(huella_pulgar=huella_recibida, condicion=True).first()

        if not empleado:
            return JsonResponse({'status': 'invalid', 'message': 'El usuario no existe o se encuentra inactivo en el sistema.'}, status=401)

        # PASO 2 EN CASCADA: VALIDACIÓN DE MAQUINA
        maquina_valida = Maquina.objects.filter(serie_dispositivo=serie_enviada, institucion=empleado.institucion).exists()
        if not maquina_valida:
            Incidencia.objects.create(
                personal=empleado, serie_dispositivo=serie_enviada, latitud=lat_capturada, longitud=lon_capturada,
                ubicacion_imagen=imagen_foto, motivo_incidencia='MAQUINA',
                detalles=f'El personal pertenece a la I.E. "{empleado.institucion.nombre}", pero intentó marcar desde un dispositivo no autorizado (Serie: {serie_enviada}).',
                corte=corte_actual # Corregido adentro del método create
            )
            return JsonResponse({'status': 'invalid', 'message': 'Dispositivo no autorizado para registrar asistencia en su institución.'}, status=401)

        # PASO 3 EN CASCADA: VALIDACIÓN DE GEOLOCALIZACIÓN
        distancia = calcular_distancia(
            float(empleado.institucion.latitud), float(empleado.institucion.longitud),
            lat_capturada, lon_capturada
        )
        
        if distancia > 50:
            Incidencia.objects.create(
                personal=empleado, serie_dispositivo=serie_enviada, latitud=lat_capturada, longitud=lon_capturada,
                ubicacion_imagen=imagen_foto, motivo_incidencia='GEOLOCALIZACION',
                detalles=f'El usuario intentó marcar fuera de rango. Distancia calculada: {round(distancia, 2)} metros.',
                corte=corte_actual
            )
            return JsonResponse({'status': 'invalid', 'message': 'Ubicación inválida: Se encuentra fuera del rango geográfico permitido para su institución.'}, status=401)

        # REGISTRO DE ASISTENCIA EXITOSA
        asistencia_diaria = Asistencia.objects.filter(personal=empleado, fecha=hoy).first()
        if not asistencia_diaria:
            asistencia_diaria = Asistencia.objects.create(personal=empleado, corte=corte_actual, fecha=hoy)

        if not asistencia_diaria.h_entrada:
            asistencia_diaria.h_entrada = ahora
            asistencia_diaria.save()
            return JsonResponse({'status': 'success', 'message': f'Entrada registrada correctamente para: {empleado.apellidos}, {empleado.nombres}'})
        elif not asistencia_diaria.h_salida:
            asistencia_diaria.h_salida = ahora
            asistencia_diaria.save()
            return JsonResponse({'status': 'success', 'message': f'Salida registrada correctamente para: {empleado.apellidos}, {empleado.nombres}'})
        else:
            return JsonResponse({'status': 'warning', 'message': 'El personal ya cuenta con sus registros de entrada y salida completos para el día de hoy.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error interno en el servidor: {str(e)}'}, status=500)
