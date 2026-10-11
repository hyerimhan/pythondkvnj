from flask import Flask, render_template, request
from extractors.wanted import extract_wandted_jobs

app = Flask("JobScrapper")

@app.route("/")
def home():
  return render_template("home.html")

db = {}

@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  if keyword in db:
    jobs=db[keyword]
  else:
    jobs = extract_wandted_jobs(keyword)
    db[keyword] = jobs
  return render_template("search.html", keyword=keyword, jobs=jobs)

app.run("0.0.0.0", port=5000)