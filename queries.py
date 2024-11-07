import pandas as pd
import numpy as np
import json

# Load the datasets
bios_df = pd.read_csv('./cleaned_data/bios.csv')
results_df = pd.read_csv('./cleaned_data/results.csv')

def get_athlete_medals(athlete_name):
    """
    Find all medals won by a specific athlete.
    Args:
        athlete_name (str): Full name of the athlete
    Returns:
        pandas.DataFrame: DataFrame containing year, discipline, event, and medal information
        False: If athlete not found or in case of any error
    Note: Requires global DataFrames 'bios_df' and 'results_df' to be defined
    """
    try:
        # Check if athlete exists in database
        athlete_data = bios_df[bios_df['name'].str.lower() == athlete_name.lower()]
        if athlete_data.empty:
            print(f"Error: Athlete '{athlete_name}' not found in database")
            return False
        athlete_id = athlete_data['athlete_id'].iloc[0]
        
        # Get their medal records
        medals = results_df[
            (results_df['athlete_id'] == athlete_id) & 
            (results_df['medal'].notna())
        ]
        
        if medals.empty:
            print(f"No medals found for athlete '{athlete_name}'")
            return False
            
        return { 
                "name":athlete_name,
                "medals":medals[['year', 'discipline', 'event', 'medal']]
            }
        
    except Exception as e:
        print(f"Error processing data for athlete '{athlete_name}': {str(e)}")
        return False

def get_country_performance(noc, year=None):
    """
    Get medal count for a country, optionally for a specific year.
    
    Args:
        noc (str): National Olympic Committee code
        year (int, optional): Specific Olympic year
        
    Returns:
        pandas.Series: Medal counts by type (Gold/Silver/Bronze)
        False: If country not found or in case of any error
    """
    try:
        # get country noc against country name
        with open('noc_mappings.json', 'r') as json_file:
            country_noc_map = json.load(json_file)
        noc_code = country_noc_map.get(noc, "404")  
        print(f"NOC CODE FOUND is {noc_code} for {noc}")  
        if noc_code == "404":
            print(f"Error: Country '{noc}' not found in database")
            return False
        
        # Verify NOC exists
        if noc_code not in results_df['noc'].unique():
            print(f"Error: Country '{noc}' not found in database")
            return False
            
        query = results_df['noc'] == noc_code
        if year:
            # Verify year exists in data
            if year not in results_df['year'].unique():
                print(f"Error: No data available for year {year}")
                return False
            query &= results_df['year'] == year
            
        medals = results_df[query & results_df['medal'].notna()]
        
        if medals.empty:
            print(f"No medals found for country '{noc}'{' in ' + str(year) if year else ''}")
            return False
            
        return medals['medal'].value_counts()
        
    except Exception as e:
        print(f"Error processing data for country '{noc}': {str(e)}")
        return False

def get_athlete_participations(athlete_name):
    """
    Get all Olympic participations for an athlete.
    Args:
        athlete_name (str): Full name of the athlete
    Returns:
        pandas.DataFrame: DataFrame containing participation details
        False: If athlete not found or in case of any error
    """
    try:
        # Check if athlete exists
        athlete_data = bios_df[bios_df['name'] == athlete_name]
        if athlete_data.empty:
            print(f"Error: Athlete '{athlete_name}' not found in database")
            return False
            
        athlete_id = athlete_data['athlete_id'].iloc[0]
        
        participations = results_df[results_df['athlete_id'] == athlete_id]
        if participations.empty:
            print(f"No participation records found for athlete '{athlete_name}'")
            return False
            
        return participations[['year', 'discipline', 'event', 'place', 'medal']]
        
    except Exception as e:
        print(f"Error processing participations for athlete '{athlete_name}': {str(e)}")
        return False

