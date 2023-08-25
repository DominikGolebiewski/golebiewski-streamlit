import json
from streamlit_elements import mui
from .dashboard import Dashboard


class Footer(Dashboard.Item):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dark_theme = False


    def __call__(self, title, value_today, value_format):
        with mui.Paper(
                key=self._key,
                elevation=5,
                sx={
                    "borderRadius": 2,
                    "overflow": "hidden",
                    "width": "25%",
                }):
            with self.title_bar():
                mui.icon.Equalizer()
                mui.Typography(
                    title,
                    sx={
                        'padding': 1,
                        'flex': 1,
                        '&:hover': {
                            # 'color': 'black',
                            'opacity': [1],
                        }})
            with mui.Box(
                    borderRadius="inherit",
                    sx={
                        "flexDirection": "row",
                        "textAlign": "center"
                    }):
                mui.Typography(
                    "£" + str(value_format.format(value_today)),
                    sx={
                        'padding': 1,
                        'fontSize': 30,
                    })