import requests
import logging
import time
from config import API_URL

logger = logging.getLogger(__name__)

def fetch_sales_for_date(date_str, retries=3, delay=2):
    params = {"date": date_str}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    for attempt in range(retries):
        try:
            logger.info(f"Запрос к API для {date_str} (попытка {attempt+1})")
            resp = requests.get(API_URL, params=params, headers=headers, timeout=30)
            logger.info(f"Статус ответа: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list):
                    logger.info(f"Получено {len(data)} записей")
                    return data
                else:
                    logger.error(f"Неожиданный формат: {type(data)}")
                    return []
            else:
                logger.warning(f"HTTP {resp.status_code}: {resp.text[:200]}")
                # Если 403, возможно, нужно сделать паузу подольше
                if resp.status_code == 403:
                    logger.warning("Возможно, IP заблокирован. Увеличим паузу.")
                    time.sleep(delay * 2)
        except Exception as e:
            logger.warning(f"Попытка {attempt+1} не удалась: {e}")
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
            else:
                logger.error(f"Не удалось получить данные за {date_str}")
                return []
    return []