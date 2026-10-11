# AI Research Explorer: Scientometric Analysis Toolkit

A modular framework for automated bibliographic data collection and longitudinal trend analysis of research literature, specifically targeting the intersection of Artificial Intelligence and mental health research.

## 🚀 Project Overview
This repository provides a rigorous pipeline to transform raw bibliographic metadata into structured scientometric insights. Moving beyond basic data collection, the toolkit combines API-driven data ingestion (`main.py`) with an advanced analytical engine (`analytics.py`) to map publication trends, citation impacts, and methodological shifts over time.

## 🛠️ Key Features
- **Automated Data Ingestion:** Interfaces with academic research APIs (OpenAlex) to retrieve structured bibliographic records.
- **Vectorized Analytical Engine:** Utilizes Pandas for efficient, high-performance statistical summaries and longitudinal trend analysis.
- **Robust Information Extraction:** Implements high-precision Regex pattern matching to extract methodologies, datasets, and metrics from research abstracts.
- **Defensive Engineering:** Handles missing values (`NaN`), malformed schemas, and dirty data gracefully to ensure uninterrupted execution.

## 📂 Repository Structure
```text
├── main.py            # Data ingestion and API orchestration pipeline
├── analytics.py       # Scientometric analytical and extraction engine
├── requirements.txt   # Project dependencies
├── output/            # Schema-validated JSON reports and data outputs
└── .gitignore         # Version control exclusion rules

## ⚙️ Tech Stack
Language: Python 3.x
Data Processing: Pandas (Vectorized statistical analysis)
API Integration: Requests (RESTful bibliographic retrieval)
Pattern Extraction: Regular Expressions (Regex)

## How to Run

1. Install dependencies:
```bash
   pip install -r requirements.txt
```
2. Run the application
```bash
   python main.py
```
2. Execute the scientometric analysis:
```bash
      python analytics.py
```


