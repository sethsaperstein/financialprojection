# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

from NetWorthCalculator import NetWorthCalculator

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Retirement Calculator'),

    html.Div(children='''
        A retirement calculator built just for me
    '''),

    dcc.Graph(id='net-worth-graph'),

    html.Br(),
    html.Label('Yearly Spend'),
    dcc.Slider(
        min=40000,
        max=70000,
        marks={i: str(i) for i in range(40000, 70000, 1000)},
        value=53000,
        id='yearly-spend',
    ),

    html.Br(),
    html.Label('Yearly Return Percent'),
    dcc.Slider(
        min=-10,
        max=25,
        marks={i: str(i) for i in range(-10, 25, 1)},
        value=7,
        id='yearly-return-percent',
    ),

    html.Br(),
    html.Label('Yearly Comp Growth Percent'),
    dcc.Slider(
        min=-20,
        max=20,
        marks={i: str(i) for i in range(-20, 20, 1)},
        value=5,
        id='yearly-comp-growth-percent',
    ),

    html.Br(),
    html.Label('Initial Investment Amount: '),
    dcc.Input(type='number', id='initial-investments', value=237000),

    html.Br(),
    html.Label('Initial Savings Amount: '),
    dcc.Input(type='number', id='initial-savings', value=20000),

    html.Br(),
    html.Label('Initial Age: '),
    dcc.Input(type='number', id='initial-age', value=25),

    html.Br(),
    html.Label('Pre Tax Initial Income: '),
    dcc.Input(type='number', id='initial-income', value=314000),
])


@app.callback(
    Output('net-worth-graph', 'figure'),
    Input('yearly-spend', 'value'),
    Input('yearly-return-percent', 'value'),
    Input('yearly-comp-growth-percent', 'value'),
    Input('initial-investments', 'value'),
    Input('initial-savings', 'value'),
    Input('initial-income', 'value'),
    Input('initial-age', 'value'),
)
def update_figure(
        yearly_spend: int,
        yearly_return_pct: int,
        yearly_comp_growth_pct: int,
        initial_investments: int,
        initial_savings: int,
        initial_income: int,
        initial_age: int,
):
    if (
        yearly_spend is None or
        yearly_return_pct is None or
        yearly_comp_growth_pct is None or
        initial_investments is None or
        initial_savings is None or
        initial_income is None or
        initial_age is None
    ):
        df = pd.DataFrame({
            "age": [],
            "net worth": [],
        })
        return px.line(df, x="age", y="net worth")

    calculator = NetWorthCalculator(
        initial_investments=float(initial_investments),
        initial_savings=float(initial_savings),
        initial_income=initial_income,
        yearly_costs=yearly_spend,
        rate_of_return=float(yearly_return_pct/100.0),
        rate_of_comp_growth=float(yearly_comp_growth_pct/100.0),
        initial_age=initial_age,
    )
    ages, net_worths = calculator.calculate_net_worth()

    df = pd.DataFrame({
        "age": ages,
        "net worth": net_worths,
    })

    fig = px.line(df, x="age", y="net worth")

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
