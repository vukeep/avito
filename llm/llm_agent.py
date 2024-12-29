import requests
from dotenv import load_dotenv
import os
import json
from .promt import system_promt_json
# Загружаем переменные окружения
load_dotenv()
api_key = os.getenv('openai_key')
http = os.getenv('http')
https = os.getenv('https')

def get_response(control_color, proposed_colors):
    
    # Формируем запрос к API
    proxies = {
        "http": http,
        "https": https
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    content_promt = f'control_color: {control_color}, proposed_colors: {proposed_colors}'

    json_data = {
        'model': 'gpt-4o-mini',
        'messages': [
            {'role': 'system', 'content': system_promt_json},
            {'role': 'user', 'content': content_promt},
        ],
        'response_format': {
            'type': 'json_schema',
            'json_schema': {
                'name': 'color_data',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'color_data': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'Control color': {'type': 'string'},
                                    'Most appropriate': {'type': 'string'},
                                    'Your confidence level': {'type': 'number'},
                                },
                                'required': [
                                    'Control color',
                                    'Most appropriate',
                                    'Your confidence level'
                                ],
                                'additionalProperties': False
                            }
                        }
                    },
                    'required': ['color_data'],
                    'additionalProperties': False
                },
                'strict': True,
            },
        },
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data, proxies=proxies)
    
    if not response.status_code == 200:
        return {'error': 'Запрос не удался, попробуйте позже.'}
    
    return json.loads(response.text)

def ai_agent(control_color, proposed_colors):
    response_dict = get_response(control_color, proposed_colors)
    if 'error' in response_dict:
        response_text = response_dict.get('error')
        return response_text
    else:
        response_icc_data = response_dict.get('choices')[0].get('message').get('content')
        color_data = json.loads(response_icc_data).get('color_data')[0]
        return color_data


if __name__ == '__main__':
    control_color = 'песчаный'
    proposed_colors = 'белый, золотистый, серый, черный'
    print(ai_agent(control_color, proposed_colors))
