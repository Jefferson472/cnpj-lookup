from django.urls import path

from apps.cnpj_lookup.views.Home import HomePage
from apps.cnpj_lookup.views.EmpresaView import (
    EmpresaCreateView, EmpresaDeleteView, EmpresaDetailView, EmpresaListView,
    EmpresaUpdateView)


app_name = 'cnpj-lookup'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('empresa/', EmpresaCreateView.as_view(), name='empresa-create'),
    path('empresa/<int:pk>/', EmpresaDetailView.as_view(), name='empresa-detail'),
    path('empresa/<int:pk>/update/', EmpresaUpdateView.as_view(), name='empresa-update'),
    path('empresa/<int:pk>/delete/', EmpresaDeleteView.as_view(), name='empresa-delete'),
    path('empresa/list/', EmpresaListView.as_view(), name='empresa-list'),
]
