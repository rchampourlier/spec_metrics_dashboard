"""
    SpecMetrics Dashboard
    ~~~~~~
    A simple dashboard to get information about SpecMetrics
    data.
    :copyright: (c) 2016 by Romain Champourlier
    :license: BSD, see LICENSE for more details.

    USAGE:
        python3 ./app.py
"""

DEBUG = True

import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import boot

from flask import Flask, render_template
import highcharts
import connector_s3, process

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/branches")
def branches_index():
    run_keys = process.fetch_run_keys(connector_s3)
    run_keys_df = process.build_run_keys_df(run_keys)
    branches = process.branches(run_keys_df=run_keys_df)
    return render_template("branches_index.html",
        branches=sorted(branches))

if __name__ == "__main__":
    app.run(debug=DEBUG)
