\
# Olympics Data Analysis (Streamlit Web App)

An interactive **Streamlit** dashboard for exploring **120 years of Olympic history** using the Kaggle “Athlete Events” dataset. The app lets you analyze medals, participation trends, country performance, and athlete demographics.

- Dataset (Kaggle): https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results

## Features

The app is organized into four sections (see the left sidebar in the UI):

- **Medal Tally**: medals by year and/or country, including totals.
- **Overall Analysis**: editions, hosts, sports, events, nations, athletes + trends over time.
- **Country-wise Analysis**: medal trend line, sport heatmap, top athletes for a selected country.
- **Athlete-wise Analysis**: age distributions, height vs weight (by sport), and men vs women participation.

## Tech Stack

- **Python**
- **Streamlit** (UI)
- **Pandas** (data processing)
- **Plotly / Matplotlib / Seaborn** (visualizations)

## Project Structure

Key files:

- `app.py` – Streamlit entrypoint.
- `preprocessor.py` – cleans/merges the raw datasets for analysis.
- `Helper.py` – helper functions used by the app (medal tally, trends, charts).
- `athlete_events.csv`, `noc_regions.csv` – raw data files expected by `app.py`.

There is also a `Data/` folder containing copies of the datasets.

## Data Files (Important)

By default, `app.py` reads:

- `athlete_events.csv`
- `noc_regions.csv`

from the **project root** (same folder as `app.py`).

If you prefer to use the copies inside `Data/`, update the paths in `app.py` accordingly.

## Run Locally

### 1) Create & activate a virtual environment (recommended)

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Start the Streamlit app

```bash
streamlit run app.py
```

Streamlit will print a local URL (usually http://localhost:8501).


These are commonly used for Heroku-style deployments to configure Streamlit’s server port.

## Troubleshooting

- **Case-sensitive imports on Linux/macOS**: the code does `import helper`, but the file in this repo is `Helper.py`. Windows often works anyway, but Linux/macOS deployments may fail. Fix by renaming `Helper.py` to `helper.py` or changing the import in `app.py`.
- **Missing CSV files**: ensure `athlete_events.csv` and `noc_regions.csv` exist in the project root (or update file paths).

## Acknowledgements

Dataset: “120 years of Olympic history: athletes and results” by Heesoo (Kaggle).
