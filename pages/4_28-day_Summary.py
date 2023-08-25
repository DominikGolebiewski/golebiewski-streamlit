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
from streamlit_elements import dashboard, elements, mui, nivo
from pages.dash.dashboard import Dashboard
from pages.dash.total import TotalElement
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


def get_data_mock(filename: str):
    data = du.read_json(filename)
    return data

def get_retailer(dataframe):
    retailer_data = du.sql("SELECT retailer FROM 'dataframe' GROUP BY retailer ORDER BY retailer").df()
    return retailer_data['retailer'].values.tolist()


def get_supplier(dataframe):
    retailer_data = du.sql("SELECT supplier FROM 'dataframe' GROUP BY supplier ORDER BY supplier").df()
    return retailer_data['supplier'].values.tolist()


def get_effective_dates(dataframe, retailer, supplier):
    query = f"""
        select
            max(date) as to_date,
            min(date) as from_date
        from 'dataframe' 
            where retailer = '{retailer}' 
            and supplier = '{supplier}'
        group by retailer, supplier
    """
    date = du.sql(query).df()
    date["to_date"] = pd.to_datetime(date["to_date"]).dt.date
    date["from_date"] = pd.to_datetime(date["from_date"]).dt.date
    from_date = str(date["from_date"][0])
    to_date = str(date["to_date"][0])
    return from_date, to_date


def get_max_date(dataframe, retailer, supplier):
    query = f"""
        select
            max(date) as today,
            today - interval 7 day as week_ago
        from 'dataframe' 
            where retailer = '{retailer}' 
            and supplier = '{supplier}'
        group by retailer, supplier
    """
    date = du.sql(query).df()
    date["today"] = pd.to_datetime(date["today"]).dt.date
    date["week_ago"] = pd.to_datetime(date["week_ago"]).dt.date
    return date


def filtered_data(dataframe, retailer, supplier, date):
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



def main():
    data = get_data_mock(FILENAME)
    retailer = get_retailer(data)
    supplier = get_supplier(data)

    def reset_filters():
        state.select_category = "all"
        state.select_day = None
        state.sales_bar_color = "gray"

    with st.sidebar:
        selected_retailer_dash = st.selectbox("Retailer", retailer, key="retailer_select_dash", on_change=reset_filters)
        selected_supplier_dash = st.selectbox("Supplier", supplier, key="supplier_select_dash", on_change=reset_filters)

    from_date, to_date = get_effective_dates(data, selected_retailer_dash, selected_supplier_dash)

    today = get_max_date(data, selected_retailer_dash, selected_supplier_dash)["today"][0]
    week_ago = get_max_date(data, selected_retailer_dash, selected_supplier_dash)["week_ago"][0]

    data_today = filtered_data(data, selected_retailer_dash, selected_supplier_dash, today)
    data_week_ago = filtered_data(data, selected_retailer_dash, selected_supplier_dash, week_ago)

    sales_value_today = total_day(data_today, today)["sales"][0]
    sales_value_week_ago = total_day(data_week_ago, week_ago)["sales"][0]

    sales_vs_last_week_percentage = (sales_value_today - sales_value_week_ago) / sales_value_today

    supplier_service_today = total_day(data_today, today)["supplier_service"][0]
    supplier_service_week_ago = total_day(data_week_ago, week_ago)["supplier_service"][0]

    supplier_vs_last_week_percentage = supplier_service_today - supplier_service_week_ago

    depot_service_today = total_day(data_today, today)["depot_service"][0]
    depot_service_week_ago = total_day(data_week_ago, week_ago)["depot_service"][0]

    depot_vs_last_week_percentage = depot_service_today - depot_service_week_ago

    cat_sales_data_json = category_sales(data_today)

    retailer_supplier_data_json = retailer_supplier_data(data, selected_retailer_dash, selected_supplier_dash)

    availability_today = total_day(data_today, today)["availability"][0]
    availability_week_ago = total_day(data_week_ago, week_ago)["availability"][0]

    availability_vs_last_week_percentage = availability_today - availability_week_ago


    st.write(sales_value_today)
    st.write(sales_value_week_ago)
    # exit()

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

    with elements("main"):
        mui.Typography("28-day Summary", variant="h4", sx={"mb": 5, "align": "center"}, align="center")
        with w.dashboard(rowHeight=57):
            w.sales_total("Sales Value", sales_value_today, sales_vs_last_week_percentage, value_format="{:,.0f}")
            w.supplier_service_total("Supplier Service", supplier_service_today, supplier_vs_last_week_percentage,
                                     value_format="{:.0%}", light_color="#cfe8ca", dark_color="#a1b59e")
            w.depot_service_total("Depot Service", depot_service_today, depot_vs_last_week_percentage,
                                  value_format="{:.0%}", light_color="#c8cae3", dark_color="#9fa1bd")
            w.availabitity_total("Availability", availability_today, availability_vs_last_week_percentage,
                                 value_format="{:.1%}", light_color="#c7c7c7", dark_color="#a3a3a3")
            w.category_sales(cat_sales_data_json, "Category Sales", onClick=category_callback,
                             onResetClick=category_reset_callback)
            w.calendar_sales(retailer_supplier_data_json, "Daily Sales Calendar", from_date, to_date, onClick=day_callback,
                             onResetClick=calendar_reset_callback)
            w.daily_sales(retailer_supplier_data_json, "Daily Sales", bar_color=state.sales_bar_color)


if __name__ == "__main__":

    if "select_category" not in state:
        state.select_category = "all"
    else:
        state.select_category = state.select_category
    if "select_day" not in state:
        state.select_day = None
    else:
        state.select_day = state.select_day
    if "sales_bar_color" not in state:
        state.sales_bar_color = "gray"
    else:
        state.sales_bar_color = state.sales_bar_color

    if "w" not in state:
        board = Dashboard()
        w = SimpleNamespace(
            dashboard=board,
            sales_total=TotalElement(board, 0, 0, 3, 3, minW=3, minH=1, maxW=3, maxH=3),
            supplier_service_total=TotalElement(board, 3, 0, 3, 3, minW=3, minH=1, maxW=3, maxH=3),
            depot_service_total=TotalElement(board, 6, 0, 3, 3, minW=3, minH=1, maxW=3, maxH=3),
            availabitity_total=TotalElement(board, 9, 0, 3, 3, minW=3, minH=1, maxW=3, maxH=3),
            category_sales=CategorySales(board, 0, 3, 3, 8, minW=3, minH=6, maxW=9, maxH=18),
            daily_sales=DailySales(board, 3, 3, 6, 8),
            calendar_sales=CalendarHeatmap(board, 9, 6, 3, 8)
        )
        state.w = w
    else:
        w = state.w

    main()