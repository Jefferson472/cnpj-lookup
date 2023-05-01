from django import forms
from .models import Empresa, Socio


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['cnpj']


class EmpresaDetalhesForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['razao_social', 'nome_fantasia', 'endereco', 'bairro',
                  'cidade', 'estado', 'cep', 'telefone', 'email',
                  'cnae_principal', 'inscricao_estadual']


class SocioForm(forms.ModelForm):
    class Meta:
        model = Socio
        fields = ['nome', 'qualificacao']


SocioFormSet = forms.inlineformset_factory(
    Empresa,
    Socio,
    form=SocioForm,
    extra=0
)
