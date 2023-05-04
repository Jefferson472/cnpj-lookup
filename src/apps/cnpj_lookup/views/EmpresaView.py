from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy

from apps.cnpj_lookup.models import Empresa, Socio
from apps.cnpj_lookup.forms import EmpresaForm, EmpresaDetalhesForm, SocioForm, SocioFormSet


class EmpresaCreateView(CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'cnpj_lookup/empresa_create.html'

    def form_valid(self, form):
        empresa = form.save(commit=False)
        data = empresa.buscar_dados_cnpj()
        if data == 429:
            form.add_error(None, 'Essa API permite somente 3 consultas por minuto. Aguarde e tente novamente')
            return self.form_invalid(form)
        empresa.razao_social = data['nome']
        empresa.nome_fantasia = data['fantasia']
        empresa.telefone = data['telefone']
        empresa.email = data['email']
        empresa.endereco = data['logradouro']
        empresa.numero = data['numero']
        empresa.complemento = data['complemento']
        empresa.bairro = data['bairro']
        empresa.cidade = data['municipio']
        empresa.estado = data['uf']
        empresa.cep = data['cep'].replace(".", "").replace("-", "")
        empresa.cnae_principal = data['atividade_principal'][0]['code']
        empresa.save()

        socios = data.get('qsa', [])
        for socio in socios:
            Socio.objects.create(
                empresa=empresa,
                nome=socio['nome'],
                qualificacao=socio['qual'],
            )

        return redirect('cnpj-lookup:empresa-detail', pk=empresa.pk)


class EmpresaUpdateView(UpdateView):
    model = Empresa
    form_class = EmpresaDetalhesForm
    success_url = reverse_lazy('cnpj-lookup:empresa-list')
    template_name = 'cnpj_lookup/empresa_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context['object']
        if self.request.POST:
            context['socios'] = SocioFormSet(self.request.POST, instance=object)
        else:
            context['form'] = EmpresaDetalhesForm(instance=object)
            context['socios'] = SocioFormSet(instance=object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        socios = context['socios']
        with transaction.atomic():
            self.object = form.save()
            if socios.is_valid():
                socios.instance = self.object
                socios.save()
        return HttpResponseRedirect(self.get_success_url())


class EmpresaDeleteView(DeleteView):
    model = Empresa
    success_url = reverse_lazy('cnpj-lookup:empresa-list')
    template_name = 'cnpj_lookup/empresa_confirm_delete.html'


class EmpresaListView(ListView):
    model = Empresa
    template_name = 'cnpj_lookup/empresa_list.html'
