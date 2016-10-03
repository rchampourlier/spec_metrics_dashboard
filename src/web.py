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
import urllib
from markupsafe import Markup

import highcharts
import connector_s3, process

app = Flask(__name__)

@app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == "Markup":
        s = s.unescape()
    s = s.encode("utf8")
    s = urllib.parse.quote_plus(s)
    return Markup(s)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/branches")
def branches_index():
    run_keys = process.fetch_run_keys(connector_s3)
    runs_df = process.build_runs_df(run_keys)
    branch_names = process.branch_names(runs_df=runs_df)
    return render_template("branches_index.html",
        branch_names=sorted(branch_names))

@app.route("/branch/<string:branch_name>/runs")
def branch_runs_index(branch_name):
    run_keys = process.fetch_run_keys(connector_s3)
    runs_df = process.build_runs_df(run_keys)
    runs_df.index = runs_df.date
    branch_runs_df = runs_df[runs_df.branch == branch_name].sort_values("date", ascending=False)
    return render_template("branch_runs_index.html",
        branch_name=branch_name,
        branch_runs=branch_runs_df.to_dict(orient="rows"))

def unquote_param(param):
    return urllib.parse.unquote_plus(param)

def run_examples_df(run_key):
    run_data = process.fetch_run_data(connector_s3, run_key)
    return process.build_run_examples_df(run_data)

@app.route("/run/<path:run_key>/overview")
def run_overview(run_key):
    df = run_examples_df(unquote_param(run_key))
    chart_js = highcharts.pie_drilldown(
        df[["path_0", "path_1", "run_time"]] \
            .groupby(['path_0', 'path_1']) \
            .sum()[['run_time']],
        serie_name='Run time',
        title="Run time",
        percentage=False,
        unit="s"
    )
    df_html = df.groupby(["path_0", "path_1", "path_2", "path_3", "path_4"]).sum().to_html()
    return render_template(
        "run_overview.html",
        run_key=run_key,
        chart_js=chart_js,
        run_examples_df_html=df_html
    )

@app.route("/run/<path:run_key>/examples_by_runtime")
def run_stats_examples_by_runtime(run_key):
    df = run_examples_df(unquote_param(run_key))
    df_html = df.sort_values("run_time", ascending=False).to_html()
    return render_template(
        "run_examples_by_runtime.html",
        run_key=run_key,
        run_examples_df_html=df_html
    )

if __name__ == "__main__":
    app.run(debug=DEBUG)
