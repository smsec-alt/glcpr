import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
pd.options.mode.chained_assignment = None


def get_chart(df: pd.DataFrame, x_values:str, y_values:str, title:str, color=None, labels=None, logs=False):
    if logs:
        df[y_values] = np.log(df[y_values])
    fig = px.line(df, x=x_values, y=y_values,
                        color=color, title=title,
                        color_discrete_sequence=px.colors.qualitative.G10,
                        labels=labels)
    fig.update_layout(hovermode="x unified", width=1000, height=600, plot_bgcolor='white', 
                      xaxis=dict(gridcolor='#FFFFFF',tickformat="%d %b %Y", linecolor='rgb(204, 204, 204)',
                                 linewidth=1, ticks='outside', tickfont=dict(size=12)),
                      yaxis=dict(gridcolor='#F8F8F8', tickfont=dict(size=12)))
    return fig


def get_seasonality_chart(df: pd.DataFrame, x_values:str, y_values:str, title:str, labels=None):
    df['DATE'] = df[x_values] + pd.offsets.DateOffset(year=2020)
    df['YEAR'] = df[x_values].dt.year
    current_year = df['YEAR'].max()
    hist_df = df[df['YEAR']<current_year-1]
    summary_df = hist_df.pivot_table(index='DATE', columns='YEAR', values=y_values).interpolate()
    summary_df['Mean'] = summary_df.mean(axis=1)
    summary_df['Max'] = summary_df.max(axis=1)
    summary_df['Min'] = summary_df.min(axis=1)

    fig = px.line(hist_df, x='DATE', y=y_values,
                    color_discrete_sequence=px.colors.qualitative.G10, color='YEAR',
                    labels=labels)
    # labels={y_values:'', 'DATE':'', 'YEAR':'Year'})
    fig.update_traces(visible="legendonly")

    fig.add_trace(go.Scatter(x=summary_df.index, y=summary_df['Max'], name='',
                                fill=None, mode='lines', line_color='#D3D3D3', line=dict(width=0)))
    fig.add_trace(go.Scatter(x=summary_df.index, y=summary_df['Min'], name='Max-Min',
                                fill='tonexty', mode='lines', line_color='#D3D3D3', line=dict(width=0)))
    fig.add_trace(
        go.Scatter(x=summary_df.index, y=summary_df['Mean'], name='Mean', line=dict(dash='dot', width=2),
                    fill=None, mode='lines', line_color='#0047AB'))
    fig.add_trace(go.Scatter(x=df[df['YEAR']==current_year-1]['DATE'],
                                y=df[df['YEAR']==current_year-1][y_values],
                                fill=None, name=str(current_year-1),
                                line=dict(color='#000000')))
    fig.add_trace(go.Scatter(x=df[df['YEAR']==current_year]['DATE'],
                                y=df[df['YEAR']==current_year][y_values],
                                fill=None, name=str(current_year),
                                line=dict(color='firebrick')))

    fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickformat="%b %d",
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                showgrid=True,
                zeroline=True,
                showline=True,
                showticklabels=True,
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ), font=dict(color='rgb(82, 82, 82)', family='Arial'),
            autosize=False,
            width=1300,
            title=title,
            height=500,
            showlegend=True,
            plot_bgcolor='white',
            hovermode='x unified',
            legend={'traceorder': 'reversed'},
        )
    return fig
