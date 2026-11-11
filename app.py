import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go

from core.twin_engine import BioreactorTwinEngine
from services.logger import SimulationLogger
from ui.svg_bioreactor import generate_bioreactor_svg

engine = BioreactorTwinEngine()
logger = SimulationLogger()
logger.log(engine.state)

app = dash.Dash(__name__, title="Bioreactor Digital Twin")

app.layout = html.Div(style={'backgroundColor': '#0f172a', 'color': '#f8fafc', 'minHeight': '100vh', 'padding': '20px', 'fontFamily': 'Segoe UI, sans-serif'}, children=[
    
    # Header
    html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'borderBottom': '1px solid #334155', 'paddingBottom': '15px'}, children=[
        html.Div([
            html.H1("Jumeau Virtuel de Bioreacteur", style={'margin': '0', 'fontSize': '26px', 'color': '#38bdf8'}),
            html.P("Controle de Bioprocede Temps Reel (Monod / ODE)", style={'margin': '5px 0 0 0', 'color': '#94a3b8'})
        ]),
        html.Div([
            html.Button("Demarrer", id="btn-toggle", n_clicks=0, style={'backgroundColor': '#10b981', 'color': 'white', 'border': 'none', 'padding': '10px 20px', 'borderRadius': '6px', 'cursor': 'pointer', 'fontWeight': 'bold', 'marginRight': '10px'}),
            html.Button("Reinitialiser", id="btn-reset", n_clicks=0, style={'backgroundColor': '#ef4444', 'color': 'white', 'border': 'none', 'padding': '10px 20px', 'borderRadius': '6px', 'cursor': 'pointer', 'fontWeight': 'bold'})
        ])
    ]),
    
    # Grille Principale
    html.Div(style={'display': 'grid', 'gridTemplateColumns': '300px 330px 1fr', 'gap': '20px', 'marginTop': '20px'}, children=[
        
        # Sliders
        html.Div(style={'backgroundColor': '#1e293b', 'padding': '20px', 'borderRadius': '10px', 'border': '1px solid #334155'}, children=[
            html.H3("Consignes Operationnelles", style={'marginTop': '0', 'color': '#38bdf8', 'fontSize': '18px'}),
            html.Label("Agitation (RPM)", style={'color': '#cbd5e1'}),
            dcc.Slider(id="slider-rpm", min=100, max=800, step=50, value=300, marks={100: '100', 400: '400', 800: '800'}, tooltip={"placement": "bottom", "always_visible": True}),
            html.Br(),
            html.Label("Debit Alimentation Feed (L/h)", style={'color': '#cbd5e1'}),
            dcc.Slider(id="slider-feed", min=0.0, max=0.5, step=0.05, value=0.0, marks={0: '0', 0.25: '0.25', 0.5: '0.5'}, tooltip={"placement": "bottom", "always_visible": True}),
            html.Br(),
            html.Label("Substrat Alimentation S_in (g/L)", style={'color': '#cbd5e1'}),
            dcc.Slider(id="slider-sin", min=10, max=200, step=10, value=100, marks={10: '10', 100: '100', 200: '200'}, tooltip={"placement": "bottom", "always_visible": True}),
        ]),

        # Iframe Persistant pour le Schéma SVG
        html.Div(style={'backgroundColor': '#1e293b', 'padding': '20px', 'borderRadius': '10px', 'border': '1px solid #334155', 'textAlign': 'center', 'overflow': 'hidden'}, children=[
            html.H3("Schema du Reacteur", style={'marginTop': '0', 'color': '#38bdf8', 'fontSize': '18px'}),
            html.Iframe(id="svg-iframe", style={'width': '100%', 'height': '300px', 'border': 'none', 'overflow': 'hidden'})
        ]),

        # Graphiques
        html.Div(style={'backgroundColor': '#1e293b', 'padding': '20px', 'borderRadius': '10px', 'border': '1px solid #334155'}, children=[
            dcc.Graph(id="graph-biomass", style={'height': '270px'}),
            dcc.Graph(id="graph-do", style={'height': '230px'})
        ])
    ]),
    
    dcc.Interval(id="interval-timer", interval=1000, n_intervals=0, disabled=True)
])


