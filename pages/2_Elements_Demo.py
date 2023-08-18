import json
import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import datetime
from streamlit_elements import dashboard, elements, mui, nivo
from types import SimpleNamespace
from pathlib import Path


FILENAME = "assets/mock_data.json"


def get_data(filename: json):
    with open(filename, "r") as f:
        data = json.loads(f.read())
    data_df = pd.DataFrame(data, columns=['date', 'retailer', 'category', 'product', 'sales'])
    data_df['date'] = pd.to_datetime(data_df['date']).dt.date
    return data_df


def get_retailer(dataframe):
    return dataframe['retailer'].unique().tolist()


def filtered_data(dataframe, retailer):
    return dataframe.query('retailer == ' + "'" + retailer + "'")


def serialize_datetime(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def main():

    st.title("Elements Demo")

    data = get_data(FILENAME)
    retailer = get_retailer(data)

    with st.sidebar:
        selected_retailer = st.selectbox("Retailer", retailer, key="retailer_select")

    with st.expander("Documentation", expanded=False):
        st.write((Path(__file__).parent.parent / "assets/elements_demo.md").read_text())

    filtered_df = filtered_data(data, selected_retailer)

    # st.write(line_data)
    # exit()

    layout = [
        dashboard.Item("pie_28_cat", 8, 0, 4, 3),
        dashboard.Item("pie_28_ret", 0, 0, 4, 3),
        dashboard.Item("cal_28", 4, 0, 4, 3),
        # dashboard.Item("today", 4, 0, 4, 3),
        dashboard.Item("bar_28", 0, 1, 12, 3),


    ]

    with elements("dashboard"):

        with dashboard.Grid(layout):
            with mui.Paper(key="pie_28_cat", sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=5):

                pie_28_df = filtered_df.groupby(['category']).agg({'sales': 'sum'}).reset_index()
                pie_28_dict = pie_28_df.to_dict(orient='records')
                pie_28_rename = pd.DataFrame(pie_28_dict).rename(columns={'category': 'id', 'sales': 'value'})
                pie_28_df = pd.pivot_table(pie_28_rename, values='value', index='id',aggfunc='sum').reset_index().to_dict(orient='records')
                pie_28_json = json.dumps(pie_28_df, indent=2, default=serialize_datetime)

                with mui.Box(sx={"display": "flex", "flexDirection": "row", "borderBottom": 3, "borderColor": "divider"}):
                    mui.icon.PieChart(sx={"padding": 1})
                    mui.Typography("28 Day Total Sales by Category", sx={"padding": 1})

                with mui.Box(sx={"flex": 1, "minHeight": 0}):
                    nivo.Pie(
                        data=json.loads(pie_28_json),
                        theme="light",
                        margin={"top": 40, "right": 80, "bottom": 80, "left": 80},
                        innerRadius=0.5,
                        padAngle=0.7,
                        cornerRadius=3,
                        activeOuterRadiusOffset=8,
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

                bar_28_df = filtered_df.groupby(['date', 'retailer']).agg({'sales': 'sum'}).reset_index().to_dict(orient='records')
                bar_28_json = json.dumps(bar_28_df, indent=2, default=serialize_datetime)

                with mui.Box(sx={"display": "flex", "flexDirection": "row", "borderBottom": 3, "borderColor": "divider"}):
                    mui.icon.BarChart(sx={ "padding": 1})
                    mui.Typography("28 Day Sales", sx={ "padding": 1})
                with mui.Box(sx={"flex": 1, "minHeight": 0}):
                    nivo.Bar(
                        data=json.loads(bar_28_json),
                        keys=["sales"],
                        indexBy="date",
                        theme="light",
                        margin={"top": 50, "right": 100, "bottom": 100, "left": 100},
                        padding=0.5,
                        valueScale={'type': 'linear'},
                        indexScale={'type': 'band', 'round': True},
                        colors=['grey'],
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
                            'tickRotation': 45,
                            'legend': 'Date',
                            'legendPosition': 'middle',
                            'legendOffset': 65
                        },
                        axisLeft={
                            'tickSize': 5,
                            'tickPadding': 0,
                            'tickRotation': 0,
                            'legend': 'Sales Value',
                            'legendPosition': 'middle',
                            'legendOffset': -65
                        },
                        motionConfig="wobbly"
                    )
            with mui.Paper(key="cal_28", sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=5):

                cal_28_df = filtered_df.groupby(['date']).agg({'sales': 'sum'}).reset_index().to_dict(orient='records')
                cal_28_rename = pd.DataFrame(cal_28_df).rename(columns={'date': 'day', 'sales': 'value'})
                cal_28_dict = cal_28_rename.to_dict(orient='records')
                cal_28_json = json.dumps(cal_28_dict, indent=2, default=serialize_datetime)

                with mui.Box(sx={"display": "flex", "flexDirection": "row", "borderBottom": 3, "borderColor": "divider"}):
                    mui.icon.CalendarToday(sx={"padding": 1})
                    mui.Typography("28 Day Sales Calendar", sx={"padding": 1})
                with mui.Box(sx={"flex": 1, "minHeight": 0}):
                    nivo.TimeRange(
                        data=json.loads(cal_28_json),
                        from_ = "2023-07-01",
                        to="2023-07-28",
                        emptyColor="#eeeeee",
                        colors=['#61cdbb', '#97e3d5', '#e8c1a0', '#f47560'],
                        margin = {'top': 40, 'right': 40, 'bottom': 40, 'left': 40},
                        dayBorderWidth = 3,
                        dayBorderColor = "#ffffff",
                        weekdayTicks = [0,1,2,3,4,5,6],
                        legends=[
                            {
                                'anchor': 'right',
                                'direction': 'column',
                                'justify': True,
                                'itemCount': 5,
                                'itemWidth': 42,
                                'itemHeight': 36,
                                'itemsSpacing': 14,
                                'itemDirection': 'right-to-left',
                                'translateX': -60,
                                'translateY': -40,
                                'symbolSize': 20
                            }
                        ]
                    )
            with mui.Paper(key="pie_28_ret", sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=5):

                pie_28_ret_df = data.groupby(['retailer']).agg({'sales': 'sum'}).reset_index()
                pie_28_ret_dict = pie_28_ret_df.to_dict(orient='records')
                pie_28_ret_rename = pd.DataFrame(pie_28_ret_dict).rename(columns={'retailer': 'id', 'sales': 'value'})
                pie_28_ret_df = pd.pivot_table(pie_28_ret_rename, values='value', index='id',aggfunc='sum').reset_index().to_dict(orient='records')
                pie_28_ret_json = json.dumps(pie_28_ret_df, indent=2, default=serialize_datetime)

                with mui.Box(sx={"display": "flex", "flexDirection": "row", "borderBottom": 3, "borderColor": "divider"}):
                    mui.icon.PieChart(sx={"padding": 1})
                    mui.Typography("28 Day Total Sales by Retailer", sx={"padding": 1})

                with mui.Box(sx={"flex": 1, "minHeight": 0}):
                    nivo.Pie(
                        data=json.loads(pie_28_ret_json),
                        theme="light",
                        margin={"top": 40, "right": 80, "bottom": 80, "left": 80},
                        innerRadius=0.5,
                        padAngle=0.7,
                        cornerRadius=3,
                        activeOuterRadiusOffset=8,
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
                        }
                    )
            # with mui.Paper(key="today", sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=5):
            #
            #     today_df = filtered_df.groupby(['date']).agg({'sales': 'sum'}).reset_index().to_dict(orient='records')
            #     today_df_latast_date = max(today_df, key=lambda x: x['date'])
            #     yesterday_df_latast_date = today_df_latast_date['date'] - datetime.timedelta(days=1)
            #     today_df_yesterday_sales_date = filtered_df.query(f'date == "{str(yesterday_df_latast_date).strip()}"')
            #     st.write(today_df_latast_date)
            #
            #     with mui.Box(sx={"display": "flex", "flexDirection": "row", "borderBottom": 3, "borderColor": "divider"}):
            #         mui.icon.PieChart(sx={"padding": 1})
            #         mui.Typography("Sales Today", sx={"padding": 1})
            #     with mui.Box():
            #         with mui.Box(sx = {"color": "text.secondary", "padding": 1} ):
            #             mui.Typography("Today Sales", sx = {"display": "flex", 'fontSize': 30, 'fontWeight': 'light', "allign": "center"})
            #             mui.Typography(f'£{today_df_latast_date["sales"]}', sx={ 'color': 'text.primary', 'fontSize': 34, 'fontWeight': 'medium' })

            # with mui.Paper(key="line_28", sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=5):
            #
            #     line_28_df = data.groupby(['date', 'retailer']).agg({'sales': 'sum'}).reset_index().sort_values(by=['retailer', 'date'])
            #     line_28_dict = pd.DataFrame(line_28_df).to_dict(orient='records')
            #     line_data = []
            #     for r in retailer:
            #         merged_data = []
            #         for entry in line_28_dict:
            #             if entry["retailer"] == r:
            #                 merged_data.append({"x": entry["date"], "y": entry["sales"]})
            #
            #         line_data.append({"id": r, "data": merged_data})
            #     line_28_json = json.dumps(line_data, indent=2, default=serialize_datetime)
            #
            #     with mui.Box(sx={"display": "flex", "flexDirection": "row", "borderBottom": 3, "borderColor": "divider"}):
            #         mui.icon.CalendarToday(sx={"padding": 1})
            #         mui.Typography("28 Day Sales Calendar", sx={"padding": 1})
            #     with mui.Box(sx={"flex": 1, "minHeight": 0}):
            #         nivo.Bump(
            #             data=json.loads(line_28_json),
            #             colors = {'scheme': 'nivo'},
            #             lineWidth = 3,
            #             activeLineWidth = 6,
            #             inactiveLineWidth = 3,
            #             inactiveOpacity = 0.15,
            #             pointSize = 10,
            #             activePointSize = 16,
            #             inactivePointSize = 0,
            #             pointColor = {'theme': 'background'},
            #             pointBorderWidth = 3,
            #             activePointBorderWidth = 3,
            #             pointBorderColor = {'from': 'serie.color'},
            #             axisTop = {
            #                 'tickSize': 5,
            #                 'tickPadding': 5,
            #                 'tickRotation': 45,
            #                 'legend': '',
            #                 'legendPosition': 'middle',
            #                 'legendOffset': -36
            #             },
            #             axisBottom = {
            #                 'tickSize': 5,
            #                 'tickPadding': 5,
            #                 'tickRotation': 45,
            #                 'legend': '',
            #                 'legendPosition': 'middle',
            #                 'legendOffset': 32
            #             },
            #             axisLeft = {
            #                 'tickSize': 5,
            #                 'tickPadding': 5,
            #                 'tickRotation': 0,
            #                 'legend': 'ranking',
            #                 'legendPosition': 'middle',
            #                 'legendOffset': -40
            #             },
            #             margin = {'top': 70, 'right': 100, 'bottom': 70, 'left': 60}
            #         )

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()