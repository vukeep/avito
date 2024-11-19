# Пример тестирования метода
from api_client import AvitoAPIClient
import os
import dotenv

dotenv.load_dotenv()

api_key = os.getenv("TOKEN")

# Инициализируем API клиент с вашим ключом
client = AvitoAPIClient(api_key=api_key)

'''# Тестируем метод get_report_items с реальными параметрами
report_id = 275045439
response = client.autoload.get_report_items(
    report_id=report_id,
    per_page=50,
    page=0,
    query='4256564537742,JBL-JBLWBUDSBLK',
    sections=None
)'''

# user_info = client.user.get_user_info()

# user_balance = client.user.get_user_balance(user_id=251411026)

# Получение истории операций
#operations_history = client.user.get_operations_history(
#    date_from="2024-09-01T00:00:00",
#    date_to="2024-10-07T00:00:00"
#)

last_completed = client.autoload.get_last_completed_report()

# Печатаем результат
print(last_completed)