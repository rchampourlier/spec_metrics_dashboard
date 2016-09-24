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
from flask import Flask, render_template
import pandas as pd
import datetime

ROOT_DIR = os.path.dirname(os.path.realpath(__file__)) + "/.."
SRC_DIR = ROOT_DIR + "/src"
LIB_DIR = SRC_DIR + "/lib"
DATA_DIR = ROOT_DIR + "/data"
sys.path.append(SRC_DIR)
sys.path.append(LIB_DIR)

import highcharts

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=DEBUG)
