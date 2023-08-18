import streamlit as st
import pandas as pd
import altair as alt
import datetime
import json
from altair import datum
from pathlib import Path


st.set_page_config(layout="wide")

st.title("DBT Artifacts - Interactive Altair Demo")


with st.expander("Documentation", expanded=False):
    st.write((Path(__file__).parent.parent / "assets/dbt_artifacts_altair.md").read_text())

weekly_columns = ['project_name', 'dbt_invocation_date', 'dbt_invocation_execution_time', 'rows_affected']

model_columns=[
            'dbt_invocation_date',
            'dbt_invocation_start_time',
            'dbt_invocation_end_time',
            'dbt_invocation_execution_time',
            'project_name',
            'materialization',
            'rows_affected',
            'model_name',
            'start_time',
            'end_time',
            'model_execution_time'
        ]


FILENAME = "assets/artifacts_mock.json"


def get_data(filename: json):
    with open(filename, "r") as f:
        data = json.loads(f.read())
    data_df = pd.DataFrame(data, columns=model_columns)
    data_df['dbt_invocation_date'] = pd.to_datetime(data_df['dbt_invocation_date']).dt.date
    return data_df


data = get_data(FILENAME)
data_agg = data.groupby(['project_name', 'dbt_invocation_date']).agg({'dbt_invocation_execution_time': 'median', 'rows_affected': 'median'}).reset_index()

brush = alt.selection_point()
selection = alt.selection_point(fields=['project_name'], bind='legend')
single = alt.selection_point(fields=['project_name', 'dbt_invocation_start_time'])
date_selection = alt.selection_point(fields=['dbt_invocation_date'])

domain = ['Discount Depot', 'SuperMart', 'ShopSmart']
range_ = ['#c7cb23', 'blue', 'steelblue', 'chartreuse', 'green', 'orange', 'pink', 'violet', 'red']

days_28 = alt.Chart(data_agg).mark_line().encode(
    x='dbt_invocation_date:T',
    y='dbt_invocation_execution_time:Q',
    color='project_name:N'
).properties(
    width=955, height=alt.Step(20)
).add_params(
    selection
).transform_filter(
    selection
)


days_28_point = alt.Chart(data_agg).mark_point().encode(
    x='dbt_invocation_date:T',
    y='dbt_invocation_execution_time:Q',
    color=alt.condition(brush, 'project_name:N', alt.value('lightgray'))
).properties(
    width=955, height=alt.Step(20)
).add_params(
    selection, date_selection, brush
).transform_filter(
    selection & date_selection & brush
)

project_gantt = alt.Chart(data).mark_bar().encode(
    x='dbt_invocation_start_time:T',
    x2='dbt_invocation_end_time:T',
    y=alt.Y('project_name:N', sort='x'),
    color=alt.Color('project_name:N',  title='DBT Project', scale=alt.Scale(domain=domain, range=range_)),
    opacity=alt.condition(selection, alt.value(1), alt.value(0)),
    tooltip=['project_name:N', 'hoursminutesseconds(dbt_invocation_start_time)', 'hoursminutesseconds(dbt_invocation_end_time)', 'dbt_invocation_execution_time']
).add_params(
    single
).properties(
    width=955, height=alt.Step(20)
).transform_filter(
    selection & date_selection
).interactive()


gantt = alt.Chart(data).mark_bar().encode(
    x='start_time:T',
    x2='end_time:T',
    y=alt.Y('model_name:N', sort='x'),
    color='project_name:N',
    tooltip=['project_name:N', 'model_name:N', 'hoursminutesseconds(start_time):T', 'hoursminutesseconds(end_time):T', 'model_execution_time:Q']
).properties(
    width=955, height=alt.Step(20)
).add_params(
    selection
).transform_filter(
    selection & single
)

chart = (days_28 + days_28_point) & project_gantt & gantt

st.altair_chart(chart, theme="streamlit", use_container_width=True)


