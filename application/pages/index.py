import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

from app import app
from pages.model_handler import models, data

"""
https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
"""

# Helper Functions
def calculate_bmi(height, weight):
    if height > 0:
        return 703*weight/(height**2)
    else:
         return 0

def make_checkbox(feature):
    checkbox = dcc.Checklist(
        options=[{'label': feature, 'value': 1}],
        value=[data.default_data['general_health_data'][feature]],
        id=feature,
    )
    return checkbox

def get_predictions():
    bmi_data = data.get_data('bmi_data')
    general_health_data = data.get_data('general_health_data')
    bmi_prediction = local_models.bmi_model.predict(bmi_data)
    general_health_prediction = local_models.general_health_model.predict(general_health_data)
    return [{'BMI Predicted': bmi_prediction}, {'General Health Predicted': general_health_prediction}]

def dict_to_div(dictionary, separator):
    assert type(dictionary) == dict
    for key, item in dictionary.items():
        line_to_add = separator.join([str(key), str(item)])
        div_elements = html.Div(line_to_add)
    return div_elements

def clean_info(data):
    # Return last item in list for checkboxes.  Otherwise return raw data.
    if type(data) == list:
        if len(data) > 1:
            return data[-1]
        else:
            return 0
    else:
        return data

# Initialize Models
local_models = models()

# Model Status
model_status_display = local_models.model_status
model_status_frame = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P(
                [
                    html.Span(model_status_display, className='mr-2')
                ]
            )
        )
    )
)

# Start Data Handler
data = data()

# Debug Predictions
'''
bmi_data = data.get_data('bmi_data')
general_health_data = data.get_data('general_health_data')
print(local_models.bmi_model.predict(bmi_data))
print(local_models.general_health_model.predict(general_health_data))
'''

# Make Checkboxes for binary features



# Layout Items

instruction_row = dbc.Col(
    dbc.Row(
        dcc.Markdown('>Enter your information as of today and see your health trajectory'),
    )
)


column1 = dbc.Col(
    [
        dcc.Markdown('Height(in)'),
        dcc.Input(
            placeholder='Enter height(in)', type='number',
            min=30, max=88,
            value=data.default_data['general_health_data']['height_in'], id='height_in'),
        dcc.Markdown('---'),
        dcc.Markdown('Weight(lb)'),
        dcc.Input(
            placeholder='Enter weight(lb)', type='number',
            min=75, max=550,
            value=data.default_data['general_health_data']['weight_lb'], id='weight_lb'),
        dcc.Markdown('---'),
        dcc.Markdown('General Health'),
        dcc.Slider(
            id='current_general_health',
            min=1,
            max=5,
            step=1,
            value=data.default_data['bmi_data']['general_health'],
            marks={n: str(n) for n in range(1,6,1)}
            ),
        dcc.Markdown('----'),
        make_checkbox('drink_soda'),
        make_checkbox('drink_diet_soda'),
        make_checkbox('snap_benefits'),
    ],
    md=2,
)


# Available prediction_input_list
prediction_input_list = [
    'height_in', 'weight_lb', 'current_general_health', 'drink_soda',
    'drink_diet_soda', 'snap_benefits'
]


## Callbacks for Column2
@app.callback(
    Output('starting_point', 'children'),
    [Input('height_in', 'value'), Input('weight_lb', 'value'), Input('current_general_health', 'value')],
)
def seed_starting_point(height_in, weight_lb, current_general_health):
    bmi = calculate_bmi(height_in, weight_lb)
    return_div_bmi = html.Div('Current BMI: {:.1f}'.format(bmi))
    return_div_general_health = html.Div('And you feel your health is at a: {}'.format(current_general_health))
    return [return_div_bmi, return_div_general_health]

@app.callback(
    Output('trajectory', 'children'),
    [Input("{}".format(_), "value") for _ in prediction_input_list],
)
def predict_trajectory(*args):
    # Update model_data
    for i, info in enumerate(args):
        info_cleaned = clean_info(info)
        data.update_model_data({prediction_input_list[i]: info_cleaned})
    # Generate new predictions
    predictions = get_predictions()
    # Create DIV elements from dictionary items
    div_list = []
    for prediction in predictions:
        div_list.append(
            dict_to_div(prediction, ': ')
        )

    return div_list

column2 = dbc.Col(
    [
        dcc.Markdown('### Starting Point'),
        html.Div(id='starting_point', className='lead'),
        dcc.Markdown('---'),
        dcc.Markdown('### Trajectory'),
        html.Div(id='trajectory', className='lead'),
    ]
)


layout = [
    dbc.Row(instruction_row),
    dbc.Row([column1, column2]),
    ]