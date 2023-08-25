import json
from streamlit_elements import mui, nivo
from .dashboard import Dashboard


class DailySales(Dashboard.Item):

    DUMMY_DATA = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._theme = {
            "dark": {
                "background": "#262730",
                "textColor": "#FAFAFA",
                "tooltip": {
                    "container": {
                        "background": "#262730",
                        "color": "FAFAFA",
                    }
                }
            },
            "light": {
                "background": "#FFFFFF",
                "textColor": "#31333F",
                "tooltip": {
                    "container": {
                        "background": "#FFFFFF",
                        "color": "#31333F",
                    }
                }
            }
        }

    def __call__(self, json_data, title, **kwargs):
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            data = self.DUMMY_DATA

        with mui.Paper(
                key=self._key,
                elevation=3,
                sx={
                   "display": "flex",
                   "flexDirection": "column",
                   "borderRadius": 2,
                   "overflow": "hidden"
                }):
            with self.title_bar():
                mui.icon.BarChart()
                mui.Typography(title, sx={"flex": 1})

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                nivo.Line(
                        data=data,
                        keys=["value"],
                        indexBy="day",
                        enableGridX=False,
                        enableGridY=True,
                        theme=self._theme["dark" if self._dark_mode else "light"],
                        margin={"top": 50, "right": 50, "bottom": 100, "left": 70},
                        padding=0.5,
                        valueScale={'type': 'linear'},
                        indexScale={'type': 'band', 'round': True},
                        colors=kwargs.get("bar_color", "gray"),
                        enableLabel=False,
                        valueFormat=">-1,.2f",
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
                            'legendOffset': 80
                        },
                        axisLeft={
                            'tickSize': 5,
                            'tickPadding': 0,
                            'tickRotation': 0,
                            'legend': 'Sales Value',
                            'legendPosition': 'middle',
                            'legendOffset': -50
                        },
                        motionConfig="wobbly",
                    )