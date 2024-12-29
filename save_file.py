from business_logic import ReportingManager
from db.db_handler import DatabaseHandler
from business_logic import card_creation

reporting = ReportingManager()
db_handler = DatabaseHandler()

card_creation()

data = db_handler.get_all_stores('iSmartChita')

reporting.generate_xlsx_report(data, 'file_name.xlsx')
