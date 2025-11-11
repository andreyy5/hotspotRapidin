# Configuração do Sistema Hotspot

## Passo 1: Clonar o repositório e configurar

\`\`\`bash
git clone <seu-repo>
cd hotspot_project
\`\`\`

## Passo 2: Criar arquivo .env

Copie o arquivo `.env.example` para `.env`:

\`\`\`bash
cp .env.example .env
\`\`\`

Edite o arquivo `.env` e adicione suas credenciais do HubSoft:

\`\`\`env
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

HUBSOFT_BASE_URL=https://api.nippontec.hubsoft.com.br
HUBSOFT_CLIENT_ID=302
HUBSOFT_CLIENT_SECRET=1bgMRPONzOY8t72uywSwhdADBqYc15WmSKOKnJli
HUBSOFT_USERNAME=dev.rafaelsoares@gmail.com
HUBSOFT_PASSWORD=Segredo124@
\`\`\`

## Passo 3: Instalar dependências

\`\`\`bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

pip install -r requirements.txt
\`\`\`

## Passo 4: Executar migrations

\`\`\`bash
python manage.py migrate
\`\`\`

## Passo 5: Rodar o servidor

\`\`\`bash
python manage.py runserver
\`\`\`

Acesse: `http://localhost:8000`

## Fluxo do Sistema

1. **Tela Inicial**: Usuário insere CPF/CNPJ
2. **Validação HubSoft**: 
   - Se cliente existe e tem status "Serviço Habilitado" ou "Serviço Suspenso Parcialmente" → Mensagem de boas-vindas
   - Se não existe → Formulário de cadastro
3. **Cadastro**: Insere Nome e Telefone
4. **Confirmação**: Mensagem de sucesso

## Variáveis de Ambiente

| Variável | Descrição |
|----------|-----------|
| `DEBUG` | Modo debug (True/False) |
| `SECRET_KEY` | Chave secreta do Django |
| `HUBSOFT_BASE_URL` | URL base da API HubSoft |
| `HUBSOFT_CLIENT_ID` | ID do cliente HubSoft |
| `HUBSOFT_CLIENT_SECRET` | Secret do cliente HubSoft |
| `HUBSOFT_USERNAME` | Email de usuário HubSoft |
| `HUBSOFT_PASSWORD` | Senha do usuário HubSoft |

## Troubleshooting

**Erro: "ModuleNotFoundError: No module named 'dotenv'"**
- Execute: `pip install python-dotenv`

**Erro: "Variáveis de ambiente não carregadas"**
- Certifique-se de que o arquivo `.env` está na raiz do projeto
- Restart o servidor: `python manage.py runserver`

**Erro de conexão com HubSoft**
- Verifique as credenciais no arquivo `.env`
- Teste a URL: `curl https://api.nippontec.hubsoft.com.br/api/v1/integracao/cliente`
