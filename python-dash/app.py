# Imports
import pandas as pd
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import calendar
from modules.actorAnalysis import actorAnalysis
from modules.countryAnalysis import countryAnalysis
from modules.movieAdditions import movieAdditions
from modules.movieGenreAnalysis import movieGenreAnalysis
from modules.catalogAnalysis import catalogAnalysis

# Criação do app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])

amazon = pd.read_csv('./data/amazon_prime_titles.csv')
netflix = pd.read_csv('./data/netflix_titles.csv')
amazon['streaming'] = 'amz'
netflix['streaming'] = 'ntx'
df = pd.concat([amazon, netflix], ignore_index=True)
df.drop(['show_id', 'rating', 'duration', 'description', 'director', 'release_year'], axis=1, inplace=True)
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# Layout da barra lateral
sidebar = html.Div(
    [
        html.H4("Dashboard", className="text-white p-1", style={"marginTop": "1rem"}),
        html.Hr(style={"borderTop": "1px dotted white"}),
        dbc.Nav(
            [
                dbc.NavLink("Actors", href="/actors", active="exact"),
                dbc.NavLink("Countries", href="/countries", active="exact"),
                dbc.NavLink("Movie Additions", href="/additions", active="exact"),
                dbc.NavLink("Movie Genre", href="/genre", active="exact"),
                dbc.NavLink("Catalog", href="/catalog", active="exact"),
            ],
            vertical=True,
            pills=True,
            style={"fontSize": 18},
        ),
        html.P(u"Version 1.0", className="fixed-bottom text-white p-2"),
    ],
    className="bg-dark",
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "14rem",
        "padding": "1rem",
    },
)

# Atores
analyzer_actor = actorAnalysis(df)
column_name = 'cast'
top_actor = analyzer_actor.topActors(column_name)
top_actor_df = top_actor.reset_index()
top_actor_df.columns = ['Actor', 'Count']
fig = px.bar(top_actor, barmode="group")
fig.update_layout(
    xaxis_title='Actors',
    yaxis_title='Count of Working Films',
    xaxis_title_font_size=18,
    yaxis_title_font_size=18,
)

# Países
analyzer_country = countryAnalysis(amazon, netflix)
column_name = 'country'
platform_name_amz, top_country_series = analyzer_country.topCountries(analyzer_country.amazon_df, 'Amazon', column_name)
fig2 = px.bar(x=top_country_series.index, y=top_country_series.values, barmode="group", labels={'x': 'Country', 'y': 'Quantity'})
top_country_list = [{'Country': country, 'Count': count} for country, count in top_country_series.items()]

platform_name_ntx, top_country_series_ntx = analyzer_country.topCountries(analyzer_country.netflix_df, 'Netflix', column_name)
fig3 = px.bar(x=top_country_series_ntx.index, y=top_country_series_ntx.values, barmode="group", labels={'x': 'Country', 'y': 'Quantity'})
top_country_list_ntx = [{'Country': country, 'Count': count} for country, count in top_country_series_ntx.items()]

# Adições de Filmes
analyzer_netflix_additions = movieAdditions(netflix)
most_common_month = analyzer_netflix_additions.mostCommonMonth()
monthly_additions = analyzer_netflix_additions.getMonthlyAdditions()
fig4 = px.bar(
    x=calendar.month_name[1:],
    y=monthly_additions.values,
    labels={'x': '', 'y': ''},
    title="Monthly Additions of Movies on Netflix",
    height=700
)
fig4.update_layout(
    title={"font": {"size": 24}}
)

# Filmes de Comédia
analyzer_movie = movieGenreAnalysis(df)
comedy_movie_count = analyzer_movie.countComedyMovies()


# Gêneros dos Filmes
all_genres_counts = analyzer_movie.allGenresQuantity()

fig_treemap = px.treemap(
    names=all_genres_counts.index,
    parents=[''] * len(all_genres_counts),
    values=all_genres_counts.values,
    branchvalues='total',
    title="Films by Genre"
)
fig_treemap.update_layout(
    title={"font": {"size": 24}},
    height=550
)

