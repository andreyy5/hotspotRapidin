from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
import re

from .forms import CPFCNPJForm, ClienteForm
from .models import Cliente
from .utils import HubSoftAPI


class InicioView(TemplateView):
    """Tela inicial - inserir CPF/CNPJ"""
    template_name = 'hotspot/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CPFCNPJForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CPFCNPJForm(request.POST)
        if form.is_valid():
            cpf_cnpj = form.cleaned_data['cpf_cnpj']
            request.session['cpf_cnpj'] = cpf_cnpj
            return redirect('validar')
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


class ValidarView(TemplateView):
    """Valida CPF/CNPJ contra HubSoft e HubSoft"""
    template_name = 'hotspot/inicio.html'

    def get(self, request, *args, **kwargs):
        cpf_cnpj = request.session.get('cpf_cnpj')
        
        if not cpf_cnpj:
            return redirect('inicio')

        # Tenta buscar cliente no HubSoft
        hubsoft = HubSoftAPI()
        cliente_hubsoft = hubsoft.search_cliente(cpf_cnpj)

        if cliente_hubsoft:
            # Cliente existe e tem serviço habilitado
            request.session['cliente_nome'] = cliente_hubsoft.get('nome', 'Cliente')
            return redirect('sucesso-existente')

        # Cliente não existe no HubSoft, ir para formulário
        return redirect('cadastro')


class CadastroView(FormView):
    """Tela de cadastro - inserir Nome e Telefone"""
    template_name = 'hotspot/cadastro.html'
    form_class = ClienteForm
    success_url = reverse_lazy('sucesso-novo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cpf_cnpj = self.request.session.get('cpf_cnpj')
        if not cpf_cnpj:
            context['redirect_home'] = True
        context['cpf_cnpj'] = cpf_cnpj
        return context

    def form_valid(self, form):
        cpf_cnpj = self.request.session.get('cpf_cnpj')
        
        if not cpf_cnpj:
            return redirect('inicio')

        # Salva cliente localmente
        cliente, created = Cliente.objects.get_or_create(
            cpf_cnpj=cpf_cnpj,
            defaults={
                'nome': form.cleaned_data['nome'],
                'telefone': form.cleaned_data['telefone'],
            }
        )
        
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        cpf_cnpj = request.session.get('cpf_cnpj')
        if not cpf_cnpj:
            return redirect('inicio')
        return super().get(request, *args, **kwargs)


class SucessoExistenteView(TemplateView):
    """Tela final para cliente existente"""
    template_name = 'hotspot/sucesso-existente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome'] = self.request.session.get('cliente_nome', 'Cliente')
        return context

    def get(self, request, *args, **kwargs):
        if 'cliente_nome' not in request.session:
            return redirect('inicio')
        return super().get(request, *args, **kwargs)


class SucessoNovoView(TemplateView):
    """Tela final para novo cliente"""
    template_name = 'hotspot/sucesso-novo.html'

    def get(self, request, *args, **kwargs):
        if 'cpf_cnpj' not in request.session:
            return redirect('inicio')
        return super().get(request, *args, **kwargs)
