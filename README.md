# Wanted Job Scrapper

Flask app with a static GitHub Pages export. Wanted scraping stays in `extractors/wanted.py`.

## Build locally

```powershell
python -m pip install -r requirements.txt
python -m playwright install chromium
python build_static.py python javascript java
```

Snapshots are saved in `data/`; generated HTML and CSV files are in `docs/`.
Repeat builds reuse snapshots. Use `--refresh` to collect again.
GitHub Pages supports only the saved keywords; scraping runs on your computer.

## Publish

1. Commit and push `docs/`, `data/`, and `.github/workflows/deploy.yml` to `develop` or `main`.
2. Wait for the **Publish GitHub Pages** Action to create/update the `gh-pages` branch. It replaces that branch with generated files only.
3. Repository **Settings > Pages > Build and deployment**: select **Deploy from a branch**, branch **gh-pages**, folder **/(root)**, and Save.
4. Submit https://hyerimhan.github.io/pythondkvnj/

For local Flask development: `python main.py`.
