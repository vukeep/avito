import pandas as pd


class ReportingManager:
    def generate_csv_report(self, data, file_name):
        """
        Экспорт заданных данных в CSV-файл.
        """
        df = pd.DataFrame(data)
        df.to_csv(file_name, index=False, encoding='utf-8')

    def generate_summary(self, data):
        """
        Генерация сводного отчета из данных.
        """
        summary = {
            'Total Items': len(data),
            'Total Value': sum(item['Price'] for item in data),
        }
        return summary
    
    def generate_xlsx_report(self, data, file_name):
        """
        Экспорт заданных данных в XLSX-файл.
        """
        df = pd.DataFrame(data)
        df.to_excel(file_name, index=False, engine='openpyxl')
