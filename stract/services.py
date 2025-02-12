import requests

class APIClient:
    def __init__(self, base_url, api_token):
        self.base_url = base_url
        self.api_token = api_token
        self.headers = {'Authorization': f'Bearer {self.api_token}'}
    
    def fetch_data(self, endpoint, params=None):
        """Faz uma requisição GET à API e retorna os dados."""
        url = f'{self.base_url}/{endpoint}'
        print(f"Fetching data from: {url} with params: {params}")  # Log da URL e parâmetros
        response = requests.get(url, headers=self.headers, params=params)
        print(f"Response: {response.status_code}, {response.text}")  # Log da resposta
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f'Failed to fetch data from {endpoint}'}, response.status_code
    
    def fetch_platforms(self):
        """Busca as plataformas disponíveis."""
        return self.fetch_data('platforms')
    
    def fetch_accounts(self, platform):
        """Busca as contas de uma plataforma."""
        return self.fetch_data(f'accounts?platform={platform}')
    
    def fetch_fields(self, platform):
        """Busca os campos disponíveis para uma plataforma."""
        return self.fetch_data(f'fields?platform={platform}')
    
    def fetch_insights(self, platform, account, fields=None):
        """Busca os insights de uma conta em uma plataforma."""
        params = {
            'platform': platform,
            'account': account['name'],  # Nome da conta
            'token': account['token']   # Token da conta
        }
        if fields:
            params['fields'] = ','.join(fields)
        return self.fetch_data('insights', params)


API_BASE_URL = 'https://sidebar.stract.to/api'
API_TOKEN = 'TOKEN-API'

api_client = APIClient(API_BASE_URL, API_TOKEN)