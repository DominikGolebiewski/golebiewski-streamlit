import json
from streamlit_elements import mui, nivo
from .dashboard import Dashboard


class CategorySales(Dashboard.Item):
    DEFAULT_DATA = [
        {"id": "java", "label": "java", "value": 465, "color": "hsl(128, 70%, 50%)"},
        {"id": "rust", "label": "rust", "value": 140, "color": "hsl(178, 70%, 50%)"},
        {"id": "scala", "label": "scala", "value": 40, "color": "hsl(322, 70%, 50%)"},
        {"id": "ruby", "label": "ruby", "value": 439, "color": "hsl(117, 70%, 50%)"},
        {"id": "elixir", "label": "elixir", "value": 366, "color": "hsl(286, 70%, 50%)"}
    ]

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
            data = self.DEFAULT_DATA

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
                mui.icon.PieChart()
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
                nivo.Pie(
                    onClick=kwargs.get("onClick", None),
                    data=data,
                    theme=self._theme["dark" if self._dark_mode else "light"],
                    margin={"top": 40, "right": 80, "bottom": 80, "left": 80},
                    innerRadius=0.5,
                    padAngle=0.7,
                    cornerRadius=3,
                    activeOuterRadiusOffset=8,
                    colors={'scheme': 'set3'},
                    borderWidth=1,
                    borderColor={
                        "from": "color",
                        "modifiers": [
                            [
                                "darker",
                                0.2,
                            ]
                        ]
                    },
                    arcLinkLabelsSkipAngle=10,
                    arcLinkLabelsTextColor="grey",
                    arcLinkLabelsThickness=2,
                    arcLinkLabelsColor={"from": "color"},
                    arcLabelsSkipAngle=10,
                    arcLabelsTextColor={
                        "from": "color",
                        "modifiers": [
                            [
                                "darker",
                                2
                            ]
                        ]
                    },
                    enableArcLabels=False,
                    motionConfig="stiff",
                )


