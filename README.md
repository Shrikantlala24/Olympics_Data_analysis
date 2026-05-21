# Olympics Data Analysis (Streamlit)

Quick, interactive exploration of Summer Olympics athlete data and medal results. The app focuses on medal trends, country performance, sport insights, and athlete profiles using a clean Streamlit UI and fast cached aggregations.

## Features

- Medal tally with country and year filters
- Overall trends for nations, athletes, sports, events, and medals
- Country-wise analysis with top sports, top athletes, and medal heatmaps
- Sport-wise analysis with medal trends and top performers
- Athlete-wise analysis with filters and spotlight view

## Setup

1. Create and activate a virtual environment (recommended).
2. Install dependencies:
   - pip install -r requirements.txt
3. Run the app:
   - streamlit run app.py

The app expects the following data files:
- Data/athlete_events.csv
- Data/noc_regions.csv

## Usage

Use the sidebar to pick the analysis section and apply filters. Heatmaps and large plots can be trimmed using the sliders for faster interaction.

## Project Structure

- app.py: Streamlit UI
- helper.py: Data aggregation utilities
- pre_process.py: Data loading and preprocessing
- Data/: Raw CSV inputs

## Performance Notes

- Caching is enabled for data loading and medal aggregates.
- Heatmaps are limited to top sports for quicker rendering.
- For Streamlit Cloud, keep requirements.txt minimal to speed up build time.

## Ideas to Improve Further

- Add athlete name autocomplete to avoid exact-match typing
- Store a preprocessed Parquet cache for faster cold starts
- Add unit tests for helper functions
- Add a lightweight search page for quick medal lookups
