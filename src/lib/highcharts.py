# highcharts.py
# VERSION 0.0.2
#
# How to use
# ==========
#
# Setup
# -----
# %run lib/setup_highcharts.py
# load_highcharts() # this must be the last line of the cell
#
# Display chart
# -------------
# highcharts(...)

import random
import string
import json
import numpy as np
import math
import pandas as pd

def base(chart_def = None, height=400):
    assert chart_def
    chart_def_json = json.dumps(chart_def)

    js = '''
        var container = document.getElementById('chart');
        chart_def = %(chart_def_json)s;
        chart_def.chart.renderTo = container;
        chart_def.chart.height = 400;
        Highcharts.chart(chart_def);
    ''' % locals()
    return js

def pie(df, serie_name='Serie', title=None, subtitle=None, percentage=True, unit='%'):
    """
    Display highcharts pie
    """

    series_total = np.asscalar(df.sum())
    series_indices = df.index
    series_data = []

    # Building serie's data
    for serie_index in series_indices:
        serie_value = df.ix[serie_index].sum()
        if math.isnan(serie_value):
            continue
        serie_value_scalar = np.asscalar(serie_value)
        serie_percentage = 100 * serie_value_scalar / series_total
        serie_y = serie_percentage if percentage else serie_value_scalar
        serie_data_item = {'name': serie_index, 'y': serie_y, 'drilldown': serie_index}
        serie_drilldown_data = []
        series_data.append(serie_data_item)

    series = [{'name': serie_name, 'colorByPoint': True, 'data': series_data}]
    chart_def = {
        'chart': { 'type': 'pie' },
        'title': { 'text': title },
        'subtitle': { 'text': subtitle },
        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': True,
                    'format': '{point.name}: {point.y:.1f}%(unit)s' % locals()
                }
            }
        },
        'tooltip': {
            'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
            'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.1f}</b><br/>'
        },
        'series': series,
    }
    return base(chart_def=chart_def)

def pie_drilldown(df, serie_name='Serie', title=None, subtitle=None, percentage=True, unit='%'):
    """
    Display highcharts pie drilldown for DataFrame with a 2-level
    multi-index index and a single numeric column.
    """

    if len(df.index.levels) != 2:
        raise Exception('invalid data', 'index should have exactly 2 levels')

    series_total = np.asscalar(df.sum())
    series_indices = df.index.levels[0]
    series_data = []
    drilldown_series = []

    for serie_index in series_indices:

        # Building serie's data
        serie_value = np.asscalar(df.ix[serie_index].sum())

        # Ignoring zero values, otherwise Highcharts will fail displaying the pie chart
        if math.isnan(serie_value):
            continue

        serie_percentage = 100 * serie_value / series_total
        serie_y = serie_percentage if percentage else serie_value
        serie_data_item = {'name': serie_index, 'y': serie_y, 'drilldown': serie_index}
        serie_drilldown_data = []
        series_data.append(serie_data_item)

        # Building serie's drilldown serie
        serie_drilldown_indices = list(df.ix[serie_index].index)
        for serie_drilldown_index in serie_drilldown_indices:
            serie_drilldown_value = df.ix[serie_index, serie_drilldown_index].sum()
            if math.isnan(serie_drilldown_value):
                continue
            serie_drilldown_value_scalar = np.asscalar(serie_drilldown_value)
            serie_drilldown_percentage = 100 * serie_drilldown_value / series_total
            serie_drilldown_y = serie_drilldown_percentage if percentage else serie_drilldown_value
            serie_drilldown_data.append([serie_drilldown_index, serie_drilldown_y])
        serie_drilldown_serie = {'name': serie_index, 'id': serie_index, 'data': serie_drilldown_data}
        drilldown_series.append(serie_drilldown_serie)

    series = [{'name': serie_name, 'colorByPoint': True, 'data': series_data}]
    drilldown = {'series': drilldown_series}
    chart_def = {
        'chart': { 'type': 'pie' },
        'title': { 'text': title },
        'subtitle': { 'text': subtitle },
        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': True,
                    'format': '{point.name}: {point.y:.1f}%(unit)s' % locals()
                }
            }
        },
        'tooltip': {
            'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
            'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%(unit)s</b> of total<br/>' % locals()
        },
        'series': series,
        'drilldown': drilldown
    }
    return base(chart_def=chart_def)

def stacked_bars(df, title=None, fillna=0):
    if type(df.index) != pd.core.index.MultiIndex:
        raise Exception('invalid data', 'index must be a MultiIndex')
    if len(df.index.levels) != 2:
        raise Exception('invalid data', 'index must be a MultiIndex with 2 levels')
    if len(df.columns) != 1:
        raise Exception('invalid data', 'index must have 1 column only')

    category_levels = list(df.index.levels[0])
    if type(category_levels[0] == pd.tslib.Timestamp):
        categories = [ts.strftime('%Y-%m-%d') for ts in list(df.index.levels[0])]
    else:
        categories = category_levels

    stacked_series = list(df.index.levels[1])
    column = df.columns[0]

    series = []
    for stacked_serie in stacked_series:
        values = []
        for category in categories:
            # We need to go through every category to fill with an empty
            # value if one of the series has no value for a given category.
            if stacked_serie in df.ix[category].index.values:
                value = np.asscalar(df.ix[category, stacked_serie])
                values.append(value)
            else:
                values.append(fillna)

        serie = { 'name': stacked_serie, 'data': values }
        series.append(serie)

    chart_def = {
        'chart': { 'type': 'column' },
        'title': { 'text': title },
        'xAxis': { 'categories': categories },
        'yAxis': {
            'min': 0,
            'title': { 'text': title },
            'stackLabels': {
                'enabled': True,
                'style': {
                    'fontWeight': 'bold',
                    'color': 'gray'
                }
            }
        },
        'legend': {
            'align': 'right',
            'x': -30,
            'verticalAlign': 'top',
            'y': 25,
            'floating': True,
            'backgroundColor': 'white',
            'borderColor': '#CCC',
            'borderWidth': 1,
            'shadow': False
        },
        'tooltip': {
            'headerFormat': '<b>{point.x}</b><br/>',
            'pointFormat': '{series.name}: {point.y:.1f}<br/>Total: {point.stackTotal:.1f}'
        },
        'plotOptions': {
            'column': {
                'stacking': 'normal',
                'dataLabels': {
                    'enabled': True,
                    'color': 'white',
                    'format': '{point.y:.1f}',
                    'style': { 'textShadow': '0 0 3px black' }
                }
            }
        },
        'series': series
    }
    return base(chart_def=chart_def)

def bars(df, title=None):
    """
    Builds an Highcharts bar chart.
    You may pass a pd.DataFrame with:
      - a simple index: the index will be used to split bars over the x-axis,
      - a multi-index: the 1st index will be used to split bars over the x-axis,
        the 2nd will be used to split each bar in a stacked-bars chart.
    Options:
        - title: a title for the graph (default: None)
    """
    if (type(df.index) == pd.core.index.MultiIndex) and (len(df.index.levels) == 2):
        return stacked_bars(df, title=title)
    raise Exception('not implemented', 'no matching rendering yet')
