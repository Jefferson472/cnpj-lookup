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
        fields = ['nome']


SocioFormSet = forms.inlineformset_factory(Empresa, Socio, form=SocioForm, extra=2)


class EmpresaSocioForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['razao_social', 'cnpj']
        widgets = {
            'razao_social': forms.TextInput(attrs={'readonly': True}),
            'cnpj': forms.TextInput(attrs={'readonly': True}),
        }

    socios = forms.ModelMultipleChoiceField(
        queryset=Socio.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['socios'].queryset = self.instance.socios.all()

    def save(self, commit=True):
        empresa = super().save(commit=commit)
        if commit:
            self.save_m2m()
        return empresa
