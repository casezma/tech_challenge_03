from django.urls import path
from app.views import criar_registro, listar_registros,listar_registros_a_partir_de_timestamp

urlpatterns = [
    path('criar-registro',criar_registro),
	path('listar-registros',listar_registros),
    path('listar-registros-a-partir-de-timestamp',listar_registros_a_partir_de_timestamp)
]