# Frequência do Catálogo de cada Plataforma
analyzer_catalog = catalogAnalysis(amazon, netflix)
analyzer_catalog_amz = analyzer_catalog.calculateFrequencyQuantity(analyzer_catalog.amazon_df)
analyzer_catalog_ntx = analyzer_catalog.calculateFrequencyQuantity(analyzer_catalog.netflix_df)

# Cria o gráfico para a plataforma Amazon
amz_fig = px.bar(
    x=analyzer_catalog_amz.index,
    y=analyzer_catalog_amz.values,
    labels={'x': 'Content', 'y': 'Frquency'},
    title="Frequency of Movies and TV Shows on Amazon",
    height=700, 
)
amz_fig.update_layout(
    title={"font": {"size": 24}}
)

# Cria o gráfico para a plataforma Netflix
ntx_fig = px.bar(
    x=analyzer_catalog_ntx.index,
    y=analyzer_catalog_ntx.values,
    labels={'x': 'Content', 'y': 'Frquency'},
    title="Frequency of Movies and TV Shows on Netflix",
    height=700
)
ntx_fig.update_layout(
    title={"font": {"size": 24}}
)


# Layout das páginas
home_page_layout = html.Div(
    [
        html.H1("Welcome to Data Analysis Application"),
        html.P("Welcome to data analysis application for streaming platforms. This is the home page of our application, where you can explore and analyze streaming data."),
        html.P("This app is part of the Data Challenge by Coodesh. On the left-hand side, you will find a menu with various topics for analysis. Feel free to explore and navigate through the app."),
    ],
    style={"margin": "2rem"}
)


actors_page_layout = html.Div(
    [
        html.H1("Top 10 Actors"),

        # Gráfico de barras
        dcc.Graph(figure=fig, style={"height": "600px","font-size": "22px"}),
        html.Div(style={"border-bottom": "1px solid black", "margin": "1rem"}),    
        
        # Tabela        
        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in top_actor_df.columns])] +
            
            # Linhas
            [html.Tr([html.Td(top_actor_df.iloc[i][col]) for col in top_actor_df.columns]) for i in range(len(top_actor_df))],
            style={"border": "1px solid black", "padding": "1rem", "margin": "1rem","font-size": "22px","text-align": "justify"}
        ),
    ]
)


countries_page_layout = dbc.Container(
    [
        html.H1("Country Analysis Page"),
        dbc.Row(
            dbc.Col(
                dbc.Tabs(
                    [
                        dbc.Tab(
                            label="Amazon",
                            tab_id="tab-amazon",
                            children=[
                                # Sessão da Amazon
                                html.H1('Amazon'),
                                dcc.Graph(figure=fig2, style={"height": "600px","font-size": "22px"}),
                                html.Div(style={"border-bottom": "1px solid black", "margin": "1rem"}),

                                # Tabela
                                html.H3(platform_name_amz),
                                html.Table(
                                    # Header
                                    [html.Tr([html.Th(col) for col in top_country_list[0].keys()])] +

                                    # Linhas
                                    [html.Tr([html.Td(data[col]) for col in data.keys()]) for data in top_country_list],
                                    style={"border": "1px solid black", "padding": "1rem", "margin": "1rem","font-size": "22px","text-align": "justify"}
                                ),
                            ]
                        ),
                        dbc.Tab(
                            label="Netflix",  
                            tab_id="tab-netflix", 
                            children=[
                                # Sessão da Netflix
                                html.H1('Netflix'),
                                dcc.Graph(figure=fig3, style={"height": "600px"}),
                                html.Div(style={"border-bottom": "1px solid black", "margin": "1rem"}),

                                # Tabela
                                html.H3(platform_name_ntx),
                                html.Table(
                                    # Header
                                    [html.Tr([html.Th(col) for col in top_country_list_ntx[0].keys()])] +

                                    # Linhas
                                    [html.Tr([html.Td(data[col]) for col in data.keys()]) for data in top_country_list_ntx],
                                    style={"border": "1px solid black", "padding": "1rem", "margin": "1rem","font-size": "22px","text-align": "justify"}
                                )
                            ]
                        ),
                    ],
                    id="tabs",
                    active_tab="tab-amazon"  
                ),
                width=8, 
                style={"padding-left": "2rem"}  
            )
        )
    ],
    fluid=True 
)


