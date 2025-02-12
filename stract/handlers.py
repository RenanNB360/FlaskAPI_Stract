from stract.services import api_client
from stract.utils import generate_csv

def _process_paginated_response(response):
    """Processa respostas paginadas da API."""
    print(f"Processing response: {response}")  # Log da resposta
    if isinstance(response, dict) and 'error' in response:
        return response
    
    # Extrai a lista de contas, campos ou insights da resposta
    if 'accounts' in response:
        return response['accounts']
    elif 'fields' in response:
        return [field['value'] for field in response['fields']]
    elif 'data' in response:
        return response['data']
    else:
        return response

def _calculate_cost_per_click(ad_data):
    """Calcula o CPC para Google Analytics, se necessário."""
    if ad_data.get('Platform') == 'Google Analytics' and ad_data.get('clicks', 0) > 0:
        ad_data['Cost per Click'] = ad_data.get('spend', 0) / ad_data['clicks']
    return ad_data

def get_ads_by_platform(platform):
    """Retorna todos os anúncios de uma plataforma."""
    print(f"Fetching accounts for platform: {platform}")  # Log da plataforma
    accounts_response = api_client.fetch_accounts(platform)
    accounts = _process_paginated_response(accounts_response)
    print(f"Accounts: {accounts}")  # Log das contas

    if 'error' in accounts:
        return {'error': f'Failed to fetch accounts for {platform}', 'status': 500}

    print(f"Fetching fields for platform: {platform}")  # Log da plataforma
    fields_response = api_client.fetch_fields(platform)
    fields = _process_paginated_response(fields_response)
    print(f"Fields: {fields}")  # Log dos campos

    if 'error' in fields:
        return {'error': f'Failed to fetch fields for {platform}', 'status': 500}

    all_ads = []
    for account in accounts:
        print(f"Fetching insights for account: {account['name']}")  # Log da conta
        insights = api_client.fetch_insights(platform, account, fields)
        print(f"Insights: {insights}")  # Log dos insights

        if 'error' in insights:
            return {'error': f'Failed to fetch insights for {platform} {account['name']}', 'status': 500}
        
        insights_data = _process_paginated_response(insights)
        for ad in insights_data:
            ad.update({'Platform': platform, 'Account Name': account['name']})
            ad = _calculate_cost_per_click(ad)
            all_ads.append(ad)

    return generate_csv(all_ads, f'{platform}_ads')

def get_summary_by_platform(platform):
    """Retorna um resumo dos anúncios de uma plataforma, agregado por conta."""
    accounts_response = api_client.fetch_accounts(platform)
    accounts = _process_paginated_response(accounts_response)
    if 'error' in accounts:
        return {'error': f'Failed to fetch accounts for {platform}', 'status': 500}

    fields_response = api_client.fetch_fields(platform)
    fields = _process_paginated_response(fields_response)
    if 'error' in fields:
        return {'error': f'Failed to fetch fields for {platform}', 'status': 500}

    summary = {}
    for account in accounts:
        insights = api_client.fetch_insights(platform, account, fields)
        if 'error' in insights:
            return {'error': f'Failed to fetch insights for {platform} {account['name']}', 'status': 500}
        
        insights_data = _process_paginated_response(insights)
        account_name = account['name']
        if account_name not in summary:
            summary[account_name] = {'Platform': platform, 'Account Name': account_name}
        
        for ad in insights_data:
            ad = _calculate_cost_per_click(ad)
            for key, value in ad.items():
                if isinstance(value, (int, float)):
                    summary[account_name][key] = summary[account_name].get(key, 0) + value

    return generate_csv(list(summary.values()), f'{platform}_summary')

def get_all_ads():
    """Retorna todos os anúncios de todas as plataformas."""
    platforms_response = api_client.fetch_platforms()
    platforms = _process_paginated_response(platforms_response)
    if 'error' in platforms:
        return {'error': 'Failed to fetch platforms', 'status': 500}

    all_ads = []
    for platform in platforms:
        ads = get_ads_by_platform(platform)
        if isinstance(ads, dict) and 'error' in ads:
            return ads
        all_ads.extend(ads)

    return generate_csv(all_ads, 'all_ads')

def get_general_summary():
    """Retorna um resumo de todas as plataformas."""
    platforms_response = api_client.fetch_platforms()
    platforms = _process_paginated_response(platforms_response)
    if 'error' in platforms:
        return {'error': 'Failed to fetch platforms', 'status': 500}

    summary = {}
    for platform in platforms:
        platform_summary = get_summary_by_platform(platform)
        if isinstance(platform_summary, dict) and 'error' in platform_summary:
            return platform_summary
        summary[platform] = platform_summary

    return generate_csv(list(summary.values()), 'general_summary')