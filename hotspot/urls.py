from django.urls import path
from .views import (
    InicioView,
    ValidarView,
    CadastroView,
    SucessoCadastroView,
)

urlpatterns = [
    path('', InicioView.as_view(), name='inicio'),
    path('validar/', ValidarView.as_view(), name='validar'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('sucesso-cadastro/', SucessoCadastroView.as_view(), name='sucesso_cadastro'),
]
