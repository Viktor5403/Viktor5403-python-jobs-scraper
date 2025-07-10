import os
import sys
import re
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import argparse
import yaml

# Setup structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Load configuration from YAML file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yml")
with open(CONFIG_PATH, "r") as f:
    CONFIG = yaml.safe_load(f)

# Apply settings from CONFIG
try:
    URL = CONFIG["url"]
    HEADERS = CONFIG.get("headers", {})
    DEFAULT_KEYWORDS = CONFIG.get("keywords", [])
    DEFAULT_OUT = CONFIG.get("out", ".")
    DEFAULT_PREFIX = CONFIG.get("prefix", "jobs")
except KeyError as e:
    logger.error(f"Missing configuration key: {e}")
    raise

# Create resilient HTTP session with retries
def create_session(retries=3, backoff_factor=0.5, status_forcelist=None):
    session = requests.Session()
    status_forcelist = status_forcelist or [429, 500, 502, 503, 504]
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

SESSION = create_session()

# Command-line arguments parsing
def get_args():
    if any('ipykernel_launcher' in arg for arg in sys.argv):
        class Args: pass
        args = Args()
        args.keywords = DEFAULT_KEYWORDS
        args.out = DEFAULT_OUT
        args.prefix = DEFAULT_PREFIX
        args.format = 'csv'
        return args

    parser = argparse.ArgumentParser(
        description="RemoteOK job scraper: fetch, filter, save, and dedupe job listings."
    )
    parser.add_argument(
        "-k", "--keywords",
        nargs="+",
        default=DEFAULT_KEYWORDS,
        help=f"Keywords to filter positions (default: {DEFAULT_KEYWORDS})"
    )
    parser.add_argument(
        "-o", "--out",
        default=DEFAULT_OUT,
        help=f"Output directory (default: {DEFAULT_OUT})"
    )
    parser.add_argument(
        "-p", "--prefix",
        default=DEFAULT_PREFIX,
        help=f"Filename prefix (default: {DEFAULT_PREFIX})"
    )
    parser.add_argument(
        "--format",
        choices=["csv", "parquet", "json"],
        default="csv",
        help="Output file format: csv, parquet, or json"
    )
    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="Skip displaying the chart (useful for CLI/automation)"
    )
    args = parser.parse_args()
    return args

# Fetch raw JSON data
def fetch_data():
    logger.info(f"Fetching data from {URL}")
    response = SESSION.get(URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data[1:] if isinstance(data, list) and len(data) > 1 else []

# Parse data into DataFrame
def parse_data(jobs_list):
    df = pd.json_normalize(jobs_list)[["date", "company", "position", "location", "url"]]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df.dropna(subset=["date"])

# Filter DataFrame by keywords
def filter_data(df, keywords):
    pattern = re.compile("|".join(map(re.escape, keywords)), flags=re.IGNORECASE)
    mask = df["position"].str.contains(pattern, na=False)
    logger.info(f"Filtering data with keywords: {keywords}, matches found: {mask.sum()}")
    return df[mask].reset_index(drop=True)

# Save DataFrame in multiple formats
def save_data(df, out_dir, prefix, fmt="csv"):
    os.makedirs(out_dir, exist_ok=True)
    today = dt.date.today().strftime("%Y%m%d")
    filename = f"{prefix}_{today}.{fmt}"
    path = os.path.join(out_dir, filename)
    if fmt == "csv":
        df.to_csv(path, index=False)
    elif fmt == "parquet":
        df.to_parquet(path, index=False)
    else:
        df.to_json(path, orient="records", lines=True, date_format="iso")
    logger.info(f"Saved {len(df)} rows to {path}")
    return path

# Plot counts by date
def plot_date_counts(df, figsize=(10, 4), title="Jobs per Day"):
    if df.empty:
        logger.warning("No data to plot, skipping chart.")
        return
    counts = df["date"].dt.date.value_counts().sort_index()
    ax = counts.plot(kind="bar", figsize=figsize)
    ax.set_xlabel("Date")
    ax.set_ylabel("Count")
    ax.set_title(title)
    plt.tight_layout()
    plt.show()

# Main pipeline with dedupe and incremental refresh
def main():
    args = get_args()
    jobs_raw = fetch_data()
    df = parse_data(jobs_raw)
    filtered = filter_data(df, args.keywords)
    filtered = (
        filtered
        .drop_duplicates(subset="url", keep="first")
        .sort_values("date", ascending=False)
        .reset_index(drop=True)
    )
    master_path = os.path.join(args.out, f"{args.prefix}_master.csv")
    if os.path.exists(master_path):
        master_df = pd.read_csv(master_path)
        seen = set(master_df["url"])
    else:
        master_df = pd.DataFrame(columns=filtered.columns)
        seen = set()
    new_jobs = filtered[~filtered["url"].isin(seen)]
    if not new_jobs.empty:
        if master_df.empty:
            combined = new_jobs.copy()
        else:
            combined = pd.concat([master_df, new_jobs], ignore_index=True)
        combined.to_csv(master_path, index=False)
        logger.info(f"Appended {len(new_jobs)} new jobs; master total now {len(combined)}")
    else:
        logger.info("No new jobs to append.")
    save_data(filtered, args.out, args.prefix, fmt=args.format)
    plot_date_counts(filtered)

if __name__ == "__main__":
    main()
