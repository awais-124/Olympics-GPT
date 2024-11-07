import random
import string

from actuators import interpret_question
from chatbotConstants import *
from fileHandling import *

def remove_punctuation(user_string):
    translator = str.maketrans('', '', string.punctuation)
    return user_string.translate(translator)

def show_sample_questions():
    print("-" * 50)
    output="You can ask similar questions like these: \n"
    for i in range(0,5):
        output+=f"{i+1}. {random.sample(sample_questions,1)}\n"
    return output+'\n'+("-" * 50)

def end_conversation():
    print("-" * 50)
    print("Olympics-GPT: ", random.choice(farewell_messages))
    print("-" * 50)
    
def start_conversation():
    print("-" * 50)
    print("OlympicGPT Here: " + random.choice(greetings))
    print("You can ask questions about Olympic history, athletes, \nand medals, countries participated, average stats etc.")
    print("Type 'quit', 'exit', or 'goodbye' to end the conversation.")
    print("-" * 50)   

def main():
    start_conversation()
    
    end_chat=False
    chatbot_response=""
    is_about_olympics = True
    already_in_file=False
    has_response_generated=False
    
    while not end_chat:
        # reset variables
        is_about_olympics = True
        already_in_file=False
        has_response_generated=False
        chatbot_response=""
        
        print('-'*60)
        user_query=(input("\nYou: "))
        user_query=remove_punctuation(user_query)
        
        if user_query in exit_words:
            end_conversation()
            end_chat=True
            return
        
        if user_query in get_file_data('./learning_data.json'):
            chatbot_response=get_file_data('./learning_data.json')[user_query]
            if chatbot_response == -1: return
            already_in_file=True
            has_response_generated=True    

        ### Checks conditions used below
        greeting=any(word.lower() in user_query.lower() for word in greeting_keywords)
        fact=any(word.lower() in user_query.lower() for word in fun_fact_keywords)
        ask_self=any(word.lower() in user_query.lower() for word in self_keywords)
        sample_quest=any(word.lower() in user_query.lower() for word in sample_keywords)
        
        if greeting and not has_response_generated:
            chatbot_response=random.choice(greeting_responses)
            is_about_olympics=False
            has_response_generated=True
            already_in_file=True
            
        if fact and not has_response_generated:
            chatbot_response=random.choice(fun_facts)
            is_about_olympics=False
            has_response_generated=True
            
        if ask_self and not has_response_generated:
            chatbot_response=chatbot_intro
            already_in_file=True
            is_about_olympics=False
            has_response_generated=True
        
        if sample_quest and not has_response_generated:
            chatbot_response=show_sample_questions()   
            is_about_olympics=False
            has_response_generated=True 
            already_in_file=True                           
            
        if is_about_olympics and not has_response_generated:
            chatbot_response=interpret_question(user_query)
            has_response_generated=True
                
        print(f"Olympics-GPT: {chatbot_response}")
        
        if not already_in_file and chatbot_response != default_response:
            add_key_value_to_file('./learning_data.json',user_query,chatbot_response)
            

if __name__ == '__main__':
    main()