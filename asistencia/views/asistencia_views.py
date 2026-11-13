from decimal import Decimal
import math
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


# Vista que renderiza la pantalla del quiosco en la tablet
def mostrar_pantalla_marcado(request):
  # Nota: Si guardaste marcar.html directamente en templates/marcar.html, cambia a 'marcar.html'
  return render(request, 'asistencia/marcar.html')


def calcular_distancia(lat1, lon1, lat2, lon2):
  rad = math.pi / 180
  dlat = (lat2 - lat1) * rad
  dlon = (lon2 - lon1) * rad
  a = (
      math.sin(dlat / 2) ** 2
      + math.cos(lat1 * rad) * math.cos(lat2 * rad) * math.sin(dlon / 2) ** 2
  )
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  return 6371000 * c


@csrf_exempt
def registrar_marcado_tiempo_real(request):
  from asistencia.models import Asistencia, Incidencia, Maquina, Personal

  if request.method != 'POST':
    return JsonResponse(
        {'status': 'error', 'message': 'Método no permitido'}, status=405
    )

  try:
    huella_recibida = request.POST.get('huella', '').strip()
    serie_enviada = request.POST.get('serie_dispositivo', '').strip()

    lat_raw = float(request.POST.get('latitud', 0))
    lon_raw = float(request.POST.get('longitud', 0))
    lat_capturada = Decimal(f'{lat_raw:.8f}')
    lon_capturada = Decimal(f'{lon_raw:.8f}')

    imagen_foto = request.FILES.get('ubicacion_imagen', None)

    ahora_lima = timezone.localtime(timezone.now())
    hoy_lima = ahora_lima.date()

    # PASO 1: BÚSQUEDA POR HUELLA (ÍNDICE O PULGAR) EN PERSONAL ACTIVO
    empleado = (
        Personal.objects.filter(
            huella_indice=huella_recibida, condicion=True
        ).first()
        or Personal.objects.filter(
            huella_pulgar=huella_recibida, condicion=True
        ).first()
    )

    if not empleado:
      Incidencia.objects.create(
          personal=None,
          serie_dispositivo=serie_enviada or 'NO_IDENTIFICADO',
          latitud=lat_capturada,
          longitud=lon_capturada,
          ubicacion_imagen=imagen_foto,
          motivo_incidencia='HUELLA',
          detalles=(
              'Huella no coincide con ningún personal activo. Código recibido:'
              f' {huella_recibida}'
          ),
      )
      return JsonResponse(
          {
              'status': 'invalid',
              'message': 'Huella no reconocida o personal inactivo.',
          },
          status=401,
      )

    # Captura de IDs requeridos
    id_personal = empleado.id
    institucion_empleado = empleado.institucion
    id_colegio = institucion_empleado.id

    # PASO 2: COMPARACIÓN Y FILTRADO POR MÁQUINA AUTORIZADA EN ESA I.E.
    maquina_valida = Maquina.objects.filter(
        serie_dispositivo=serie_enviada, institucion_id=id_colegio
    ).exists()

    if not maquina_valida:
      Incidencia.objects.create(
          personal=empleado,
          serie_dispositivo=serie_enviada or 'NO_IDENTIFICADO',
          latitud=lat_capturada,
          longitud=lon_capturada,
          ubicacion_imagen=imagen_foto,
          motivo_incidencia='MAQUINA',
          detalles=(
              f'Dispositivo no autorizado. El personal (ID: {id_personal})'
              f' pertenece a "{institucion_empleado.nombre}" (ID:'
              f' {id_colegio}). Serie usada: {serie_enviada}.'
          ),
      )
      return JsonResponse(
          {
              'status': 'invalid',
              'message': (
                  'Dispositivo no autorizado para registrar asistencia en su'
                  ' institución.'
              ),
          },
          status=401,
      )

    # PASO 3: COMPARACIÓN Y FILTRADO POR RANGO GEOGRÁFICO GPS (MAX 50 METROS)
    lat_ie = float(institucion_empleado.latitud or 0)
    lon_ie = float(institucion_empleado.longitud or 0)

    if lat_ie == 0 or lon_ie == 0:
      return JsonResponse(
          {
              'status': 'error',
              'message': (
                  'La institución educativa no tiene coordenadas GPS'
                  ' configuradas en el sistema.'
              ),
          },
          status=400,
      )

    if lat_raw == 0 or lon_raw == 0:
      return JsonResponse(
          {
              'status': 'invalid',
              'message': (
                  'No se pudo capturar la ubicación GPS de la tablet. Active el'
                  ' GPS e intente nuevamente.'
              ),
          },
          status=401,
      )

    distancia = calcular_distancia(lat_ie, lon_ie, lat_raw, lon_raw)

    if distancia > 50:
      Incidencia.objects.create(
          personal=empleado,
          serie_dispositivo=serie_enviada,
          latitud=lat_capturada,
          longitud=lon_capturada,
          ubicacion_imagen=imagen_foto,
          motivo_incidencia='GEOLOCALIZACION',
          detalles=(
              'Usuario fuera de rango permitido en I.E.'
              f' "{institucion_empleado.nombre}". Distancia:'
              f' {round(distancia, 2)} metros.'
          ),
      )
      return JsonResponse(
          {
              'status': 'invalid',
              'message': (
                  'Se encuentra fuera del rango geográfico permitido para su'
                  f' institución ({round(distancia, 1)}m).'
              ),
          },
          status=401,
      )

    # PASO 4: REGISTRO EN LA TABLA ASISTENCIA (ENTRADA O SALIDA)
    asistencia_diaria = Asistencia.objects.filter(
        personal_id=id_personal, fecha=hoy_lima
    ).first()

    if not asistencia_diaria:
      asistencia_diaria = Asistencia.objects.create(
          personal_id=id_personal, fecha=hoy_lima, justificado=False
      )

    if not asistencia_diaria.h_entrada:
      asistencia_diaria.h_entrada = ahora_lima
      asistencia_diaria.save()
      return JsonResponse({
          'status': 'success',
          'message': (
              f'Entrada registrada con éxito para: {empleado.apellidos},'
              f' {empleado.nombres}'
          ),
      })

    elif not asistencia_diaria.h_salida:
      asistencia_diaria.h_salida = ahora_lima
      asistencia_diaria.save()
      return JsonResponse({
          'status': 'success',
          'message': (
              f'Salida registrada con éxito para: {empleado.apellidos},'
              f' {empleado.nombres}'
          ),
      })

    else:
      return JsonResponse({
          'status': 'warning',
          'message': (
              'El personal ya cuenta con sus registros completos (Entrada y'
              ' Salida) para el día de hoy.'
          ),
      })

  except Exception as e:
    return JsonResponse(
        {'status': 'error', 'message': f'Error interno en procesamiento: {str(e)}'},
        status=500,
    )
