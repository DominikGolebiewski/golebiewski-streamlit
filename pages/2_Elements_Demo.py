import json
import duckdb as du
import streamlit as st
import pandas as pd
import datetime
import requests
import tempfile


from streamlit import session_state as ss
from types import SimpleNamespace
from pathlib import Path
from streamlit_elements import dashboard, elements, mui, nivo


FILENAME = "assets/mock_data.json"
GET_DATA_URL = f'https://api.mockaroo.com/api/101c51a0?count=1000&key={st.secrets["MOCKAROO_API"]}'
st.set_page_config(layout="wide")

@st.cache_data
def get_data_url(json_url: str):
    temp_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    request_data = requests.get(json_url).json()
    json.dump(request_data, temp_file)
    temp_file.flush()
    filename = temp_file.name
    return filename

def get_data(filename: str):
    data = du.read_json(filename)
    return data

def get_retailer(data: json):
    retailer_data = du.sql("SELECT retailer FROM 'data' GROUP BY retailer").df()
    return retailer_data['retailer'].values.tolist()


def filtered_data(data: json, retailer: str):
    filtered = du.sql(f"SELECT * FROM 'data' WHERE retailer = '{retailer}'")
    return filtered


def serialize_datetime(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def pie_28_cat(data: json, retailer: str):
    pie_data = du.sql(f"SELECT category as id, SUM(sales) as value FROM 'data' WHERE retailer = '{retailer}' GROUP BY id").df()
    pie_data_dict = pie_data.to_dict(orient='records')
    pie_28_json = json.dumps(pie_data_dict, indent=2, default=serialize_datetime)
    return pie_28_json

def bar_28(data: json, retailer: str):
    bar_28_df = du.sql(f"""
        WITH filterd_data AS (
            SELECT 
                date, 
                SUM(sales) as sales 
            FROM 'data' 
            WHERE retailer = '{retailer}'
            AND category = IF('{ss.pie_category}' = 'all', category , '{ss.pie_category}')
            GROUP BY date
        ),
        filtered_date as (
            SELECT 
                *,
                EXTRACT(DOW FROM IF('{ss.time_chart.day}' != '{None}', DATE '{ss.time_chart.day}', date)) as day_of_week
            FROM filterd_data
            WHERE EXTRACT(DOW FROM date) = day_of_week
        )
        SELECT
            date,
            sales
        FROM filtered_date
        ORDER BY date
    """).df()
    bar_28_df['date'] = pd.to_datetime(bar_28_df['date']).dt.date
    bar_28_dict = bar_28_df.to_dict(orient='records')
    bar_28_json = json.dumps(bar_28_dict, indent=2, default=serialize_datetime)
    return bar_28_json


def cal_28(data: json, retailer: str):
    cal_28_df = du.sql(f"""
        SELECT 
            date as day, 
            SUM(sales) as value 
        FROM 'data' 
        WHERE retailer = '{retailer}' 
        AND category = IF('{ss.pie_category}' = 'all', category , '{ss.pie_category}')
        GROUP BY date
    """).df()
    cal_28_df['day'] = pd.to_datetime(cal_28_df['day']).dt.date
    cal_28_mindate = cal_28_df['day'].min()
    cal_28_maxdate = cal_28_df['day'].max()
    cal_28_dict = cal_28_df.to_dict(orient='records')
    cal_28_json = json.dumps(cal_28_dict, indent=2, default=serialize_datetime)
    return cal_28_json, str(cal_28_mindate), str(cal_28_maxdate)

def pie_total(data: json, retailer: str):
    pie_total_df = du.sql(f"SELECT retailer as id, SUM(sales) as value FROM 'data' GROUP BY id").df()
    pie_total_dict = pie_total_df.to_dict(orient='records')
    pie_total_json = json.dumps(pie_total_dict, indent=2, default=serialize_datetime)
    return pie_total_json

def pie_category_callback(event):
    ss.pie_category = event.id
    ss.pie_category_color = event.color

def reset_pie_category(event):
    ss.pie_category = "all"
    ss.pie_category_color = "grey"

def reset_time_chart(event):
    ss.time_chart.day = None
    ss.time_chart.firstWeek = None

def time_range_callback(info):
    ss.time_chart.day = info.day
    ss.time_chart.firstWeek = info.firstWeek

def main():

    st.title("Elements Demo")

    data = get_data(FILENAME)
    retailer = get_retailer(data)

    with st.sidebar:
        selected_retailer = st.selectbox("Retailer", retailer, key="retailer_select")

    with st.expander("Documentation", expanded=False):
        st.write((Path(__file__).parent.parent / "assets/elements_demo.md").read_text())

    filtered_df = filtered_data(data, selected_retailer)

    layout = [
        dashboard.Item("pie_28_cat", 0, 0, 3, 3),
        dashboard.Item("cal_28", 4, 0, 9, 3),
        dashboard.Item("bar_28", 0, 1, 12, 4),
    ]

    with elements("dashboard"):

        with dashboard.Grid(layout):
            with mui.Paper(key="pie_28_cat", sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=5):

                pie_28_data = pie_28_cat(data, selected_retailer)

                with mui.Box(sx={"display": "flex", "flexDirection": "row", "borderBottom": 3, "borderColor": "divider"}):
                    mui.icon.PieChart(sx={"padding": 1})
                    mui.Typography("28 Day Total Sales by Category", sx={"padding": 1})
                    mui.Button(
                        "Reset Filter",
                        variant="outlined",
                        sx={
                            "marginLeft": "auto",
                            "marginRight": "1",
                            "marginTop": "1",
                            "marginBottom": "1",
                            "color": "black",
                            "borderColor": None,
                            "borderRadius": 0,
                            "borderWidth": 0,
                            "borderStyle": "solid",
                            "textTransform": "none",
                            "fontSize": "0.75rem",
                            "fontWeight": "bold",
                            "fontSize": 12,
                            "transition": "none",
                            '&:hover': {
                                'color': 'red',
                                'backgroundColor': 'white',
                                'borderColor': 'white',
                            },
                        },
                        disableRipple=True,
                        onClick=reset_pie_category)

                with mui.Box(sx={"flex": 1, "minHeight": 0}):
                    nivo.Pie(
                        onClick=pie_category_callback,
                        data=json.loads(pie_28_data),
                        theme="light",
                        margin={"top": 40, "right": 80, "bottom": 80, "left": 80},
                        innerRadius=0.5,
                        padAngle=0.7,
                        cornerRadius=3,
                        activeOuterRadiusOffset=8,
                        colors={'scheme': 'pastel1'},
                        borderWidth=1,
                        borderColor={
                            "from": "color",
                            "modifiers": [
                                [
                                    "darker",
                                    0.2,
                                ]
                            ]
                        },
                        arcLinkLabelsSkipAngle=10,
                        arcLinkLabelsTextColor="grey",
                        arcLinkLabelsThickness=2,
                        arcLinkLabelsColor={"from": "color"},
                        arcLabelsSkipAngle=10,
                        arcLabelsTextColor={
                            "from": "color",
                            "modifiers": [
                                [
                                    "darker",
                                    2
                                ]
                            ]
                        },
                        enableArcLabels=False,
                        motionConfig="wobbly"
                    )
            with mui.Paper(key="bar_28", sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=5):

                bar_28_data = bar_28(data, selected_retailer)

                with mui.Box(sx={"display": "flex", "flexDirection": "row", "borderBottom": 3, "borderColor": "divider"}):
                    mui.icon.BarChart(sx={ "padding": 1})
                    mui.Typography("28 Day Sales", sx={ "padding": 1})
                with mui.Box(sx={"flex": 1, "minHeight": 0}):
                    nivo.Bar(
                        data=json.loads(bar_28_data),
                        keys=["sales"],
                        indexBy="date",
                        theme="light",
                        margin={"top": 50, "right": 100, "bottom": 100, "left": 100},
                        padding=0.5,
                        valueScale={'type': 'linear'},
                        indexScale={'type': 'band', 'round': True},
                        colors=ss.pie_category_color,
                        enableLabel=False,
                        borderColor={
                            "from": "color",
                            "modifiers": [
                                [
                                    "darker",
                                    0.2,
                                ]
                            ]
                        },
                        axisBottom={
                            'tickSize': 5,
                            'tickPadding': 5,
                            'tickRotation': 90,
                            'legend': 'Date',
                            'legendPosition': 'middle',
                            'legendOffset': 80
                        },
                        axisLeft={
                            'tickSize': 5,
                            'tickPadding': 0,
                            'tickRotation': 0,
                            'legend': 'Sales Value',
                            'legendPosition': 'middle',
                            'legendOffset': -40
                        },
                        motionConfig="wobbly"
                    )
            with mui.Paper(key="cal_28", sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=5):

                cal_28_data, min_date, max_date = cal_28(data, selected_retailer)

                with mui.Box(sx={"display": "flex", "flexDirection": "row", "borderBottom": 3, "borderColor": "divider"}):
                    mui.icon.CalendarToday(sx={"padding": 1})
                    mui.Typography("28 Day Sales Calendar", sx={"padding": 1})
                    mui.Button(
                        "Reset Filter",
                        variant="outlined",
                        sx={
                            "marginLeft": "auto",
                            "marginRight": "1",
                            "marginTop": "1",
                            "marginBottom": "1",
                            "color": "black",
                            "borderColor": None,
                            "borderRadius": 0,
                            "borderWidth": 0,
                            "borderStyle": "solid",
                            "textTransform": "none",
                            "fontSize": "0.75rem",
                            "fontWeight": "bold",
                            "fontSize": 12,
                            "transition": "none",
                            '&:hover': {
                                'color': 'red',
                                'backgroundColor': 'white',
                                'borderColor': 'white',
                            },
                        },
                        disableRipple=True,
                        onClick=reset_time_chart)
                with mui.Box(sx={"flex": 1, "minHeight": 0}):
                    nivo.TimeRange(
                        onClick=time_range_callback,
                        data=json.loads(cal_28_data),
                        from_ = min_date,
                        to=max_date,
                        emptyColor="#eeeeee",
                        colors=['#61cdbb', '#97e3d5', '#e8c1a0', '#f47560'],
                        margin = {'top': 40, 'right': 40, 'bottom': 40, 'left': 40},
                        dayBorderWidth = 3,
                        dayBorderColor = "#ffffff",
                        weekdayTicks = [0,1,2,3,4,5,6],
                        legends=[
                            {
                                'anchor': 'top-right',
                                'direction': 'column',
                                'justify': True,
                                'itemCount': 5,
                                'itemWidth': 42,
                                'itemHeight': 36,
                                'itemsSpacing': 14,
                                'itemDirection': 'right-to-left',
                                'translateX': -50,
                                'translateY': 0,
                                'symbolSize': 20
                            }
                        ]
                    )

if __name__ == "__main__":
    if "pie_category" not in ss:
        ss.pie_category = "all"
    else:
        ss.pie_category = ss.pie_category
    if "pie_category_color" not in ss:
        ss.pie_category_color = "grey"
    else:
        ss.pie_category_color = ss.pie_category_color
    # if "time_range" not in ss:
    #     ss.time_range = None
    # else:
    #     ss.time_range = ss.time_range
    if "time_chart" not in ss:
        time_chart = SimpleNamespace(
            firstWeek=None,
            day=None)
        ss.time_chart = time_chart
        time_chart.firstWeek = None
        time_chart.range = None
    else:
        time_chart = ss.time_chart
    main()
