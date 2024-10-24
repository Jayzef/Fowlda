from django import forms
from .models import *

class CadastroForm(forms.ModelForm):
    perfil = forms.BooleanField(initial=False, required=False, widget=forms.HiddenInput())  # Campo oculto

    class Meta:
        model = Usuario
        fields = ['email', 'senha', 'perfil']

    def __init__(self, *args, **kwargs):
        super(CadastroForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'usuario'})
        self.fields['senha'].widget = forms.PasswordInput(attrs={'class': 'usuario'})

    def clean_perfil(self):
        return False

class SenhaForm(forms.Form):
    email = forms.CharField(
        label='E-mail',
        max_length=200
    )
    senha = forms.CharField(
        label='Senha',
        max_length=200,
        widget=forms.PasswordInput()
    )

class ArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ['arquivo', 'chave']
    def __init__(self, *args, **kwargs):
        super(ArquivoForm, self).__init__(*args, **kwargs)
        self.fields['chave'].widget.attrs.update({'style': 'display:none'})
        self.fields['chave'].label = ''