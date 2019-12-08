import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import dash_table
from dash.dependencies import Input, Output, State
import pickle
import numpy as np
from sqlalchemy import create_engine

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

engine = create_engine('mysql+mysqlconnector://root:fadillahfarhan99@localhost/adver?host=localhost?port=3306')
conn = engine.connect()
dfAuto=pd.DataFrame(conn.execute('SELECT * FROM advertising').fetchall(),columns=pd.read_csv('advertising.csv').columns)
# dfAuto=pd.read_csv('advertising.csv')
pred_model = pickle.load(open('Advertising_model', 'rb'))[0]

dropdwn=['All',*[str(i) for i in dfAuto['Country'].unique()]]

app.layout = html.Div(children = [
    html.H1('Dashboard Advertising Project'),
    html.P('Created by: Farhan Fadillah'),
    dcc.Tabs(value = 'tabs', id = 'tabs-1', children = [
        dcc.Tab(label = 'Table', id = 'table', children = [
            html.Center(html.H1('DATAFRAME ADVERTISING')),
            html.Div(className = 'col-6', children=[
                html.P('Country'),
                dcc.Dropdown(id= 'table-dropdown', value = 'All',
                    options= [
                        {'label': i, 'value': i} for i in dropdwn
                    ]
                )
            ]),
            html.Div(className = 'col-3', children=[
                html.P('Max Rows:'),
                dcc.Input(
                    id='page-size',
                    type='number',
                    value=10,
                    min=3,max=20,step=1
                )
            ]),
            html.Div(className = 'col-12', children = [
                html.Button(id='Search', n_clicks=0, children='Search',style={
                    'margin-top':'14px',
                    'margin-bottom':'14px'})
            ]),
            html.Div(id='div-table',className = 'col-12', children = [
                dash_table.DataTable(
                    id= 'dataTable',
                    data= dfAuto.to_dict('records'),
                    columns= [{'id': i, 'name': i} for i in dfAuto.columns],
                    page_action= 'native',
                    page_current= 0,
                    page_size = 10,
                    style_table={'overflowX': 'scroll'}
                )
            ])
        ]), 
        
        dcc.Tab(label = 'Bar Chart', id = 'bar', children = [
            html.Div(className = 'col-12', children = [
                html.Div(className = 'row', children = [
                    html.Div(className = 'col-4',children= [
                        html.P(f'Y1'),
                        dcc.Dropdown(id= f'y-axis-1', value = f'Daily Time Spent on Site',
                            options= [
                                {'label': i, 'value': i} for i in dfAuto.select_dtypes('number').columns
                            ]
                        )
                    ]),
                    html.Div(className = 'col-4',children= [
                        html.P(f'Y2'),
                        dcc.Dropdown(id= f'y-axis-2', value = f'Age',
                            options= [
                                {'label': i, 'value': i} for i in dfAuto.select_dtypes('number').columns
                            ]
                        )
                    ]),
                    html.Div(className = 'col-4',children= [
                        html.P(f'X'),
                        dcc.Dropdown(id= f'y-axis-3', value = f'Country',
                            options= [
                                {'label': i, 'value': i} for i in ['Country','City',]
                            ]
                        )
                    ])
                ]),
                html.Div(children= [dcc.Graph(
                    id = 'contoh-graph-bar',
                    figure={'data' : [{
                        'x': dfAuto['Age'],
                        'y': dfAuto['Daily Internet Usage'],
                        'type': 'bar',
                        'name': 'Daily Internet Usage'
                    },{
                        'x': dfAuto['Age'],
                        'y': dfAuto['Daily Time Spent on Site'],
                        'type': 'bar',
                        'name': 'Daily Time Spent on Site'
                    }],
                        'layout': {'title': 'Bar Chart'}
                    }
                )])
            ])
        ]),
    
        dcc.Tab(label = 'Scatter Chart', id = 'scatter', children = [
        html.Div(children = dcc.Graph(
            id = 'graph-scatter',
            figure = {'data':[go.Scatter(
                x= dfAuto[dfAuto['Age']==i]['Daily Time Spent on Site'],
                y= dfAuto[dfAuto['Age']==i]['Daily Internet Usage'],
                text= dfAuto[dfAuto['Age']==i]['Area Income'],
                mode='markers',
                name= f'{i}'    
            ) for i in dfAuto['Age'].unique()
            ],
                'layout':go.Layout(
                    xaxis= {'title':'Daily Time Spent on Site'},
                    yaxis = {'title' : 'Daily Internet Usage'},
                    hovermode = 'closest'
                )
            }
        ),className = 'col-12')
    ]),

    dcc.Tab(label = 'Pie Chart', id = 'tab-dua', children = [
        html.Div(className = 'col-4',children= [
            html.P('Select value'),
            dcc.Dropdown(id= f'pie-dropdown', value = 'Daily Internet Usage',
                options= [
                    {'label': i, 'value': i} for i in dfAuto.select_dtypes('number').columns
                ]
            )
        ]),
        html.Div(className = 'col-12', children = dcc.Graph(
            id = 'pie-chart',
            figure= {'data' : [go.Pie(
                labels=list(i for i in dfAuto['Age'].unique()),
                values=list(dfAuto.groupby('Age').mean()['Daily Internet Usage'])
            )
            ], 'layout': {'title': 'Mean Pie Chart'},}
        ))
    ]),
     dcc.Tab(label='Prediction', id='tab-predict', children=[
            html.Div(children=[
                html.H5('Data Advertising', className='mx-auto'),
                html.Div(children=[
                    html.Div(children=[
                        html.P('Daily Time Spent on Site: ', className='ml-2 mr-2'),
                        dcc.Input(id='Daily_Time_Spent_on_Site', type='number', value='0', className='col-2 form-control',),
                        html.P('Age: ', className='ml-2 mr-2'),
                        dcc.Input(id='Age', type='number', value='0', className='col-2 form-control',),
                        html.P('Area Income: ', className='ml-2 mr-2'),
                        dcc.Input(id='Area_Income', type='number', value='0', className='col-2 form-control',),
                        html.P('Daily Internet Usage: ', className='ml-2 mr-2'),
                        dcc.Input(id='Daily_Internet_Usage', type='number', value='0', className='col-2 form-control',),
                        html.P('Male: ', className='ml-2 mr-2'),
                            dcc.Dropdown(
                                id='Male',
                                options=[
                                    {'label': 'yes', 'value': 1},
                                    {'label': 'no', 'value': 0}
                            ],
                            value=''
                            ), 
                        html.Button(children='Predict', id='predict', className='ml-2 btn btn-secondary')
                    ], style={'marginTop': 50, 'fontSize': 14}, className='row mb-2 ml-1'),

                    html.Div(children=[
                        html.P('Prediction result:'),
                        html.P(children='Please fill all needed value!', id='pred-result')
                    ], style={'marginTop': 50, 'fontSize': 14})
                ])
            ])
        ]),
    
    ],
        content_style = {
            'fontFamily': 'Arial',
            'borderBottom': '1px solid #d6d6d6',
            'borderRight': '1px solid #d6d6d6',
            'borderLeft': '1px solid #d6d6d6',
            'padding': '44px'
        },
        className = 'row'
    )
], 
    style={
        'maxwidth': '1200px', 'margin': '0 auto'
    }
)

