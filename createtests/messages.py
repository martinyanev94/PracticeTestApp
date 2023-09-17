languages = {
    'English': "English",
    "Bulgarian": "Bulgarian",
    "Spanish": "Spanish",
    "French": "French",
    "German": "German",
    "Italian": "Italian",
    "Portuguese": "Portuguese",
    "Dutch": "Dutch",
    "Russian": "Russian",
    "Arabic": "Arabic",
    "Chinese": "Chinese",
    "Japanese": "Japanese",
    "Korean": "Korean",
    "Turkish": "Turkish",
    "Hindi": "Hindi",
    "Urdu": "Urdu",
    "Swahili": "Swahili",
    "Greek": "Greek",
    "Hebrew": "Hebrew",
    "Polish": "Polish",
    "Swedish": "Swedish"
}


preparation_prompt = f"I want to create a question from a content. " \
                     f"Below I will ask you to create a question. I will specify the question type," \
                     f" question format, template and content. \n" \
                     f"Make sure the question is well explained and structured. "


def multi_choice_prompt(teaching_material):
    multiple_choice_prompt = f"""
       Question type: multiple choice
       
       Format: Type a star(*) before every question and a (~) before every possible answer. Number the possible answers. 
       Write the correct answer below with (&) symbol in front. The explanation should have (|) in front.
       This is the question template (The explanation should be one sentence long): 
       
       "
       *Question Here
       
       ~1 Answer
       ~2 Answer
       ~3 Answer
       ~4 Answer
       
       &Number of the correct answer here
       
       |Explanation here
       "
       
       Content:\n {teaching_material}
       
       
       
       Please inside the question do not include the word "Content".
       
       """
    return ["msq", multiple_choice_prompt]


def multi_selection_prompt(teaching_material):
    multiple_selection_prompt = f"""
       Question type: multiple selection

       Format: Type a star(*) before every question and a (~) before every possible answer. Number the possible answers. 
       There should be more than one correct answers. 
       Write the correct answers on a single line separated by (,) with (&) symbol in front. The explanation should have (|) in front.
       This is the question template (The explanation should be one sentence long): 
       
        "
        
       *Question Here
       
       ~1 Answer
       ~2 Answer
       ~3 Answer
       ~4 Answer
       ~5 Answer
       
       &3,5 
       
       |Explanation here
       "

       Content:\n {teaching_material}

       """
    return ["mcq", multiple_selection_prompt]


def open_answer_prompt(teaching_material):
    open_answer_prompt = f"""
       Question type: open answer

       Format: Type a star(*) before every question.Write the answer below the question. The answer should have (|) in front.
       This is how the question should look like (The explanation should be one sentence long): 

       *What is the capital of France?

       |Paris

       Content:\n {teaching_material}

       """
    return ["oaq", open_answer_prompt]


print(open_answer_prompt)
