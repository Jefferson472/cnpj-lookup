from gettext import translation
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy

from apps.cnpj_lookup.models import Empresa, Socio
from apps.cnpj_lookup.forms import EmpresaForm, EmpresaDetalhesForm, SocioForm, EmpresaSocioForm


class EmpresaCreateView(CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'cnpj_lookup/empresa_create.html'

    def form_valid(self, form):
        empresa = form.save(commit=False)
        data = empresa.buscar_dados_cnpj()
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


class EmpresaDetailView(DetailView):
    model = Empresa
    template_name = 'cnpj_lookup/empresa_detalhes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['socio_form'] = SocioForm()
        context['empresa_socio_form'] = EmpresaSocioForm(instance=self.object)
        return context


class EmpresaUpdateView(UpdateView):
    model = Empresa
    form_class = EmpresaDetalhesForm
    success_url = reverse_lazy('cnpj-lookup:empresa-list')
    template_name = 'cnpj_lookup/empresa_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context['object']
        SocioFormSet = formset_factory(SocioForm, extra=2)
        if self.request.POST:
            context['socios'] = SocioFormSet(self.request.POST)
        else:
            context['form'] = EmpresaDetalhesForm(instance=object)
            context['socios'] = SocioFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        socios = context['socios']
        with translation.atomic():
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


class SocioCreateView(CreateView):
    model = Socio
    form_class = SocioForm
    template_name = 'cnpj_lookup/socio_create.html'

    def form_valid(self, form):
        empresa_pk = self.kwargs['empresa_pk']
        empresa = get_object_or_404(Empresa, pk=empresa_pk)
        socio = form.save(commit=False)
        socio.empresa = empresa
        socio.save()
        return redirect('empresa_detalhes', pk=empresa.pk)


class SocioDeleteView(DeleteView):
    model = Socio
    template_name = 'cnpj_lookup/socio_confirm_delete.html'

    def get_success_url(self):
        empresa_pk = self.kwargs['empresa_pk']
        return reverse_lazy('empresa_detalhes', kwargs={'pk': empresa_pk})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        empresa_pk = self.kwargs['empresa_pk']
        empresa = get_object_or_404(Empresa, pk=empresa_pk)
        self.object.empresa = None
        self.object.save()
        return redirect('empresa_detalhes', pk=empresa.pk)
