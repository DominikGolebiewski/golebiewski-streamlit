import streamlit_authenticator as stauth
import yaml
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from yaml.loader import SafeLoader
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from io import StringIO, BytesIO
from streamlit_elements import elements, mui, html, nivo
import json

st.set_page_config(layout='wide')

with open('.streamlit/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login('Login', 'main')


class Authenticate:

    def __init__(self):
        self.name = name
        self.authentication_status = authentication_status
        self.username = username

    def __enter__(self):
        if self.authentication_status:
            authenticator.logout('Logout', 'main')
            st.write(f'Welcome *{name}*')
        elif not self.authentication_status:
            st.error('Username/password is incorrect')

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def csv_to_df(file):
    df = pd.read_csv(file)
    return df


def main():
    auth = Authenticate()
    with auth:
        if auth.authentication_status:
            uploaded_file = st.file_uploader("Choose a file")

            if uploaded_file is not None:
                df = csv_to_df(uploaded_file)
                df = df[df['Debit Amount'].notnull()]

            df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
            # df['Transaction Description'] = df['Transaction Description'].map({'KLARNA': 'Klarna', 'Klarna': 'Klarna', 'KLARNA AB': 'Klarna', 'ASDA SUPERSTORE  4': 'Asda', 'ICELAND': 'Iceland'})

            mapping = {
                'Spending': {
                    'Grocery': {
                        'asda': 'Asda',
                        'iceland': 'Iceland',
                        'aldi': 'Aldi',
                        'lidl': 'Lidl',
                        'WILKO RETAIL LIMIT': 'Wilko',
                        'LNK SPENNY BOOZERS': 'Spenny Boozer',
                        'FARMFOODS': 'Farmfoods',
                        'MARTIN MCCOLL': 'Martin McColl',
                        'THE WORKS': 'The Works',
                        'COSTA COFFEE': 'Costa Coffee',
                        'HOME BARGAINS': 'Home Bargains',
                        'SAINSBURYS': 'Sainsburys',
                    },
                    'Clothing': {
                        'TK MAXX': 'TK Maxx',
                    },
                    'Utilities': {
                        'utility warehouse': 'Utility Warehouse',
                        'nwl & esw water': 'Water',
                        'virgin media': 'Internet',
                    },
                    'Car': {
                        'dvla': 'DVLA',
                        'HASTINGS INSURANCE': 'Car Insurance',
                        'KAROLINA TADAK': 'Pysia - Car',
                    },
                    'Housing': {
                        'carl bates': 'Monthly Rent',
                        'infinity cycles': 'Infinity Cycles',
                        'r a milburn': 'Furnitures',
                    },
                    'Loan': {
                        'lloyds bank loan': 'Lloyds Loan',
                        'klarna': 'Klarna',
                        'DAILY OD INT': 'Overdraft Interest',
                    },
                    'Credit Cards': {
                        'LLOYDS BANK PLATIN': 'Lloyds Credit Card Payment',
                        'WWW.CREATIONCF.COM': 'Currys Store Card Payment',
                        'VANQUIS': 'Vanquis Credit Card Payment',
                        'CURRYS': 'Currys Store Card Payment',
                    },
                    'Leasure' : {
                        'HAMSTERLEY': 'Hamsterley',
                        'DOWNEYS OF SEAHAM': 'Downeys of Seaham',
                        'CROWS NEST': 'Crows Nest',
                        'Creams of Seaham': 'Creams of Seaham',
                        'HAMSTERY F': 'Hamsterley',
                        'Janies Pan': 'SumUp Janies Pan',
                        'THE RIVERWALK CAR': 'The Riverwalk Car Park',
                        'Jubilee Confection': 'Jubilee Confection',
                        'Fat Hippo Durham': 'Fat Hippo Durham',
                        'CAR PARK': 'Car Park',
                        'SUBWAY': 'Subway',
                    },
                    'Savings': {
                        'MONEYBOX': 'Moneybox',
                    },
                    'PayPal': {
                        'PAYPAL': 'PayPal',
                    },
                    'Uncategorized': {
                        'null': 'Other',
                        'ACT TRADING LTD': 'ACT Trading Ltd',
                        'The Pancake Kitche': 'The Pancake Kitchen',
                        'Zettle': 'Zettle_WONDERFUL',
                        'P.O. OXFORD STREET': 'P.O. OXFORD STREET',
                        'ORIGINAL FACTORY S': 'Original Factory Shop',

                    }
                }
            }

            def map_description(dataframe, description: dict):
                for types in description.values():
                    for key, value in types.items():
                        for desc, map_desc in value.items():
                            # st.write(key, desc, map_desc)
                            df.loc[df['Transaction Description'].str.contains(f'{desc}', case=False), 'Transaction Description'] = f'{map_desc}'
                            df.loc[df['Transaction Description'].str.contains(f'{map_desc}', case=False), 'Spending Type'] = f'{key}'
                return dataframe

            df = map_description(df, mapping)

            def create_json_data(dataframe, date_column, value_column, key_column):
                df = dataframe[[date_column, value_column, key_column]]
                df = df.groupby([date_column, key_column]).sum().reset_index()
                df = df.pivot(index=date_column, columns=key_column, values=value_column).reset_index()
                df = df.fillna(0)
                df_json = df.to_json(orient='records')
                return df_json

            dj = create_json_data(df, 'Transaction Date', 'Debit Amount', 'Spending Type')
            # st.write(json.loads(dj))

            df_keys= df['Spending Type'].dropna().unique().tolist()
            # st.write(df_keys)
            with elements("spending_bar"):
                with mui.Paper(sx={"minHeight": 400}):
                    with mui.Box(sx={"flex": 1, "height": 600, "width": 1900}):
                        nivo.Bar(
                            data=json.loads(dj),
                            keys=df_keys,
                            indexBy='Transaction Date',
                            enableGridX=False,
                            enableGridY=True,
                            theme='dark',
                            margin={"top": 50, "right": 150, "bottom": 100, "left": 70},
                            padding=0.2,
                            valueScale={'type': 'linear'},
                            indexScale={'type': 'band', 'round': True},
                            colors={"scheme": "category10"},
                            enableLabel=False,
                        axisBottom={
                            'tickSize': 5,
                            'tickPadding': 5,
                            'tickRotation': 45,
                            'legend': 'Date',
                            'legendPosition': 'middle',
                            'legendOffset': 80
                        },
                        axisLeft={
                            'tickSize': 5,
                            'tickPadding': 0,
                            'tickRotation': 0,
                            'legend': 'Value',
                            'legendPosition': 'middle',
                            'legendOffset': -50
                        },
                            legends=[
                                {
                                    'dataFrom': 'keys',
                                    'anchor': 'bottom-right',
                                    'direction': 'column',
                                    'justify': False,
                                    'translateX': 120,
                                    'translateY': 0,
                                    'itemsSpacing': 2,
                                    'itemWidth': 100,
                                    'itemHeight': 20,
                                    'itemDirection': 'left-to-right',
                                    'itemOpacity': 0.85,
                                    'symbolSize': 20,
                                    'effects': [
                                        {
                                            'on': 'hover',
                                            'style': {
                                                'itemOpacity': 1
                                            }
                                        }
                                    ]
                                }]

                        )


if __name__ == "__main__":
    main()





        # Create a datetime slider with a range of one week
        # start_date = datetime(2023, 7, 1)
        # end_date = start_date + timedelta(days=100)
        #
        # selected_date = st.slider(
        #     "Select a date range",
        #     min_value=start_date,
        #     max_value=end_date,
        #     value=(start_date, end_date),
        #     step=timedelta(days=1)
        # )
        # st.write(selected_date[0].strftime('%Y-%m-%d'))
        # columns = ['date', 'type', 'srt', 'acc', 'desc', 'dbt', 'crd', 'bal']
        # df = pd.read_csv(uploaded_file, sep=",", names=columns, header=None, skiprows=1)
        # df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
        # df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        # df['abs_bal'] = df['bal'].abs()
        # # df['desc'] = df['desc'].map({'KLARNA': 'Klarna', 'Klarna': 'Klarna', 'KLARNA AB': 'Klarna',
        # #                              'ASDA SUPERSTORE  4': 'Asda', 'ICELAND': 'Iceland'})
        # df.loc[df['desc'].str.contains('ASDA'), 'desc'] = 'Asda'
        # df.loc[df['desc'].str.contains('ICELAND'), 'desc'] = 'Iceland'
        # df.loc[df['desc'].str.contains('KLARNA'), 'desc'] = 'Klarna'
        # df.loc[df['desc'].str.contains('Klarna'), 'desc'] = 'Klarna'
        # df.loc[df['desc'].str.contains('KLARNA AB'), 'desc'] = 'Klarna'
        # df.loc[df['desc'].str.contains('DAILY OD INT'), 'desc'] = 'Daily OD Charge'
        # df.loc[df['desc'].str.contains('DVLA'), 'desc'] = 'DVLA'
        # df.loc[df['desc'].str.contains('LIDL'), 'desc'] = 'Lidl'
        # df.loc[df['desc'].str.contains('PAYPAL'), 'desc'] = 'PayPal'
        # df.loc[df['desc'].str.contains('ALDI'), 'desc'] = 'Aldi'
        # df.loc[df['desc'].str.contains('CARL BATES'), 'desc'] = 'Monthly Rent'
        # df.loc[df['desc'].str.contains('KAROLINA TADAK'), 'desc'] = 'Pysia - Car'
        # df.loc[df['desc'].str.contains('UTILITY WAREHOUSE'), 'desc'] = 'Utilities - Electricity & Gas'
        # df.loc[df['desc'].str.contains('HOME BARGAINS'), 'desc'] = 'Home Bargains'
        # df.loc[df['desc'].str.contains('VANQUIS'), 'desc'] = 'Vanquis Credit Card Payment'
        # df.loc[df['desc'].str.contains('WWW.CREATION'), 'desc'] = 'Currys Store Card Payment'
        # df.loc[df['desc'].str.contains('LLOYDS BANK LOAN'), 'desc'] = 'Lloyds Loan'
        # df.loc[df['desc'].str.contains('LLOYDS BANK PLATIN'), 'desc'] = 'Lloyds Credit Card Payment'
        # df.loc[df['desc'].str.contains('Revolut'), 'desc'] = 'Revolut Transfer'
        # df.loc[df['desc'].str.contains('SUBWAY'), 'desc'] = 'Subway'
        # df.loc[df['desc'].str.contains('HAMSTERLEY'), 'desc'] = 'Hamsterley'
        # df.loc[df['desc'].str.contains('CROOK STORES'), 'desc'] = 'Crook Stores'
        # df.loc[df['desc'].str.contains('CAR PARK'), 'desc'] = 'Car Park'
        # df.loc[df['desc'].str.contains('CURRYS'), 'desc'] = 'Currys'
        # df.loc[df['desc'].str.contains('FARMFOODS'), 'desc'] = 'Farmfoods'
        # df.loc[df['desc'].str.contains('HASTINGS'), 'desc'] = 'Car Insurance'
        # df.loc[df['desc'].str.contains('VIRGIN MEDIA'), 'desc'] = 'Internet'
        # df.loc[df['desc'].str.contains('R A MILBURN'), 'desc'] = 'Furnitures'
        # df.loc[df['desc'].str.contains('CB CARD'), 'desc'] = 'Pysia UW Transfer'
        # df.loc[df['desc'].str.contains('NWL & ESW WATER'), 'desc'] = 'Utilities - Water'
        # df['desc'] = np.where((df['desc'].str.contains('PayPal')) & (df['dbt'] >= 196), 'Council Tax', df['desc'])
        #
        # df['shopping_type'] = df['desc'].map({
        #     'Lloyds Loan': 'Loan',
        #     'Currys Store Card Payment': 'Credit Card',
        #     'Klarna': 'Loan',
        #     'Vanquis Credit Card Payment': 'Credit Card',
        #     'Lloyds Credit Card Payment': 'Credit Card',
        #     'Home Bargains': 'Shopping',
        #     'Electricity & Gas': 'Housing',
        #     'Pysia - Car': 'Car',
        #     'Monthly Rent': 'Housing',
        #     'Aldi': 'Shopping',
        #     'PayPal': 'PayPal',
        #     'Lidl': 'Shopping',
        #     'DVLA': 'Car',
        #     'Daily OD Charge': 'Overdraft Charges',
        #     'Iceland': 'Shopping',
        #     'MONEYBOX': 'Savings',
        #     'Utilities - Water': 'Housing',
        #     'OPENAI': 'Leasure',
        #     'Asda': 'Shopping',
        #     'Subway': 'Shopping',
        #     'Hamsterley': 'Leasure',
        #     'Crook Stores': 'Shopping',
        #     'Car Park': 'Leasure',
        #     'Currys': 'Credit Card',
        #     'Farmfoods': 'Shopping',
        #     'Car Insurance': 'Car',
        #     'Infinity Cycles': 'Leasure',
        #     'TK MAXX': 'Shopping',
        #     'Internet': 'Housing',
        #     'Revolut Transfer': 'Revolut',
        #     'Furnitures': 'Housing',
        #     'Pysia UW Transfer': 'Housing',
        #     'Council Tax': 'Housing',
        #     'null': 'Other',
        #
        # })
        #
        # # st.dataframe(df)
        # project_select = alt.selection_point(fields=["desc"])
        #
        # type_select = alt.selection_point(fields=["shopping_type"])
        #
        # type_pie = (
        #     (
        #         alt.Chart(df)
        #         .mark_arc(innerRadius=50)
        #         .encode(
        #             theta=alt.Theta(
        #                 "dbt",
        #                 type="quantitative",
        #                 aggregate="sum",
        #                 title="Sum of Debit",
        #             ),
        #             color=alt.Color(
        #                 field="shopping_type",
        #                 type="nominal",
        #                 title="Desc",
        #             ),
        #             opacity=alt.condition(type_select, alt.value(1), alt.value(0.25)),
        #         )
        #     )
        #     .add_params(type_select)
        #     .transform_filter(alt.datum.date >= f"{selected_date[0].strftime('%Y-%m-%d')}")
        #     .properties(title="Total Debit by Shopping Type")
        # )
        #
        # dbt_pie = (
        #     (
        #         alt.Chart(df)
        #         .mark_arc(innerRadius=50)
        #         .encode(
        #             theta=alt.Theta(
        #                 "dbt",
        #                 type="quantitative",
        #                 aggregate="sum",
        #                 title="Sum of Debit",
        #             ),
        #             color=alt.Color(
        #                 field="desc",
        #                 type="nominal",
        #                 title="Desc",
        #             ),
        #             tooltip=['desc', 'sum(dbt)']
        #         )
        #
        #     )
        #     .transform_filter(type_select)
        #     .transform_filter(alt.datum.date >= f"{selected_date[0].strftime('%Y-%m-%d')}")
        #     .properties(title="Debit Type by Day")
        # )
        #
        # dbt = (
        #     alt.Chart(df)
        #     .mark_bar()
        #     .encode(
        #         x="date:O",
        #         y="dbt:Q",
        #         color=alt.Color("desc:N", legend=None),
        #         tooltip=['date', 'desc', 'dbt', 'crd', 'bal']
        #     )
        # ).transform_filter(alt.datum.date >= f"{selected_date[0].strftime('%Y-%m-%d')}"
        #                    ).transform_filter(type_select
        #                                       ).properties(width=1000)
        #
        # tpe = (
        #     alt.Chart(df)
        #     .mark_bar()
        #     .encode(
        #         x="date:O",
        #         y="sum(dbt):Q",
        #         color="shopping_type:N",
        #         tooltip=['date', 'shopping_type', 'sum(dbt)']
        #     )
        # ).transform_filter(alt.datum.date >= f"{selected_date[0].strftime('%Y-%m-%d')}"
        #                    ).transform_filter(type_select
        #                                       ).properties(width=1000)
        #
        # st.altair_chart((type_pie | tpe) & (dbt_pie | dbt), use_container_width=True)

