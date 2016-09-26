# How to use
# ==========
#
# Setup
# -----
# %run setup_highcharts.py
# load_highcharts() # this must be the last line of the cell
# load_highcharts_modules() # must be last line of the cell, and in a separate cell from load_highcharts()
#
# Display chart
# -------------
# highcharts(...)

from IPython.core.display import HTML, display

# Thus return value of this method must be the result of the cell
# evaluation for Highcharts to be loaded in the current notebook.
def load_highcharts():
    html = '''
<script src="http://code.highcharts.com/highcharts.js"></script>
'''
    return HTML(html)

def load_highcharts_modules():
    html = '''
<script src="http://code.highcharts.com/modules/exporting.js"></script>
<script src="http://code.highcharts.com/modules/drilldown.js"></script>
'''
    return HTML(html)
