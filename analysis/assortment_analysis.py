import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных (предполагаем, что файлы уже загружены)
sales = pd.read_csv('sales.csv', names=['client_id', 'gender', 'product_id', 'purchase_datetime', 
                                        'purchase_time_seconds', 'quantity', 'price_per_item', 
                                        'discount_per_item', 'total_price'], header=None)

# Анализ ассортимента
df_product = sales.groupby('product_id').agg({
    'total_price': 'sum',
    'quantity': 'sum',
    'discount_per_item': 'mean',
    'price_per_item': 'mean'
}).reset_index()
df_product['avg_discount_rate'] = df_product['discount_per_item'] / df_product['price_per_item']

df_product = df_product.sort_values('total_price', ascending=False)
df_product['cum_revenue'] = df_product['total_price'].cumsum()
df_product['cum_pct'] = df_product['cum_revenue'] / df_product['total_price'].sum() * 100
df_product['abc_group'] = df_product['cum_pct'].apply(lambda x: 'A' if x <= 80 else ('B' if x <= 95 else 'C'))

# Графики
plt.figure(figsize=(12,6))
sns.barplot(data=df_product.head(50), x='product_id', y='total_price', hue='abc_group', dodge=False)
plt.xticks(rotation=90)
plt.title('ABC-анализ товаров (топ-50)')
plt.tight_layout()
plt.savefig('abc_analysis.png')
plt.show()

df_product['revenue_share'] = df_product['total_price'] / df_product['total_price'].sum()
df_product['qty_share'] = df_product['quantity'] / df_product['quantity'].sum()

plt.figure(figsize=(10,6))
sc = plt.scatter(df_product['revenue_share'], df_product['qty_share'],
                 alpha=0.6, c=df_product['avg_discount_rate'], cmap='coolwarm')
plt.xlabel('Доля в выручке')
plt.ylabel('Доля в количестве')
plt.title('BCG-матрица (цвет = средняя скидка)')
plt.colorbar(sc)
plt.savefig('bcg_matrix.png')
plt.show()

# Товары для вывода
df_drop = df_product[(df_product['abc_group'] == 'C') & (df_product['avg_discount_rate'] > 0.3)]
print(f"Рекомендуется вывести {len(df_drop)} товаров")
df_drop[['product_id', 'total_price', 'avg_discount_rate']].to_csv('products_to_drop.csv', index=False)

print("✅ Анализ ассортимента завершён. Файлы сохранены.")