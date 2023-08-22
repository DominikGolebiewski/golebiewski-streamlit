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

with elements("bar"):
    with mui.Box(sx={ 'flexGrow': 1 }):
        with mui.AppBar( position="static"):
            with mui.Toolbar():
                with mui.IconButton(size = "large",aria_label = "account of current user",aria_controls = "menu-appbar",aria_haspopup = "true",color = "inherit"):
                    mui.icon.Menu(sx = {'color': 'white'})
                mui.Typography("DBT Elements", variant="h6", component="div", sx={ 'flexGrow': 1 })
                mui.Button("Login", color="inherit", onClick=lambda: st.write("Clicked!"), sx={ 'color': 'white' }, formattext="none", variant="text")
