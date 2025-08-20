from django import forms
from .models import Denuncia

class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ['motivo']
        widgets = {
            'motivo': forms.RadioSelect(),  # para usar botões
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove qualquer opção vazia do choices
        self.fields['motivo'].choices = [
            (val, label) for val, label in self.fields['motivo'].choices if val
        ]

