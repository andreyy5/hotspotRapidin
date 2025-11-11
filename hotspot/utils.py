import os
import requests
from django.conf import settings

def autenticar_hubsoft():
    """Autentica na API HubSoft e retorna o token"""
    url = f"{settings.HUBSOFT_BASE_URL}/oauth/token"
    
    payload = {
        'client_id': settings.HUBSOFT_CLIENT_ID,
        'client_secret': settings.HUBSOFT_CLIENT_SECRET,
        'username': settings.HUBSOFT_USERNAME,
        'password': settings.HUBSOFT_PASSWORD,
        'grant_type': 'password'
    }
    
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        token = response.json().get('access_token')
        print(f"[v0] Token obtido com sucesso")
        return token
    except requests.exceptions.RequestException as e:
        print(f"[v0] Erro ao autenticar HubSoft: {e}")
        return None


def validar_cliente_hubsoft(cpf_cnpj):
    """Valida se o cliente existe na API HubSoft e tem serviço ativo"""
    token = autenticar_hubsoft()
    
    if not token:
        print(f"[v0] ERRO: Falha ao autenticar na API HubSoft")
        return None
    
    # Remove formatação do CPF/CNPJ
    cpf_cnpj_clean = ''.join(filter(str.isdigit, cpf_cnpj))
    print(f"[v0] CPF/CNPJ informado: {cpf_cnpj}")
    print(f"[v0] CPF/CNPJ limpo: {cpf_cnpj_clean}")
    
    url = f"{settings.HUBSOFT_BASE_URL}/api/v1/integracao/cliente"
    
    params = {
        'busca': 'cpf_cnpj',
        'termo_busca': cpf_cnpj_clean,
        'limit': 10,
    }
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    print(f"[v0] URL da API: {url}")
    print(f"[v0] Parâmetros: {params}")
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        print(f"[v0] Status code da resposta: {response.status_code}")
        print(f"[v0] Resposta completa da API: {response.json()}")
        
        data = response.json()
        
        # Verifica se a resposta contém clientes
        if isinstance(data, dict) and 'clientes' in data:
            clientes = data['clientes']
            
            if isinstance(clientes, list) and len(clientes) > 0:
                cliente = clientes[0]
                
                # Verifica se o cliente tem algum serviço ativo
                servicos = cliente.get('servicos', [])
                
                for servico in servicos:
                    status_servico = servico.get('status', '')
                    print(f"[v0] Status do serviço: {status_servico}")
                    
                    if status_servico in ['Serviço Habilitado', 'Serviço Suspenso Parcialmente']:
                        nome_cliente = cliente.get('nome_razaosocial', 'Cliente')
                        print(f"[v0] CLIENTE ENCONTRADO: {nome_cliente} com serviço ativo")
                        return cliente
                
                print(f"[v0] Cliente encontrado, mas SEM serviço ativo")
        
        print(f"[v0] NENHUM CLIENTE ENCONTRADO para o CPF: {cpf_cnpj_clean}")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"[v0] Erro ao consultar cliente: {e}")
        return None
