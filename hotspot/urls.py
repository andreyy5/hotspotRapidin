from django.urls import path
from .views import (
    InicioView,
    ValidarView,
    CadastroView,
    SucessoExistenteView,
    SucessoNovoView,
)

urlpatterns = [
    path('', InicioView.as_view(), name='inicio'),
    path('validar/', ValidarView.as_view(), name='validar'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('sucesso-existente/', SucessoExistenteView.as_view(), name='sucesso-existente'),
    path('sucesso-novo/', SucessoNovoView.as_view(), name='sucesso-novo'),
]
