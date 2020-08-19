import os
import dash
import pandas_datareader
import dash_core_components as dcc
import dash_html_components as html
import pandas_datareader.data as web
from dash.dependencies import Input, Output, State
from datetime import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

stock = "TSLA"
start = datetime(1980, 1, 1)
end = datetime.now()

df = web.DataReader(stock, "yahoo", start, end=end)

app.layout = html.Div(children=[
    html.Div(children="Name of Stock to Graph"),
    dcc.Input(id="input", value="", type="text"),
    html.Div(id="output-graph")
],
)

all_added_graphs = {}
ret_graph_list = []

app.layout = html.Div(children=[html.Div(children="Stock symbol to graph"),
                                html.Div(children=[
                                    dcc.Input(id="added-graphs", value="", type="text"),
                                    html.Button("Add graph", id="add-graph-btn", n_clicks=0)
                                ]),
                                html.Div(id="other-graphs")],
                      style={
                          "font-family": "Arial",
                          "font-size": 16,
                          "padding-top": 20,
                          "padding-left": 15
                      })


@app.callback(Output("other-graphs", "children"),
              [Input("add-graph-btn", "n_clicks")],
              state=[State("added-graphs", "value")])
def add_more_graphs(n_clicks, comp_name):
    global all_added_graphs, ret_graph_list

    for item in all_added_graphs.keys():
        if str(comp_name).lower().strip() == item:
            return html.Div("Graph already exists."), html.Div(children=ret_graph_list)

    _stock = comp_name
    _start = datetime(1980, 1, 1)
    _end = datetime.now()

    try:
        _df = web.DataReader(name=_stock, data_source="yahoo", start=_start, end=_end)
    except pandas_datareader._utils.RemoteDataError:
        return html.Div(children=["Could not find symbol."]), html.Div(children=ret_graph_list)

    all_added_graphs[f"{comp_name.lower()}"] = dcc.Graph(
        id=f"added_graph",
        figure={
            "data": [
                {"x": _df.index, "y": _df.Close, "type": "line", "name": _stock}
            ],
            "layout": {
                "title": _stock
            }
        }
    )

    ret_graph_list = [item for item in all_added_graphs.values()]
    return html.Div(children=ret_graph_list)


if __name__ == '__main__':
    app.run_server(host="localhost", port=8080)
