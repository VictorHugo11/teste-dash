from dash import Dash, html, dcc, callback, Output, Input
import yfinance as yf
import plotly.graph_objects as go
import datetime as dt
import requests
from bs4 import BeautifulSoup
import plotly.express as px

def news_petr4():
    response = requests.get('https://braziljournal.com/?s=petr4')
    content = response.content
    site = BeautifulSoup(content, 'html.parser')

    noticias = site.findAll('figcaption', attrs={'class': "boxarticle-infos"})
    
    news_list = []
    for idx, noticia in enumerate(noticias[:3]):
        titulo = noticia.find('p', attrs={'class': "boxarticle-infos-tag"}).text.lstrip()
        subtitulo = noticia.find('h2', attrs={'class': "boxarticle-infos-title"}).text.lstrip()
        link = noticia.find('h2', attrs={'class': "boxarticle-infos-title"}).find('a', attrs={'href': True})['href']
        news_list.append({'title': titulo, 'subtitle': subtitulo, 'link': link})
    
    return news_list

def news_weg():
    response = requests.get('https://braziljournal.com/?s=weg')
    content = response.content
    site = BeautifulSoup(content, 'html.parser')

    noticias = site.findAll('figcaption', attrs={'class': "boxarticle-infos"})
    
    news_list = []
    for idx, noticia in enumerate(noticias[:3]):
        titulo = noticia.find('p', attrs={'class': "boxarticle-infos-tag"}).text.lstrip()
        subtitulo = noticia.find('h2', attrs={'class': "boxarticle-infos-title"}).text.lstrip()
        link = noticia.find('h2', attrs={'class': "boxarticle-infos-title"}).find('a', attrs={'href': True})['href']
        news_list.append({'title': titulo, 'subtitle': subtitulo, 'link': link})
    
    return news_list

def news_cea():
    response = requests.get('https://braziljournal.com/?s=c%26a')
    content = response.content
    site = BeautifulSoup(content, 'html.parser')

    noticias = site.findAll('figcaption', attrs={'class': "boxarticle-infos"})
    
    news_list = []
    for idx, noticia in enumerate(noticias[:3]):
        titulo = noticia.find('p', attrs={'class': "boxarticle-infos-tag"}).text.lstrip()
        subtitulo = noticia.find('h2', attrs={'class': "boxarticle-infos-title"}).text.lstrip()
        link = noticia.find('h2', attrs={'class': "boxarticle-infos-title"}).find('a', attrs={'href': True})['href']
        news_list.append({'title': titulo, 'subtitle': subtitulo, 'link': link})
    
    return news_list

tickers = ["PETR4.SA", "WEGE3.SA", "CEAB3.SA"]

# datas
start_date = dt.datetime(2010, 1, 1)
end_date = dt.datetime.now()

# acoes
petr = yf.download("PETR4.SA", start=start_date, end=end_date)
wege = yf.download("WEGE3.SA", start=start_date, end=end_date)
cea = yf.download("CEAB3.SA", start=start_date, end=end_date)

app = Dash(__name__)
fig = go.Figure()

app.layout = html.Div([
    html.H1(children='', style={'textAlign': 'center', 'color': '#000'}),
    dcc.Dropdown(options=[{'label': ticker, 'value': ticker} for ticker in tickers],
                 value='PETR4.SA',
                 id='dropdown-selection',
                 style={'background-color': '#fff', 'color': '#000', 'border': '1   px solid #dee2e6', 'margin': 'auto', 'width': '50%', 'marginTop': '10px', 'outline': 'none', 'box-shadow': 'none'}),
    html.Div(style={'display': 'flex', 'justify-content': 'space-between'}, children=[
        dcc.Graph(id='graph-content',
                  figure=fig,
                  style={'background-color': '#fff', 'color': '#000', 'font-family': 'Lato, sans-serif', 'height': '70vh', 'width': '80%'}),
        html.Div(id='news-content', style={'padding': '20px', 'width': '40%', 'margin-top': '68px'})
    ])
], style={'width': '80%', 'margin': 'center', 'padding': '10px', 'background-color': '#fff', 'color': '#000', 'font-family': 'Lato, sans-serif'})

@app.callback(
    [Output('graph-content', 'figure'),
     Output('news-content', 'children')],
    Input('dropdown-selection', 'value')
)
def update_layout(value):
    if value == 'PETR4.SA':
        selected_ticker = petr
        
        news_list = news_petr4()
    elif value == 'WEGE3.SA':
        selected_ticker = wege
        
        news_list = news_weg()
    elif value == 'CEAB3.SA':
        selected_ticker = cea
        
        news_list = news_cea()

    new_fig = go.Figure(data=[go.Candlestick(x=selected_ticker.index,
                                              open=selected_ticker['Open'],
                                              high=selected_ticker['High'],
                                              low=selected_ticker['Low'],
                                              close=selected_ticker['Close'])],
                         layout=go.Layout(xaxis={'rangeslider': {'visible': False}}))
    
    return new_fig, [html.H3('Notícias'), 
                     *[html.Div([html.H4(news['title']),
                                 html.P(news['subtitle']),
                                 html.A('Link Notícia', href=news['link'], target='_blank')]) for news in news_list]]

if __name__ == '__main__':
    app.run_server(debug=True)
