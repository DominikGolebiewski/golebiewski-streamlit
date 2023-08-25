import json
from streamlit_elements import mui

def reset_filter(**kwargs):
    mui.Button(
        "Reset Filter",
        variant="outlined",
        sx={
            "color": "gray",
            "borderColor": None,
            "borderRadius": 0,
            "borderWidth": 0,
            "textTransform": "none",
            "fontSize": "0.5rem",
            "fontSize": 10,
            "transition": "none",
            '&:hover': {
                'color': 'red',
                'backgroundColor': 'white',
                'borderColor': 'white',
                'borderWidth': 0,
                'borderStyle': 'solid'
            },
        },
        disableRipple=True,
        onClick=kwargs.get("onClick", None),
    )