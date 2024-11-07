# Olympics Chatbot

### A Rule-based chatbot that can handle queries related to Olympics dataset.

---


> Get started
- clone the repo `git clone https://github.com/awais-124/Olympics-GPT.git`
- you need python editor for this
- install requried libs
- Enjoy. Have a good day!

---

> A Rule-Based Chatbot, explantion of code
- Separate files for different tasks.
- `learning_data.json` stores user query and bot response as key-value pair
- `noc_mappings.json` is a file to convert NOC to country names
- `chabotConstant.py` stores all constant needed for chatbot
- `dataExtractorMethods.py` has all query functions that interprets user query and extract data accordingly from dataset.
- `actuators.py` is a file that gets output from dataExtractorMethods and format them to diplay in paragrapgh form
- `fileHandling.py` has helper functions for file handling
- `chatbot.py` is main file from where code runs
- Two folders for dataset cleaned and uncleaned
- `dataset_cleaning.ipynb` notebook for data cleaning code

---

> Code Flow
```python
def main():
    start_conversation()

    """ Set necessary Variables """
    
    """ start loop """:
        # reset variables

        """ Get input from user """
        """ Perform pre-processing on it """
        
        """ If user wants to end: END """
        """ IF query in `learning.json` get response from there """
        """ IF user is greeting greet """
        """ IF user is asking for olympics fact, show """
        """ IF user is asking about self: show intro """
        """ IF user is asking about dataset, use functions to generate response """
        """ PRINT response """
        """ IF response not in file, add it to leanring.json """   



""" CALL TO MAIN FUNCTION """
```