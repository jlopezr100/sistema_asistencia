from decimal import Decimal, InvalidOperation
import math
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


def mostrar_pantalla_marcado(request):
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


def limpiar_coordenada(valor_str):
  try:
    val = float(valor_str)
    return Decimal(f'{val:.8f}'), val
  except (ValueError, TypeError, InvalidOperation):
    return Decimal('0.00000000'), 0.0


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

    lat_decimal, lat_float = limpiar_coordenada(request.POST.get('latitud', 0))
    lon_decimal, lon_float = limpiar_coordenada(request.POST.get('longitud', 0))
    imagen_foto = request.FILES.get('ubicacion_imagen', None)

    ahora_lima = timezone.localtime(timezone.now())
    hoy_lima = ahora_lima.date()
    hora_texto = ahora_lima.strftime('%H:%M:%S')

    # 1. VALIDAR HUELLA (ÍNDICE O PULGAR)
    empleado = None
    if huella_recibida:
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
          serie_dispositivo=serie_enviada or 'SIN_SERIE',
          latitud=lat_decimal,
          longitud=lon_decimal,
          ubicacion_imagen=imagen_foto,
          motivo_incidencia='HUELLA',
          detalles=(
              'Huella no reconocida o personal inactivo. Código capturado:'
              f' "{huella_recibida}"'
          ),
      )
      return JsonResponse(
          {
              'status': 'invalid',
              'message': (
                  'Huella no reconocida o personal inactivo. Incidencia'
                  ' registrada.'
              ),
          },
          status=401,
      )

    # 2. VALIDAR MÁQUINA AUTORIZADA PARA LA INSTITUCIÓN DEL DOCENTE
    institucion_empleado = empleado.institucion
    maquina_valida = Maquina.objects.filter(
        serie_dispositivo=serie_enviada, institucion=institucion_empleado
    ).exists()

    if not maquina_valida:
      Incidencia.objects.create(
          personal=empleado,
          serie_dispositivo=serie_enviada or 'SIN_SERIE',
          latitud=lat_decimal,
          longitud=lon_decimal,
          ubicacion_imagen=imagen_foto,
          motivo_incidencia='MAQUINA',
          detalles=(
              f'Dispositivo "{serie_enviada}" no autorizado para la I.E.'
              f' "{institucion_empleado.nombre}" (ID:'
              f' {institucion_empleado.id}).'
          ),
      )
      return JsonResponse(
          {
              'status': 'invalid',
              'message': (
                  'Dispositivo no autorizado para su institución. Incidencia'
                  ' registrada.'
              ),
          },
          status=401,
      )

    # 3. VALIDAR UBICACIÓN GPS DE LA INSTITUCIÓN (MÁXIMO 50 METROS)
    lat_ie = float(institucion_empleado.latitud or 0)
    lon_ie = float(institucion_empleado.longitud or 0)

    if lat_float == 0 or lon_float == 0:
      Incidencia.objects.create(
          personal=empleado,
          serie_dispositivo=serie_enviada,
          latitud=lat_decimal,
          longitud=lon_decimal,
          ubicacion_imagen=imagen_foto,
          motivo_incidencia='GEOLOCALIZACION',
          detalles=(
              'La tablet envió coordenadas en cero (0, 0). Señal GPS no'
              ' detectada.'
          ),
      )
      return JsonResponse(
          {
              'status': 'invalid',
              'message': (
                  'Sin señal GPS válida en la tablet. Incidencia registrada.'
              ),
          },
          status=401,
      )

    distancia = calcular_distancia(lat_ie, lon_ie, lat_float, lon_float)

    if distancia > 50:
      Incidencia.objects.create(
          personal=empleado,
          serie_dispositivo=serie_enviada,
          latitud=lat_decimal,
          longitud=lon_decimal,
          ubicacion_imagen=imagen_foto,
          motivo_incidencia='GEOLOCALIZACION',
          detalles=(
              'Fuera de rango permitido para I.E.'
              f' "{institucion_empleado.nombre}". Distancia:'
              f' {round(distancia, 2)} metros.'
          ),
      )
      return JsonResponse(
          {
              'status': 'invalid',
              'message': (
                  f'Fuera de rango geográfico ({round(distancia, 1)}m).'
                  ' Incidencia registrada.'
              ),
          },
          status=401,
      )

    # 4. REGISTRAR ENTRADA O SALIDA EN ASISTENCIA
    asistencia_diaria, _ = Asistencia.objects.get_or_create(
        personal=empleado, fecha=hoy_lima, defaults={'justificado': False}
    )

    if not asistencia_diaria.h_entrada:
      asistencia_diaria.h_entrada = ahora_lima
      asistencia_diaria.save()
      return JsonResponse({
          'status': 'success',
          'message': (
              f'ENTRADA registrada ({hora_texto}) para: {empleado.apellidos},'
              f' {empleado.nombres}'
          ),
      })

    elif not asistencia_diaria.h_salida:
      asistencia_diaria.h_salida = ahora_lima
      asistencia_diaria.save()
      return JsonResponse({
          'status': 'success',
          'message': (
              f'SALIDA registrada ({hora_texto}) para: {empleado.apellidos},'
              f' {empleado.nombres}'
          ),
      })

    else:
      return JsonResponse({
          'status': 'warning',
          'message': (
              f'{empleado.apellidos}, {empleado.nombres} ya cuenta con Entrada'
              ' y Salida registradas hoy.'
          ),
      })

  except Exception as e:
    return JsonResponse(
        {'status': 'error', 'message': f'Error interno en servidor: {str(e)}'},
        status=500,
    )
