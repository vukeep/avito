import argparse
from scripts.update_avito_data import update_avito_data
from scripts.update_prices import update_prices
from utils.logger import get_logger

logger = get_logger("Основное применение")


def main():
    """
    Основная точка входа в приложение.
    Предоставляет возможности для обновления данных Avito, обновления цен или запуска других скриптов.
    """
    parser = argparse.ArgumentParser(description="Приложение для управления данными Avito")
    parser.add_argument(
        "--update-avito-data",
        action="store_true",
        help="Обновление данных Avito и синхронизация с локальной базой данных."
    )
    parser.add_argument(
        "--update-prices",
        action="store_true",
        help="Получение и обновление цен в локальной базе данных и Avito."
    )

    args = parser.parse_args()

    if args.update_avito_data:
        logger.info("Начало обновления данных Avito...")
        try:
            update_avito_data()
            logger.info("Обновление данных Avito завершено успешно.")
        except Exception as e:
            logger.error(f"Ошибка при обновлении данных Avito: {e}")

    if args.update_prices:
        logger.info("Начало обновления цен...")
        try:
            update_prices()
            logger.info("Обновление цен завершено успешно.")
        except Exception as e:
            logger.error(f"Ошибка при обновлении цен: {e}")

    if not (args.update_avito_data or args.update_prices):
        parser.print_help()


if __name__ == "__main__":
    main()

