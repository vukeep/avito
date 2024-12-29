import os
from dotenv import load_dotenv
from .descriptions import Description_iSmart

load_dotenv()

# Example credentials loaded from .env
client_id = os.getenv("Client_id_iSmartChita")
client_secret = os.getenv("Client_secret_iSmartChita")

# Account configurations
accounts = [
    {
        'key': 'iSmartChita',
        'data_details': {
            'Description': Description_iSmart,
            'Condition': 'Новое',
            'ContactPhone': '88005509022',
            'AdType': 'Товар приобретен на продажу',
            'Address': 'г. Чита, ул. Шилова 100 ТЦ Макси',
            'ManagerName': 'iSmart',
            'Box_Sealed': 'Да',
            },
        'client_id': client_id,
        'client_secret': client_secret,
        'stores': ['Чита Склад Макси 4 iSmart', 'Чита Склад Новосити iSmart'],
    }
]
