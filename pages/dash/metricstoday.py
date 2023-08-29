import json
from streamlit_elements import mui, nivo, html
from .dashboard import Dashboard
from .style import TOP_BACKGROUND, NIVO_THEME_TOP
from streamlit import session_state as state

class MetricsToday(Dashboard.Item):

    DUMMY_DATA = [{}]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._top_background = TOP_BACKGROUND
        self._theme_top = NIVO_THEME_TOP


    def __call__(self, json_data, title, value_today, value_vs, value_format, key_column, value_prefix="", **kwargs):
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            data = self.DUMMY_DATA

        with html.div(
                key=self._key,
                css=
                {
                    "display": "flex",
                    "background-color": self._top_background["light" if self._dark_mode else "dark"],
                    "flexDirection": "column",
                    "border-radius": "10px",
                    "overflow": "hidden",
                    "backdrop-filter": "blur(10px)",
                    "-webkit-backdrop-filter": "blur(10px)",
                    "box-shadow": "0 8px 8px 0 rgba(0, 0, 0, 0.18)",
                }
        ):
            with self.title_bar(**kwargs):
                mui.icon.BarChart()
                mui.Typography(title, sx={"flex": 1})

            with mui.Box(sx={"flex": 1, "minHeight": 0}, **kwargs):
                nivo.Bar(
                        data=data,
                        keys=[f"{key_column}"],
                        indexBy="day",
                        enableGridX=False,
                        enableGridY=False,
                        margin={"top": 10, "right": 10, "bottom": 10, "left": 10},
                        padding=0.2,
                        valueScale={'type': 'linear'},
                        indexScale={'type': 'band', 'round': True},
                        colors=[kwargs.get("dark_color", "#363636") if self._dark_mode else kwargs.get("light_color", "#e6e6e6")],
                        enableLabel=False,
                        # valueFormat=">-1,.2f",
                        axisBottom=None,
                        axisLeft=None,
                        tooltip="none",
                        borderColor={
                            "from": "color",
                            "modifiers": [
                                [
                                    "darker",
                                    0.2,
                                ]
                            ]
                        },
                        motionConfig="molasses",
                    )

                with html.div(
                        className="overlay_text",
                        css={
                            "text-align": "center",
                            "position": "absolute",
                            "top": "50%",
                            "left": "50%",
                            "transform": "translate(-50%, -50%)",
                            "color": ["white" if self._dark_mode else "black"],
                            "font-size": "2rem",
                            "font-weight": "bold",
                            "margin-top": "2rem",
                        },
                ):
                    mui.Typography(
                        f"{value_prefix}" + str(value_format.format(value_today)),
                        sx={
                            'padding': 1,
                            'fontSize': 30,
                        })
                    mui.Typography(
                        self.arrow(value_vs),
                        sx={
                            'display': 'inline',
                            'fontSize': 14,
                            'mr': 1,
                            'color': 'green',
                            'verticalAlign': 'middle'
                        })
                    mui.Typography(
                        str("{:.0%}".format(value_vs)) + " vs. last week",
                        sx={
                            'display': 'inline',
                            'mb': 1,
                            'fontSize': 16,
                            'color': ['white' if self._dark_mode else "black"],
                        })
    def arrow(self, target_value):
        value = round(target_value * 100, 0)
        if value > 0:
            arrow = mui.icon.TrendingUp(sx={"color": ["lightgreen" if self._dark_mode else "green"]})
        elif value < 0:
            arrow = mui.icon.TrendingDown(sx={"color": "red"})
        elif value == 0:
            arrow = mui.icon.TrendingFlat(sx={"color": "blue"})
        else:
            arrow = ""
        return arrow