additions_page_layout = html.Div(
    [
        html.H1("Movie Additions Page"),

        # Card com a informação do mês mais comum
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Month with the most Movie Additions on Netflix:"),
                        html.H2(html.Strong(most_common_month)),
                    ],
                    style={
                        "width": "400px",
                        "height": "400px",
                        "padding": "20px",
                        "border": "1px solid #000",
                        "border-radius": "10px",
                        "background-color": "#f9f9f9",
                        "text-align": "center",
                        "margin-bottom": "20px",
                    },
                ),                
                html.Div(style={"border-bottom": "1px solid black", "margin": "1rem"}),
            ],
            style={"margin": "20px"},
        ),     
        dcc.Graph(figure=fig4),
    ]
)


genre_page_layout = html.Div(
    [
        html.H1("Movie Genre Analysis Page"),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Number of Movies Listed as Comedy:"),
                        html.H2(html.Strong(comedy_movie_count)),
                    ],
                    style={
                        "width": "400px",
                        "height": "400px",
                        "padding": "20px",
                        "border": "1px solid #000",
                        "border-radius": "10px",
                        "background-color": "#f9f9f9",
                        "text-align": "center",                     
                    },
                ),
            ],
            style={"display": "flex", "justify-content": "space-between", "margin": "20px"},
        ),
        html.Div(
            [
                dcc.Graph(figure=fig_treemap),
            ],
            style={
                "width": "100%", 
                "height": "600px",
                "padding": "20px",
                "border": "1px solid #000",
                "border-radius": "10px",
                "background-color": "#f9f9f9",
                "text-align": "center",
                "margin-top": "20px",
            },
        ),
    ]
)


catalog_page_layout = html.Div(
    [
        html.H1("Catalog Analysis Page"),
        
        dbc.Tabs(
            [
                dbc.Tab(
                    label="Amazon",
                    tab_id="tab-amazon",
                    children=[
                        html.Div(
                            [
                                # Sessão da Amazon
                                html.H1('Amazon'),
                                dcc.Graph(figure=amz_fig),
                                html.Div(
                                    [], 
                                    style={"border-bottom": "1px solid black", "padding": "1rem", "margin": "1rem","font-size": "22px"}
                                ),
                                html.Div(
                                    [
                                        html.H2(html.Strong(f"Movies: {analyzer_catalog_amz['Movie']}, TV Shows: {analyzer_catalog_amz['TV Show']}"))
                                    ], 
                                    style={"padding": "1rem"}
                                )
                            ]
                        )
                    ]
                ),
                dbc.Tab(
                    label="Netflix",
                    tab_id="tab-netflix",
                    children=[
                        html.Div(
                            [
                                # Sessão da Netflix
                                html.H1('Netflix'),
                                dcc.Graph(figure=ntx_fig),
                                html.Div(
                                    [], 
                                    style={"border-bottom": "1px solid black", "padding": "1rem", "margin": "1rem","font-size": "22px"}
                                ),
                                html.Div(
                                    [
                                        html.H2(html.Strong(f"Movies: {analyzer_catalog_ntx['Movie']}, TV Shows: {analyzer_catalog_ntx['TV Show']}"))
                                    ], 
                                    style={"padding": "1rem"}
                                )
                            ]
                        )
                    ]
                ),
            ],
            id="tabs",
            active_tab="tab-amazon"
        )
    ]
)



# Organização do layout geral
content = html.Div(id="page-content", children=[], style={"marginLeft": "15rem", "margin-right": "1rem", "padding": "0rem 0rem", 'background-color': '#FFF',})

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# Callback para renderização das páginas
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/actors":
        return [actors_page_layout]
    elif pathname == "/countries":
        return [countries_page_layout]
    elif pathname == "/additions":
        return [additions_page_layout]
    elif pathname == "/genre":
        return [genre_page_layout]
    elif pathname == "/catalog":
        return [catalog_page_layout]
    elif pathname == "/":
        return [home_page_layout]
    else:
        return [html.H2("404 - Página não encontrada")]

# Executa a app
if __name__ == "__main__":
    app.run_server(debug=True)
