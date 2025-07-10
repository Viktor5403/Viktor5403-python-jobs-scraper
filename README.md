# Python Jobs Scraper

A CLI tool and Jupyter notebook for scraping, filtering, deduplicating, and exporting job listings from [RemoteOK](https://remoteok.com). This package enables you to automate the collection of remote tech‑job data, transform it into a structured format, and visualize key metrics—all with a few simple commands or notebook cells.

---

## Table of Contents

1. [Features](#features)
2. [Getting Started](#getting-started)

   * [Prerequisites](#prerequisites)
   * [Installation](#installation)
3. [Usage](#usage)

   * [Command‑Line Interface (CLI)](#command-line-interface-cli)
   * [Jupyter Notebook](#jupyter-notebook)
4. [Configuration](#configuration)
5. [Project Structure](#project-structure)
6. [Extending & Customizing](#extending--customizing)
7. [License](#license)

---

## Features

* **Fetch** live postings from RemoteOK’s public JSON API
* **Filter** roles by keyword list (e.g., Python, Data, SQL)
* **Deduplicate** entries based on job URL, appending new listings to a master file
* **Export** results in CSV, Parquet, or JSON formats
* **Visualize** posting trends over time via bar charts
* **CLI entry point**: `scrape-jobs` script for automated runs or cron jobs
* **Notebook**: interactive exploration with pandas & matplotlib

---

## Getting Started

### Prerequisites

Ensure you have:

* Python 3.8 or higher
* `pip` package manager
* (Optional) A virtual environment tool like `venv`

### Installation

1. **Clone** the repository:

   ```bash
   git clone https://github.com/<your-username>/python-jobs-scraper.git
   cd python-jobs-scraper
   ```

2. **Create and activate** a virtual environment:

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install** dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. **Install** the package in editable mode:

   ```bash
   pip install -e .
   ```

Now you have access to the `scrape-jobs` console script.

---

## Usage

### Command-Line Interface (CLI)

Fetch, filter, and export in one step:

```bash
# Basic run with defaults:
# keywords = [Power BI, Python], format = csv
scrape-jobs

# Custom keywords, JSON output, no plot:
scrape-jobs \
  --keywords Python Data SQL JavaScript AWS Docker \
  --format json \
  --out data \
  --prefix all_jobs \
  --no-plot
```

**Arguments:**

* `-k`, `--keywords`: List of keywords to filter positions by.
* `-o`, `--out`: Output directory for result files.
* `-p`, `--prefix`: Filename prefix (appended with date).
* `--format`: `csv`, `parquet`, or `json`.
* `--no-plot`: Skip chart display (useful for automated runs).

Results:

* `all_jobs_YYYYMMDD.csv`
* `all_jobs_master.csv` (accumulates all previous runs)

### Jupyter Notebook

Open `scraper.ipynb` in Jupyter or VS Code. Key cells:

1. **Fetch & parse** data:

   ```python
   from scraper import fetch_data, parse_data
   jobs_raw = fetch_data()
   df = parse_data(jobs_raw)
   ```

2. **Filter**:

   ```python
   from scraper import filter_data
   keywords = ["Python", "Data", "SQL"]
   filtered = filter_data(df, keywords)
   filtered.head()
   ```

3. **Visualize**:

   ```python
   import matplotlib.pyplot as plt
   counts = filtered['position'].value_counts()
   plt.figure(figsize=(10,4))
   counts.plot(kind='bar')
   plt.title('Open Positions by Title')
   plt.show()
   ```

4. **Save** to CSV:

   ```python
   from scraper import save_data
   save_data(filtered, out_dir='data', prefix='filtered_jobs', fmt='csv')
   ```

---

## Configuration

Edit `config.yml` to customize defaults:

```yaml
# config.yml
url: https://remoteok.com/api
headers:
  User-Agent: Mozilla/5.0 (compatible; YourNameBot/1.0)
keywords:
  - Power BI
  - Python
out: data
prefix: jobs
```

* **`url`**: API endpoint
* **`headers`**: HTTP headers for requests
* **`keywords`**: Default keyword filters
* **`out`**: Default output folder
* **`prefix`**: Default file name prefix

---

## Project Structure

```
python-jobs-scraper/
├── LICENSE
├── README.md
├── config.yml
├── pyproject.toml
├── setup.py
├── requirements.txt
├── scraper.ipynb
├── remoteok_scraper/
│   ├── __init__.py
│   └── scraper.py
└── data/  # output folder created at runtime
```

---

## Extending & Customizing

* **Add fields**: modify `parse_data` to include additional JSON keys (e.g., `salary`).
* **Advanced filters**: extend `filter_data` to filter by tags, date ranges, or location.
* **Scheduling**: wrap `scrape-jobs` in a cron or Windows Task Scheduler job for daily updates.
* **Web dashboard**: integrate the CSV/Parquet into a BI tool or build a Streamlit app.

---

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use and adapt!

---

*Happy scraping!*
