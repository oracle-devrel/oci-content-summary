# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Automatically scrapes trending GitHub repositories daily and generates AI-powered summaries using OCI Generative AI Service. For content creators and marketing teams.

**Tech Stack:** Python 3.10, Scrapy, OCI GenAI Service (Cohere/Llama), Oracle Autonomous Database, OCI SDK

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Automatic (all components)
chmod a+x run.sh
./run.sh

# Manual step-by-step
scrapy runspider trending_spider.py  # Fetch trending repos
scrapy runspider info_spider.py      # Extract README files
python main.py                       # Summarize with LLM
```

## Architecture

```
GitHub Trending Page
    ↓
Scrapy Spider (trending_spider.py)
    ↓
Repository URLs
    ↓
Scrapy Spider (info_spider.py)
    ↓
README.md Extraction
    ↓
Text Preprocessing (normalization, HTML removal, token limiting)
    ↓
OCI Generative AI Service
    ├─ Cohere Command-R
    └─ Llama 3.1
    ↓
Summary Generation
    ↓
Oracle Database (persistence)
    ↓
Output Files (output_*.txt)
```

## Important Patterns

### Web Scraping Pipeline
- **trending_spider.py**: Fetches trending repository URLs
- **info_spider.py**: Extracts README content from each repo
- Sequential processing with intermediate file storage

### Text Preprocessing
- ASCII encoding normalization
- HTML tag removal
- Token limiting (~10K tokens)
- Special character handling

### LLM Model Selection
- Flexible model switching (Cohere Command-R, Llama 3.1)
- Hyperparameters: Temperature 1.0, Top-p 0.75, Frequency penalty 0.0
- Configurable via main.py

### Database Integration
- Persistent storage in Oracle Autonomous Database
- File path tracking
- Summary metadata storage

### Scheduled Execution
- Designed for daily cron jobs
- Automated trending content capture

## Key Files

- `main.py` - LLM summarization orchestrator
- `db_handler.py` - Oracle DB operations
- `trending_spider.py` - GitHub trending scraper
- `info_spider.py` - README extraction
- `info_grabber.py` - Alternative repository info fetcher
- `readme_reader.py` - README file reader/parser
- `summarize_from_file.py` - Summarize from local file input (offline mode)
- `summarize_llm.py` - LLM summarization utilities
- `run.sh` - Automated execution script
- `output_*.txt` - Generated summaries

## Configuration

- `config.yaml` - Active configuration (OCI credentials, model settings, DB connection)
- `config_example.yaml` - Example configuration template (copy to `config.yaml` and fill in values)

## Output

- `outputs/` - Directory containing generated summary output files
