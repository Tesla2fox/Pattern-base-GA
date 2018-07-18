# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 14:41:26 2018

@author: stef_leonA
"""

from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
import plotly

py.sign_in('tesla_fox', 'HOTRQ3nIOdYUUszDIfgN')

trace1 = go.Scatter(
    x=[1, 2, 3],
    y=[4, 5, 6],
    mode='markers+text',
    text=['Text A', 'Text B', 'Text C'],
    textposition='bottom'
)
trace2 = go.Scatter(
    x=[2, 3, 4],
    y=[5, 6, 7],
    mode='markers+text',
    text=['Text D', 'Text E', 'Text F'],
    textposition='bottom'
)

fig = tools.make_subplots(rows=1, cols=2)

fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 2)

fig['layout'].update(height=600, width=800, title='i <3 annotations and subplots')
fig['layout']['shapes']  = [
        # unfilled Rectangle
        {
            'type': 'rect',
            'xref': 'x2',
            'yref': 'y2',
            'x0': 1,
            'y0': 1,
            'x1': 2,
            'y1': 3,
            'line': {
                'color': 'rgba(128, 0, 128, 1)',
            },
        },
        # filled Rectangle
        {
            'type': 'rect',
            'x0': 3,
            'y0': 1,
            'x1': 6,
            'y1': 2,
            'line': {
                'color': 'rgba(128, 0, 128, 1)',
                'width': 2,
            },
            'fillcolor': 'rgba(128, 0, 128, 0.7)',
        },
    ]
#py.iplot(fig, filename='simple-subplot-with-annotations')
plotly.offline.plot(fig, filename='simple-subplot-with-annotations')