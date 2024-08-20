"""
Olympic Medals Analysis Application

This application is designed to display and analyze data on Olympic medals, allowing users to filter and explore the data based on various parameters such as country, discipline, athlete, and more. It uses Streamlit for the user interface and Plotly for generating visualizations.

Main Features:
- Filter Olympic medal data by year, discipline, country, athlete, and more.
- Display filtered data in a tabular format.
- Aggregate and visualize medal counts by country and athlete.
- Interactive sidebar for navigation and filtering options.

Dependencies:
- streamlit
- pandas
- plotly

Usage:
Run this script using Streamlit to start the application.

Example:
    $ streamlit run olympic_medals_app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px


def replace_column_names_with_medals(df):
    medal_mapping = {
        1: "🥇",  # Gold Medal
        2: "🥈",  # Silver Medal
        3: "🥉"   # Bronze Medal
    }
    # Replace the column names
    df = df.rename(columns=medal_mapping)
    return df


class OlympicMedalsApp:
    def __init__(self):
        """
        Initialize the OlympicMedalsApp class.

        This includes loading the Olympic medals data from an Excel file and setting up 
        the initial state of the application, including the data view and filtering options.
        """
        self.data_path = "data/olympic_medals.xlsx"
        self.olympic_medals = self.get_data()
        self.olympic_medals, self.filtered_data = self.transform_for_display()
        self.view = "Filtered Data View"

    @st.cache_data
    def get_data(_self):
        """
        Load the Olympic medals data from an Excel file.

        Returns:
            pd.DataFrame: DataFrame containing the Olympic medals data.
        """
        df = pd.read_excel(_self.data_path, index_col=None)
        return df
    

    @st.cache_data    
    def transform_for_display(_self):
        """
        Transform and clean the Olympic medals data for display.

        This method prepares the data by:
        - Converting the year to a string format.
        - Removing any unnamed columns.
        - Reordering and renaming columns for easier analysis and display.

        Returns:
            pd.DataFrame: Cleaned and transformed DataFrame ready for display.
            pd.DataFrame: A copy of the cleaned DataFrame for further filtering.   
        """
        def format_slug(slug):
            """ 
            Transform and clean the Game column for display.
            
            This method prepares the data by:
            - Splitting the slug at the last hyphen "-".
            - Capitalizing the location.
            - Reordering by placing the year before the location.
            """
            # Split the string by the hyphen
            parts = slug.rsplit('-', 1)
            # Check if the second part is numeric
            if len(parts) == 2 and parts[1].isdigit():
                location = parts[0]
                year = parts[1]
            # Capitalize the first letter of the location
            location = location.capitalize()
            # Return the formatted string
            return f"{year} {location}"
        
        _self.olympic_medals["year"] = _self.olympic_medals["year"].astype(str)
        _self.olympic_medals["slug_game"] = _self.olympic_medals['slug_game'].apply(format_slug)
        _self.olympic_medals = _self.olympic_medals.loc[:, ~_self.olympic_medals.columns.str.contains("^Unnamed")]        
        
        
        
        # Reorder the columns in the specified sequence
        df_olympic_medals = _self.olympic_medals[
            [                                
                "slug_game",
                "medal_code",
                "athlete_full_name",
                "country_name",
                "discipline_title",
                "event_title",
                "event_gender",
                "participant_type",
                "year"
            ]
        ]
        
        # Rename the columns
        df_olympic_medals = df_olympic_medals.rename(
            columns={
                "slug_game": "Game",
                "medal_code": "Placement",
                "athlete_full_name": "Athlete",
                "country_name": "Country",
                "discipline_title": "Discipline",
                "event_title": "Event",
                "event_gender": "Event Gender",
                "participant_type": "Participant Type",
                "year": "Year",
            }
        )

        # Create a copy for the filtered data
        df_filtered_data = df_olympic_medals.copy()

        return df_olympic_medals, df_filtered_data
    
    def render_sidebar(self):
        """
        Render the Streamlit sidebar with navigation and filtering options.

        The sidebar allows users to navigate between different views of the data and 
        apply filters such as year, discipline, event gender, and country to refine the data.
        """
        st.sidebar.header("Navigation")
        self.view = st.sidebar.radio(
            "Select View", ["Filtered Data View", "Aggregated Data View"]
        )

        st.sidebar.header("Filters")

        # Year or Year Range
        year_range = st.sidebar.checkbox("Filter by Year Range", value=False)
        if year_range:
            start_year, end_year = st.sidebar.slider(
                "Select Year Range",
                min_value=int(self.olympic_medals["Year"].min()),
                max_value=int(self.olympic_medals["Year"].max()),
                value=(2000, 2024),
            )
         
        else:
            start_year, end_year = None, None

        # Sidebar filters
        game = st.sidebar.multiselect(
            "Game", sorted(self.olympic_medals["Game"].unique())
        )
        athlete = st.sidebar.multiselect(
            "Athlete", sorted(self.olympic_medals["Athlete"].unique(), key=str)
        )
        
        participant_type = st.sidebar.multiselect(
            "Participant Type", sorted(self.olympic_medals["Participant Type"].unique())
        )
        event_gender = st.sidebar.multiselect(
            "Event Gender", sorted(self.olympic_medals["Event Gender"].unique())
        )
        placement = st.sidebar.multiselect(
            "Placement", sorted(self.olympic_medals["Placement"].unique())
        )
        country = st.sidebar.multiselect(
            "Country", sorted(self.olympic_medals["Country"].unique(), key=str)
        )
        discipline = st.sidebar.multiselect(
            "Discipline", sorted(self.olympic_medals["Discipline"].unique())
        )

        # Apply filters to the data to determine available event titles
        filtered_data_temp = self.olympic_medals

        if game:
            filtered_data_temp = filtered_data_temp[
                filtered_data_temp["Game"].isin(game)
            ]
        if athlete:
            filtered_data_temp = filtered_data_temp[
                filtered_data_temp["Athlete"].isin(athlete)
            ]
        if discipline:
            filtered_data_temp = filtered_data_temp[
                filtered_data_temp["Discipline"].isin(discipline)
            ]
        if participant_type:
            filtered_data_temp = filtered_data_temp[
                filtered_data_temp["Participant Type"].isin(participant_type)
            ]
        if event_gender:
            filtered_data_temp = filtered_data_temp[
                filtered_data_temp["Event Gender"].isin(event_gender)
            ]
        if placement:
            filtered_data_temp = filtered_data_temp[
                filtered_data_temp["Placement"].isin(placement)
            ]
        if country:
            filtered_data_temp = filtered_data_temp[
                filtered_data_temp["Country"].isin(country)
            ]

        # Update the event title filter based on the filtered data
        event = st.sidebar.multiselect(
            "Event Title", sorted(filtered_data_temp["Event"].unique())
        )

        # Apply filters to the data
        self.filtered_data = self.olympic_medals

  
        if start_year and end_year:
            self.filtered_data = self.filtered_data[
                (self.filtered_data["Year"].astype(int) >= start_year)
                & (self.filtered_data["Year"].astype(int) <= end_year)
            ]

        if game:
            self.filtered_data = self.filtered_data[
                self.filtered_data["Game"].isin(game)
            ]
        if athlete:
            self.filtered_data = self.filtered_data[
                self.filtered_data["Athlete"].isin(athlete)
            ]
        if discipline:
            self.filtered_data = self.filtered_data[
                self.filtered_data["Discipline"].isin(discipline)
            ]
        if participant_type:
            self.filtered_data = self.filtered_data[
                self.filtered_data["Participant Type"].isin(participant_type)
            ]
        if event_gender:
            self.filtered_data = self.filtered_data[
                self.filtered_data["Event Gender"].isin(event_gender)
            ]
        if placement:
            self.filtered_data = self.filtered_data[
                self.filtered_data["Placement"].isin(placement)
            ]
        if country:
            self.filtered_data = self.filtered_data[
                self.filtered_data["Country"].isin(country)
            ]
        if event:
            self.filtered_data = self.filtered_data[
                self.filtered_data["Event"].isin(event)
            ]
        
    def render_data_view(self):
        """
        Render the filtered data and display it in the Streamlit app.

        This method displays the Olympic medals data in a tabular format based on the 
        filters applied by the user. It also shows the number of records after filtering.
        """
        st.title("Olympic Medalists Filter")
        st.write(f"Number of records: {self.filtered_data.shape[0]}")
        st.dataframe(self.filtered_data, hide_index=True)
        

    def render_aggregate_view(self):
        """
        Render an aggregate view of Olympic medals by country, discipline, game, and medal type.

        This view groups and sums the number of gold, silver, and bronze medals for each 
        combination of country, discipline, and game. It also provides an aggregated view by athlete.
        """
        st.title("Olympic Medals Aggregated View")

        # Group by 'country_name' and 'medal_type'
        aggregated_country_data = (
            self.filtered_data.groupby(
                [
                    "Country",                    
                    "Placement",
                ]
            )
            .size()
            .unstack(fill_value=0)
            .reset_index()
        )

        # Reorder the columns to have 'Gold', 'Silver', and 'Bronze'
        columns_order = [
            "Country",
            1,
            2,
            3,
        ]
        aggregated_country_data = (
            aggregated_country_data[columns_order]
            if all(col in aggregated_country_data.columns for col in columns_order)
            else aggregated_country_data
        )

        aggregated_country_data['Medals Total'] = aggregated_country_data[1] + aggregated_country_data[2] + aggregated_country_data[3]

        aggregated_country_data = replace_column_names_with_medals(aggregated_country_data)        

        st.write("### Aggregated Medal Count by Country")
        st.dataframe(aggregated_country_data, hide_index=True)


        # Aggregate data by 'athlete_full_name' and 'medal_type'
        aggregated_athlete_data = (
            self.filtered_data.groupby(
                [
                    "Athlete",                    
                    "Placement",
                ]
            )
            .size()
            .unstack(fill_value=0)
            .reset_index()
        )
        
        

        # Reorder the columns to have 'Gold', 'Silver', and 'Bronze'
        columns_order_athlete = [
            "Athlete",
            1,
            2,
            3,
        ]
        aggregated_athlete_data = (
            aggregated_athlete_data[columns_order_athlete]
            if all(col in aggregated_athlete_data.columns for col in columns_order_athlete)
            else aggregated_athlete_data
        )

    

        aggregated_athlete_data['Medals Total'] = aggregated_athlete_data[1] + aggregated_athlete_data[2] + aggregated_athlete_data[3]
        aggregated_athlete_data = replace_column_names_with_medals(aggregated_athlete_data)
        
        st.write("### Aggregated Medal Count by Athlete")
    
        aggregated_athlete_data = aggregated_athlete_data.loc[~aggregated_athlete_data['Athlete'].str.contains('TEAM')]

        st.dataframe(aggregated_athlete_data, hide_index=True)
        
        
        self.plot_medals_per_country()
        
        self.plot_medals_per_athlete()
        
        
    def plot_medals_per_country(self):
        """
        Plot the number of medals per country.
        """
         # Group by 'country_name' and sum the medals
        medal_counts = (
            self.filtered_data.groupby("Country")["Placement"]
            .value_counts()
            .unstack(fill_value=0)
            .reset_index()
        )

        # Convert to long format for plotting
        medal_counts_long = medal_counts.melt(id_vars="Country", 
                                            value_vars=[1, 2, 3],
                                            var_name="Placement", 
                                            value_name="Count")

        # Define custom colors for each medal type
        custom_colors = {
            1: "#FFD700",   # Gold color
            2: "#C0C0C0", # Silver color
            3: "#CD7F32"  # Bronze color
        }

        # Plot using Plotly
        fig = px.bar(medal_counts_long, 
                    x="Country", 
                    y="Count", 
                    color="Placement",
                    title="Medals per Country",
                    labels={"Country": "Country", "Count": "Number of Medals"},
                    height=600,
                    color_discrete_map=custom_colors)  # Apply custom colors
        
        st.plotly_chart(fig)


    def plot_medals_per_athlete(self):
        """
        Plot the number of medals per athlete.
        """
        
        # athlete_data = self.filtered_data.loc[~self.filtered_data['Athlete'].str.contains('TEAM')]
        
        # Group by 'athlete_full_name' and sum the medals
        medal_counts = (
            athlete_data.groupby("Athlete")["Placement"]
            .value_counts()
            .unstack(fill_value=0)
            .reset_index()
        )

        # Convert to long format for plotting
        medal_counts_long = medal_counts.melt(id_vars="Athlete", 
                                            value_vars=[1, 2, 3],
                                            var_name="Placement", 
                                            value_name="Count")

        # Define custom colors for each medal type
        custom_colors = {
            1: "#FFD700",   # Gold color
            2: "#C0C0C0", # Silver color
            3: "#CD7F32"  # Bronze color
        }

        # Plot using Plotly
        fig = px.bar(medal_counts_long, 
                    x="Athlete", 
                    y="Count", 
                    color="Placement",
                    title="Medals per Athlete",
                    labels={"Athlete": "Athlete", "Count": "Number of Medals"},
                    height=600,
                    color_discrete_map=custom_colors)  # Apply custom colors

        st.plotly_chart(fig)
        
        

    def run(self):
        """
        Run the Streamlit application.

        This method coordinates the rendering of the sidebar and the main view based on the 
        selected view (filtered data view or aggregated data view).
        """
        self.render_sidebar()

        if self.view == "Filtered Data View":
            self.render_data_view()
        elif self.view == "Aggregated Data View":
            self.render_aggregate_view()

if __name__ == "__main__":
    app = OlympicMedalsApp()
    app.run()
