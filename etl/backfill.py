import logging
import time
from datetime import datetime, timedelta
from daily_etl import process_day

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def backfill(start_date, end_date, pause=1):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    current = start
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        logging.info(f"Backfill {date_str}")
        process_day(date_str)
        time.sleep(pause)
        current += timedelta(days=1)

if __name__ == "__main__":
    # Укажите диапазон, например с 2023-01-01 до вчера
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    backfill(start_date, end_date)