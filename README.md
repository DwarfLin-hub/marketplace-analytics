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
    
    - Added presentation slides (PPTX and PDF)
    - Compiled analysis results into reports/
    - Updated README with project overview, setup, and access details
    - Final commit before submission
