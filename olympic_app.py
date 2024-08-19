import streamlit as st
import pandas as pd
import plotly.express as px

class OlympicMedalsApp:
    def __init__(self):
        """
        Initialize the OlympicMedalsApp class.
        This includes loading the data and setting up the Streamlit app components.
        """
        self.data_path = "data/olympic_medals.xlsx"
        self.olympic_medals = self.get_data()
        self.olympic_medals, self.filtered_data = self.transform_for_display()
        self.view = "Filtered Data View"

    @st.cache_data    
    def transform_for_display(_self):
        _self.olympic_medals["year"] = _self.olympic_medals["year"].astype(str)
        _self.olympic_medals = _self.olympic_medals.loc[:, ~_self.olympic_medals.columns.str.contains("^Unnamed")]        
        
        # Reorder the columns in the specified sequence
        df_olympic_medals = _self.olympic_medals[
            [                                
                "discipline_title",
                "event_title",
                "medal_code",                               
                "athlete_full_name",
                "country_name",
                "country_code",
                "participant_type",
                "athlete_url",
                "medal_type",
                "year",
                "location",
                "event_gender",
                "slug_game",
            ]
        ]
        
        # Rename the columns
        df_olympic_medals = df_olympic_medals.rename(
            columns={
                "discipline_title": "Discipline",
                "event_title": "Event",
                "medal_code": "Medal",
                "athlete_full_name": "Athlete",
                "country_name": "Country",
                "country_code": "Country Code",
                "participant_type": "Participant Type",
                "athlete_url": "Athlete URL",
                "medal_type": "Medal Type",
                "year": "Year",
                "location": "Location",
                "event_gender": "Event Gender",
                "slug_game": "Game",
            }
        )

        # Create a copy for the filtered data
        df_filtered_data = df_olympic_medals.copy()

        return df_olympic_medals, df_filtered_data
    
    @st.cache_data
    def get_data(_self):
        """
        Load the Olympic medals data from an Excel file.

        Returns:
            pd.DataFrame: DataFrame containing the Olympic medals data.
        """
        df = pd.read_excel(_self.data_path, index_col=None)
        return df
    
    def render_sidebar(self):
        """
        Render the sidebar with navigation options and filtering options.
        This method includes filters for year or year range, location, discipline, event gender, medal type, and country.
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
            year = None
        else:
            year = st.sidebar.selectbox(
                "Select Year",
                options=[None] + sorted(self.olympic_medals["Year"].unique()),
                index=len(self.olympic_medals["Year"].unique()),
            )
            start_year, end_year = None, None

        # Sidebar filters
        game = st.sidebar.multiselect(
            "Game", sorted(self.olympic_medals["Game"].unique())
        )
        # location = st.sidebar.multiselect(
        #     "Location", sorted(self.olympic_medals["Location"].unique())
        # )
        participant_type = st.sidebar.multiselect(
            "Participant Type", sorted(self.olympic_medals["Participant Type"].unique())
        )

        discipline = st.sidebar.multiselect(
            "Discipline", sorted(self.olympic_medals["Discipline"].unique())
        )
        event_gender = st.sidebar.multiselect(
            "Event Gender", sorted(self.olympic_medals["Event Gender"].unique())
        )
        medal_type = st.sidebar.multiselect(
            "Medal Type", sorted(self.olympic_medals["Medal Type"].unique())
        )
        country = st.sidebar.multiselect(
            "Country", sorted(self.olympic_medals["Country"].unique(), key=str)
        )

        # Apply filters to the data to determine available event_titles
        filtered_data_temp = self.olympic_medals

        if game:
            filtered_data_temp = filtered_data_temp[
                filtered_data_temp["Game"].isin(game)
            ]
        # if location:
        #     filtered_data_temp = filtered_data_temp[
        #         filtered_data_temp["Location"].isin(location)
        #     ]
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
        if medal_type:
            filtered_data_temp = filtered_data_temp[
                filtered_data_temp["Medal Type"].isin(medal_type)
            ]
        if country:
            filtered_data_temp = filtered_data_temp[
                filtered_data_temp["Country"].isin(country)
            ]

        # Update the event_title filter based on the filtered data
        event = st.sidebar.multiselect(
            "Event Title", sorted(filtered_data_temp["Event"].unique())
        )

        # Apply filters to the data
        self.filtered_data = self.olympic_medals

        if year:
            self.filtered_data = self.filtered_data[self.filtered_data["Year"] == year]
        elif start_year and end_year:
            self.filtered_data = self.filtered_data[
                (self.filtered_data["Year"].astype(int) >= start_year)
                & (self.filtered_data["Year"].astype(int) <= end_year)
            ]

        if game:
            self.filtered_data = self.filtered_data[
                self.filtered_data["Game"].isin(game)
            ]
        # if location:
        #     self.filtered_data = self.filtered_data[
        #         self.filtered_data["Location"].isin(location)
        #     ]
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
        if medal_type:
            self.filtered_data = self.filtered_data[
                self.filtered_data["Medal Type"].isin(medal_type)
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
        """
        st.title("Olympic Medalists Filter")
        st.write(f"Number of records: {self.filtered_data.shape[0]}")
        st.dataframe(self.filtered_data,hide_index=True)

    def render_aggregate_view(self):
        """
        Render an aggregate view of Olympic medals by country, discipline, game, and medal type.
        This view sums the number of gold, silver, and bronze medals for each combination of country, discipline, and game,
        and orders them with gold first, followed by silver and bronze. It also provides an aggregated view by athlete.
        """
        st.title("Olympic Medals Aggregated View")

        # Group by 'country_name' and 'medal_type'
        aggregated_country_data = (
            self.filtered_data.groupby(
                [
                    "country_name",                    
                    "medal_type",
                ]
            )
            .size()
            .unstack(fill_value=0)
            .reset_index()
        )

        # Reorder the columns to have 'Gold', 'Silver', and 'Bronze'
        columns_order = [
            "country_name",
            "GOLD",
            "SILVER",
            "BRONZE",
        ]
        aggregated_country_data = (
            aggregated_country_data[columns_order]
            if all(col in aggregated_country_data.columns for col in columns_order)
            else aggregated_country_data
        )

        # Sorting options for country view
        st.subheader("Medals by Country")
        sort_by_country = st.selectbox(
            "Sort by (Country)",
            ["GOLD", "SILVER", "BRONZE", "country_name"],
            index=0
        )
        
        sort_order_country = st.radio(
            "Sort order (Country)",
            ("Descending", "Ascending"),
            index=0,
            key="country_order"
        )
        
        ascending_country = True if sort_order_country == "Ascending" else False
        aggregated_country_data = aggregated_country_data.sort_values(by=sort_by_country, ascending=ascending_country)

        # Show the top 10 countries
        st.dataframe(aggregated_country_data.head(10))

        # Group by 'athlete_full_name' and 'medal_type'
        aggregated_athlete_data = (
            self.filtered_data.groupby(
                [
                    "athlete_full_name",                    
                    "medal_type",
                ]
            )
            .size()
            .unstack(fill_value=0)
            .reset_index()
        )

        # Reorder the columns to have 'Gold', 'Silver', and 'Bronze'
        columns_order_athlete = [
            "athlete_full_name",
            "GOLD",
            "SILVER",
            "BRONZE",
        ]
        aggregated_athlete_data = (
            aggregated_athlete_data[columns_order_athlete]
            if all(col in aggregated_athlete_data.columns for col in columns_order_athlete)
            else aggregated_athlete_data
        )

        # Sorting options for athlete view
        st.subheader("Medals by Athlete")
        sort_by_athlete = st.selectbox(
            "Sort by (Athlete)",
            ["GOLD", "SILVER", "BRONZE", "athlete_full_name"],
            index=0
        )
        
        sort_order_athlete = st.radio(
            "Sort order (Athlete)",
            ("Descending", "Ascending"),
            index=0,
            key="athlete_order"
        )
        
        ascending_athlete = True if sort_order_athlete == "Ascending" else False
        aggregated_athlete_data = aggregated_athlete_data.sort_values(by=sort_by_athlete, ascending=ascending_athlete)

        # Show the top 10 athletes
        st.dataframe(aggregated_athlete_data.head(10))

    def plot_medals_per_country(self):
        """
        Plot the number of medals per country.
        """
         # Group by 'country_name' and sum the medals
        medal_counts = (
            self.filtered_data.groupby("country_name")["medal_type"]
            .value_counts()
            .unstack(fill_value=0)
            .reset_index()
        )

        # Convert to long format for plotting
        medal_counts_long = medal_counts.melt(id_vars="country_name", 
                                            value_vars=["GOLD", "SILVER", "BRONZE"],
                                            var_name="Medal Type", 
                                            value_name="Count")

        # Define custom colors for each medal type
        custom_colors = {
            "GOLD": "#FFD700",   # Gold color
            "SILVER": "#C0C0C0", # Silver color
            "BRONZE": "#CD7F32"  # Bronze color
        }

        # Plot using Plotly
        fig = px.bar(medal_counts_long, 
                    x="country_name", 
                    y="Count", 
                    color="Medal Type",
                    title="Medals per Country",
                    labels={"country_name": "Country", "Count": "Number of Medals"},
                    height=600,
                    color_discrete_map=custom_colors)  # Apply custom colors
        
        st.plotly_chart(fig)


    def plot_medals_per_athlete(self):
        """
        Plot the number of medals per athlete.
        """
        # Group by 'athlete_full_name' and sum the medals
        medal_counts = (
            self.filtered_data.groupby("athlete_full_name")["medal_type"]
            .value_counts()
            .unstack(fill_value=0)
            .reset_index()
        )

        # Convert to long format for plotting
        medal_counts_long = medal_counts.melt(id_vars="athlete_full_name", 
                                            value_vars=["GOLD", "SILVER", "BRONZE"],
                                            var_name="Medal Type", 
                                            value_name="Count")

        # Define custom colors for each medal type
        custom_colors = {
            "GOLD": "#FFD700",   # Gold color
            "SILVER": "#C0C0C0", # Silver color
            "BRONZE": "#CD7F32"  # Bronze color
        }

        # Plot using Plotly
        fig = px.bar(medal_counts_long, 
                    x="athlete_full_name", 
                    y="Count", 
                    color="Medal Type",
                    title="Medals per Athlete",
                    labels={"athlete_full_name": "Athlete", "Count": "Number of Medals"},
                    height=600,
                    color_discrete_map=custom_colors)  # Apply custom colors

        st.plotly_chart(fig)


    def run(self):
        """
        Run the Streamlit app by rendering the sidebar, and switching between the data view, aggregate view, and plot view.
        """
        self.render_sidebar()

        if self.view == "Filtered Data View":
            self.render_data_view()
        elif self.view == "Aggregated Data View":
            self.render_aggregate_view()
            self.plot_medals_per_country()
            self.plot_medals_per_athlete()


if __name__ == "__main__":
    app = OlympicMedalsApp()
    app.run()
