import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input

import pandas as pd
import plotly.graph_objs as go
import numpy as np

########### setup app attributes  
APP_TITLE = "UFO Sightings"
STYLE_SHEETS = ['./assets/my_bWLwgP.css']
DATA_FILE = "ufo2.csv"


########### placeholder chart
placeholder_data = [1,2,2,2,2,2,3,3,3,4,4,4,5,5,5,5,6,6,6,6,6,6,7,7,7,8,8,8,8,8,8,9,9,9,9,3,2]
data = [go.Histogram(y=placeholder_data)]
placeholder_fig = go.Figure(data = data)


########### create data frame
data = pd.read_csv(DATA_FILE)
data.drop(["Index"], inplace = True, axis="columns")

data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

########### Initiate the app
app = dash.Dash(__name__, external_stylesheets = STYLE_SHEETS)
server = app.server
app.title = APP_TITLE


########### Define app layout
# dropdown list of values
shape_items = data.sort_values(by='Shape Reported', ascending=True)['Shape Reported'].unique()
colors_items = data.sort_values(by='Colors Reported', ascending=True)['Colors Reported'].unique()

# filter on color, shape and date
# report as map - count, barchart stacked color, shape, and pie chart by day of week
# sum of sightings, count
app.layout = html.Div(id = "wrapper-id",
    children = [
      html.H1(
        id = 'header-id',
        children = 'UFO Sighting across the USA',
        className = "header"
      ),
      html.Div(
        id = 'menu-id',
        children = [
          # colors reported dropdown
          html.Div(children="Colors Reported", className="menu-title"),
          dcc.Dropdown(
            id="colors-filter",
            options=[
              {"label": item, "value": item}
              for item in colors_items
            ],
            value="",
            clearable=True,
            className="dropdown"
          ),
          # shape reported dropdown
          html.Div(
            children="Shape Reported",
            className="menu-title"),
          dcc.Dropdown(
            id="shape-filter",
            options=[
              {"label": item, "value": item}
              for item in shape_items
            ],
            value="",
            clearable=True,
            className="dropdown"
          ),
          # date range picker
          html.Div(
            children=[
              html.Div(
                children="Date Range",
                className="menu-title"
              ),
              dcc.DatePickerRange(
                id="date-range",
                min_date_allowed=data.Date.min().date(),
                max_date_allowed=data.Date.max().date(),
                start_date=data.Date.min().date(),
                end_date=data.Date.max().date(),
              ),
            ]
          )
        ],
        className = 'menu'
      ),
      html.Div(
        children = [
          html.Div(
            children = [
              html.H4("Chart 1 title"),
              dcc.Graph(
                id='chart1-id',
                figure = placeholder_fig,
                className = "card"
              )
            ],
            # className = "six columns"
            className = "four columns"
          ),
          html.Div(
            children = [
              html.H4("Chart 2 title"),
              dcc.Graph(
                 id='chart2-id',
                 figure=placeholder_fig,
                 className="card")
            ],
            # bootstrap has 12 columns grid system -
            # six converts to 2 columns, each using 6 cells of the grid system
            # four would convert to 3 columns of 4 cells each
            className = "seven columns"
            # className = "six columns"
            # className = "four columns"
          ),
          html.Div(
            children=[
              html.H4("Chart 3 title"),
              dcc.Graph(
                 id='chart3-id',
                 figure=placeholder_fig,
                 className="card")
            ],
            className = "six columns"
            # className="four columns"
          )
        ],
        className ="row"
      ),
      html.Div(
        children = [
          html.H4("Summary notes"),
          html.P("Insert summary notes here... \
                 Insert summary notes here... \
                 Insert summary notes here... \
                 Insert summary notes here...")
        ]
      )
    ],
    className = "wrapper"
)


########### Define callback  
# @app.callback(
#     [Output("<dcc.component.id1>", "<dcc.component.property1>"),
#      Output("<dcc.component.id1>", "<dcc.component.property2>"),
#      ...]
#     [
#         Input("<component_id>","<component_property"),
#         Input("region-filter", "value"),
#         Input("type-filter", "value"),
#         Input("date-range", "start_date"),
#         Input("date-range", "end_date"),
#     ],
# )
#
# def update_charts(<input1>, region, type, start_date, end_date):
#     mask = (
#         (data.<input1> == <input1">)
#         & (data.region == region)
#         & (data.type == avocado_type)
#         & (data.Date >= start_date)
#         & (data.Date <= end_date)
#     )
#     filtered_data = data.loc[mask, :]
# [...]
#
#     my_chart_figure = {
#         "data": [
#             {
#                 "x": filtered_data["Date"],
#                 "y": filtered_data["AveragePrice"],
#                 "type": "lines",
#                 "hovertemplate": "$%{y:.2f}<extra></extra>",
#             },
#         ],
#         "layout": {
#             "title": {
#                 "text": "Average Price of Avocados",
#                 "x": 0.05,
#                 "xanchor": "left",
#             },
#             "xaxis": {"fixedrange": True},
#             "yaxis": {"tickprefix": "$", "fixedrange": True},
#             "colorway": ["#17B897"],
#         },
#     }
#
#     second_chart_figure = {
#         "data": [...]
#
#     return my_chart_figure, second_chart_figure

############ Deploy
if __name__ == '__main__':
    app.run_server()