"""Collect Wanted jobs locally and export Flask templates for GitHub Pages."""
import argparse
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from main import app
from extractors.wanted import extract_wandted_jobs

ROOT = Path(__file__).resolve().parent

def build(keywords, refresh=False):
    output = ROOT / "docs"
    output.mkdir(exist_ok=True)
    cache = ROOT / "data"
    cache.mkdir(exist_ok=True)
    pages = {}
    for keyword in keywords:
        keyword = keyword.strip().lower()
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", keyword):
            raise ValueError("Use English letters, digits or hyphens for keywords")
        snapshot = cache / f"{keyword}.json"
        if refresh or not snapshot.exists():
            jobs = extract_wandted_jobs(keyword)
            if not jobs:
                raise RuntimeError(f"No jobs collected for {keyword}; check Wanted selectors. Existing snapshot preserved.")
            snapshot.write_text(json.dumps({"collected_at": datetime.now(timezone.utc).isoformat(), "jobs": jobs}, ensure_ascii=False, indent=2), encoding="utf-8")
        saved = json.loads(snapshot.read_text(encoding="utf-8"))
        jobs = saved["jobs"]
        filename = f"{keyword}.html"
        pages[keyword] = filename
        with (output / f"{keyword}.csv").open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "company_name", "reward", "link"], extrasaction="ignore")
            writer.writeheader()
            writer.writerows(jobs)
        with app.app_context():
            html = app.jinja_env.get_template("search.html").render(keyword=keyword, jobs=jobs, export_url=f"{keyword}.csv")
        html = html.replace('<hgroup>', '<hgroup><a href="./index.html">Home</a><p>Collected: ' + saved["collected_at"] + '</p>')
        (output / filename).write_text(html, encoding="utf-8")
        print(f"{keyword}: {len(jobs)} jobs")
    with app.app_context():
        html = app.jinja_env.get_template("home.html").render()
    html = html.replace('action="/search"', 'id="search-form" action="./index.html"')
    script = """<p>Available keywords: KEYWORDS. Results are saved snapshots.</p>
<p id="search-message" role="status"></p>
<script>
const pages = PAGES;
document.getElementById('search-form').addEventListener('submit', function(event) {
  event.preventDefault();
  const keyword = this.elements.keyword.value.trim().toLowerCase();
  if (Object.prototype.hasOwnProperty.call(pages, keyword)) location.href = './' + pages[keyword];
  else document.getElementById('search-message').textContent = 'Choose a saved keyword: ' + Object.keys(pages).join(', ');
});
</script>""".replace("KEYWORDS", ", ".join(pages)).replace("PAGES", json.dumps(pages))
    (output / "index.html").write_text(html.replace("</main>", script + "</main>"), encoding="utf-8")
    (output / ".nojekyll").touch()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("keywords", nargs="*", default=["python", "javascript", "java"])
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    build(args.keywords, args.refresh)
