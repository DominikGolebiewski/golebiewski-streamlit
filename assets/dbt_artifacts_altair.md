# DBT Artifacts - Interactive Altair Demo

This is a Streamlit application that demonstrates interactive visualizations using the Altair library. The application visualizes data related to DBT (Data Build Tool) artifacts, including project invocations and model execution times.

## Requirements

Make sure you have the following libraries installed before running the code:

- `streamlit`
- `pandas`
- `altair`
- `datetime`
- `json`

## Main Functionality

The code defines a Streamlit application that displays interactive visualizations for DBT artifacts. Here's an overview of the main functionalities:

1. **Data Loading and Preprocessing:**
    - Data is loaded from a JSON file using the `get_data` function.
    - The data is structured and processed into a Pandas DataFrame.
    - Date columns are converted to appropriate date formats using `pd.to_datetime`.

2. **Interactive Visualizations:**
    - The application provides interactive visualizations for project invocations and model execution times.
    - The visualizations include line charts, bar charts, and a combination of both.
    - Data selection and highlighting are enabled using Altair's selection features.

3. **Visualizations Overview:**
    - **Line Chart (28-day Execution Time):**
        - Displays the median execution time of project invocations over the last 28 days.
        - Colors differentiate between different project names.
        - Interaction: Clicking on the legend highlights the corresponding project.
        
    - **Point Chart (28-day Execution Time):**
        - Displays individual data points for the execution time over the last 28 days.
        - Points change color based on selection (brush) and project name.
        - Interaction: Clicking on the legend or a data point highlights the corresponding data.
        
    - **Gantt Chart (Project Execution Time):**
        - Shows a Gantt chart of project invocations with start and end times.
        - Projects are colored based on a predefined color range.
        - Interaction: Clicking on a project name in the legend or a data bar highlights the corresponding data.
        
    - **Gantt Chart (Model Execution Time):**
        - Displays a Gantt chart of model execution times with start and end times.
        - Models are grouped by project and colored based on project names.
        - Interaction: Clicking on a project name in the legend or a data bar highlights the corresponding data.

## Running the Application

To run the application, execute the script. The Streamlit app will open in your browser, showing interactive visualizations related to DBT artifacts. You can interact with the charts by clicking on legends, data points, or data bars to highlight and explore specific data points.