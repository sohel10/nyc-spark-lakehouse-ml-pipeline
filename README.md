# 🚕 NYC Spark Lakehouse & ML Pipeline

Production-style distributed data engineering pipeline built with PySpark, simulating real-world multi-year big data ingestion, schema evolution management, and ML-ready dataset preparation using NYC Yellow Taxi data.

This project demonstrates distributed data processing, schema harmonization, partition optimization, and ML-ready dataset construction using Spark.

---

## 🧰 Tech Stack

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![PySpark](https://img.shields.io/badge/PySpark-Distributed%20Processing-orange)](https://spark.apache.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.x-E25A1C)](https://spark.apache.org/)
[![Parquet](https://img.shields.io/badge/Storage-Parquet-4B8BBE)](https://parquet.apache.org/)
[![Lakehouse](https://img.shields.io/badge/Architecture-Lakehouse-blue)]()
[![Distributed Systems](https://img.shields.io/badge/Concept-Distributed%20Systems-lightgrey)]()
[![Ubuntu](https://img.shields.io/badge/OS-Ubuntu-FCC624)](https://ubuntu.com/)
[![Git](https://img.shields.io/badge/Version%20Control-Git-F05032)](https://git-scm.com/)

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

## 🏗 Architecture Overview

This project implements a production-style lakehouse architecture for scalable multi-year data ingestion and analytical dataset preparation.

## ⚙ Example Execution

Below shows a diagran ingestion and merge process executed with PySpark:

<p align="center">
  <img src="docs/figures/pipeline.png" width="600"/>
</p>


Each layer isolates responsibilities:
- Raw ingestion
- Schema harmonization
- Partition optimization
- Analytical dataset construction

## 📊 Dataset Scale

The pipeline processes large-scale NYC Yellow Taxi trip data:

- **17,089,605 records** ingested and harmonized
- Year-level standardized parquet dataset
- Optimized across **72 Spark partitions**
- Partition-aware dataset design for distributed execution
- Structured for scalable analytical and ML-ready workflows

## ⚙ Example Execution

Below shows a successful yearly ingestion and merge process executed with PySpark:

![Spark Execution](docs/figures/spark.png)

## ⚡ Performance Considerations

To ensure scalability across multi-year data:

- Avoided full-year in-memory unions
- Streamed ingestion at month-level
- Used controlled `repartition()` strategy
- Designed partitioned write layer for pruning
- Prevented small-file explosion problem
- Minimized Spark shuffle operations
---

## 🔄 Schema Evolution Handling

NYC taxi parquet schemas evolve across years.

Key solutions implemented:

- Used `unionByName(allowMissingColumns=True)`
- Standardized numeric casting across years
- Resolved physical/logical parquet type mismatches
- Explicit column alignment before union

## 📂 Project Structure
```` text
nyc-spark-lakehouse-ml-pipeline/
│
├── jobs/              # Spark job orchestration scripts
├── src/               # Core transformations & schema logic
├── data_raw/          # Raw monthly parquet files (ignored)
├── data_clean_tmp/    # Memory-safe ingestion layer
├── data_clean/        # Harmonized yearly datasets
├── data_processed/    # Partitioned analytical dataset
├── docs/              # Architecture & execution images
├── requirements.txt
├── environment.yml
└── README.md

````

## 🎯 What This Project Demonstrates

- Distributed data engineering workflows
- Handling large-scale multi-year datasets
- Schema drift resolution
- Spark memory management strategies
- Partition-aware dataset design
- Lakehouse architectural layering
- Production-style pipeline structuring



## 📊 ML-Ready Dataset

The final `data_processed/` layer is partitioned by:

year=YYYY/
month=MM/


This enables:

- Efficient distributed training
- Partition pruning
- Faster analytical queries
- Scalable model experimentation



## 🚀 How to Run


```bash
python -m jobs.clean_year_tmp

📜 License

MIT License


