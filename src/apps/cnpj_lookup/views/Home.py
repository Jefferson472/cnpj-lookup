from django.views.generic import RedirectView


class HomePage(RedirectView):
    url = '/empresas/'
