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
    with mui.AppBar(position="static", sx={"backgroundColor": "#fff"}):
        with mui.Container( maxWidth="xl"):
            with mui.Toolbar(disableGutters=True):
                mui.Typography(
                    "LOGO",
                    variant="h6",
                    noWrap=True,
                    component = "a",
                    # href = "/",
                    sx = {
                        'mr': 2,
                        # 'display': {'xs': 'none', 'md': 'flex'},
                        'fontFamily': 'monospace',
                        'fontWeight': 700,
                        'letterSpacing': '.3rem',
                        'color': 'black',
                        'textDecoration': 'none',
                    }
                )
                with mui.Box(sx = {'flexGrow': 1, 'display': {'xs': 'flex', 'md': 'none'}}):
                    mui.IconButton(size = "large",aria_label = "account of current user",aria_controls = "menu-appbar",aria_haspopup = "true",color = "inherit")