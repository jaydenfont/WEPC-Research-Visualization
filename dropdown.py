import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import datetime

app = dash.Dash(__name__)


# extract each state's data
data = pd.read_csv('bullying_viz_data.csv')
data['date'] = pd.to_datetime(data['date'])
data['date'] = data['date'].dt.strftime("%b-%d-%y")

states = data.groupby('state')
states_names = states.groups

all_states = {}
for s in states_names:
    all_states[s] = states.get_group(s)


app.layout = html.Div(children=[
    html.H1(children='Wheelock Dashboard'),

    html.Div([
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'Alaska', 'value': 'AK'},
                {'label': 'Alabama', 'value': 'AL'},
                {'label': 'Arkansas', 'value': 'AR'},
                {'label': 'Arizona', 'value': 'AZ'},
                {'label': 'California', 'value': 'CA'},
                {'label': 'Colorado', 'value': 'CO'},
                {'label': 'Connecticut', 'value': 'CT'},
                {'label': 'Delaware', 'value': 'DE'},
                {'label': 'Florida', 'value': 'FL'},
                {'label': 'Georgia', 'value': 'GA'},
                {'label': 'Hawaii', 'value': 'HI'},
                {'label': 'Idaho', 'value': 'ID'},
                {'label': 'Illinois', 'value': 'IL'},
                {'label': 'Indiana', 'value': 'IN'},
                {'label': 'Iowa', 'value': 'IA'},
                {'label': 'Kansas', 'value': 'KS'},
                {'label': 'Kentucky', 'value': 'KY'},
                {'label': 'Louisiana', 'value': 'LA'},
                {'label': 'Maine', 'value': 'ME'},
                {'label': 'Maryland', 'value': 'MD'},
                {'label': 'Massachusetts', 'value': 'MA'},
                {'label': 'Michigan', 'value': 'MI'},
                {'label': 'Minnesota', 'value': 'MN'},
                {'label': 'Mississippi', 'value': 'MS'},
                {'label': 'Missouri', 'value': 'MO'},
                {'label': 'Montana', 'value': 'MT'},
                {'label': 'Nebrasks', 'value': 'NE'},
                {'label': 'Nevada', 'value': 'NV'},
                {'label': 'New Hampshire', 'value': 'NH'},
                {'label': 'New Jersey', 'value': 'NJ'},
                {'label': 'New Mexico', 'value': 'NM'},
                {'label': 'New York', 'value': 'NY'},
                {'label': 'North Carolina', 'value': 'NC'},
                {'label': 'North Dakota', 'value': 'ND'},
                {'label': 'Ohio', 'value': 'OH'},
                {'label': 'Oklahoma', 'value': 'OK'},
                {'label': 'Oregon', 'value': 'OR'},
                {'label': 'Pennsylvania', 'value': 'PA'},
                {'label': 'Rhode Island', 'value': 'RI'},
                {'label': 'South Carolina', 'value': 'SC'},
                {'label': 'South Dakota', 'value': 'SD'},
                {'label': 'Tennessee', 'value': 'TN'},
                {'label': 'Texas', 'value': 'TX'},
                {'label': 'Utah', 'value': 'UT'},
                {'label': 'Vermont', 'value': 'VT'},
                {'label': 'Virginia', 'value': 'VA'},
                {'label': 'Washington', 'value': 'WA'},
                {'label': 'West Virginia', 'value': 'WV'},
                {'label': 'Wisconsin', 'value': 'WI'},
                {'label': 'Wyoming', 'value': 'WY'}
            ],
            placeholder="Select a State",
        ),
    ]),
    

    html.Div(
        dcc.Graph(
            id='graph',
            className='dropgraph'
        ),
    )
    
])

@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown', 'value')]
) 
def update_graph(value):

    if value == None:
        #default plot displayed is CA
        value = 'CA'

    
    #get plot based on selection
    x_axis = all_states[value]['date']
    y_axis1 = all_states[value]['sch_bly']
    y_axis2 = all_states[value]['cy_bly']

    return {'data': [go.Scatter(
                x=x_axis, 
                y=y_axis1,
                name='sch_bly',
                line=dict(color='#cc1900')),
                
                go.Scatter(
                x=x_axis, 
                y=y_axis2,
                name='cy_bly',
                line=dict(color='#004876'))
                ],
            'layout': go.Layout(
                title='School Bullying Searches Over The Years in ' + value,

                xaxis=dict(
                    title='Time',
                    showgrid=True,
                    # showline=True,
                    color='black',
                    showticklabels= True,
                    tickangle= 45,
                    tickvals=['Jan-01-16', 'Jan-01-17', 'Jan-01-18', 'Jan-01-19', 'Jan-01-20', 'Jan-01-21'],
                    ticktext=['Jan 01 2016', 'Jan 01 2017', 'Jan 01 2018', 'Jan 01 2019', 'Jan 01 2020', 'Jan 01 2021'],
                ),
                yaxis=dict(
                    title= 'True Value',
                    showgrid=True,
                    showline=True,
                    color='black',
                    range = [0,80],
                ),
                
            )
    }


if __name__ == '__main__':
    app.run_server(debug=True)