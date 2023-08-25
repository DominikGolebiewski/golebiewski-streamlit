import json
from streamlit_elements import mui
from .dashboard import Dashboard


class TotalElement(Dashboard.Item):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dark_theme = False


    def __call__(self, title, value_today, value_vs, value_format, light_color="#e6e6e6", dark_color="gray"):
        arrow = self.arrow
        with mui.Paper(
                key=self._key,
                elevation=5,
                sx={
                    "borderRadius": 2,
                    "overflow": "hidden",
                    "width": "25%",
                }):
            with self.title_bar(light_color=light_color, dark_color=dark_color):
                mui.icon.QueryStats()
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
                mui.Typography(
                    arrow(value_vs),
                    sx={
                        'display': 'inline',
                        'fontSize': 14,
                        'mr': 1,
                        'color': 'green',
                        'verticalAlign': 'middle'
                    })
                mui.Typography(
                    str("{:.0%}".format(value_vs))  + " vs. last week",
                    sx={
                        'display': 'inline',
                        'mb': 1,
                        'fontSize': 16,
                        'color': 'gray',
                    })

    def arrow(self, target_value):
        value = round(target_value * 100, 0)
        if value > 0:
            arrow = mui.icon.TrendingUp(sx={"color": "green"})
        elif value < 0:
            arrow = mui.icon.TrendingDown(sx={"color": "red"})
        elif value == 0:
            arrow = mui.icon.TrendingFlat(sx={"color": "lightblue"})
        else:
            arrow = ""
        return arrow
