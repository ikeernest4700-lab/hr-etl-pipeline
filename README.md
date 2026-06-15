# hr-etl-pipeline
Automated ETL pipeline built in Python — extracts, cleans and loads 20,000 HR records into PostgreSQL using Pandas, NumPy &amp; SQLAlchemy. Fully logged.
![Python](https://img.shields.io/badge/Python-3.x-blue) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-316192) ![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)

---

## 🗂️ Dataset
5 columns — `name`, `age`, `country`, `salary`, `job` — across 20,000 synthetic HR employee records.

<!-- 📸 INSERT IMAGE: Screenshot of raw messy dataset (df.head() or CSV preview) -->
![Raw Data](images/raw_data.png)

---

## ⚙️ Tech Stack
`Python` • `Pandas` • `NumPy` • `SQLAlchemy` • `PostgreSQL` • `Logging` • `Jupyter Notebook`

---

## 🔁 Pipeline

### 📥 Extract
Loaded raw CSV into a Pandas DataFrame. Logger confirmed: `20,000 rows and 5 columns extracted`.

### 🔎 Inspect
Profiled every column before touching a single value:

| Issue Found | Count |
|-------------|-------|
| Duplicate rows | 751 |
| Null values in `age` | 1,387 |
| Negative values in `age` | 264 |
| Null values in `salary` | 1,535 |
| String inconsistencies | Multiple |

<!-- 📸 INSERT IMAGE: df.info() output / logger terminal screenshot -->
![Logger Output](images/logger_output.png)

### 🧹 Clean

| Problem | Fix | Why |
|---------|-----|-----|
| 751 duplicates | `drop_duplicates()` | Exact copies add no value |
| 1,387 null ages | Imputed with median | Dropping = losing 7%+ of data |
| 264 negative ages | Replaced with valid values | A person can't be -7 years old |
| 1,535 null salaries | Imputed with median | Preserves statistical integrity |
| String columns | Stripped & standardised | PostgreSQL compatibility |
| Numeric fields | Rounded to 2dp via `np.issubdtype` | Precision & consistency |

<!-- 📸 INSERT IMAGE: Before/after comparison of cleaned DataFrame -->
![Cleaned Data](images/cleaned_data.png)

### 📤 Load
Connected to PostgreSQL via SQLAlchemy. Schema defined programmatically. Clean DataFrame pushed with `df.to_sql()` — no manual imports.

<!-- 📸 INSERT IMAGE: PostgreSQL table showing loaded clean data -->
![PostgreSQL Table](images/postgres_loaded.png)

---

## 📊 Results

| Metric | Value |
|--------|-------|
| Raw rows | 20,000 |
| Clean rows | **19,249** |
| Data retained | **96.2%** |
| Execution time | < 1 second |

---

## 🚀 Run It

```bash
# 1. Clone
git clone https://github.com/your-username/hr-etl-pipeline.git

# 2. Install
pip install pandas numpy sqlalchemy psycopg2-binary jupyter

# 3. Configure DB connection in notebook
engine = create_engine('postgresql://username:password@localhost:5432/your_db')

# 4. Run
jupyter notebook ETL_script.ipynb
```

---

## 🔮 What's Next
**Project 2:** REST API extraction → PostgreSQL → Power BI dashboard

---

## 🤝 Connect
**Emeka Ike** — Data Analyst & Engineer
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/emeka-ike-108748198)

---
*Built with Python • PostgreSQL • Pandas • SQLAlchemy*
