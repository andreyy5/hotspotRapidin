from django import forms
from .models import Cliente
import re


class CPFCNPJForm(forms.Form):
    """Formulário para validação de CPF/CNPJ"""
    cpf_cnpj = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition',
            'placeholder': 'Digite seu CPF ou CNPJ',
            'inputmode': 'numeric',
        })
    )

    def clean_cpf_cnpj(self):
        cpf_cnpj = self.cleaned_data.get('cpf_cnpj')
        # Remove caracteres especiais
        cpf_cnpj = re.sub(r'\D', '', cpf_cnpj)
        if not cpf_cnpj or (len(cpf_cnpj) not in [11, 14]):
            raise forms.ValidationError('CPF ou CNPJ inválido')
        return cpf_cnpj


class ClienteForm(forms.ModelForm):
    """Formulário para cadastro de novo cliente"""
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition',
                'placeholder': 'Seu nome completo',
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition',
                'placeholder': '(11) 99999-9999',
                'inputmode': 'tel',
            }),
        }
