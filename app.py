import dash
from flask import Flask, app, send_from_directory
from plot import getPlot
from dataGraph import Cmain
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
import os

if not os.path.exists("images"):
    os.mkdir("images")

app = Flask(__name__)
dashApp = Dash(__name__, server=app)

name , fig= Cmain()
dashApp.layout = html.Div([
    dcc.Graph(figure=fig)
])

@app.route('/image')
def getFigure():
    return send_from_directory(directory= 'images', path='./',filename=name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT")) ,debug=True)