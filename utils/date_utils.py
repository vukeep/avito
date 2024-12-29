from datetime import datetime, timedelta

def format_date(date: datetime, format: str = '%Y-%m-%dT%H:%M:%S') -> str:
    """
    Преобразование объекта datetime в строку.
    """
    return date.strftime(format)

def calculate_date_range(days: int = 14) -> tuple:
    """
    Рассчитывает диапазон дат от текущей даты до прошлого количества дней.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date
