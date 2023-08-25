import json
from streamlit_elements import nivo, mui
from .dashboard import Dashboard
from .resetfilter import reset_filter

class CalendarHeatmap(Dashboard.Item):

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

    def __call__(self, json_data, title, from_date, to_date, **kwargs):
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            data = self.DUMMY_DATA

        with mui.Paper(
                key=self._key,
                sx={
                    "display": "flex",
                    "flexDirection": "column",
                    "borderRadius": 2,
                    "overflow": "hidden"},
                elevation=3):
            with self.title_bar():
                mui.icon.CalendarToday()
                mui.Typography(title, sx={"flex": 1})
                mui.Button(
                    "Reset Filter",
                    variant="text",
                    elevation=5,
                    sx={
                        "color": "white",
                        "borderRadius": 5,
                        "color": "gray" if not self._dark_mode else "lightgray",
                        "textTransform": "none",
                        "fontSize": "0.75rem",
                        "fontSize": 10,
                        "transition": "none",
                        '&:hover': {
                            'color': 'red'
                        },
                    },
                    disableRipple=True,
                    onClick=kwargs.get("onResetClick", None),
                )
            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                nivo.TimeRange(
                    onClick=kwargs.get("onClick", None),
                    data=data,
                    from_=from_date,
                    to=to_date,
                    emptyColor="#eeeeee",
                    colors=['#daf0ce', '#bee3aa', '#a1d485', '#81bf60','#6c9e51','#548739'],
                    theme=self._theme["dark" if self._dark_mode else "light"],
                    margin={'top': 40, 'right': 40, 'bottom': 40, 'left': 40},
                    dayBorderWidth=2,
                    dayBorderColor="#ffffff",
                    weekdayTicks=[0, 1, 2, 3, 4, 5, 6],
                    motionConfig="wobbly",
                    legends=[
                        {
                            'anchor': 'top-right',
                            'direction': 'column',
                            'justify': True,
                            'itemCount': 5,
                            'itemWidth': 60,
                            'itemHeight': 36,
                            'itemsSpacing': 20,
                            'itemDirection': 'right-to-left',
                            'translateX': -50,
                            'translateY': 0,
                            'symbolSize': 14
                        }
                    ]
                )