import dash

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    # external_stylesheets=[dbc.themes.LUX],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
