from uuid import uuid4
from abc import ABC, abstractmethod
from streamlit_elements import dashboard, mui
from contextlib import contextmanager


class Dashboard:

    DRAGGABLE_CLASS = "draggable"

    def __init__(self):
        self._layout = []

    def _register(self, item):
        self._layout.append(item)

    @contextmanager
    def __call__(self, **props):
        # Draggable classname query selector.
        props["draggableHandle"] = f".{Dashboard.DRAGGABLE_CLASS}"

        with dashboard.Grid(self._layout, **props):
            yield

    class Item(ABC):

        def __init__(self, board, x, y, w, h, **item_props):
            self._key = str(uuid4())
            self._draggable_class = Dashboard.DRAGGABLE_CLASS
            self._dark_mode = False
            board._register(dashboard.Item(self._key, x, y, w, h, **item_props))

        def _switch_theme(self):
            self._dark_mode = not self._dark_mode

        @contextmanager
        def title_bar(self, padding="5px 15px 5px 15px", dark_switcher=True, **kwargs):
            with mui.Stack(
                className=self._draggable_class,
                alignItems="center",
                direction="row",
                backgroundColor=kwargs.get("light_color", "#e6e6e6") if not self._dark_mode else kwargs.get("dark_color", "gray"),
                color="black" if not self._dark_mode else "white",
                spacing=1,
                sx={
                    "padding": padding,
                    "borderBottom": 1,
                    "borderColor": "divider",
                    '&:hover': {
                        'opacity': [0.8],
                        'cursor': 'grab',
                        'backgroundColor': kwargs.get("dark_color", "gray") if not self._dark_mode else kwargs.get("light_color", "#e6e6e6"),
                        }
                },
            ):
                yield

                if dark_switcher:
                    if self._dark_mode:
                        mui.IconButton(mui.icon.DarkMode, onClick=self._switch_theme)
                    else:
                        mui.IconButton(mui.icon.LightMode, sx={"color": "#ffc107"}, onClick=self._switch_theme)

        @abstractmethod
        def __call__(self):
            """Show elements."""
            raise NotImplementedError