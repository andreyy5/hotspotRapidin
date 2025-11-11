from django import forms
from .models import Cliente
import re


def validar_telefone(valor):
    """
    Valida o telefone:
    - Exatamente 11 dígitos
    - Não todos os dígitos iguais
    """
    # Remove caracteres especiais
    telefone_limpo = re.sub(r'\D', '', valor)
    
    # Verificar se tem exatamente 11 dígitos
    if len(telefone_limpo) != 11:
        raise forms.ValidationError('Telefone deve ter exatamente 11 dígitos')
    
    # Verificar se todos os dígitos são iguais
    if len(set(telefone_limpo)) == 1:
        raise forms.ValidationError('Telefone inválido - dígitos não podem ser todos iguais')
    
    # Verificar se começa com 9 (celular válido)
    if telefone_limpo[2] != '9':
        raise forms.ValidationError('Telefone deve ser um celular válido (terceiro dígito deve ser 9)')


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
                'placeholder': '99 9 8442-8630',
                'inputmode': 'tel',
                'maxlength': '15',  # added maxlength to prevent extra characters
            }),
        }
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            validar_telefone(telefone)
        return telefone
