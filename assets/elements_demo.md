# Streamlit Elements Demo

This is a Streamlit application demonstrating the usage of different visual elements and components to display and visualize sales data. The application employs the Streamlit library in conjunction with components from 'streamlit_elements', 'elements', 'mui', and 'nivo' libraries.

## Requirements

Ensure that you have the following libraries installed before running the code:

- `json`
- `streamlit`
- `pandas`
- `datetime`
- `streamlit_elements`
- `elements`
- `mui`
- `nivo`
- `SimpleNamespace` from `types`

## Main Functionality

The code defines a Streamlit application that showcases sales data through various visualizations. Below is an outline of the primary functionalities:

1. **Data Loading and Filtering:**
    - Data is sourced from a JSON file utilizing the `get_data` function.
    - A unique list of retailers is extracted using the `get_retailer` function.
    - Users can select a retailer using a dropdown widget in the sidebar.

2. **Visualizations:**
    - The code establishes a dashboard layout using the `dashboard.Grid` and `dashboard.Item` components.
    - The dashboard encompasses multiple visualizations:
        - **Pie Chart (Category Sales):**
            - Presents total sales by category for the chosen retailer over the past 28 days.
            - Relies on the `nivo.Pie` component for visualization.
        - **Bar Chart (Daily Sales):**
            - Displays daily sales for the selected retailer over the last 28 days.
            - Leverages the `nivo.Bar` component for visualization.
        - **Calendar Chart (Daily Sales):**
            - Exhibits a calendar heatmap illustrating daily sales for the selected retailer over the last 28 days.
            - Utilizes the `nivo.TimeRange` component for visualization.
        - **Pie Chart (Retailer Sales):**
            - Depicts total sales by retailer for the chosen retailer over the past 28 days.
            - Utilizes the `nivo.Pie` component for visualization.

3. **Serialization and Visualization:**
    - Data is serialized into JSON format using the `serialize_datetime` function to accommodate datetime objects.
    - The visualizations utilize components from the 'nivo' library, offering interactive and customizable charting capabilities.

## Running the Application

To launch the application, execute the script. The Streamlit app will open in your browser. You can pick a retailer using the dropdown in the sidebar to view various visualizations of sales data for that retailer over the past 28 days.