from dash import Dash
from views import ContentRender

def create_app():
    app = ContentRender().app
    return app

