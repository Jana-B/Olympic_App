import pandas as pd
import numpy as np

# Import Daten 2024 
olympic_medals_2024 = pd.read_csv("data/olympic_games_results_2024/medallists.csv")
olympic_medals_2024['team'] = olympic_medals_2024['team'].fillna('no_team')
olympic_medals_2024['team_gender'] = olympic_medals_2024['team_gender'].fillna('no_team_gender')
olympic_medals_2024['nationality'] = olympic_medals_2024['nationality'].fillna('no_nationality')
olympic_medals_2024 = olympic_medals_2024.dropna()

olympic_medals_2024_bak = olympic_medals_2024.copy()

# Import Data 1896-2022
olympic_medals = pd.read_csv("data/olympic_games_results_1896_2022/olympic_medals.csv")





# Create columns location and year
def split_location_year(slug_game):
    # Split by the last hyphen
    parts = slug_game.rsplit('-', 1)
    # Check if the second part is numeric
    if len(parts) == 2 and parts[1].isdigit():
        return parts[0], parts[1]
    else:
        return slug_game, None

# Apply the function to the 'slug_game' column
location_year = olympic_medals['slug_game'].apply(lambda x: pd.Series(split_location_year(x)))
olympic_medals[['location', 'year']] = location_year

# Reorder columns to make 'year' and 'location' the first two columns
columns_order = ['year', 'location'] + [col for col in olympic_medals.columns if col not in ['year', 'location']]
olympic_medals = olympic_medals[columns_order]

# Create one Dataframe
# Create a new DataFrame from olympic_medals_2024 with the required mappings and defaults
olympic_medals_2024_mapped = olympic_medals_2024_bak.copy()

# Mapping columns
olympic_medals_2024_mapped['year'] = 2024
olympic_medals_2024_mapped['location'] = 'paris'
olympic_medals_2024_mapped['slug_game'] = 'paris-2024'

# Mapping discipline and event titles
olympic_medals_2024_mapped['discipline_title'] = olympic_medals_2024_mapped['discipline']
olympic_medals_2024_mapped['event_title'] = olympic_medals_2024_mapped['event']

# Mapping event gender
def map_gender(gender):
    if pd.isna(gender):
        return 'Mixed'
    if gender.lower() == 'male':
        return 'Male'
    elif gender.lower() == 'female':
        return 'Female'
    return 'Mixed'

olympic_medals_2024_mapped['event_gender'] = olympic_medals_2024_mapped['gender'].apply(map_gender)

# Mapping medal type
def map_medal_type(medal_type):
    if 'Gold' in medal_type:
        return 'GOLD'
    elif 'Silver' in medal_type:
        return 'SILVER'
    elif 'Bronze' in medal_type:
        return 'BRONZE'
    return 'UNKNOWN'

olympic_medals_2024_mapped['medal_type'] = olympic_medals_2024_mapped['medal_type'].apply(map_medal_type)

# Determine participant type
olympic_medals_2024_mapped['participant_type'] = olympic_medals_2024_mapped['event_type'].apply(lambda x: 'Athlete' if x == 'ATH' else 'GameTeam')

# Mapping participant title, athlete URL, and full name
olympic_medals_2024_mapped['participant_title'] = olympic_medals_2024_mapped['name']
base_url = 'https://olympics.com'
olympic_medals_2024_mapped['athlete_url'] = base_url + olympic_medals_2024_mapped['url_event']
olympic_medals_2024_mapped['athlete_full_name'] = olympic_medals_2024_mapped['name']

# Mapping country fields
olympic_medals_2024_mapped['country_name'] = olympic_medals_2024_mapped['country'].replace('United States', 'United States of America')
olympic_medals_2024_mapped['country_code'] = olympic_medals_2024_mapped['country_code']
olympic_medals_2024_mapped['country_3_letter_code'] = olympic_medals_2024_mapped['code']  # Assuming 'code' is a 3-letter code

# Select only the columns that exist in the olympic_medals DataFrame
olympic_medals_2024_mapped = olympic_medals_2024_mapped[[
    'year', 'location', 'discipline_title', 'slug_game', 'event_title',
    'event_gender', 'medal_type', 'participant_type', 'participant_title',
    'athlete_url', 'athlete_full_name', 'country_name', 'country_code',
    'country_3_letter_code'
]]

# Append the mapped 2024 data to the existing olympic_medals DataFrame
olympic_medals_combined = pd.concat([olympic_medals, olympic_medals_2024_mapped], ignore_index=True)


# Convert year to numeric and sort
# Convert the 'year' column to numeric, forcing errors to NaN if any non-convertible values exist
olympic_medals_combined['year'] = pd.to_numeric(olympic_medals_combined['year'], errors='coerce')

# If you want to drop rows where 'year' could not be converted
olympic_medals_combined.dropna(subset=['year'], inplace=True)

# Now sort the DataFrame by the 'year' column
olympic_medals_combined_sorted = olympic_medals_combined.sort_values(by='year',ascending=False)

# Medal mapping
# Define the mapping of medal types to codes
medal_mapping = {
    'GOLD': 1,
    'SILVER': 2,
    'BRONZE': 3
}

# Create a new column 'medal_code' using the mapping
olympic_medals_combined['medal_code'] = olympic_medals_combined['medal_type'].map(medal_mapping)

# Export
olympic_medals_combined.to_excel('data/olympic_medals.xlsx')