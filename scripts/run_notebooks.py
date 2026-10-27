"""Execute all repository notebooks in order. Run from any working directory."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
ORDER = [
    'jupyter-labs-spacex-data-collection-api-v2.ipynb',
    'jupyter-labs-webscraping.ipynb',
    'labs-jupyter-spacex-Data-wrangling-v2.ipynb',
    'jupyter-labs-eda-dataviz-v2.ipynb',
    'jupyter-labs-eda-sql-coursera_sqllite.ipynb',
    'lab-jupyter-launch-site-location-v2.ipynb',
    'SpaceX-Machine-Learning-Prediction-Part-5-v1.ipynb',
]
if __name__ == '__main__':
    for filename in ORDER:
        path = ROOT / 'notebooks' / filename
        print(f'Executing {filename}', flush=True)
        notebook = nbformat.read(path, as_version=4)
        NotebookClient(notebook, timeout=1200, kernel_name='python3',
                       resources={'metadata': {'path': str(ROOT / 'notebooks')}}).execute()
        nbformat.write(notebook, path)
    print('All notebooks executed and saved.')