@app.callback(
    Output(component_id= 'contoh-graph-bar', component_property= 'figure'),
    [Input(component_id=f'y-axis-{i}', component_property='value') for i in range(1,4)]
)
def create_graph_bar(y1,y2,x):
    figure={'data' : [{
        'x': dfAuto[x],
        'y': dfAuto[y1],
        'type': 'bar',
        'name': y1
    },{
        'x': dfAuto[x],
        'y': dfAuto[y2],
        'type': 'bar',
        'name': y2
    }]
        
    }
    return figure

@app.callback(
    Output(component_id= 'pie-chart', component_property= 'figure'),
    [Input(component_id=f'pie-dropdown', component_property='value')]
)
def create_pie_chart(pie):
    figure= {'data' : [go.Pie(
            labels=list(i for i in dfAuto['Age'].unique()),
            values=list(dfAuto.groupby('Age').mean()[pie])
        )
        ], 'layout': {'title': 'Mean Pie Chart'}
    }
    return figure

@app.callback(
    Output(component_id= 'dataTable', component_property= 'data'),
    [Input(component_id='Search', component_property='n_clicks')],
    [State(component_id='table-dropdown',component_property='value')]
)

def update_data(n_clicks,Country):
    if Country == 'All':
        df = dfAuto.to_dict('records')
    else:
        df = dfAuto[dfAuto['Country']==Country].to_dict('records')
    return df

@app.callback(
    Output(component_id= 'dataTable', component_property= 'page_size'),
    [Input(component_id='Search', component_property='n_clicks')],
    [State(component_id='page-size',component_property='value')]
)

def update_data(n_clicks,size):
    return size

@app.callback(
    Output(component_id='pred-result', component_property='children'),
    [Input(component_id='predict', component_property='n_clicks')],
    [State(component_id='Daily_Time_Spent_on_Site', component_property='value'),
    State(component_id='Age', component_property='value'),
    State(component_id='Area_Income', component_property='value'),
    State(component_id='Daily_Internet_Usage', component_property='value'),
    State(component_id='Male', component_property='value')]
)
def predict_legendary(n_clicks, Daily_Time_Spent_on_Site, Age, Area_Income, Daily_Internet_Usage, Male):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    if Daily_Time_Spent_on_Site == '0' or Age == '0' or Area_Income == '0' or Daily_Internet_Usage == '0' or Male == '':
        children = 'Please fill all needed value!'
    else:
        X_test = np.array([Daily_Time_Spent_on_Site, Age, Area_Income, Daily_Internet_Usage, Male]).reshape(1, -1)
        predict_result = pred_model.predict(X_test)[0]
       

        if int(predict_result) > 0:
            children = 'Your Customer clicked the ad'
        else:
            children = "Your Customer didn't click the ad "
    
    return children


if __name__ == '__main__':
    app.run_server(debug=True)