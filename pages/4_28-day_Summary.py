import json
import duckdb as du
import streamlit as st
import pandas as pd
import datetime
import requests
import tempfile
from streamlit import session_state as state
from types import SimpleNamespace
from pathlib import Path
from streamlit_elements import dashboard, elements, mui, nivo, html
from pages.dash.dashboard import Dashboard
from pages.dash.metricstoday import MetricsToday
from pages.dash.category import CategorySales
from pages.dash.calendar import CalendarHeatmap
from pages.dash.dailysales import DailySales
from pages.dash.footer import Footer


st.set_page_config(layout="wide")
FILENAME = "assets/mock_28.json"


def serialize_datetime(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def dump_json(dataframe):
    data_dict = dataframe.to_dict(orient="records")
    data_json = json.dumps(data_dict, indent=2, default=serialize_datetime)
    return data_json


@st.cache_data
def get_retailer(filename):
    query = f"""
        select retailer
        from '{filename}'
        group by 1
        order by 1
    """
    data = du.sql(query).df()
    return data['retailer'].values.tolist()


@st.cache_data
def get_supplier(filename):
    query = f"""
        select supplier
        from '{filename}'
        group by 1
        order by 1
    """
    data = du.sql(query).df()
    return data['supplier'].values.tolist()


@st.cache_data
def get_data_mock(filename: str, retailer: str, supplier: str):
    query = f"""
        select * 
        from '{filename}'
        where retailer = '{retailer}'
            and supplier = '{supplier}'
    """
    data = du.sql(query).df()
    return data


def filtered_data(dataframe, date):
    query = f"""
        select *
        from 'dataframe'
        where date = '{date}'
            and retailer = '{retailer}' 
            and supplier = '{supplier}'
    """
    data = du.sql(query).df()
    return data


def category_sales(dataframe):
    query = f"""
        select
            category as id,
            coalesce(sum(sales), 1) as value
        from 'dataframe'
        group by 1
        order by 2 asc
    """
    data = du.sql(query).df()
    data_dict = data.to_dict(orient="records")
    data_json = json.dumps(data_dict, indent=2, default=serialize_datetime)
    return data_json


def retailer_supplier_data(dataframe, retailer, supplier):
    query = f""" 
        with data as (

                select
                    date as day,
                    sum(sales) as value
                from 'dataframe'
                where retailer = '{retailer}'
                    and supplier = '{supplier}'
                    and category = IF('{state.select_category}' = 'all', category , '{state.select_category}')
                group by 1

            ),
            filtered_day_data as (

                select
                    day,
                    value,
                    extract(dow from if('{state.select_day}' != '{None}', date '{state.select_day}', day)) as day_of_week
                from data
                where extract(dow from day) = day_of_week

            )
        select
            day,
            value 
        from filtered_day_data
        order by 1
    """
    data = du.sql(query).df()
    data['day'] = pd.to_datetime(data['day']).dt.date
    data_dict = data.to_dict(orient="records")
    data_json = json.dumps(data_dict, indent=2, default=serialize_datetime)
    return data_json


def total_day(dataframe, date):
    query = f"""
        select
            sum(sales) as sales,
            sum(smatched) / (sum(smatched) + sum(scredited)) as supplier_service,
            sum(dmatched) / (sum(dmatched) + sum(dcredited)) as depot_service,
            sum(sstocked) / sum(sranged) as availability
        from 'dataframe'
        where date = '{date}'
    """
    data = du.sql(query).df()
    data.fillna(0, inplace=True)
    return data


# SESSION STATE HANLDERS

def reset_filters():
    state.select_category = "all"
    state.select_day = None
    state.sales_bar_color = "gray"


def category_callback(event):
    state.select_category = event.data.id
    state.sales_bar_color = event.color


def day_callback(event):
    state.select_day = event.day


def calendar_reset_callback(info):
    state.select_day = None


def category_reset_callback(info):
    state.select_category = "all"
    state.sales_bar_color = "gray"


def switch_mode():
    state.dark_mode = not state.dark_mode
    state.main_background = "black" if state.dark_mode else "white"

def main():

    retailer = get_retailer(FILENAME)
    supplier = get_supplier(FILENAME)

    with st.sidebar:
        selected_retailer_dash = st.selectbox("Retailer", retailer, key="retailer_select_dash", on_change=reset_filters)
        selected_supplier_dash = st.selectbox("Supplier", supplier, key="supplier_select_dash", on_change=reset_filters)

    data = get_data_mock(FILENAME, selected_retailer_dash, selected_supplier_dash)

    first_date = data["date"].min() # from_date
    last_date = data["date"].max() # today and to_date is now last_date
    week_ago = last_date - datetime.timedelta(days=7)

    data_today = data[data["date"] == last_date]
    data_week_ago = data[data["date"] == week_ago]

    sales_value_today = data_today["sales"].sum()
    sales_value_week_ago = data_week_ago["sales"].sum()
    sales_vs_last_week_percentage = (sales_value_today - sales_value_week_ago) / sales_value_today

    supplier_service_today = data_today["smatched"].sum() / (data_today["smatched"].sum() + data_today["scredited"].sum())
    supplier_service_week_ago = data_week_ago["smatched"].sum() / (data_week_ago["smatched"].sum() + data_week_ago["scredited"].sum())
    supplier_vs_last_week_percentage = supplier_service_today - supplier_service_week_ago

    depot_service_today = data_today["dmatched"].sum() / (data_today["dmatched"].sum() + data_today["dcredited"].sum())
    depot_service_week_ago = data_week_ago["dmatched"].sum() / (data_week_ago["dmatched"].sum() + data_week_ago["dcredited"].sum())
    depot_vs_last_week_percentage = depot_service_today - depot_service_week_ago

    availability_today = data_today["sstocked"].sum() / data_today["sranged"].sum()
    availability_week_ago = data_week_ago["sstocked"].sum() / data_week_ago["sranged"].sum()
    availability_vs_last_week_percentage = availability_today - availability_week_ago

    sales_by_category_today = data_today.groupby("category")["sales"].sum().reset_index() # cat_sales_data_json

    #
    # st.write(sales_by_category_today)
    # exit()
    retailer_supplier_data_json = data

    with elements("main"):

        if not state.dark_mode:
            mui.IconButton(mui.icon.LightMode, sx={"color": "#ffc107"}, onClick=switch_mode)
        else:
            mui.IconButton(mui.icon.DarkMode, onClick=switch_mode)

        with html.div(
                css={
                    "backdrop-filter": "blur(10px)",
                    "background": f"{state.main_background} url('https://png2.cleanpng.com/sh/a1fa59c9e71bbbf6484f9d0a898336a5/L0KzQYm3U8AzN5Z6j5H0aYP2gLBuTgNpaaFqRdpueHHqf7A0kBNqbZ9ofZ9qbnSwhLbqiP5wdJDskZ98aHHzdX68gck6bGo3TdY5OUO3QnA7WcE5P2k9S6MAMkCzQ4O3U8c5PWU4RuJ3Zx==/kisspng-shape-hexagon-science-and-technology-shape-5a99d925d09342.4918788315200320378543.png')",
                    "background-repeat": "no-repeat",
                    "background-size": "contain",
                    "background-position": "top center",
                }
        ):
            mui.Typography("28-day Summary", variant="h4", sx={"mb": 10}, align="center")

            with w.dashboard(rowHeight=57):
                w.sales_total(
                    json_data=dump_json(data),
                    title="Sales Value",
                    value_today=sales_value_today,
                    value_vs=sales_vs_last_week_percentage,
                    key_column="value",
                    value_format="{:,.0f}",
                    value_prefix="£",
                )
                w.supplier_service_total(
                    json_data=dump_json(data),
                    title="Supplier Service",
                    value_today=supplier_service_today,
                    value_vs=supplier_vs_last_week_percentage,
                    key_column="supplier_service",
                    value_format="{:.1%}",
                    light_color="#90bd8f",
                    dark_color="#5cb05a",
                )
                w.depot_service_total(
                    json_data=dump_json(data),
                    title="Depot Service",
                    value_today=depot_service_today,
                    value_vs=depot_vs_last_week_percentage,
                    key_column="depot_service",
                    value_format="{:.1%}",
                    light_color="#8c8ebf",
                    dark_color="#545687",
                )
                w.availabitity_total(
                    json_data=dump_json(data),
                    title="Availability",
                    value_today=availability_today,
                    value_vs=availability_vs_last_week_percentage,
                    key_column="availability",
                    value_format="{:.1%}",
                    light_color="#bc99bd",
                    dark_color="#9f5ca1",
                )
                # w.category_sales(
                #     title="Category Sales",
                #     json_data=cat_sales_data_json,
                #     onClick=category_callback,
                #     onResetClick=category_reset_callback,
                #     light_color="#bdbdbd",
                #     dark_color="#595959",
                # )
                # w.calendar_sales(
                #     json_data=retailer_supplier_data_json,
                #     title="Daily Sales Calendar",
                #     from_date=from_date,
                #     to_date=to_date,
                #     onClick=day_callback,
                #     onResetClick=calendar_reset_callback,
                #     light_color="#bdbdbd",
                #     dark_color="#595959"
                # )
                # w.daily_sales(
                #     title="Daily Sales",
                #     json_data=retailer_supplier_data_json,
                #     bar_color=state.sales_bar_color,
                #     light_color="#bdbdbd",
                #     dark_color="#595959"
                # )
                # w.forecast(
                #     title="Order Forecast",
                #     value_today=forecast_filtered,
                #     value_format="{:,.0f}",
                #     prefix="£",
                #     light_color="#8fb3b1",
                #     dark_color="#4f7573",
                # )
                # w.forecast_variance(
                #     title="Forecast Variance",
                #     value_today=forecast_variance_filtered,
                #     value_format="{:,.0f}",
                #     suffix="SKUS",
                #     light_color="#8fb3b1",
                #     dark_color="#4f7573",
                # )
                # w.supplier_shorted(
                #     title="Supplier Shorted",
                #     value_today=supplier_shorted_filtered,
                #     value_format="{:,.0f}",
                #     suffix=supplier_shorted_data['ind'].unique()[0],
                #     light_color="#cf8382",
                #     dark_color="#8f4746",
                # )
                # w.depot_shorted(
                #     title="Depot Shorted",
                #     value_today=depot_shorted_sum_of_value,
                #     value_format="{:,.0f}",
                #     suffix=depot_shorted_data['ind'].unique()[0],
                #     light_color="#cf8382",
                #     dark_color="#8f4746",
                # )
                # w.availability_issues(
                #     title="Availability Issues",
                #     value_today=availability_issues_sku_count,
                #     value_format="{:,.0f}",
                #     suffix="SKUS",
                #     light_color="#cf8382",
                #     dark_color="#8f4746",
                # )


if __name__ == "__main__":
    if "dark_mode" not in state:
        state.dark_mode = False
        state.main_background = "white"
    else:
        state.dark_mode = state.dark_mode
        state.main_background = state.main_background

    if "select_category" not in state:
        state.select_category = "all"
    else:
        state.select_category = state.select_category
    if "select_day" not in state:
        state.select_day = None
    else:
        state.select_day = state.select_day
    if "sales_bar_color" not in state:
        state.sales_bar_color = "#e6e6e6"
    else:
        state.sales_bar_color = state.sales_bar_color

    if "w" not in state:
        board = Dashboard()
        w = SimpleNamespace(
            dashboard=board,
            sales_total=MetricsToday(board, 0, 0, 3, 3),
            supplier_service_total=MetricsToday(board, 3, 0, 3, 3),
            depot_service_total=MetricsToday(board, 6, 0, 3, 3),
            availabitity_total=MetricsToday(board, 9, 0, 3, 3),
            # category_sales=CategorySales(board, 0, 3, 3, 6),
            # daily_sales=DailySales(board, 3, 3, 6, 6),
            # calendar_sales=CalendarHeatmap(board, 9, 5, 3, 6),
            # forecast=Footer(board, 0, 6, 2, 2),
            # forecast_variance=Footer(board, 2, 6, 2, 2),
            # supplier_shorted=Footer(board, 4, 6, 2, 2),
            # depot_shorted=Footer(board, 6, 6, 2, 2),
            # availability_issues=Footer(board, 8, 6, 2, 2)
        )
        state.w = w
    else:
        w = state.w

    main()