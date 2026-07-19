import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import files

# 1. Загрузка данных (предполагаем, что sales.csv уже загружен)
sales = pd.read_csv('sales.csv', 
                    names=['client_id', 'gender', 'product_id', 'purchase_datetime', 
                           'purchase_time_seconds', 'quantity', 'price_per_item', 
                           'discount_per_item', 'total_price'], header=None)
sales['purchase_date'] = pd.to_datetime(sales['purchase_datetime'])
print(f"Загружено {len(sales)} записей о продажах")

# 2. RFM-анализ (на выборке для скорости)
sample = sales.sample(n=min(200000, len(sales)), random_state=42)
print(f"Используем выборку из {len(sample)} записей для RFM")

today = pd.to_datetime('2023-12-31')
rfm = sample.groupby('client_id').agg(
    recency=('purchase_date', lambda x: (today - x.max()).days),
    frequency=('purchase_date', 'count'),
    monetary=('total_price', 'sum')
).reset_index()

# Удаляем клиентов с нулевыми показателями (если есть)
rfm = rfm[(rfm['frequency'] > 0) & (rfm['monetary'] > 0)]

# Создаём оценки (квартили)
try:
    rfm['r_score'] = pd.qcut(rfm['recency'], 4, labels=[4,3,2,1])
    rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 4, labels=[1,2,3,4])
    rfm['m_score'] = pd.qcut(rfm['monetary'], 4, labels=[1,2,3,4])
except ValueError:
    # Если данных мало или одинаковые значения – используем равные интервалы
    rfm['r_score'] = pd.cut(rfm['recency'], bins=4, labels=[4,3,2,1])
    rfm['f_score'] = pd.cut(rfm['frequency'], bins=4, labels=[1,2,3,4])
    rfm['m_score'] = pd.cut(rfm['monetary'], bins=4, labels=[1,2,3,4])

rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)

def segment(row):
    if row['rfm_score'] in ['444','443','434','344']:
        return 'Champions'
    elif row['rfm_score'] in ['442','433','343','334','432']:
        return 'Loyal'
    elif row['rfm_score'] in ['411','412','421','422']:
        return 'New'
    elif row['rfm_score'] in ['311','312','321','322','331']:
        return 'At Risk'
    else:
        return 'Others'

rfm['segment'] = rfm.apply(segment, axis=1)
seg_counts = rfm['segment'].value_counts()
print("\nРаспределение сегментов RFM (на основе выборки):")
print(seg_counts)
seg_counts.to_csv('rfm_segments.csv')

# 3. Когортный LTV (на всех данных, оптимизированно)
print("\nСтроим когортный LTV на всех данных (может занять 1-2 минуты)...")
sales['purchase_month'] = sales['purchase_date'].dt.to_period('M')
first_purchase = sales.groupby('client_id')['purchase_month'].min().reset_index(name='cohort_month')
sales_merged = sales.merge(first_purchase, on='client_id')

# Быстрое вычисление months_since (без apply)
sales_merged['purchase_dt'] = sales_merged['purchase_month'].dt.start_time
sales_merged['cohort_dt'] = sales_merged['cohort_month'].dt.start_time
sales_merged['months_since'] = (sales_merged['purchase_dt'].dt.year - sales_merged['cohort_dt'].dt.year) * 12 + \
                                (sales_merged['purchase_dt'].dt.month - sales_merged['cohort_dt'].dt.month)

ltv = sales_merged.groupby(['cohort_month', 'months_since'])['total_price'].mean().reset_index()
ltv_pivot = ltv.pivot(index='cohort_month', columns='months_since', values='total_price')

# Сохраняем LTV в CSV
ltv_pivot.to_csv('ltv_cohorts.csv')

# Тепловая карта
plt.figure(figsize=(14,8))
sns.heatmap(ltv_pivot, annot=True, fmt='.0f', cmap='YlGnBu')
plt.title('Когортный анализ LTV (средний чек по месяцам)')
plt.xlabel('Месяцы с момента первой покупки')
plt.ylabel('Месяц первой покупки')
plt.tight_layout()
plt.savefig('ltv_cohorts.png')
plt.show()

print("\n✅ Анализ завершён. Сохранены файлы:")
print("- rfm_segments.csv")
print("- ltv_cohorts.csv")
print("- ltv_cohorts.png")

# 4. Скачивание всех файлов (включая те, что могли быть созданы ранее)
# Если вы уже выполняли ABC-анализ, то там есть файлы:
# abc_analysis.png, bcg_matrix.png, products_to_drop.csv
# Добавим их в список для скачивания (если они существуют)

files_to_download = [
    'rfm_segments.csv',
    'ltv_cohorts.csv',
    'ltv_cohorts.png',
    'abc_analysis.png',
    'bcg_matrix.png',
    'products_to_drop.csv'
]

print("\nСкачивание файлов...")
for f in files_to_download:
    try:
        files.download(f)
        print(f"✅ {f} скачан")
    except:
        print(f"❌ {f} не найден (возможно, ещё не создан)")

print("\n🎉 Готово! Используйте скачанные файлы для презентации.")