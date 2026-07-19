import logging
import sys
from datetime import datetime, timedelta
from fetch_data import fetch_sales_for_date
from db_utils import upsert_clients_batch, upsert_products_batch, insert_sales_batch, test_connection

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/etl.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def process_day(date_str):
    logger.info(f"=== Начинаем обработку {date_str} ===")
    
    # Проверка подключения к БД
    if not test_connection():
        logger.error("Подключение к БД не установлено. Остановка.")
        return

    records = fetch_sales_for_date(date_str)
    if not records:
        logger.info(f"Нет данных за {date_str}")
        return

    logger.info(f"Получено {len(records)} записей, начинаем обработку")

    clients = {}
    products = set()
    for r in records:
        clients[r['client_id']] = r['gender']
        products.add(r['product_id'])

    logger.info(f"Найдено {len(clients)} клиентов и {len(products)} товаров")

    logger.info("Обновление справочника клиентов...")
    upsert_clients_batch(clients)
    logger.info("Справочник клиентов обновлён")

    logger.info("Обновление справочника товаров...")
    upsert_products_batch(products)
    logger.info("Справочник товаров обновлён")

    logger.info("Начинаем вставку продаж...")
    insert_sales_batch(records)
    logger.info(f"Загрузка за {date_str} завершена")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_date = sys.argv[1]
    else:
        target_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    process_day(target_date)