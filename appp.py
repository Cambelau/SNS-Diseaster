from dash import Dash, html, Input, Output
import dash_daq as daq
import  twitter_api 


import threading
import time


should_run = False
class a:
    def __init__(self):
        while True:
            if should_run:
                # twitter_api
                qrrez=2







app = Dash(__name__)

app.layout = html.Div([
    daq.ToggleSwitch(
        id='my-toggle-switch',
        value=False
    ),
    html.Div(id='my-toggle-switch-output')
])


@app.callback(
    Output('my-toggle-switch-output', 'children'),
    Input('my-toggle-switch', 'value')
)
def update_output(value):
    # global should_run
    # should_run = value
    return f'The switch is {value}.'



if __name__ == '__main__':
    # t1 = threading.Thread(target=a,daemon=True)
    # t1.start()
    app.run_server(debug=False, host='0.0.0.0')