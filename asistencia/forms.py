from django import forms
from .models import Ugel
from .models import Cargo
from .models import Nivel
from .models import Turno
from .models import Distrito
from .models import Falta, Tardanza

class UgelForm(forms.ModelForm):
    class Meta:
        model = Ugel
        fields = [
            'nombre', 'ruc', 'direccion', 'correo', 'telefono',
            'eslogan', 'quienes_somos', 'mision', 'vision',
            'logo', 'banner', 'descripcion'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '11'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'eslogan': forms.TextInput(attrs={'class': 'form-control'}),
            'quienes_somos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'mision': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vision': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'banner': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['nombre', 'descripcion', 'estado']
        labels = {
            'nombre': 'Nombre del Cargo',
            'descripcion': 'Descripción',
            'estado': 'Estado Activo',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input-search',
                'placeholder': 'Ingrese el nombre del cargo...',
                'style': 'width: 100%; padding: 8px; border: 1px solid #b8c7d6; border-radius: 4px;'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-input-search',
                'placeholder': 'Descripción opcional del cargo...',
                'rows': 3,
                'style': 'width: 100%; padding: 8px; border: 1px solid #b8c7d6; border-radius: 4px;'
            }),
            'estado': forms.CheckboxInput(attrs={
                'style': 'cursor: pointer; transform: scale(1.2);'
            }),
        }
        
class NivelForm(forms.ModelForm):
    class Meta:
        model = Nivel
        fields = ['nombre', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej. Inicial, Primaria, Secundaria...',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Ingrese una descripción opcional...',
                'rows': 3
            }),
            'estado': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            })
        }

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['nombre', 'hora_entrada', 'hora_salida', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej. Mañana, Tarde, Noche...',
                'required': True
            }),
            'hora_entrada': forms.TimeInput(attrs={
                'class': 'form-input',
                'type': 'time',
                'required': False
            }),
            'hora_salida': forms.TimeInput(attrs={
                'class': 'form-input',
                'type': 'time',
                'required': False
            }),
            'estado': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            })
        }

class DistritoForm(forms.ModelForm):
    class Meta:
        model = Distrito
        fields = ['nombre', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej. Yungay, Mancos, Shupluy...',
                'required': True
            }),
            'estado': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            })
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre_limpio = nombre.strip()
            # Verifica duplicados excluyendo el registro actual si se está editando
            queryset = Distrito.objects.filter(nombre__iexact=nombre_limpio)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise forms.ValidationError("Ya existe un distrito registrado con este nombre.")
            return nombre_limpio
        return nombre

class FaltaForm(forms.ModelForm):
    class Meta:
        model = Falta
        fields = ['tipo_falta', 'descripcion', 'justificable', 'estado']
        widgets = {
            'tipo_falta': forms.TextInput(attrs={
                'class': 'form-control-custom', 
                'placeholder': 'Ej. Inasistencia Injustificada'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control-custom', 
                'rows': 3, 
                'placeholder': 'Descripción o detalles opcionales...'
            }),
            'justificable': forms.CheckboxInput(attrs={'class': 'form-check-input-custom'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input-custom'}),
        }

    def clean_tipo_falta(self):
        tipo_falta = self.cleaned_data.get('tipo_falta', '').strip()
        qs = Falta.objects.filter(tipo_falta__iexact=tipo_falta)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un tipo de falta registrado con este nombre.")
        return tipo_falta


class TardanzaForm(forms.ModelForm):
    class Meta:
        model = Tardanza
        fields = ['tipo_tardanza', 'descripcion', 'justificable', 'estado']
        widgets = {
            'tipo_tardanza': forms.TextInput(attrs={
                'class': 'form-control-custom', 
                'placeholder': 'Ej. Papeleta de Salida'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control-custom', 
                'rows': 3, 
                'placeholder': 'Descripción o detalles opcionales...'
            }),
            'justificable': forms.CheckboxInput(attrs={'class': 'form-check-input-custom'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input-custom'}),
        }

    def clean_tipo_tardanza(self):
        tipo_tardanza = self.cleaned_data.get('tipo_tardanza', '').strip()
        qs = Tardanza.objects.filter(tipo_tardanza__iexact=tipo_tardanza)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un tipo de tardanza registrado con este nombre.")
        return tipo_tardanza
    