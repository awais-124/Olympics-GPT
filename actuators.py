from dataExtractorMethods import * 
from chatbotConstants import *

def show_athlete_stats(discipline):
    avg_data = get_athlete_stats(discipline)
    if  type(avg_data) == bool:
        return "_"*50
    output = f"{avg_data["count"]} players participated with average height = {avg_data["avg_height"]} and average weight = {avg_data["avg_weight"]}"
    return output

def show_athlete_medals(athlete_name):
    all_medals = get_athlete_medals(athlete_name)
    if type(all_medals) == bool:
        return "_"*50
    output=f"Following medals are won by {all_medals["name"]}: \n"
    for index, medal in all_medals["medals"].iterrows():
        output+=f"{medal['medal']} medal in {medal['discipline']} in the year {int(medal['year'])} at {medal["event"]}."
    return output

def show_country_performance(noc, year=None):
    medals_count=get_country_performance(noc, year)
    if  type(medals_count) == bool:
        return "_"*50
    output = f"Silver medals = {medals_count.get('Silver',0)}\nGold medals = {medals_count.get('Gold',0)}\nBronze medals = {medals_count.get("Bronze",0)}"
    return output

def show_athlete_participations(athlete_name):
    parts=get_athlete_participations(athlete_name)
    if type(parts) == bool:
        return "_"*50
    output=""
    for _, row in parts["part_of"].iterrows():
        output += f"In {int(row['year'])}, {parts["name"]} competed in the {row['discipline']} {row['event']} event, finishing in {int(row['place'])}th place and winning a {row['medal']} medal.\n"
    return output

def show_athletes_by_sport(sport, year=None):
    athletes_by_sport=find_athletes_by_sport(sport, year)
    if type(athletes_by_sport) == bool
        return "_"*50
    counter=1
    output=""
    for index, athletes in athletes_by_sport.iterrows():
        output+=f"{counter}: Athlete id={index} -> {athletes["name"]}  participated from {athletes["NOC"]}.\n"
        counter+=1
    return output

def show_medalists_by_year(year, discipline=None): 
    medalists = get_medalists_by_year(year, discipline)
    if  type(medalist) == bool:
        return "_"*50
    output=""
    for index, medalist in medalists.iterrows():
        output+=f"{index}. {medalist['name']} from {medalist['NOC']} won a {medalist['medal']} medal in {medalist['event']} ({medalist['discipline']}).\n"
    return output

def show_athlete_bio(athlete_name):
    athlete=get_athlete_bio(athlete_name)
    if type(athlete) == bool:
        return "_"*50
    output=f"Athlete ID: {athlete['athlete_id']}"
    output+=f"\nName: {athlete['name']}"
    output+=f"\nDate of Birth: {athlete['born_date']} (Born in {athlete['born_city']}, {athlete['born_region']}, {athlete['born_country']})"
    output+=f"\nHeight: {athlete['height_cm']} cm"
    output+=f"\nWeight: {athlete['weight_kg']} kg"
    output+=f"\nDate of Death: {athlete['died_date']}"
    return output
    

def interpret_question(question: str):
    """Match user question to appropriate dynamic queries"""
    avg_in_question = any(word in question.lower() for word in ["average", "avg", "mean", "averages"]) 
    medals_in_question = any(word in question.lower() for word in ["medals", "medal", "awards", "award","trophies","trophy"])   
    athlete_bio_in_question = any(word in question.lower() for word in ["bio","information about","personal information", "personal info","bio data","biodata"])
    sport_in_question = any(word.lower() in question.lower() for word in results_df["discipline"].unique())
    country_in_question = any(word.lower() in question.lower() for word in bios_df["NOC"])
    participation_in_question=any(word in question.lower() for word in ["participated","took part in","participate","was part of","participations","included","played in"])
    

    if avg_in_question:
        for sport in results_df['discipline'].unique():
            if sport.lower() in question.lower():
                return show_athlete_stats(sport)
        return show_athlete_stats("Tennis")
    
    if country_in_question and medals_in_question:
        for country in bios_df['NOC']:
            if country.lower() in question.lower():
                return show_country_performance(country)
            
    if medals_in_question:
        if any(year in question for year in map(str, range(1900, 2024))):
            year = int(''.join(filter(str.isdigit, question)))
            if any(sport.lower() in question.lower() for sport in results_df["discipline"].unique()):
                sport = next(s for s in results_df["discipline"].unique() if s.lower() in question.lower())
                return show_medalists_by_year(year, sport)
            return show_medalists_by_year(year)
            
        if any(name.lower() in question.lower() for name in bios_df['name']):
            name = next(name for name in bios_df['name'] if name in question)
            return show_athlete_medals(name)
    
    if athlete_bio_in_question:
        for name in bios_df['name']:
            if name.lower() in question.lower():
                return show_athlete_bio(name)
    
    if sport_in_question:
        for sport in results_df['discipline'].unique():
            if sport.lower() in question.lower():
                if any(year in question for year in map(str, range(1900, 2024))):
                    year = int(''.join(filter(str.isdigit, question)))
                    return show_athletes_by_sport(sport, year)
                return show_athletes_by_sport(sport)
            
    if participation_in_question:
        for name in bios_df['name']:
            if name.lower() in question.lower():
                return show_athlete_participations(name)
            
    return default_response
