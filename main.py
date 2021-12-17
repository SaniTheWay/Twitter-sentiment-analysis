from os import name
from data_clean import *
from app import app

app = Dash(__name__)


# -----------App layout--------------------
app.layout = html.Div(
    [
        html.H1("Twitter Data Analysis Dashboard - Keev",
                style={"text-align": "center"}),
        dcc.Tabs(  # creating tabs
            [
                dcc.Tab(
                    label="Dataset Sentiment",
                    children=[
                        dcc.Dropdown(
                            id="slct_sentiments",
                            options=[
                                {
                                    "label": "Sentiments- Positive | Negetive | Neutral",
                                    "value": 1,
                                },
                            ],
                            # multi=False,
                            value="Positive",
                            style={"width": "40%"},
                        ),
                        html.Div(id="tab0", children=[]),
                        html.Br(),
                        dcc.Graph(id="sentiment_pie", figure={}),
                    ],
                ),
                dcc.Tab(
                    label="Words",
                    children=[
                        dcc.Dropdown(
                            id="slct_words",
                            options=[
                                {"label": "Positive", "value": "Positive"},
                                {"label": "Negative", "value": "Negative"},
                                {"label": "Neutral", "value": "Neutral"},
                            ],
                            multi=False,
                            value="Positive",
                            style={"width": "40%"},
                        ),
                        html.Div(id="tab1", children=[]),
                        html.Br(),
                        dcc.Graph(id="wordgraph", figure={}),
                    ],
                ),
                dcc.Tab(
                    label="Location",
                    children=[
                        dcc.Dropdown(
                            id="slct_location",
                            options=[
                                {"label": "Positive", "value": "Positive"},
                                {"label": "Negative", "value": "Negative"},
                                {"label": "Neutral", "value": "Neutral"},
                            ],
                            multi=False,
                            value="Positive",
                            style={"width": "40%"},
                        ),
                        html.Div(id="tab2", children=[]),
                        html.Br(),
                        dcc.Graph(id="locationgraph", figure={}),
                    ],
                ),
                dcc.Tab(
                    label="Users",
                    children=[
                        dcc.Dropdown(
                            id="slct_user",
                            options=[
                                {"label": "Positive", "value": "Positive"},
                                {"label": "Negative", "value": "Negative"},
                                {"label": "Neutral", "value": "Neutral"},
                            ],
                            multi=False,
                            value="Positive",
                            style={"width": "40%"},
                        ),
                        html.Div(id="tab3", children=[]),
                        html.Br(),
                        dcc.Graph(id="usergraph", figure={}),
                    ],
                ),
                dcc.Tab(
                    label="Hashtags",
                    children=[
                        dcc.Dropdown(
                            id="slct_hashtag",
                            options=[
                                {"label": "Positive", "value": "Positive"},
                                {"label": "Negative", "value": "Negative"},
                                {"label": "Neutral", "value": "Neutral"},
                            ],
                            multi=False,
                            value="Positive",
                            style={"width": "40%"},
                        ),
                        html.Div(id="tab4", children=[]),
                        html.Br(),
                        dcc.Graph(id="hash_graph", figure={}),
                    ],
                ),
                dcc.Tab(
                    label="Reach of Tweets",
                    children=[
                        dcc.Dropdown(
                            id="slct_reach",
                            options=[
                                {"label": " ", "value": 1},
                            ],
                            multi=False,
                            value="Positive",
                            style={"width": "40%"},
                        ),
                        html.Div(id="tab5", children=[]),
                        html.Br(),
                        dcc.Graph(id="reach_graph", figure={}),
                    ],
                ),
                dcc.Tab(
                    label="WordCloud",
                    children=[
                        dcc.Dropdown(
                            id="slct_cloud",
                            options=[
                                {"label": "Positive", "value": "Positive"},
                                {"label": "Negative", "value": "Negative"},
                                {"label": "Neutral", "value": "Neutral"},
                            ],
                            multi=False,
                            value="Positive",
                            style={"width": "40%"},
                        ),
                        html.Div(id="tab6", children=[]),
                        html.Br(),
                        html.Img(
                            src=app.get_asset_url("./cloud.png"),
                            id="image_wc",
                        ),
                    ],
                ),
            ]
        ),
        html.Hr(),
        html.H3(
            "Created with 💚 by Sanidhya Dave",
            style={"text-align": "center", "color": "olivedrab"},
        ),
    ]
)

# -------------------------------END OF LAYOUT------------------


# -----------------------------------@app.callback(s)---------------------------------------------

# -----------------------------------Overall Sentiment-------------------------------------
@app.callback(
    [
        Output(component_id="tab0", component_property="children"),
        Output(component_id="sentiment_pie", component_property="figure"),
    ],
    [Input(component_id="slct_sentiments", component_property="value")],
)
def update_pie(option_slctd):

    container = "Sentiment of Twitter Data Analysis."

    dff = data.copy()

    dff = dff["sentiment"].value_counts()

    fig = px.pie(
        dff,
        values="sentiment",
        names=dff.index,
        title="Sentiment",
    )
    return container, fig


