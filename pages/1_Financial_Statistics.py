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


# with open('filekey.key', 'rb') as filekey:
#     key = filekey.read()

# using the generated key
# fernet = Fernet(key)

# opening the original file to encrypt
# with open('assets/22118568_20233808_0708.csv', 'rb') as file:
#     original = file.read()

# encrypting the file
# encrypted = fernet.encrypt(original)

# opening the file in write mode and
# writing the encrypted data
# with open('assets/e202301-202308.csv', 'wb') as encrypted_file:
#     encrypted_file.write(encrypted)

with open('.streamlit/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:

    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')

    filekey = st.secrets["FILEKEY"]
    fernet = Fernet(filekey)
    with open('assets/e202301-202308.csv', 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)
    csvStringIO = BytesIO(decrypted)
    decoded = csvStringIO.read().decode('utf-8')

    # Create a datetime slider with a range of one week
    start_date = datetime(2023, 8, 31)
    end_date = start_date + timedelta(days=-62)

    selected_date = st.slider(
        "Select a date range",
        min_value=start_date,
        max_value=end_date,
        value=(start_date, end_date),
        step=timedelta(days=1)
    )
    st.write(selected_date[0].strftime('%Y-%m-%d'))
    columns = ['date', 'type', 'srt', 'acc', 'desc', 'dbt', 'crd', 'bal']
    df = pd.read_csv(StringIO(decoded), sep=",", names=columns, header=None, skiprows=1)
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    df['abs_bal'] = df['bal'].abs()
    # df['desc'] = df['desc'].map({'KLARNA': 'Klarna', 'Klarna': 'Klarna', 'KLARNA AB': 'Klarna',
    #                              'ASDA SUPERSTORE  4': 'Asda', 'ICELAND': 'Iceland'})
    df.loc[df['desc'].str.contains('ASDA'), 'desc'] = 'Asda'
    df.loc[df['desc'].str.contains('ICELAND'), 'desc'] = 'Iceland'
    df.loc[df['desc'].str.contains('KLARNA'), 'desc'] = 'Klarna'
    df.loc[df['desc'].str.contains('Klarna'), 'desc'] = 'Klarna'
    df.loc[df['desc'].str.contains('KLARNA AB'), 'desc'] = 'Klarna'
    df.loc[df['desc'].str.contains('DAILY OD INT'), 'desc'] = 'Daily OD Charge'
    df.loc[df['desc'].str.contains('DVLA'), 'desc'] = 'DVLA'
    df.loc[df['desc'].str.contains('LIDL'), 'desc'] = 'Lidl'
    df.loc[df['desc'].str.contains('PAYPAL'), 'desc'] = 'PayPal'
    df.loc[df['desc'].str.contains('ALDI'), 'desc'] = 'Aldi'
    df.loc[df['desc'].str.contains('CARL BATES'), 'desc'] = 'Monthly Rent'
    df.loc[df['desc'].str.contains('KAROLINA TADAK'), 'desc'] = 'Pysia - Car'
    df.loc[df['desc'].str.contains('UTILITY WAREHOUSE'), 'desc'] = 'Utilities - Electricity & Gas'
    df.loc[df['desc'].str.contains('HOME BARGAINS'), 'desc'] = 'Home Bargains'
    df.loc[df['desc'].str.contains('VANQUIS'), 'desc'] = 'Vanquis Credit Card Payment'
    df.loc[df['desc'].str.contains('WWW.CREATION'), 'desc'] = 'Currys Store Card Payment'
    df.loc[df['desc'].str.contains('LLOYDS BANK LOAN'), 'desc'] = 'Lloyds Loan'
    df.loc[df['desc'].str.contains('LLOYDS BANK PLATIN'), 'desc'] = 'Lloyds Credit Card Payment'
    df.loc[df['desc'].str.contains('Revolut'), 'desc'] = 'Revolut Transfer'
    df.loc[df['desc'].str.contains('SUBWAY'), 'desc'] = 'Subway'
    df.loc[df['desc'].str.contains('HAMSTERLEY'), 'desc'] = 'Hamsterley'
    df.loc[df['desc'].str.contains('CROOK STORES'), 'desc'] = 'Crook Stores'
    df.loc[df['desc'].str.contains('CAR PARK'), 'desc'] = 'Car Park'
    df.loc[df['desc'].str.contains('CURRYS'), 'desc'] = 'Currys'
    df.loc[df['desc'].str.contains('FARMFOODS'), 'desc'] = 'Farmfoods'
    df.loc[df['desc'].str.contains('HASTINGS'), 'desc'] = 'Car Insurance'
    df.loc[df['desc'].str.contains('VIRGIN MEDIA'), 'desc'] = 'Internet'
    df.loc[df['desc'].str.contains('R A MILBURN'), 'desc'] = 'Furnitures'
    df.loc[df['desc'].str.contains('CB CARD'), 'desc'] = 'Pysia UW Transfer'
    df.loc[df['desc'].str.contains('NWL & ESW WATER'), 'desc'] = 'Utilities - Water'
    df['desc'] = np.where((df['desc'].str.contains('PayPal')) & (df['dbt'] >= 196), 'Council Tax', df['desc'])

    df['shopping_type'] = df['desc'].map({
        'Lloyds Loan': 'Loan',
        'Currys Store Card Payment': 'Credit Card',
        'Klarna': 'Loan',
        'Vanquis Credit Card Payment': 'Credit Card',
        'Lloyds Credit Card Payment': 'Credit Card',
        'Home Bargains': 'Shopping',
        'Electricity & Gas': 'Housing',
        'Pysia - Car': 'Car',
        'Monthly Rent': 'Housing',
        'Aldi': 'Shopping',
        'PayPal': 'PayPal',
        'Lidl': 'Shopping',
        'DVLA': 'Car',
        'Daily OD Charge': 'Overdraft Charges',
        'Iceland': 'Shopping',
        'MONEYBOX': 'Savings',
        'Utilities - Water': 'Housing',
        'OPENAI': 'Leasure',
        'Asda': 'Shopping',
        'Subway': 'Shopping',
        'Hamsterley': 'Leasure',
        'Crook Stores': 'Shopping',
        'Car Park': 'Leasure',
        'Currys': 'Credit Card',
        'Farmfoods': 'Shopping',
        'Car Insurance': 'Car',
        'Infinity Cycles': 'Leasure',
        'TK MAXX': 'Shopping',
        'Internet': 'Housing',
        'Revolut Transfer': 'Revolut',
        'Furnitures': 'Housing',
        'Pysia UW Transfer': 'Housing',
        'Council Tax': 'Housing',
        'null': 'Other',

    })

    # st.dataframe(df)
    project_select = alt.selection_point(fields=["desc"])

    type_select = alt.selection_point(fields=["shopping_type"])

    type_pie = (
        (
            alt.Chart(df)
            .mark_arc(innerRadius=50)
            .encode(
                theta=alt.Theta(
                    "dbt",
                    type="quantitative",
                    aggregate="sum",
                    title="Sum of Debit",
                ),
                color=alt.Color(
                    field="shopping_type",
                    type="nominal",
                    title="Desc",
                ),
                opacity=alt.condition(type_select, alt.value(1), alt.value(0.25)),
            )
        )
        .add_params(type_select)
        .transform_filter(alt.datum.date >= f"{selected_date[0].strftime('%Y-%m-%d')}")
        .properties(title="Total Debit by Shopping Type")
    )

    dbt_pie = (
        (
            alt.Chart(df)
            .mark_arc(innerRadius=50)
            .encode(
                theta=alt.Theta(
                    "dbt",
                    type="quantitative",
                    aggregate="sum",
                    title="Sum of Debit",
                ),
                color=alt.Color(
                    field="desc",
                    type="nominal",
                    title="Desc",
                ),
                tooltip=['desc', 'sum(dbt)']
            )

        )
        .transform_filter(type_select)
        .transform_filter(alt.datum.date >= f"{selected_date[0].strftime('%Y-%m-%d')}")
        .properties(title="Debit Type by Day")
    )

    dbt = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="date:O",
            y="dbt:Q",
            color=alt.Color("desc:N", legend=None),
            tooltip=['date', 'desc', 'dbt', 'crd', 'bal']
        )
    ).transform_filter(alt.datum.date >= f"{selected_date[0].strftime('%Y-%m-%d')}"
                       ).transform_filter(type_select
                                          ).properties(width=1000)

    tpe = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="date:O",
            y="sum(dbt):Q",
            color="shopping_type:N",
            tooltip=['date', 'shopping_type', 'sum(dbt)']
        )
    ).transform_filter(alt.datum.date >= f"{selected_date[0].strftime('%Y-%m-%d')}"
                       ).transform_filter(type_select
                                          ).properties(width=1000)

    st.altair_chart((type_pie | tpe) & (dbt_pie | dbt), use_container_width=True)

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')