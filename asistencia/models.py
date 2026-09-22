from django.db import models

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
    