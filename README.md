# 📊 Econ ELT (DuckDB + dbt Toy Project)

## Overview

This project is a **toy ELT pipeline** for processing and modeling macroeconomic time series data derived from the dataset originally referenced in the *flyleaf of the Russian edition of Brue & McConnell (Economics textbook)*.

It is designed for **educational and experimental purposes only**, focusing on:

* Lightweight ELT architecture using **DuckDB**
* Transformation workflows using **dbt**
* Config-driven modeling of economic relationships
* Simple econometric-style curve fitting (power laws, bounded interpolation, scaling laws)

The project is intentionally simplified and **not production-grade infrastructure**.

---

## ⚠️ Disclaimer

This repository is a **learning and experimentation sandbox**.

* It is not intended for financial forecasting or economic decision-making.
* Models are stylized mathematical approximations, not validated econometric models.
* Data transformations are simplified representations of textbook-style macroeconomic relationships.

---

## 🧱 Architecture

The pipeline follows a simple ELT structure:

### 1. Ingestion (Python)

* Reads raw `.parquet` files
* Loads them into a DuckDB database (`raw` schema)

### 2. Transformation (dbt)

* `raw` → `interim` → `marts`
* All transformations executed in SQL
* Models defined using reusable macros

### 3. Output (DuckDB)

* Final analytical tables stored in `marts` schema
* Includes model estimates and error metrics (MSD / RMSD)

---

## 📁 Project Structure

```text
econ-elt/
├── config/              # Pipeline configuration (models + parameters)
├── ingestion/           # Raw data ingestion into DuckDB
├── dbt/                 # dbt project (models, macros, marts)
├── data/
│   ├── raw/             # Input parquet files
│   └── processed/       # DuckDB database
├── README.md
└── pyproject.toml
```

---

## ⚙️ Setup

### 1. Create environment

```bash
uv venv --python 3.12
```

---

### 2. Install dependencies

```bash
uv pip install duckdb dbt-core dbt-duckdb pyyaml
```

---

## 🚀 Running the Pipeline

### 1. Load raw data into DuckDB

```bash
uv run python -m ingestion.load_raw
```

This will:

* Create schema `raw`
* Load all parquet files from `data/raw/`
* Register tables inside DuckDB database

---

### 2. Run dbt transformations

```bash
uv run dbt run --project-dir dbt --profiles-dir dbt
```

This will build:

* `raw` → staging models
* `interim` → model computations
* `marts` → final aggregated outputs

---

## 📊 Models Included

The project includes simplified macroeconomic models:

* **GDP growth model**

  * Power-law time growth approximation

* **Income model**

  * Bounded nonlinear interpolation over interest rates

* **Investment model**

  * Inverse power scaling with respect to interest rates

Each model produces:

* Estimated values
* Squared error
* Aggregate error metrics (MSD, RMSD)

---

## 📐 Metrics

Each model is evaluated using:

* **MSD**: Mean Squared Deviation
* **RMSD**: Root Mean Squared Deviation

These are implemented via reusable dbt macros.

---

## 🧪 Design Philosophy

This project intentionally prioritizes:

* Simplicity over performance
* Transparency over abstraction
* SQL readability over framework complexity
* Config-driven modeling over hardcoded logic

---

## 📦 Future Ideas (optional experiments)

* Fully config-compiled dbt models
* Automatic model generation from YAML
* Parameter validation layer
* Incremental models in dbt
* Model versioning / experiment tracking

---

## 📚 Origin

This project is inspired by structured datasets referenced in:

> *Flyleaf dataset associated with the Russian edition of Brue & McConnell: Economics*

It is reconstructed for experimentation and does not represent the original dataset in full fidelity.

---

## 🧑‍🔬 Author Note

This is a **personal research/learning sandbox** exploring:

* ELT architecture patterns
* Declarative data modeling
* Lightweight analytics engineering with DuckDB

---
