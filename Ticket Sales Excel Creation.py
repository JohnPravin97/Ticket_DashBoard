#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import folium
from geopy.geocoders import Nominatim
import requests


# In[2]:


res = requests.get(
    "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/germany.geojson"
)


# In[3]:


path = r"C:\Users\arockias\Desktop\Dashboard\Ticket Sales.csv"
df = pd.read_csv(path)
df.drop("Unnamed: 0", axis=1, inplace=True)


# In[4]:


#model_project_list = ['Dortmund', 'Cologne', 'Munich', 'Hamburg', 'Berlin', 'Essen', 'Freiburg im Breisgau', "Stuttgart"]
#df["Month"] = pd.date_range('2019-01-01', '2027-05-01', freq = "M")
#df["Sales"] = np.random.randint(1, 100, size = 100)
#df['Model Project'] = np.random.choice(model_project_list, 100)
#df.to_csv(path)


# In[5]:


'''
geolocator = Nominatim(user_agent="geoapiExercises")
def coor_latitude(row):
    location = geolocator.geocode(row)
    return location.latitude

def coor_longitude(row):
    location = geolocator.geocode(row)
    return location.longitude
    
def year_splitter(date):
    year = int(str(date).split('-')[2])
    return year

df["Year"] = df["Month"].apply(year_splitter)
df["Latitude"] = df['Model Project'].apply(coor_latitude)
df["Longitude"] = df['Model Project'].apply(coor_longitude)
df.to_csv(path)
'''


# In[6]:


df.head()


# In[7]:


df[df['Model Project'].isin(["Hamburg"])]


# In[8]:


fig = px.bar(data_frame=df, x = "Month", y = "Sales", color = "Type")
fig.show()


# In[9]:


fig = px.scatter_mapbox(lat= df["Latitude"], lon=df['Longitude'],  color= df['Model Project'], hover_name=df['Model Project'])
fig.update_layout(mapbox={
        "style": "carto-darkmatter",
        "zoom": 4,
        "layers": [
            {
                "source": res.json(),
                "type": "line",
                "color": "red",
                "line": {"width": 2},
            }
        ],
    })
fig.show()


# In[ ]:


app = Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Ticket Dashboard"

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(children=[
    html.H1(children='Dash'),

    html.Div(children=[
        html.Label('Model Project'),
        dcc.Dropdown(
            df["Model Project"].unique(), 
            ["Hamburg", "Essen"],
             id='drop', 
            multi=True
        ),
            
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([
        
        html.Div(children=[
            dcc.Graph(
                id='example-graph'
            ),
            dcc.Slider(
                df['Year'].min(),
                df['Year'].max(),
                step=None,
                id='year--slider',
                value=df['Year'].max(),
                marks={str(year): str(year) for year in df['Year'].unique()},

    )
            
            ], style={'display': 'inline-block', 'width': '45%', 'float': 'right'}),
        
        
        html.Div(children=[
            dcc.Graph(id='map-series')
        ], style={'display': 'inline-block', 'width': '40%', 'height': '15%', 'float': 'left'})
        ])
])

@app.callback(
    Output('example-graph', 'figure'),
    Input('drop', 'value'),
    Input('year--slider', 'value')
)  
def update_graph(drop_name, year_slider):
    dff = df[df["Model Project"].isin(drop_name)]
    dff_final = dff[dff["Year"] == year_slider]
    fig = px.bar(x = dff_final['Month'], y = dff_final["Sales"], color = dff_final["Type"], pattern_shape = dff_final["Model Project"], title="Tickets Sales Graph", labels={"x": "Date", 'y':'Sales'})
    #fig = px.line(x = dff_final['Month'], y = dff_final["Sales"], color = dff_final["Type"], title="Tickets Sales Graph", labels={"x": "Date", 'y':'Sales'})
    
    fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'], 
)
    return fig

@app.callback(
    Output('map-series', 'figure'),
    [Input('drop', 'value')]
) 
def update_map(drop_name):
    dff_map = df[df["Model Project"].isin(drop_name)]

    fig = px.scatter_mapbox(lat=dff_map["Latitude"], lon=dff_map['Longitude'], color= dff_map['Model Project'], hover_name=dff_map['Model Project'], title="Germany Project Map")
    
    fig.update_layout(
        mapbox={
        "style": "white-bg",
        "zoom": 3.6,
        "layers": [
            {
                "source": res.json(),
                "type": "line",
                "color": "green",
                "line": {"width": 2},
            }
        ],
    })
    return fig

    
if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:





# In[ ]:




