import plotly.graph_objects as go

def create_gauge(score):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "ATS Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "green"},
                "steps": [
                    {"range": [0, 50], "color": "#ff4b4b"},
                    {"range": [50, 80], "color": "#f39c12"},
                    {"range": [80, 100], "color": "#2ecc71"},
                ],
            },
        )
    )

    fig.update_layout(height=300)

    return fig