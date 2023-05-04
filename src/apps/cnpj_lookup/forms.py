from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

from .models import Empresa, Socio


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['cnpj']


class EmpresaDetalhesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('nome_fantasia', css_class='form-group col-md-6 mb-0'),
                Column('razao_social', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('cnpj', css_class='form-group col-md-6 mb-0'),
                Column('inscricao_estadual', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('telefone', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('cnae_principal', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('endereco', css_class='form-group mb-0'),
            ),
            Row(
                Column('bairro', css_class='form-group mb-0'),
                Column('cidade', css_class='form-group mb-0'),
                Column('estado', css_class='form-group mb-0'),
                Column('cep', css_class='form-group mb-0'),
            ),
        )

    class Meta:
        model = Empresa
        fields = ['razao_social', 'nome_fantasia', 'endereco', 'bairro',
                  'cidade', 'estado', 'cep', 'telefone', 'email',
                  'cnae_principal', 'inscricao_estadual', 'cnpj']


class SocioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='form-group mb-0'),
                Column('qualificacao', css_class='form-group mb-0'),
            )
        )

    class Meta:
        model = Socio
        fields = ['nome', 'qualificacao']


SocioFormSet = forms.inlineformset_factory(
    Empresa,
    Socio,
    form=SocioForm,
    extra=0
)
