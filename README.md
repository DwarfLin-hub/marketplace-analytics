# marketplace-analytics
Аналитика продаж маркетплейса. ETL, PostgreSQL, Metabase, аналитика.
commit 1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
Author: Linar (linar.shabalin.03@mail.ru)
Date:   Sunday Jul 19 10:15:00 2026 +0300

    feat: initial project structure and API exploration
    
    - Created project folders: etl/, analysis/, docs/
    - Added test_api.py to explore API endpoint
    - Confirmed GET method with date parameter
    - Added requirements.txt

commit 2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u
Author: Linar (linar.shabalin.03@mail.ru)
Date:   Sunday Jul 19 11:30:00 2026 +0300

    feat: database schema and connection utilities
    
    - Designed PostgreSQL schema (clients, products, sales)
    - Added config.py and db_utils.py with connection functions
    - Created schema.sql for database initialization
    - Tested connection locally

commit 3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v
Author: Linar (linar.shabalin.03@mail.ru)
Date:   Sunday Jul 19 14:45:00 2026 +0300

    feat: ETL scripts (daily and backfill)
    
    - Added fetch_data.py with retry logic and proper headers
    - Implemented daily_etl.py for incremental loads
    - Implemented backfill.py for historical data (2023-2024)
    - Added logging and error handling

commit 4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w
Author: Linar (linar.shabalin.03@mail.ru)
Date:   Sunday Jul 19 16:00:00 2026 +0300

    feat: automation with Windows Task Scheduler
    
    - Added cron-equivalent scheduled task (daily at 7:00)
    - Provided .bat script for easy registration
    - Updated README with scheduling instructions

commit 5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x
Author: Linar (linar.shabalin.03@mail.ru)
Date:   Sunday Jul 19 16:20:00 2026 +0300

    feat: Metabase setup and dashboard creation
    
    - Deployed Metabase via Docker (or JAR)
    - Connected to PostgreSQL database
    - Created 8 key questions (revenue trend, top products, etc.)
    - Assembled dashboard with auto-refresh

commit 6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y
Author: Linar (linar.shabalin.03@mail.ru)
Date:   Sunday Jul 19 17:30:00 2026 +0300

    feat: assortment analysis (ABC + BCG)
    
    - Added assortment_analysis.py (local and Colab versions)
    - Generated ABC chart, BCG matrix, products_to_drop.csv
    - Identified 11,502 items for removal

commit 7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z
Author: Linar (linar.shabalin.03@mail.ru)
Date:   Sunday Jul 19 18:10:00 2026 +0300

    feat: client analysis (RFM + LTV cohorts)
    
    - Added client_analysis.py for RFM segmentation and cohort LTV
    - Generated RFM segments (Champions, Loyal, At Risk, Others)
    - Created LTV heatmap
    - Provided specific recommendations for each segment

commit 8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a
Author: Linar (linar.shabalin.03@mail.ru)
Date:   Sunday Jul 19 20:00:00 2026 +0300

    docs: final report and presentation
    - Added presentation slides (PPTX)
    - Compiled analysis results into reports/
    - Updated README with project overview, setup, and access details
    - Final commit before submission

КОММИТ
МЕТАБЕЙЗ РАЗВОРАЧИВАНИЕ ЛОКАЛЬНО И КАК ПРОЕКТ ЗАПУСКАЕТСЯ

МЕТАБЕЙЗ развернут локально на ноутбуке
- Для этого мы скачиваем приложение Docker desctop
- устанавливаем его и запускаем
- После запуска заходим в командную строку
- В командной строке пишем: docker run -d -p 3000:3000 --name metabase -e MB_DB_TYPE=postgres -e MB_DB_DBNAME=marketplace -e MB_DB_PORT=5432 -e MB_DB_USER=analyst -e MB_DB_PASS=ваш_пароль -e MB_DB_HOST=host.docker.internal metabase/metabase
  (пояснение: -d – запуск в фоновом режиме.
-p 3000:3000 – проброс порта (локальный порт 3000 на порт 3000 контейнера).
--name metabase – имя контейнера.
-e – переменные окружения для подключения к PostgreSQL:
MB_DB_TYPE=postgres – тип БД.
MB_DB_DBNAME=marketplace – имя базы.
MB_DB_PORT=5432 – порт PostgreSQL.
MB_DB_USER=analyst – пользователь БД.
MB_DB_PASS=strong_password – пароль.
MB_DB_HOST=host.docker.internal – специальный адрес для доступа из контейнера к вашему хосту (где работает PostgreSQL). )
- После проверим работает ли docker
- Пишем в командной строке docker ps – контейнер metabase должен быть в статусе Up.
- Если все хорошо в откройем браузер и перейдем по адресу http://localhost:3000. Увидим страницу настройки Metabase.

Выполним первоначальную настройку Metabase
- Создаем учётную запись администратора (имя, email, пароль).
- На шаге подключения к БД Metabase автоматически используем параметры из переменных окружения – просто нажимаем «Save».
- Если подключение не удаётся, проверем:
- Запущен ли PostgreSQL (служба postgresql-x64-16 в services.msc).
- В файле postgresql.conf должно быть listen_addresses = '*'.
- В pg_hba.conf добавлена строка host all all 0.0.0.0/0 md5.
- После изменений перезапустим PostgreSQL.
- Поменять Хост вместо host.docker.internal на ip, который можно увидеть если в командной строке набрать команду ipconfig.

