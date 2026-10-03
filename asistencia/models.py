from django.db import models
#from .models import Institucion # Asegúrate de que la clase Institucion esté importada


class Ugel(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre de la Institución/UGEL")
    ruc = models.CharField(max_length=11, unique=True, verbose_name="RUC")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    correo = models.EmailField(max_length=100, verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    eslogan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Eslogan")
    quienes_somos = models.TextField(blank=True, null=True, verbose_name="Quiénes Somos")
    mision = models.TextField(blank=True, null=True, verbose_name="Misión")
    vision = models.TextField(blank=True, null=True, verbose_name="Visión")
    logo = models.ImageField(upload_to='media/ugel/', blank=True, null=True, verbose_name="Logo Institucional")
    banner = models.ImageField(upload_to='media/ugel/', blank=True, null=True, verbose_name="Banner Institucional")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción Adicional")

    class Meta:
        db_table = 'ugel'
        verbose_name = 'UGEL'
        verbose_name_plural = 'Datos de UGEL'

    def __str__(self):
        return self.nombre

# ==========================================
# TABLAS AUXILIARES / CATÁLOGOS
# ==========================================

class Turno(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre del Turno")  # Ej: Mañana, Tarde, Noche, Completo
    hora_entrada = models.TimeField(verbose_name="Hora de Entrada", null=True, blank=True)
    hora_salida = models.TimeField(verbose_name="Hora de Salida", null=True, blank=True)
    estado = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        db_table = 'turno'
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Nivel(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nivel Educativo")  # Ej: Inicial, Primaria, Secundaria, Superior
    descripcion = models.CharField(max_length=150, blank=True, null=True, verbose_name="Descripción")
    estado = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        db_table = 'nivel'
        verbose_name = 'Nivel Educativo'
        verbose_name_plural = 'Niveles Educativos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Distrito(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Distrito")
    estado = models.BooleanField(default=True, verbose_name="Estado")

    class Meta:
        db_table = 'distrito'  # O el nombre exacto de la tabla en tu BD
        verbose_name = 'Distrito'
        verbose_name_plural = 'Distritos'

    def __str__(self):
        return self.nombre


class Cargo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Cargo")  # Ej: Director, Docente, Administrativo, Auxiliar
    descripcion = models.CharField(max_length=150, blank=True, null=True, verbose_name="Descripción")
    estado = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        db_table = 'cargo'
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Falta(models.Model):
    tipo_falta = models.CharField(max_length=100, unique=True, verbose_name="Tipo de Falta")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    justificable = models.BooleanField(default=False, verbose_name="¿Es Justificable?")
    estado = models.BooleanField(default=True, verbose_name="Estado")

    class Meta:
        db_table = 'falta'
        verbose_name = 'Falta'
        verbose_name_plural = 'Faltas'

    def __str__(self):
        return self.tipo_falta


class Tardanza(models.Model):
    tipo_tardanza = models.CharField(max_length=100, unique=True, verbose_name="Tipo de Tardanza")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    justificable = models.BooleanField(default=False, verbose_name="¿Es Justificable?")
    estado = models.BooleanField(default=True, verbose_name="Estado")

    class Meta:
        db_table = 'tardanza'
        verbose_name = 'Tardanza'
        verbose_name_plural = 'Tardanzas'

    def __str__(self):
        return self.tipo_tardanza


class Institucion(models.Model):
    codigo_modular = models.CharField(max_length=12, unique=True, verbose_name="Código Modular")
    nombre = models.CharField(max_length=150, verbose_name="Nombre de la Institución")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    tolerancia = models.IntegerField(default=15, help_text="Tolerancia en minutos", verbose_name="Tolerancia (Min)")
    
    # Claves Foráneas para Combos
    turno = models.ForeignKey('Turno', on_delete=models.PROTECT, related_name='instituciones', verbose_name="Turno")
    distrito = models.ForeignKey('Distrito', on_delete=models.PROTECT, related_name='instituciones', verbose_name="Distrito")
    
    # Coordenadas numéricas exactas
    latitud = models.DecimalField(max_digits=10, decimal_places=8, verbose_name="Latitud")
    longitud = models.DecimalField(max_digits=11, decimal_places=8, verbose_name="Longitud")
    
    estado = models.BooleanField(default=True, verbose_name="Estado")

    class Meta:
        db_table = 'instituciones'
        verbose_name = 'Institución'
        verbose_name_plural = 'Instituciones'
        ordering = ['-id']

    def __str__(self):
        return f"{self.codigo_modular} - {self.nombre}"

# asistencia/models.py
class Personal(models.Model):
    DIAS_DESCANSO = [
        ('LUNES', 'Lunes'),
        ('MARTES', 'Martes'),
        ('MIERCOLES', 'Miércoles'),
        ('JUEVES', 'Jueves'),
        ('VIERNES', 'Viernes'),
    ]

    cod_modular = models.CharField(max_length=12, unique=True, verbose_name="Código Modular")
    dni = models.CharField(max_length=8, unique=True, verbose_name="DNI")
    apellidos = models.CharField(max_length=50, verbose_name="Apellidos")
    nombres = models.CharField(max_length=50, verbose_name="Nombres")
    
    # Huellas como CharField para permitir unique=True en MySQL
    huella_indice = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name="Huella Índice")
    huella_pulgar = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name="Huella Pulgar")
    
    # Horarios
    h_entrada = models.TimeField(verbose_name="Hora de Entrada")
    h_salida = models.TimeField(verbose_name="Hora de Salida")
    
    condicion = models.BooleanField(default=True, verbose_name="Estado/Condición")
    dia_descanso = models.CharField(
        max_length=15, 
        choices=DIAS_DESCANSO, 
        null=True, 
        blank=True, 
        verbose_name="Día de Descanso"
    )
    
    # Relaciones
    cargo = models.ForeignKey('Cargo', on_delete=models.PROTECT, verbose_name="Cargo")
    institucion = models.ForeignKey('Institucion', on_delete=models.PROTECT, verbose_name="Institución")
    distrito = models.ForeignKey('Distrito', on_delete=models.PROTECT, verbose_name="Distrito")
    nivel = models.ForeignKey('Nivel', on_delete=models.PROTECT, verbose_name="Nivel Educativo")
    turno = models.ForeignKey('Turno', on_delete=models.PROTECT, verbose_name="Turno")

    class Meta:
        verbose_name = "Personal"
        verbose_name_plural = "Personal"
        ordering = ['-id']

    def __str__(self):
        return f"{self.apellidos}, {self.nombres} ({self.dni})"


class Maquina(models.Model):
    serie_dispositivo = models.CharField(max_length=100, unique=True, verbose_name="Serie del Dispositivo")
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, related_name="maquinas", verbose_name="Institución Educativa")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Máquina"
        verbose_name_plural = "Máquinas"
        ordering = ['-id']

    def __str__(self):
        return f"{self.serie_dispositivo} - {self.institucion.nombre}"