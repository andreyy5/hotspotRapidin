import requests
import json
from django.conf import settings
from typing import Optional, Dict


class HubSoftAPI:
    """Classe para integração com API do HubSoft"""

    def __init__(self):
        self.base_url = settings.HUBSOFT_BASE_URL
        self.client_id = settings.HUBSOFT_CLIENT_ID
        self.client_secret = settings.HUBSOFT_CLIENT_SECRET
        self.username = settings.HUBSOFT_USERNAME
        self.password = settings.HUBSOFT_PASSWORD
        self.token = None

    def authenticate(self) -> bool:
        """Autentica e obtém token da API HubSoft"""
        try:
            url = f"{self.base_url}/api/v1/oauth/token"
            payload = {
                'grant_type': 'password',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'username': self.username,
                'password': self.password,
            }
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            self.token = response.json().get('access_token')
            return bool(self.token)
        except Exception as e:
            print(f"[v0] Erro ao autenticar HubSoft: {str(e)}")
            return False

    def search_cliente(self, cpf_cnpj: str) -> Optional[Dict]:
        """
        Busca cliente no HubSoft pelo CPF/CNPJ
        Retorna None se não autenticado ou cliente não encontrado
        """
        if not self.token and not self.authenticate():
            return None

        try:
            url = f"{self.base_url}/api/v1/integracao/cliente"
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json',
            }
            params = {
                'busca': cpf_cnpj,
                'termo_busca': cpf_cnpj,
                'limit': 10,
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            
            # Procura cliente com CPF/CNPJ e status válido
            if isinstance(data, list):
                for cliente in data:
                    if (cliente.get('cpf_cnpj') == cpf_cnpj and 
                        cliente.get('status') in ['Serviço Habilitado', 'Serviço Suspenso Parcialmente']):
                        return cliente
            elif isinstance(data, dict) and data.get('data'):
                for cliente in data.get('data', []):
                    if (cliente.get('cpf_cnpj') == cpf_cnpj and 
                        cliente.get('status') in ['Serviço Habilitado', 'Serviço Suspenso Parcialmente']):
                        return cliente

            return None
        except Exception as e:
            print(f"[v0] Erro ao buscar cliente HubSoft: {str(e)}")
            return None
