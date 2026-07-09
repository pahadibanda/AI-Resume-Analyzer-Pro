import plotly.express as px
import pandas as pd


def create_skill_chart(skills):

    if not skills:
        skills = ["No Skills Found"]

    df = pd.DataFrame({
        "Skills": skills,
        "Count": [1] * len(skills)
    })

    fig = px.bar(
        df,
        x="Skills",
        y="Count",
        title="Resume Skills",
        text="Count"
    )

    fig.update_layout(
        xaxis_title="Skills",
        yaxis_title="Count",
        height=400
    )

    return fig