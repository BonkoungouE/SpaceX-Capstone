# SpaceX Falcon 9 Landing Prediction

IBM Data Science Capstone project by **Emmanuel BONKOUNGOU**.

## Project objective
Use historical launch attributes to explore and predict the first-stage landing label. The project covers API data collection, web scraping, data wrangling, SQL analysis, visualization, interactive maps, a Dash application and classification models.

The datasets are historical teaching snapshots. The model predicts the course's landing label, not the launch price or a guaranteed reusable recovery.

## Main results

| Analysis | Result | Population |
| --- | --- | --- |
| Landing labels | 60 positive, 30 negative | 90 modeling launches |
| Generated EDA features | 80 numeric predictors | Four categorical columns explicitly encoded |
| Supplied ML reference features | 83 predictors | Also dummy-encodes GridFins, Reused and Legs |
| Classifier test accuracy | 83.33% for all four models | 15 correct predictions out of 18 |
| Best mean cross-validation accuracy | Decision tree, 87.68% | 10 folds on 72 training records |
| SQL NASA (CRS) total payload | 45,596 kg | Customer-filtered SQL records |
| First successful ground landing | 22 December 2015 | SQL teaching dataset |
| Highest Dash site success rate | KSC LC-39A: 10/13, 76.92% | 56-launch interactive sample |
| Scraped historical launch rows | 121 | Wikipedia revision dated 9 June 2021 |

**Dataset scope matters:** SQL has 101 records, while the geographic and Dash dataset has 56 launches. The modeling sample contains 90 launches. These samples must not be pooled or their rates compared without reconciliation.

## Repository structure

```text
SpaceX-Capstone/
├── README.md
├── requirements.txt
├── .gitignore
├── app/
│   └── spacex_dash_app.py
├── notebooks/             # Seven completed notebooks with execution outputs
├── data/
│   ├── raw/              # API JSON, historical HTML, SQL and interactive CSVs
│   ├── reference/        # Immutable course snapshots used by the labs
│   └── processed/        # Generated CSV exports
├── maps/                 # Exported interactive Folium HTML
├── reports/              # PowerPoint and submission PDF
├── docs/                 # Source manifest, data dictionary, upload guide
└── scripts/
    └── run_notebooks.py
```

## Installation
Python 3.11 or 3.12 is recommended.

```bash
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Then install dependencies:

```bash
python -m pip install -r requirements.txt
```

The dependency versions used during verification are recorded in `docs/environment_versions.txt`. Broad requirements allow installation on supported systems, but exact scores and selected hyperparameters can vary between library versions.

## Notebook order

1. `jupyter-labs-spacex-data-collection-api-v2.ipynb`
2. `jupyter-labs-webscraping.ipynb`
3. `labs-jupyter-spacex-Data-wrangling-v2.ipynb`
4. `jupyter-labs-eda-dataviz-v2.ipynb`
5. `jupyter-labs-eda-sql-coursera_sqllite.ipynb`
6. `lab-jupyter-launch-site-location-v2.ipynb`
7. `SpaceX-Machine-Learning-Prediction-Part-5-v1.ipynb`

Launch the notebook interface from the repository root:

```bash
python -m jupyterlab
```

Or execute the notebooks in order and save their outputs:

```bash
python scripts/run_notebooks.py
```

The notebooks read immutable inputs from `data/reference` or `data/raw`. They write generated exports to `data/processed`. In particular, the ML notebook intentionally uses the supplied 83-column reference snapshot to reproduce the report. It does not substitute the generated 80-column EDA export.

## SpaceX Dash application

```bash
python app/spacex_dash_app.py
```

Open **http://127.0.0.1:8050** and keep the terminal running. Stop with Ctrl+C.

- The dropdown selects all launch sites or one site.
- With ALL selected, the pie chart counts successful landings per site.
- With one site selected, the pie compares successful and failed landings.
- The 0–10,000 kg slider filters the scatterplot.
- The scatterplot colors launches by booster version category.

The application reads the local `data/raw/spacex_launch_dash.csv` file. No external API is needed for normal dashboard use.

## API availability and provenance

During repository preparation, the live SpaceX resource API returned **HTTP 522**. The API notebook therefore defaults to an explicitly documented historical fallback:

1. Parse the actual bundled historical launch JSON supplied by IBM.
2. Load the IBM course's enriched 90-row dataset instead of claiming fresh REST resource lookups.
3. Retain the original REST enrichment functions for optional future execution with `USE_LIVE_API = True`.

The fallback payload masses are already imputed. The notebook says so. Its saved outputs must not be represented as a newly completed live API collection.

The scraping notebook parses the real archived Wikipedia HTML included in the repository. Its extraction generated 121 rows in the verified execution.

## Maps

Open `maps/spacex_launch_sites_map.html` in a browser. Map tiles and JavaScript dependencies require Internet access even though the notebook reads local launch data. GitHub may not render Folium's interactive outputs directly.

Distance measurements use the Haversine formula. The coastline coordinate comes from the lab example. Other study coordinates are approximate, explicitly marked for verification, and do not constitute validated minimum distances to infrastructure.

## Modeling limitations

- The lab fits `StandardScaler` before the train/test split. This introduces preprocessing leakage. A rigorous evaluation should split raw data first and fit a scaler inside each cross-validation training fold through a pipeline.
- The test set has only 18 records. One prediction changes accuracy by about 5.56 percentage points.
- Class 1 includes `True Ocean` under the course convention. Successful reusable recovery requires a stricter target.
- Serial identifiers and reuse counts require an as-of-launch audit before future deployment.
- The 80-column generated EDA matrix and the 83-column supplied modeling snapshot encode binary fields differently. Their results need not be identical.

## Presentation and submission

The `reports` folder contains the editable PowerPoint and the PDF. The presentation preserves an explicit repository-link placeholder on slide 51 because the destination GitHub URL has not yet been supplied.

Before submission, upload this repository, insert its actual public URL on slide 51, and export the updated PDF. Choose only one submission route, AI grading or peer grading.

French upload instructions: [`docs/DEPOT_GITHUB_FR.md`](docs/DEPOT_GITHUB_FR.md).

## Attribution

Original notebooks, lab instructions, template and teaching data come from IBM Skills Network and retain their original copyright notices. The historical HTML comes from Wikipedia and retains its source notices. Map attribution belongs to OpenStreetMap contributors. No blanket license is asserted over third-party materials.

Source URLs and file hashes are listed in `docs/data_manifest.csv`.
