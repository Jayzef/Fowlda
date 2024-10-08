from django import forms
from .models import *

class CadastroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields =  ['email', 'senha']
    
    def __init__(self, *args, **kwargs):
        super(CadastroForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'usuario'})
        self.fields['senha'].widget = forms.PasswordInput(attrs={'class': 'usuario'})

class ArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ['arquivo', 'chave']
    def __init__(self, *args, **kwargs):
        super(ArquivoForm, self).__init__(*args, **kwargs)
        self.fields['chave'].widget.attrs.update({'style': 'display:none'})
        self.fields['chave'].label = ''