from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
import re

from .forms import CPFCNPJForm, ClienteForm
from .models import Cliente
from .utils import validar_cliente_hubsoft


class InicioView(TemplateView):
    template_name = 'hotspot/verificar.html'
    
    def post(self, request, *args, **kwargs):
        cpf_cnpj = request.POST.get('cpf_cnpj', '').strip()
        
        if not cpf_cnpj:
            messages.error(request, 'Por favor, insira um CPF ou CNPJ')
            return redirect('inicio')
        
        # Armazena na sessão para uso posterior
        request.session['cpf_cnpj'] = cpf_cnpj
        
        # Valida contra HubSoft
        cliente_data = validar_cliente_hubsoft(cpf_cnpj)
        
        if cliente_data:
            # Cliente encontrado e ativo
            request.session['cliente_nome'] = cliente_data.get('nome_razao_social', 'Cliente')
            request.session['cliente_ativo'] = True
            return redirect('validar')
        else:
            # Cliente não encontrado, ir para cadastro
            request.session['cliente_ativo'] = False
            return redirect('cadastro')


class ValidarView(TemplateView):
    template_name = 'hotspot/sucesso.html'
    
    def get(self, request, *args, **kwargs):
        # Verifica se o cliente já foi validado
        if 'cliente_ativo' not in request.session:
            return redirect('inicio')
        
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente_nome'] = self.request.session.get('cliente_nome', 'Cliente')
        context['cliente_ativo'] = self.request.session.get('cliente_ativo', False)
        return context


class CadastroView(FormView):
    template_name = 'hotspot/cadastro.html'
    form_class = ClienteForm
    success_url = reverse_lazy('sucesso_cadastro')
    
    def form_valid(self, form):
        cpf_cnpj = self.request.session.get('cpf_cnpj', '')
        
        # Cria novo cliente
        cliente = form.save(commit=False)
        cliente.cpf_cnpj = cpf_cnpj
        cliente.save()
        
        self.request.session['cliente_novo'] = True
        return super().form_valid(form)


class SucessoCadastroView(TemplateView):
    template_name = 'hotspot/sucesso.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente_novo'] = self.request.session.get('cliente_novo', False)
        return context
