#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Sets up Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python mod imports
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
import base64
from dash.dependencies import Input, Output

#Config plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# import for your CRUD module
from animalShelter import AnimalShelter
from bson.objectid import ObjectId

username = "aacuser"
password = "SNHU1234"
host= "localhost" 
port= 27017
database = "AAC"
collection = "animals"

shelter = AnimalShelter()

df = pd.DataFrame.from_records(shelter.read({}))

df.drop(columns = ["_id"], inplace = True)

# Debug
# print(df.columns)

##################
# Dashboard View #
##################

app = JupyterDash('SimpleExample')

image_filename = 'Grazioso Salvare Logo.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([
    html.Div(id="hidden-div", style={"display":"none"}),
    html.Div(className='header',
             style={'display' : 'flex'},
             children=[ 
                 html.B(html.H1("SNHU CS-340 Dashoard - Makayla Anderson-Tucker ")),
                 html.A(html.Img(
                     src= "data:image/png;base64,{}".format(encoded_image.decode()),
                     style={'width': '160px', 'height': '120px'}
                 ),
                        href= "https://www.snhu.edu", 
                        target= "_blank"  # new tab
                       )
            
             ]),
    html.Hr(),
    html.Div(id="hidden-div", style={"display":"none"}),
    dcc.RadioItems(
        id = "filter-type",
        options = [
            {"label" : "Water Rescue", "value": "Water Rescue"},
            {"label" : "Mountain Rescue", "value": "Mountain Rescue"},
            {"label" : 'Disaster Rescue', "value": "Disaster Rescue"},
            {"label" : "Reset", "value" : "Reset"}
        ],
        value="Reset"),
    dash_table.DataTable(
        id="datatable-id",
        columns=[{"name": i, "id": i, "deletable": False, "selectable": True}
            for i in df.columns],
        data = df.to_dict("records"),
        editable = False,
        filter_action = "native",
        sort_action = "native",
        sort_mode = "multi",
        column_selectable= False,
        row_selectable = "single",
        row_deletable = False,
        selected_columns = [],
        selected_rows= [0],
        page_action = "native",
        page_current = 0,
        page_size=6 
    ),
    html.Br(),
    html.Hr(),
    html.Div(className='row',
             style={'display' : 'flex'},
             children=[
                 html.Div(
                     id='graph-id',
                     className='col s12 m6'
                 ),
                 html.Div(
                     id='map-id',
                     className='col s12 m6'
                 )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################

@app.callback(Output('datatable-id','data'),
              [Input('filter-type', 'value')])

def update_dashboard(filter_type):
    data = pd.DataFrame.from_records(shelter.read({}))
    columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
    
    if (str(filter_type) == "Water Rescue"):
        data= pd.DataFrame.from_records(shelter.read({
            "breed": {'$in': ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }))
    elif (str(filter_type) == "Mountain Rescue"):
        data= pd.DataFrame.from_records(shelter.read({
            "breed": {'$in': ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }))
    elif (str(filter_type) == "Disaster Rescue"):
        data= pd.DataFrame.from_records(shelter.read({
            "breed": {'$in': ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300}
        }))
        
        
    data.drop(columns=['_id'],inplace=True)
    return data.to_dict('records')


#This callback will highlight a row on the data table when the user selects it
@app.callback(Output("datatable-id", "style_data_conditional"),
              [Input("datatable-id", "selected_columns")
              ])

def update_styles(selected_columns):
    return [{
        "if" : { "column_id": i },
        "background_color": "#D2F3FF"
    } for i in selected_columns]

# Display the breeds of animal based on quantity represented in
# the data table 
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")])

def update_graphs(viewData):
    ###FIX ME ####
    # add code for chart of your choice (e.g. pie chart) #
    if viewData is None:
        return px.pie(names=[], values=[], title="Animal Types")
    
    df = pd.DataFrame.from_dict(viewData)
    
    return [
        dcc.Graph(
            figure = px.pie(df, names="breed", title='Preferred Animals')
        )]


# Map with Geolocation
# This callback will update the geo-location chart for the selected data entry
# derived_virtual_data will be the set of data available from the datatable in the form of 
# a dictionary.
# derived_virtual_selected_rows will be the selected row(s) in the table in the form of
# a list. For this application, we are only permitting single row selection so there is only
# one value in the list.
# The iloc method allows for a row, column notation to pull data from the datatable
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(viewData, index):  
    if viewData is None:
        return []
    elif index is None:
        return []
    
    dff = pd.DataFrame.from_dict(viewData)
    # Because we only allow single row selection, the list can be converted to a row index here
    if index is None:
        row = 0
    else: 
        row = index[0]
        
    # Austin TX is at [30.75,-97.48]
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            # Column 13 and 14 define the grid-coordinates for the map
            # Column 4 defines the breed for the animal
            # Column 9 defines the name of the animal
            dl.Marker(position=[dff.iloc[row,13],dff.iloc[row,14]], children=[
                dl.Tooltip(dff.iloc[row,4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[row,9])
                ])
            ])
        ])
    ]
    
    

app.run_server(debug=True)


# In[ ]:





# In[ ]:




