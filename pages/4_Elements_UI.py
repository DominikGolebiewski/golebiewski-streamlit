import json
import duckdb as du
import streamlit as st
import pandas as pd
import datetime
import requests
import tempfile
from streamlit import session_state as ss
from types import SimpleNamespace as sn
from pathlib import Path
from streamlit_elements import dashboard, elements, mui, nivo

RETAILERS = [
    {"verbose_name": "Morrisons", "name": "morrisons", "id": 17},
    {"verbose_name": "Tesco", "name": "tesco", "id": 14},
]

REPOS = [
    {"name": "morrisons_transformer", "verbose_name": "Morrisons Transformer", "id": 17, "database": "aa_transformer_morrisons", "schema": "dbt_prod"},
    {"name": "tesco_transformer", "verbose_name": "Tesco Transformer", "id": 14, "database": "aa_transformer_tesco", "schema": "dbt_prod"},
    {"name": "dsr", "verbose_name": "DSR Analytics", "id": None, "database": "aa_dsr_analytics", "schema": "dbt_dsr_prod"},
    {"name": "desire_analytics", "verbose_name": "Desire Analytics", "id": None, "database": "aa_desire_analytics", "schema": "production"},
]


if "cf" not in ss:
    cf = {
        'selected_tab': 0,
        'selected_repo': None,
        'selected_database': None,
        'selected_schema': None,
        'selected_verbose_name': None,
        'selected_retailer': None,
        'selected_retailer_id': None,
    }
    ss.cf = cf
else:
    cf = ss.cf




with elements("repository_select"):

    def repo_select_callback(event, info):
        filtered_repos = []
        ss.cf["selected_repo"] = info.props.value
        ss.cf["selected_database"] = [repo["database"] for repo in REPOS if repo["name"] == ss.cf["selected_repo"]]
        ss.cf["selected_schema"] = [repo["schema"] for repo in REPOS if repo["name"] == ss.cf["selected_repo"]]
        ss.cf["selected_retailer_id"] = [repo["id"] for repo in REPOS if repo["name"] == ss.cf["selected_repo"]]

    with mui.Box(sx={ "minWidth": 120}):
        with mui.FormControl(sx={"m": 1, "minWidth": 120}):
            with mui.InputLabel(id="repo-select-label"):
                mui.Typography("Select Repository")
            with mui.Select(
                labelId="repo-select-label",
                id="repo-select",
                label="Select Repository",
                value=ss.cf["selected_repo"],
                MenuProps={
                    'PaperProps': {
                        'sx': {
                            'autoHeight': True,
                            'height': 100,
                            'width': 300,
                            'borderRadius': 3,
                            'border': '1px solid #ced4da'
                        },
                    },
                },
                sx={
                    "width": 300,
                    "borderRadius": 3,
                    "border": "1px solid #ced4da",
                    "flex": "1",
                },
                onChange=repo_select_callback):

                for repo in REPOS:
                    mui.MenuItem(repo["verbose_name"], value=repo["name"])


    def tab_select_callback(event, info):
        ss.cf["selected_tab"] = info

    with mui.lab.TabContext(value=ss.cf["selected_tab"]):
        with mui.Box(sx={"borderBottom": 1, "borderColor": "divider"}):
            with mui.lab.TabList(onChange=tab_select_callback):
                mui.Tab(label="Insert By Replace", value=1, index=1)
                mui.Tab(label="Editor", value=2, disabled=True, index=2)
                mui.Tab(label="Data grid", value=3, index=3)

        def retailer_selection_callback(event, info):
            ss.cf["selected_retailer"] = info.props.value

        with mui.lab.TabPanel(value=1):
            with mui.FormControl(sx={"m": 1, "minWidth": 120}):
                with mui.InputLabel(id="replace-select-retailer-label"):
                    mui.Typography("Select Retailer")
                with mui.Select(
                        labelId="replace-select-retailer-label",
                        id="replace-select-retailer",
                        label="Select Retailer",
                        value=ss.cf["selected_retailer"],
                        MenuProps={
                            'PaperProps': {
                                'sx': {
                                    'autoHeight': True,
                                    'height': 100,
                                    'width': 300,
                                    'borderRadius': 3,
                                    'border': '1px solid #ced4da'
                                },
                            },
                        },
                        sx={
                            "width": 300,
                            "borderRadius": 3,
                            "border": "1px solid #ced4da",
                            "flex": "1",
                        },
                        onChange=retailer_selection_callback):
                    for retailer in RETAILERS:
                        mui.MenuItem(retailer["verbose_name"], value=retailer["name"])
                mui.lab.DatePicker(
                    label="Select Start Date"
                )
                mui.lab.DatePicker(
                    label="Select End Date"
                )