@app.callback(
    Output("interval-timer", "disabled"),
    Output("btn-toggle", "children"),
    Output("btn-toggle", "style"),
    Input("btn-toggle", "n_clicks"),
    State("interval-timer", "disabled"),
    prevent_initial_call=True
)
def toggle_simulation(n_clicks, is_disabled):
    if n_clicks == 0:
        return True, "Demarrer", {'backgroundColor': '#10b981', 'color': 'white', 'border': 'none', 'padding': '10px 20px', 'borderRadius': '6px', 'cursor': 'pointer', 'fontWeight': 'bold'}
    
    new_disabled = not is_disabled
    btn_text = "Pause" if not new_disabled else "Reprendre"
    btn_color = '#f59e0b' if not new_disabled else '#10b981'
    
    return new_disabled, btn_text, {'backgroundColor': btn_color, 'color': 'white', 'border': 'none', 'padding': '10px 20px', 'borderRadius': '6px', 'cursor': 'pointer', 'fontWeight': 'bold'}


@app.callback(
    Output("svg-iframe", "srcDoc"),
    Output("graph-biomass", "figure"),
    Output("graph-do", "figure"),
    Input("interval-timer", "n_intervals"),
    Input("btn-reset", "n_clicks"),
    State("slider-rpm", "value"),
    State("slider-feed", "value"),
    State("slider-sin", "value"),
    State("interval-timer", "disabled")
)
def update_simulation(n_intervals, reset_clicks, rpm, feed, s_in, is_disabled):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else ""

    if triggered_id == "btn-reset":
        global engine, logger
        engine = BioreactorTwinEngine()
        logger = SimulationLogger()
        logger.log(engine.state)
    elif not is_disabled:
        engine.step(dt=0.2, F_in=feed or 0.0, S_in=s_in or 100.0, RPM=rpm or 300.0)
        logger.log(engine.state)

    df = logger.to_dataframe()
    current_state = engine.state

    svg_html = generate_bioreactor_svg(
        volume=current_state.volume,
        rpm=current_state.agitation,
        do=current_state.dissolved_o2,
        is_running=not is_disabled
    )

    fig_bio = go.Figure()
    fig_bio.add_trace(go.Scatter(x=df["time"], y=df["biomass"], mode='lines', name='Biomasse X (g/L)', line=dict(color='#10b981', width=3)))
    fig_bio.add_trace(go.Scatter(x=df["time"], y=df["substrate"], mode='lines', name='Substrat S (g/L)', line=dict(color='#38bdf8', width=2)))
    fig_bio.add_trace(go.Scatter(x=df["time"], y=df["product"], mode='lines', name='Produit P (g/L)', line=dict(color='#a855f7', width=2)))
    fig_bio.update_layout(
        title="Cinetique Cellulaire Temps Reel",
        paper_bgcolor='#1e293b', plot_bgcolor='#0f172a',
        font=dict(color='#cbd5e1'), margin=dict(l=40, r=20, t=40, b=30),
        xaxis=dict(title="Temps (h)", gridcolor='#334155'),
        yaxis=dict(title="Concentration (g/L)", gridcolor='#334155'),
        uirevision="constant"
    )

    fig_do = go.Figure()
    fig_do.add_trace(go.Scatter(x=df["time"], y=df["dissolved_o2"], mode='lines', name='Oxygene DO (%)', line=dict(color='#ef4444', width=2)))
    fig_do.update_layout(
        title="Oxygene Dissous (% Saturation)",
        paper_bgcolor='#1e293b', plot_bgcolor='#0f172a',
        font=dict(color='#cbd5e1'), margin=dict(l=40, r=20, t=40, b=30),
        xaxis=dict(title="Temps (h)", gridcolor='#334155'),
        yaxis=dict(title="O2 (%)", range=[0, 110], gridcolor='#334155'),
        uirevision="constant"
    )

    return svg_html, fig_bio, fig_do


if __name__ == "__main__":
    app.run(debug=False, port=8050)
