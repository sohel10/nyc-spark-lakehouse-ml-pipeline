# 🚕 NYC Spark Lakehouse & ML Pipeline

Scalable PySpark-based data engineering and machine learning pipeline built on multi-year NYC Yellow Taxi trip data.

This project demonstrates distributed data processing, schema harmonization, partition optimization, and ML-ready dataset construction using Spark.

---

## 📌 Project Overview

NYC Yellow Taxi data is published in monthly parquet files across multiple years.  
Although already in parquet format, the schema evolves over time and requires harmonization for large-scale analytical processing.

This project implements a **production-style lakehouse architecture**:

- Handles schema drift across years
- Resolves datatype inconsistencies
- Avoids Spark memory crashes during ingestion
- Controls partitioning to optimize file sizes
- Builds a partitioned analytical dataset for ML workloads

---

## 🏗️ Architecture

data_raw/ → Original monthly parquet files
data_clean_tmp/ → Memory-safe ingestion layer (streaming month-level processing)
data_clean/ → Standardized yearly datasets
data_processed/ → Partitioned analytical dataset (year/month)
models/ → ML training & artifacts


---

## 🔧 Engineering Highlights

### ✅ Schema Harmonization
- Used `unionByName(allowMissingColumns=True)` to handle evolving schemas
- Resolved parquet physical/logical type mismatches
- Standardized numeric casting across years

### ✅ Memory-Safe Processing
- Streamed ingestion at month-level to prevent `Java heap space` crashes
- Avoided full-year in-memory unions
- Used controlled `repartition` strategy for scalable writes

### ✅ Partition Optimization
- Balanced file size and distributed performance
- Prevented small-file problem
- Designed partitioned analytical layer for partition pruning

### ✅ Lakehouse Design
- Raw → Clean → Processed layering
- ML-ready dataset construction
- Separation of ingestion and modeling concerns

---

## ⚡ Technology Stack

- **PySpark**
- **Parquet**
- **Distributed Data Processing**
- **Lakehouse Architecture**
- **Partition Optimization**
- **Feature Engineering**

---

## 📊 ML-Ready Dataset

The final `data_processed/` layer is partitioned by:

year=YYYY/
month=MM/


This enables:

- Efficient distributed training
- Partition pruning
- Faster analytical queries
- Scalable model experimentation

---

## 🚀 How to Run


This enables:

- Efficient distributed training
- Partition pruning
- Faster analytical queries
- Scalable model experimentation

---

## 🚀 How to Run


This enables:

- Efficient distributed training
- Partition pruning
- Faster analytical queries
- Scalable model experimentation

---

## 🚀 How to Run

### 1️⃣ Clean Monthly Data (Memory-Safe)
```bash
python -m jobs.clean_year_tmp

📜 License

MIT License
---

# 🔥 This README Signals

✔ Data engineering maturity  
✔ Distributed systems understanding  
✔ ML pipeline readiness  
✔ Production architecture thinking  

---

If you'd like, next I can:

- Add an architecture diagram (visual style)
- Add performance benchmarking section
- Add ML model training section
- Optimize for recruiter keywords
- Create a professional GitHub profile summary

Tell me which direction you want next 🚀