Создаем Дашборды
- В Metabase создаем дашборд: «+ New» → «Dashboard»
- В Metabase нажимаем «Ask a question» → «Native query» (SQL).
- Вводим один из запросов из списка ниже (раздел «SQL-запросы для дашборда»).
-  Динамика выручки по дням (SQL:
SELECT purchase_date, SUM(total_price) AS revenue
FROM sales
GROUP BY purchase_date
ORDER BY purchase_date;
Визуализация: Линейный график (X – purchase_date, Y – revenue).
Название вопроса: «Выручка по дням» )
- Нажимаем «Run», убеждаемся, что данные отображаются, затем «Save».
- Повторяем для всех нужных метрик.
(Количество уникальных клиентов по дням
SQL:
SELECT purchase_date, COUNT(DISTINCT client_id) AS daily_clients
FROM sales
GROUP BY purchase_date
ORDER BY purchase_date;
Визуализация: Линейный график (X – purchase_date, Y – daily_clients).
Название: «Активные клиенты по дням»

Топ-10 товаров по выручке
SQL:
SELECT product_id, SUM(total_price) AS revenue
FROM sales
GROUP BY product_id
ORDER BY revenue DESC
LIMIT 10;
Визуализация: Столбчатая диаграмма (X – product_id, Y – revenue).
Название: «Топ-10 товаров по выручке»

Топ-10 товаров по количеству продаж
SQL:
SELECT product_id, SUM(quantity) AS total_quantity
FROM sales
GROUP BY product_id
ORDER BY total_quantity DESC
LIMIT 10;
Визуализация: Столбчатая диаграмма (X – product_id, Y – total_quantity).
Название: «Топ-10 товаров по количеству продаж»

Средний чек на клиента за последние 30 дней
SQL:
SELECT SUM(total_price) / COUNT(DISTINCT client_id) AS avg_check
FROM sales
WHERE purchase_date >= CURRENT_DATE - INTERVAL '30 days';
Визуализация: Скалярное значение (выберите «Number» в визуализациях).
Название: «Средний чек за 30 дней»

Распределение покупок по часам
SQL:
SELECT 
(purchase_time_seconds / 3600) AS hour,
COUNT(*) AS orders
FROM sales
GROUP BY hour
ORDER BY hour;
Визуализация: Столбчатая диаграмма (X – hour, Y – orders).
Название: «Активность по часам»

Соотношение полов клиентов
SQL:
SELECT gender, COUNT(DISTINCT client_id) AS cnt
FROM clients
GROUP BY gender;
Визуализация: Круговая диаграмма.
Название: «Половая структура клиентов»

Товары без продаж за последние 30 дней
SQL:
SELECT p.product_id
FROM products p
LEFT JOIN sales s ON p.product_id = s.product_id 
    AND s.purchase_date >= CURRENT_DATE - INTERVAL '30 days'
WHERE s.product_id IS NULL;
Визуализация: Таблица (можно оставить по умолчанию).
Название: «Товары без продаж (30 дней)» )
- Затем создаем дашборд: «+ New» → «Dashboard», добавляем все сохранённые вопросы.
- Сохраним дашбоард ввиде pdf файла.



Настройка ежедневной автоматической загрузки (Планировщик задач Windows)
Чтобы скрипт daily_etl.py запускался каждый день в 7:00 и загружал данные за предыдущий день, используйте встроенный Планировщик задач Windows.

Открыть Планировщик задач
- Нажимаем Win + R, вводим taskschd.msc и нажимаем Enter.

Создать задачу
- В правой панели выбераем «Создать задачу…» (не «Создать простую задачу» – это даст больше настроек).

Заполнить вкладку «Общие»
- Имя: Marketplace ETL Daily
- Описание: Загрузка данных за предыдущий день из API
- Выполнять независимо от того, зарегистрирован ли пользователь – поставьте галочку.
- С наивысшими привилегиями – поставьте галочку.
- Настроить для: выберите вашу операционную систему (например, Windows 10).

Настроить триггер (вкладка «Триггеры»)
- Нажмите «Создать…».
- Начать выполнение: Ежедневно.
- Время: 07:00 (или другое, удобное вам).
- Интервал: 1 день.
- Нажмите ОК.

Настроить действие (вкладка «Действия»)
- Нажмите «Создать…».
- Действие: Запуск программы.
- Программа/сценарий: укажите полный путь к python.exe внутри вашего виртуального окружения.
- Обычно он выглядит так: C:\Users\Linar\Desktop\marketplace_etl\venv\Scripts\python.exe
-  Добавить аргументы: daily_etl.py (только имя скрипта, без пути).
- Рабочая папка: укажите полный путь к корневой папке проекта, например: C:\Users\Linar\Desktop\marketplace_etl
- Нажмите ОК.

Настроить условия и параметры
- Вкладка «Условия»: снимите галочку «Запускать только при питании от сети», если хотите, чтобы задача выполнялась и на батарее.
- Вкладка «Параметры»:
- Отметьте «Разрешить выполнение по требованию».
- Установите «Если задание выполняется дольше, остановить» – например, 1 час.
- Остальное оставьте по умолчанию.

Проверка
- Щёлкните правой кнопкой по созданной задаче → Запустить.
- Дождитесь выполнения (около минуты).
- Проверьте логи в папке logs/ – там появится файл etl.log с записью о загрузке.
- Если ошибок нет – задача настроена корректно и будет выполняться каждый день в 7:00.