def find_athletes_by_sport(sport, year=None):
    """
    Find all athletes in a specific sport, optionally for a specific year.
    
    Args:
        sport (str): Sport/discipline name
        year (int, optional): Specific Olympic year
        
    Returns:
        pandas.DataFrame: DataFrame containing athlete names and their NOCs
        False: If sport not found or in case of any error
    """
    try:
        # Verify sport exists in data
        if sport not in results_df['discipline'].unique():
            print(f"Error: Sport '{sport}' not found in database")
            return False
            
        query = results_df['discipline'] == sport
        if year:
            # Verify year exists
            if year not in results_df['year'].unique():
                print(f"Error: No data available for year {year}")
                return False
            query &= results_df['year'] == year
            
        athlete_ids = results_df[query]['athlete_id'].unique()
        
        if len(athlete_ids) == 0:
            print(f"No athletes found for sport '{sport}'{' in ' + str(year) if year else ''}")
            return False
            
        return bios_df[bios_df['athlete_id'].isin(athlete_ids)][['name', 'NOC']]
        
    except Exception as e:
        print(f"Error processing athletes for sport '{sport}': {str(e)}")
        return False

def get_medalists_by_year(year, discipline=None):   #processed
    """
    Get all medalists in a specific year, optionally filtered by sport.
    
    Args:
        year (int): Olympic year
        discipline (str, optional): Sport/discipline name
        
    Returns:
        pandas.DataFrame: DataFrame containing medalist details
        False: If year not found or in case of any error
    """
    try:
        # Verify year exists
        if year not in results_df['year'].unique():
            print(f"Error: No data available for year {year}")
            return False
            
        query = (results_df['year'] == year) & results_df['medal'].notna()
        
        if discipline:
            # Verify discipline exists
            if discipline not in results_df['discipline'].unique():
                print(f"Error: Sport '{discipline}' not found in database")
                return False
            query &= results_df['discipline'] == discipline
            
        medalists = results_df[query]
        
        if medalists.empty:
            print(f"No medalists found for year {year}{' in ' + discipline if discipline else ''}")
            return False
            
        return pd.merge(
            medalists[['discipline', 'event', 'medal', 'athlete_id']], 
            bios_df[['athlete_id', 'name', 'NOC']], 
            on='athlete_id'
        )
        
    except Exception as e:
        print(f"Error processing medalists for year {year}: {str(e)}")
        return False

def get_athlete_bio(athlete_name):
    """
    Get biographical information for an athlete.
    
    Args:
        athlete_name (str): Full name of the athlete
        
    Returns:
        pandas.Series: Athlete's biographical information
        False: If athlete not found or in case of any error
    """
    try:
        athlete_data = bios_df[bios_df['name'] == athlete_name]
        
        if athlete_data.empty:
            print(f"Error: Athlete '{athlete_name}' not found in database")
            return False
            
        return athlete_data.iloc[0]
        
    except Exception as e:
        print(f"Error retrieving bio for athlete '{athlete_name}': {str(e)}")
        return False

def get_athlete_stats(discipline):
    """
    Get average height/weight stats for athletes in a sport.
    Args:
        discipline (str): Sport/discipline name
    Returns:
        dict: Dictionary containing average height, weight, and athlete count
        False: If sport not found or in case of any error
    """
    try:
        # Verify sport exists
        if discipline not in results_df['discipline'].unique():
            print(f"Error: Sport '{discipline}' not found in database")
            return False
            
        athlete_ids = results_df[results_df['discipline'] == discipline]['athlete_id'].unique()
        athletes = bios_df[bios_df['athlete_id'].isin(athlete_ids)]
        
        if athletes.empty:
            print(f"No athletes found for sport '{discipline}'")
            return False
            
        # Handle potential NaN values in height/weight
        avg_height = athletes['height_cm'].mean()
        avg_weight = athletes['weight_kg'].mean()
        
        if pd.isna(avg_height) and pd.isna(avg_weight):
            print(f"No height/weight data available for athletes in '{discipline}'")
            return False
            
        return {
            'avg_height': avg_height if not pd.isna(avg_height) else None,
            'avg_weight': avg_weight if not pd.isna(avg_weight) else None,
            'count': len(athletes)
        }
        
    except Exception as e:
        print(f"Error processing stats for sport '{discipline}': {str(e)}")
        return False
    
    


