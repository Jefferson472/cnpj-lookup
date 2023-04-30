from django.urls import path

from apps.cnpj_lookup.views.Home import HomePage


app_name = 'cnpj-lookup'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
]
