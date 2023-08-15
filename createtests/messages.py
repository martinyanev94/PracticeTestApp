preparation_prompt = f"I want to create a sample question from a teaching text. " \
                     f"Below I will ask you to create a sample question. I will specify the question type," \
                     f" question format and teaching material. \n" \
                     f"When building the question select a random word, sentence or idea from the text and focus the " \
                     f"question on that. "


def multi_choice_prompt(teaching_material):
    multiple_choice_prompt = f"""
       Question type: multiple choice
       
       Format: Type a star(*) before every question and a (~) before every possible answer. Number the possible answers. 
       Write the correct answer below with (&) symbol in front. The explanation should have (|) in front.
       This is how the question should look like (The explanation should be one sentence long): 
       "
       *Which of the following AWS services can be used to store and manage objects such as photos, videos, and documents?
       
       ~1 Amazon EC2
       ~2 Amazon RDS
       ~3 Amazon S3
       ~4 Amazon CloudFront
       
       &3
       
       |Amazon S3 (Simple Storage Service) is an object storage service that offers industry-leading scalability, data availability, security, and performance.
       "
       Do you understand?
       
       Teaching material:\n {teaching_material}
       
       """
    return ["msq", multiple_choice_prompt]


def multi_selection_prompt(teaching_material):
    multiple_selection_prompt = f"""
       Question type: multiple selection

       Format: Type a star(*) before every question and a (~) before every possible answer. Number the possible answers. 
       There should be more than one correct answers. 
       Write the correct answers on a single line separated by (,) with (&) symbol in front. The explanation should have (|) in front.
       This is how the question should look like (The explanation should be one sentence long): 
        "
       *Which of the following are characteristics of a mammal? Select all that apply.

       ~1 Lays eggs
       ~2 Has feathers
       ~3 Warm-blooded
       ~4 Breathes through gills
       ~5 Gives live birth

       &3,5
        "
       |Mammals are warm-blooded and give birth to live young, which are usually nourished with milk produced by the mother.

       Teaching material:\n {teaching_material}

       """
    return ["mcq", multiple_selection_prompt]


def open_answer_prompt(teaching_material):
    open_answer_prompt = f"""
       Question type: open answer

       Format: Type a star(*) before every question.Write the answer below the question. The answer should have (|) in front.
       This is how the question should look like (The explanation should be one sentence long): 

       *What are some common symptoms of the flu?

       |Common symptoms of the flu include fever, cough, sore throat, body aches, fatigue, and sometimes vomiting and diarrhea.

       Teaching material:\n {teaching_material}

       """
    return ["oaq", open_answer_prompt]


print(open_answer_prompt)