def interpret_question(question: str):
    """Match user question to appropriate query"""
    
    # Dynamic Queries
    avg_in_question = any(word in question for word in ["average", "avg", "mean", "averages"]) 
    medals_in_question = any(word in question for word in ["medals", "medal", "awards", "award","trophies","trophy"])   
    athlete_bio_in_question = any(word in question for word in ["bio","information about","personal information", "personal info","bio data","biodata"])
    sport_in_question = any(word.lower() in question.lower() for word in results_df["discipline"].unique())
    country_in_question = any(word.lower() in question.lower() for word in bios_df["NOC"])
    # Look for key phrases and words
    if avg_in_question:
        for sport in results_df['discipline'].unique():
            if sport.lower() in question.lower():
                return get_athlete_stats(sport)
        return get_athlete_stats("Tennis")
    
    if country_in_question and medals_in_question:
        for country in bios_df['NOC']:
            if country.lower() in question.lower():
                return get_country_performance(country)
            
    if medals_in_question:
        if any(year in question for year in map(str, range(1900, 2024))):
            # Looking for medals in a specific year
            year = int(''.join(filter(str.isdigit, question)))
            if any(sport.lower() in question.lower() for sport in results_df["discipline"].unique()):
                sport = next(s for s in results_df["discipline"].unique() if s.lower() in question.lower())
                return get_medalists_by_year(year, sport)
            return get_medalists_by_year(year)
            
        if any(name.lower() in question.lower() for name in bios_df['name']):
            # this lines is required to get the actual name in varibale 
            # to pass it to function
            name = next(name for name in bios_df['name'] if name in question)
            return get_athlete_medals(name)
            # query: Give medals won by Jean Borotra
    
    if athlete_bio_in_question:
        for name in bios_df['name']:
            if name.lower() in question.lower():
                return get_athlete_bio(name)
    
    if sport_in_question:
        for sport in results_df['discipline'].unique():
            if sport.lower() in question.lower():
                if any(year in question for year in map(str, range(1900, 2024))):
                    year = int(''.join(filter(str.isdigit, question)))
                    return find_athletes_by_sport(sport, year)
                return find_athletes_by_sport(sport)

            
            
    # Default response if no match found
    return "I'm not sure what information you're looking for. Could you rephrase your question?"

# Example usage:

def main():
    print(" ----- MAIN STARTED ----- ")
    # These questions should return appropriate results:
    # print(interpret_question("Show me medals won by Jean Borotra"))
    # print(interpret_question("Tell me about Henri Cochet"))
    # avg_data = interpret_question("Tell me average stats of all players in Golf?")
    # print(f"{avg_data["count"]} players participated in golf with average height = {avg_data["avg_height"]} and average weight = {avg_data["avg_weight"]}")
    # medals_count=interpret_question("How many medals won by France?")
    # print(f"Silver medals = {medals_count.get('Silver',0)}\nGold medals = {medals_count.get('Gold',0)}\nBronze medals = {medals_count.get("Bronze",0)}")
    # athlete=interpret_question("Show bio data of Jean Borotra.")
    # print(f"Athlete ID: {athlete['athlete_id']}")
    # print(f"Name: {athlete['name']}")
    # print(f"Date of Birth: {athlete['born_date']} (Born in {athlete['born_city']}, {athlete['born_region']}, {athlete['born_country']})")
    # print(f"Height: {athlete['height_cm']} cm")
    # print(f"Weight: {athlete['weight_kg']} kg")
    # print(f"Date of Death: {athlete['died_date']}")
    print(" ----- MAIN ENDED ----- ")
main()       