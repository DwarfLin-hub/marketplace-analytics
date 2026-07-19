import psycopg2
import logging
from config import DB_CONFIG

logger = logging.getLogger(__name__)

def get_connection():
    """Возвращает подключение к PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)

def test_connection():
    """Тест подключения к БД."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        cur.close()
        conn.close()
        logger.info("Подключение к БД успешно")
        return True
    except Exception as e:
        logger.error(f"Ошибка подключения к БД: {e}")
        return False

def upsert_clients_batch(clients_dict):
    """Массовая вставка/обновление клиентов."""
    if not clients_dict:
        return
    conn = get_connection()
    cur = conn.cursor()
    args = [(cid, gender) for cid, gender in clients_dict.items()]
    try:
        cur.executemany("""
            INSERT INTO clients (client_id, gender)
            VALUES (%s, %s)
            ON CONFLICT (client_id) DO UPDATE
            SET gender = EXCLUDED.gender
        """, args)
        conn.commit()
        logger.info(f"Обновлено {len(args)} клиентов")
    except Exception as e:
        logger.error(f"Ошибка вставки клиентов: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def upsert_products_batch(product_ids):
    """Массовая вставка товаров."""
    if not product_ids:
        return
    conn = get_connection()
    cur = conn.cursor()
    args = [(pid,) for pid in product_ids]
    try:
        cur.executemany("""
            INSERT INTO products (product_id)
            VALUES (%s)
            ON CONFLICT (product_id) DO NOTHING
        """, args)
        conn.commit()
        logger.info(f"Обновлено {len(args)} товаров")
    except Exception as e:
        logger.error(f"Ошибка вставки товаров: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def insert_sales_batch(records, batch_size=500):
    """Массовая вставка продаж."""
    if not records:
        logger.info("Нет записей для вставки")
        return
    conn = get_connection()
    cur = conn.cursor()
    total = len(records)
    logger.info(f"Всего записей для вставки: {total}")

    for i in range(0, total, batch_size):
        batch = records[i:i+batch_size]
        args = []
        for r in batch:
            args.append((
                r['client_id'],
                r['product_id'],
                r['purchase_datetime'],
                r['purchase_time_as_seconds_from_midnight'],
                r['quantity'],
                r['price_per_item'],
                r['discount_per_item'],
                r['total_price']
            ))
        try:
            cur.executemany("""
                INSERT INTO sales (
                    client_id, product_id, purchase_date, purchase_time_seconds,
                    quantity, price_per_item, discount_per_item, total_price
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (client_id, product_id, purchase_date, purchase_time_seconds)
                DO NOTHING
            """, args)
            conn.commit()
            logger.info(f"✅ Батч {i//batch_size + 1} ({len(args)} строк) успешно вставлен")
        except Exception as e:
            logger.error(f"❌ Ошибка вставки батча {i//batch_size + 1}: {e}")
            conn.rollback()
            import traceback
            logger.error(traceback.format_exc())
    cur.close()
    conn.close()
    logger.info("Вставка всех записей завершена")