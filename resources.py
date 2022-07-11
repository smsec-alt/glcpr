import numpy as np
import pandas as pd
import plotly.express as px



def get_chart(df: pd.DataFrame, x_values:str, y_values:str, title:str, color=None, labels=None, logs=False):
    if logs:
        df[y_values] = np.log(df[y_values])
    fig = px.line(df, x=x_values, y=y_values,
                        color=color, title=title,
                        color_discrete_sequence=px.colors.qualitative.G10,
                        labels=labels)
    # "%b %d"
    fig.update_layout(hovermode="x unified", width=1000, height=600, plot_bgcolor='white', 
                      xaxis=dict(gridcolor='#FFFFFF',tickformat="%d %b %Y", linecolor='rgb(204, 204, 204)',
                                 linewidth=1, ticks='outside', tickfont=dict(size=12)),
                      yaxis=dict(gridcolor='#F8F8F8', tickfont=dict(size=12)))
    return fig