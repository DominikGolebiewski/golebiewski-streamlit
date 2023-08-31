from streamlit_elements import html, elements
from contextlib import contextmanager
from abc import ABC, abstractmethod
import uuid


class ChartContainer:
    def __init__(self, height, width, border="2px solid #d3d3d3"):
        self._key = str(uuid.uuid4())
        self.height = height
        self.width = width
        self.border = border

    @contextmanager
    def div(self):
        with html.div(
            key=self._key,
            css={
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "background-color": "white",
                    "border": "2px solid #d3d3d3",
                    "border-radius": "10px",
                    "box-shadow": "5px 5px 5px 0 rgba(0, 0, 0, 0.4)",
                    "height": self.height,
                    "width": self.width,
                    "margin": "10px"
                }
        ):
            yield
