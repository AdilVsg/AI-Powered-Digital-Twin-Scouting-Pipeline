# TwinScout: An AI-Powered Digital Twin Scouting Pipeline

![Author](https://img.shields.io/badge/Author-Adil%20CHOUKAIRE-blue)

![Python](https://img.shields.io/badge/Python-3.14.2-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0.0-EE4C2C)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991)

A technology scouting pipeline for the automated identification and classification of GitHub repositories to isolate true Level 3 Digital Twin projects.

## 📁 Project Structure
```bash
TwinScout/
├── data/
├── 📁 src/
│   ├── config.py
│   ├── github_scraper.py
│   ├── rdm_analyser.py
│   └── rdm_keywords.py
├── main.py
├── requirements.txt
└── README.md
```


## 🛠️ Scripts Description

### `main.py`

The orchestration script for the data collection phase. It integrates keyword generation and the GitHub scraper to execute a mass mining operation. It manages API rate limits, prevents duplicate entries, and incrementally saves the scraped repository metadata and README contents into a fault-tolerant JSONL database.

### `src/config.py`

Contains the core parameters and semantic definitions driving the classification engine:
- A detailed taxonomy of Digital Representation levels:
    - Level 1: Digital Model (Manual data flow) 
    - Level 2: Digital Shadow (Automated one-way data flow) 
    - Level 3: Digital Twin (Automated bidirectional data flow) 
- System instructions and absolute rules for the binary LLM classifier.
- Language model configuration (e.g., TinyLlama) and automatic hardware/device mapping logic (CPU/GPU).

### `src/github_scraper.py`

A custom scraping module designed to interface with the GitHub REST API.
  - Utilizes Personal Access Tokens for authenticated requests, significantly increasing the hourly rate      limit.
  - Extracts repository metadata (ID, name, URL, description) and the raw text of the `README.md` file.

### `src/rdm_keywords.py`

Script designed to broaden the search scope through terminology expansion.
  - Uses an LLM API (Groq/OpenAI) to expand base concepts into a targeted list of domain-specific technical queries.
  - Generates precise keywords focusing on industrial protocols and frameworks (e.g., OPC UA, Eclipse Ditto, FMI Standard).

### `src/rdm_analyser.py`

The primary semantic classification and filtering script.
  - Loads the local LLM specified in `config.py` into GPU memory.
  - Implements a two-stage filtering strategy:
     - Stage 1: A deterministic Python filter utilizing string matching to drop obvious false positives (e.g., tutorials, general libraries).
     - Stage 2: An LLM-based semantic classification of the truncated README text.
  - Evaluates the repository to determine if it meets the strict criteria of a Level 3 Digital Twin, outputting the final validated dataset to a CSV file.

## 🎯 Objective

The objective of this project is to automate the extraction and filtering of GitHub repositories to isolate projects that strictly adhere to the definition of a Level 3 Digital Twin. This requires demonstrating an automated bidirectional data and control flow between a physical object and its virtual counterpart.

## ⚠️ Notes

- This pipeline relies on the semantic analysis of repository README files; repositories lacking comprehensive documentation may be bypassed
- Running the `rdm_analyser.py` script requires adequate hardware acceleration (NVIDIA GPU recommended) for optimal inference times.
- API tokens (GitHub and Groq/OpenAI) must be configured as environment variables or injected into the scripts prior to execution.
