# Аналитический дашборд для маркетплейса
Описание проекта
Проект реализует полный цикл автоматизированного сбора данных по API, их загрузку в БД PostgreSQL и визуализацию ключевых метрик через Metabase (локальный дашборд).
Цель - обеспечить стабильный поток данных для аналитики клиентской активности, продаж и ассортиментной матрицы.

marketplace-analytics/
├── README.md                           # документация проекта
├── requirements.txt                    # зависимости ETL-скриптов
│
├── etl/                                # ETL-скрипты
│   ├── __init__.py
│   ├── config.py                       # конфигурация подключения к БД и API
│   ├── db_utils.py                     # работа с PostgreSQL (upsert, батчи)
│   ├── fetch_data.py                   # сбор данных из API
│   ├── daily_etl.py                    # ежедневный сбор данных за предыдущий день
│   └── backfill.py                     # единоразовая загрузка исторических данных (2023 год)
│   └── requirements.txt                # зависимости
│
├── analysis/                           # аналитические скрипты
│   ├── __init__.py
│   ├── assortment_analysis.py          # ABC и BCG анализ, рекомендации по ассортименту
│   ├── client_analysis.py              # RFM-сегментация, когортный LTV
│
├── sql/
│   └── schema.sql                      # SQL-запросы для создания таблиц и ограничений
│
├── reports/                            # сгенерированные отчёты
│   ├── abc_analysis.png                # график ABC-анализа
│   ├── bcg_matrix.csv                  # матрица BCG
│   ├── ltv_cohorts.png                 # когортный анализ LTV
│   ├── products_to_drop.csv            # список товаров для вывода
│   ├── rfm_segments.csv                # распределение клиентов по RFM-сегментам
│   └── ltv_cohorts_correct.png         # когортный анализ LTV
│   └── LTV.jpg                         # когортный анализ LTV
│   └── Metabase - Аналитика продаж.pdf # Metabase - Аналитика продаж
│   └── Выручка по группам ABC.jpg      # Выручка по группам ABC
│   └── Распределение товаров по группам ABC (по количеству).jpg         # Распределение товаров по группам ABC (по количеству)
│
├── docs/                               # финальные отчёты
│   ├── Оптимизация ассортиментной матрицы.pptx     # презентация по ассортименту
│   └── Работа с клиентской базой (увеличение LTV).pptx        # презентация по клиентам
│
└── logs/
    └── .gitkeep                        # папка для логов (содержимое не хранится в Git)
    └── etl.log                         # папка для логов 

Доступ к БД
Параметр	Значение
Тип	PostgreSQL
IP	localhost (локальная установка)
Порт	5432
База	marketplace
Пользователь	analyst
Пароль	strong_password
Права	SELECT, INSERT, UPDATE (полный доступ для ETL-скриптов)
Доступ к Metabase
Параметр	Значение
URL	http://localhost:3000 (локально)
Тип	Metabase (запуск через Docker)
Подключение к БД	PostgreSQL (автоматически через переменные окружения)
Дашборд	"Marketplace Analytics" (8 ключевых метрик)

Автоматизация
Ежедневная загрузка данных
На Windows настроена задача через Планировщик задач:
Время запуска: ежедневно в 7:00 (МСК)
Действие: запуск daily_etl.py через виртуальное окружение
Логика: скрипт загружает данные за предыдущий день и записывает их в PostgreSQL

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


MB_DB_TYPE=postgres – тип БД.
MB_DB_DBNAME=marketplace – имя базы.
MB_DB_PORT=5432 – порт PostgreSQL.
MB_DB_USER=analyst – пользователь БД.
MB_DB_PASS=strong_password – пароль.
MB_DB_HOST=host.docker.internal – специальный адрес для доступа из контейнера к вашему хосту (где работает PostgreSQL). )



