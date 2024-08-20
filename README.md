# Olympic Medals Analysis Application

## Overview

The Olympic Medals Analysis Application is a Streamlit-based web app designed to display and analyze data on Olympic medals. Users can filter and explore the data based on various parameters such as country, discipline, athlete, and more. The application uses Streamlit for the user interface, Pandas for data manipulation, and Plotly for generating visualizations.

## Features

- **Interactive Filtering**: Filter the Olympic medal data by year, discipline, country, athlete, and more.
- **Data Display**: View filtered data in a tabular format.
- **Data Aggregation**: Aggregate and visualize medal counts by country and athlete.
- **User-Friendly Interface**: Utilize an interactive sidebar for navigation and filtering options.

## File Structure

- `olympic_app.py`: The main Python script containing the Streamlit application code.
- `requirements.txt`: A file listing the required Python packages for the project.
- `data/olympic_medals.xlsx`: The Excel file containing Olympic medals data.

## Dependencies

This project requires the following Python libraries:

- [Streamlit](https://streamlit.io): For creating the interactive web interface.
- [Pandas](https://pandas.pydata.org): For data manipulation and analysis.
- [Plotly](https://plotly.com): For creating interactive visualizations.

These libraries are specified in the `requirements.txt` file.

## Installation

To set up the project, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Jana-B/Olympic_App
   cd olympic_medals_analysis
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the Streamlit application, use the following command:

```bash
streamlit run olympic_app.py
```

This will start a local server and open the application in your default web browser.

## Code Overview

The application is implemented in `olympic_app.py`, and it consists of:

- **`OlympicMedalsApp` class**: Manages the loading, processing, and filtering of data, and renders the Streamlit interface.
  - `__init__()`: Initializes the application, loads data, and prepares it for display.
  - `get_data()`: Loads the Olympic medals data from an Excel file.
  - `transform_for_display()`: Cleans and transforms the data for display.
  - `render_sidebar()`: Creates the sidebar for filtering and navigation.
  - `render_data_view()`: Displays the filtered data.
  - `render_aggregate_view()`: Shows aggregated medal counts by country and athlete.
  - `run()`: Runs the Streamlit application.