# --------------------------------------------WordsGraph------------------------------------
@app.callback(
    [
        Output(component_id="tab1", component_property="children"),
        Output(component_id="wordgraph", component_property="figure"),
    ],
    [Input(component_id="slct_words", component_property="value")],
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Graph for most: {} words".format(option_slctd)

    dff = data.copy()

    dff = dff[dff["sentiment"] == option_slctd]["clean_data"]

    token_slctd = [token for line in dff for token in line.split()]
# counting

    def get_maxtoken(tweets, num=30):
        word_tokens = Counter(tweets)
        max_common = word_tokens.most_common(num)
        return dict(max_common)

    # Plotly Express
    df = pd.DataFrame(get_maxtoken(token_slctd).items(),
                      columns=["words", "count"])
    fig = px.bar(
        df,
        x="words",
        y="count",
        title=option_slctd,
    )
    return container, fig


# ---------------------------LOCATION------------------------------------------------------
@app.callback(
    [
        Output(component_id="tab2", component_property="children"),
        Output(component_id="locationgraph", component_property="figure"),
    ],
    [Input(component_id="slct_location", component_property="value")],
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Graph for most: {} Location".format(option_slctd)

    dff = data.copy()

    dff = dff[dff["sentiment"] == option_slctd]["user_location"]

    def get_maxtoken(tweets, num=30):
        loc_tokens = Counter(tweets)
        max_common = loc_tokens.most_common(num)
        return dict(max_common)

    # Plotly Express
    df = pd.DataFrame(get_maxtoken(dff).items(), columns=["location", "count"])
    fig = px.bar(
        df,
        x="location",
        y="count",
        title=option_slctd,
    )
    return container, fig


# ---------------------------UserName-----------------------------------------
@app.callback(
    [
        Output(component_id="tab3", component_property="children"),
        Output(component_id="usergraph", component_property="figure"),
    ],
    [Input(component_id="slct_user", component_property="value")],
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Graph for most: {} Userhandles".format(option_slctd)

    dff = data.copy()

    dff = dff[dff["sentiment"] == option_slctd]["user_name"]

    def get_maxtoken(tweets, num=30):
        loc_tokens = Counter(tweets)
        max_common = loc_tokens.most_common(num)
        return dict(max_common)

    # Plotly Express
    df = pd.DataFrame(get_maxtoken(dff).items(), columns=["Username", "count"])
    fig = px.bar(
        df,
        x="Username",
        y="count",
        title=option_slctd,
    )
    return container, fig


# ---------------------------Hashtags-----------------------------------------
@app.callback(
    [
        Output(component_id="tab4", component_property="children"),
        Output(component_id="hash_graph", component_property="figure"),
    ],
    [Input(component_id="slct_hashtag", component_property="value")],
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Graph for most: {} Userhandles".format(option_slctd)

    dff = data.copy()

    dff = dff[dff["sentiment"] == option_slctd]["hashtags"]

    # token_slctd = [token for li in dff for token in li.split("'")]
    # negative_tokens = [token for line in dff for token in line.split()]
    # neutral_tokens = [token for line in dff for token in line.split()]

    # to get most used Location
    def get_maxtoken(tweets, num=30):
        loc_tokens = Counter(tweets)
        max_common = loc_tokens.most_common(num)
        return dict(max_common)

    # Plotly Express
    df = pd.DataFrame(get_maxtoken(dff).items(), columns=["hashtags", "count"])
    fig = px.bar(
        df,
        x="hashtags",
        y="count",
        title=option_slctd,
    )
    return container, fig


# ---------------------------Retweets-----------------------------------------
@app.callback(
    [
        Output(component_id="tab5", component_property="children"),
        Output(component_id="reach_graph", component_property="figure"),
    ],
    [Input(component_id="slct_reach", component_property="value")],
)
def update_graph(o):
    container = "Graph for most Reach. <ZOOM IN to the graph to see the bar plotting.>"
    dff = data.copy()
    reach = pd.DataFrame({"Tweet": dff["text"], "Count": dff["retweets"]})
    reach = reach.sort_values(by=["Count"], ascending=False).dropna()

    # Plotly Express
    fig = px.bar(
        reach,
        x="Tweet",
        y="Count",
        title="Reach of Tweets",
    )
    return container, fig


# ---------------------------WordCloud-----------------------------------------
def plot_wordcloud(data):
    d = {a: x for a, x in data.values}
    wc = WordCloud(background_color="white", width=1760, height=650)
    wc.fit_words(d)
    return wc.to_image()


@app.callback(
    Output("tab6", "children"),
    dd.Output("image_wc", "src"),
    [dd.Input("slct_cloud", "value")],
)
def make_image(option_slctd):

    dff = data.copy()
    dff = dff[dff["sentiment"] == option_slctd]["clean_data"]

    def get_maxtoken(tweets, num=30):
        loc_tokens = Counter(tweets)
        max_common = loc_tokens.most_common(num)
        return dict(max_common)

    token_slctd = [token for li in dff for token in li.split()]
    df = pd.DataFrame(get_maxtoken(token_slctd).items(),
                      columns=["cloud", "count"])

    img = BytesIO()
    plot_wordcloud(data=df).save(img, format="PNG")
    # container for TEXT
    container = "Graph for most: {} WordCloud".format(option_slctd)

    return container, "data:image/png;base64,{}".format(
        base64.b64encode(img.getvalue()).decode()
    )
# ---------------------------------END @appcallback(s)------------------------------------------------


if __name__ == "__main__":
    app.run_server(debug=True)
