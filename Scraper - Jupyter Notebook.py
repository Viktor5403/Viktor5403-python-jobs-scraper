# %%
pip install pandas requests ipykernel --quiet


# %%
import numpy
import pandas
print("NumPy:", numpy.__version__)
print("Pandas:", pandas.__version__)


# %%
from scraper import URL, HEADERS
print(URL, HEADERS)


# %%
import os
print("Working Directory:", os.getcwd())
print("Contents:", os.listdir())


# %%
import importlib, scraper
importlib.reload(scraper)              # force Python to re‑read scraper.py
print("Module contents:", [name for name in dir(scraper) if not name.startswith("_")])


# %%
from scraper import fetch_data, URL, HEADERS

# Fetch and inspect
jobs = fetch_data(URL, HEADERS)
print(f"✅ Fetched {len(jobs)} postings, first item type:", type(jobs[0]))
# Optionally peek at the first dict
from pprint import pprint
pprint(jobs[0])

# %%
import importlib, scraper
importlib.reload(scraper)

from scraper import fetch_data, parse_data, URL, HEADERS

# %%
# Fetch raw data
jobs_raw = fetch_data(URL, HEADERS)

# Parse into DataFrame
df = parse_data(jobs_raw)

# Inspect results
print(f"✅ Parsed into DataFrame with {len(df)} rows.")
df.head()


# %%
import importlib
import scraper
importlib.reload(scraper)
from scraper import fetch_data, parse_data, filter_data, URL, HEADERS

# %%
# Full pipeline test
raw = fetch_data(URL, HEADERS)
df = parse_data(raw)
filtered = filter_data(df, ["Power BI", "Python"])

print(f"✅ After filtering: {len(filtered)} rows remain.")
filtered.head()

# %%
import importlib
import scraper
importlib.reload(scraper)
from scraper import save_data, fetch_data, parse_data, filter_data, URL, HEADERS

# %%
# Run full pipeline
raw = fetch_data(URL, HEADERS)
df = parse_data(raw)
filtered = filter_data(df, ["Power BI", "Python"])

# Save to CSV
csv_path = save_data(filtered, out_dir=".")
print(f"✅ Data saved to: {csv_path}")

# Verify file exists
import os
print("Exists:", os.path.exists(csv_path))

# %%
import sys
print("Python executable:", sys.executable)


# %%
import importlib, scraper
importlib.reload(scraper)
print("URL:", scraper.URL)
print("HEADERS:", scraper.HEADERS)
print("Available funcs:", [f for f in dir(scraper) if not f.startswith("_")])


# %%
import importlib, scraper
importlib.reload(scraper)

from scraper import (
    fetch_data,
    parse_data,
    filter_data,
    save_data,
    plot_date_counts,
    URL,
    HEADERS,
)


# %%
# 1️⃣ Fetch raw data
jobs_raw = fetch_data(URL, HEADERS)

# 2️⃣ Parse into DataFrame
df = parse_data(jobs_raw)

# 3️⃣ Filter for Power BI & Python roles
filtered = filter_data(df, ["Power BI", "Python"])

# 4️⃣ Save to CSV
csv_path = save_data(filtered, out_dir=".")
print(f"✅ Saved filtered data ({len(filtered)} rows) to: {csv_path}")

# 5️⃣ Plot counts by date
plot_date_counts(filtered)


# %%
import importlib, scraper
importlib.reload(scraper)
from scraper import fetch_data, URL, HEADERS, SESSION

# Quick check that SESSION is a requests.Session with retry logic
print("Session mounts:", SESSION.adapters.keys())

# Test fetch_data still works
jobs = fetch_data(URL, HEADERS)
print(f"✅ fetch_data via SESSION returned {len(jobs)} postings")

# %%
import os
print([f for f in os.listdir() if f.endswith((".yml",".yaml"))])


# %%
import importlib, scraper
importlib.reload(scraper)

# Check that config values loaded
print("URL:", scraper.URL)
print("HEADERS:", scraper.HEADERS)
print("Default keywords:", scraper.DEFAULT_KEYWORDS)
print("Default out/prefix:", scraper.DEFAULT_OUT, scraper.DEFAULT_PREFIX)

# %%
import importlib, scraper
importlib.reload(scraper)
scraper.main()

# %%
import importlib, scraper
importlib.reload(scraper)

# Run the pipeline to see structured logs
scraper.main()


# %%
import importlib, scraper
importlib.reload(scraper)
scraper.main()

# %%
import importlib
import remoteok_scraper.scraper as mod
importlib.reload(mod)
mod.main()

# %%
import importlib
from remoteok_scraper import scraper

# Reload to pick up your latest scraper.py
importlib.reload(scraper)

# 1️⃣ Fetch & filter (override keywords here as desired)
jobs_raw = scraper.fetch_data()
df = scraper.parse_data(jobs_raw)
filtered = scraper.filter_data(df, ["Python", "Data", "Engineer", "SQL", "JavaScript", "AWS", "Docker"])


# %%
# 2️⃣ Detailed Tabular Column
from IPython.display import display
display(filtered)

# 3️⃣ Bar Graph: Job Title vs. Number of Openings
import matplotlib.pyplot as plt

# Count how many times each position appears
counts = filtered["position"].value_counts()

# %%
import matplotlib.pyplot as plt


# %%
import importlib
import remoteok_scraper.scraper as scraper
importlib.reload(scraper)

# 1️⃣ Fetch raw data
jobs_raw = scraper.fetch_data()

# 2️⃣ Parse into DataFrame
df = scraper.parse_data(jobs_raw)

# 3️⃣ Filter with your broad keyword list
keywords = ["Python", "Data", "Engineer", "SQL", "JavaScript", "AWS", "Docker"]
filtered = scraper.filter_data(df, keywords)


# %%
from IPython.display import display
display(filtered)


# %%
import matplotlib.pyplot as plt

counts = filtered["position"].value_counts()

plt.figure(figsize=(12, 6))
plt.bar(counts.index, counts.values)
plt.xlabel("Job Title")
plt.ylabel("Number of Openings")
plt.title("Open Positions by Job Title")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()



