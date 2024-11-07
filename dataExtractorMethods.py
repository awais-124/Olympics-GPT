import pandas as pd
import json


bios_df = pd.read_csv('./cleaned_data/bios.csv')
results_df = pd.read_csv('./cleaned_data/results.csv')

def get_athlete_medals(athlete_name):
    try:
        athlete_data = bios_df[bios_df['name'].str.lower() == athlete_name.lower()]
        if athlete_data.empty:
            print(f"Error: Athlete '{athlete_name}' not found in database")
            return False
        athlete_id = athlete_data['athlete_id'].iloc[0]
        
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
    try:
        with open('noc_mappings.json', 'r') as json_file:
            country_noc_map = json.load(json_file)
        noc_code = country_noc_map.get(noc, "404")  
        print(f"NOC CODE FOUND is {noc_code} for {noc}")  
        if noc_code == "404":
            print(f"Error: Country '{noc}' not found in database")
            return False
        
        if noc_code not in results_df['noc'].unique():
            print(f"Error: Country '{noc}' not found in database")
            return False
            
        query = results_df['noc'] == noc_code
        if year:
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
    try:
        athlete_data = bios_df[bios_df['name'] == athlete_name]
        if athlete_data.empty:
            print(f"Error: Athlete '{athlete_name}' not found in database")
            return False
            
        athlete_id = athlete_data['athlete_id'].iloc[0]
        
        participations = results_df[results_df['athlete_id'] == athlete_id]
        if participations.empty:
            print(f"No participation records found for athlete '{athlete_name}'")
            return False
            
        return  { 
                "name":athlete_name,
                "part_of":participations[['year', 'discipline', 'event', 'place', 'medal']]
                }
        
    except Exception as e:
        print(f"Error processing participations for athlete '{athlete_name}': {str(e)}")
        return False

def find_athletes_by_sport(sport, year=None):
    try:
        if sport not in results_df['discipline'].unique():
            print(f"Error: Sport '{sport}' not found in database")
            return False
            
        query = results_df['discipline'] == sport
        if year:
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

def get_medalists_by_year(year, discipline=None):   
    try:
        if year not in results_df['year'].unique():
            print(f"Error: No data available for year {year}")
            return False
            
        query = (results_df['year'] == year) & results_df['medal'].notna()
        
        if discipline:
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
    try:
        if discipline not in results_df['discipline'].unique():
            print(f"Error: Sport '{discipline}' not found in database")
            return False
            
        athlete_ids = results_df[results_df['discipline'] == discipline]['athlete_id'].unique()
        athletes = bios_df[bios_df['athlete_id'].isin(athlete_ids)]
        
        if athletes.empty:
            print(f"No athletes found for sport '{discipline}'")
            return False
            
        # Handle potential NaN values in height/weight
        avg_height = round(athletes['height_cm'].mean(), 2)
        avg_weight = round(athletes['weight_kg'].mean(), 2)
        
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