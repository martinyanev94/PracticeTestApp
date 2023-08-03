import pdb
import time
from copy import copy, deepcopy
import roman
import openai
import time
import re
from .messages import preparation_prompt, multi_choice_prompt, multi_selection_prompt, open_answer_prompt

openai.api_key = "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"

total_tokens = 0
def gpt_engine(prompt, n=1, max_tokens=200):
    global total_tokens
    gpt_35_turbo = {"type": "gpt-3.5-turbo", "prompt_cost": 0.0015, "completion_cost": 0.002}
    gpt_35_turbo_16k = {"type": "gpt-3.5-turbo-16k", "prompt_cost": 0.003, "completion_cost": 0.004}
    model = gpt_35_turbo
    response = openai.ChatCompletion.create(
        model=model['type'],
        n=n,
        max_tokens=max_tokens,
        temperature=0.7,
        messages=[
            {"role": "user", "content": f"{preparation_prompt}"},
            {"role": "assistant", "content": "Ok"},
            {"role": "user", "content": f" {prompt[1]}"}
        ]
    )
    print(response)
    total_tokens += response['usage']['total_tokens']
    response_text = []
    if n == 1:
        response_text.append({"type": prompt[0], "question": response["choices"][0]["message"]["content"]})

    else:
        for choice in response["choices"]:
            response_text.append({"type": prompt[0], "question": choice["message"]["content"]})

    response_cost = response['usage']['prompt_tokens'] / 1000 * model['prompt_cost'] + \
                    response['usage']['completion_tokens'] / 1000 * model['completion_cost']
    return response_text

def gpt_headers(prompt, n=1, max_tokens=200):
    global total_tokens
    gpt_35_turbo = {"type": "gpt-3.5-turbo", "prompt_cost": 0.0015, "completion_cost": 0.002}
    gpt_35_turbo_16k = {"type": "gpt-3.5-turbo-16k", "prompt_cost": 0.003, "completion_cost": 0.004}
    model = gpt_35_turbo
    response = openai.ChatCompletion.create(
        model=model['type'],
        n=n,
        max_tokens=max_tokens,
        temperature=0.7,
        messages=[
            {"role": "user", "content": f"{preparation_prompt}"},
            {"role": "assistant", "content": "Ok"},
            {"role": "user", "content": f" {prompt}"}
        ]
    )
    print(response)
    total_tokens += response['usage']['total_tokens']
    response_text = [response["choices"][0]["message"]["content"]]

    return response_text



def generate_header(teaching_material):
    return gpt_headers(f"I am a building a practice test. "
                      f"Based on the text below create a header "
                      f"for this practice test. Write the header only without any additional words: \n {teaching_material[:500]}")[0]


def generate_subtitle(header):
    return gpt_headers(f"Based on the following practice test title, create a subtitle. Write the subtitle only "
                       f"without any additional words: \n {header}")[0]



def generate_footer_info(header):
    return f"Congratulations on completing the {header} test! " \
           f"We hope you found this practice test to be " \
           f"both challenging and insightful. Remember, " \
           f"every question is an opportunity to learn and grow." \
           f" Your dedication to preparing for this exam will undoubtedly pay off in the long run."


# In Teaching material -> Out questions
def generate_questions(teaching_material, number_of_questions):
    a = time.time()
    max_words_per_cut = 2000  # number of words used for each text cut

    text_cuts = split_into_parts(teaching_material, max_words=max_words_per_cut)

    mcq_record = deepcopy(number_of_questions["mcq"])
    mcq_cut = distribute_text_cuts(number_of_questions["mcq"], len(text_cuts))

    msq_record = deepcopy(number_of_questions["msq"])
    msq_cut = distribute_text_cuts(number_of_questions["msq"], len(text_cuts))

    oaq_record = deepcopy(number_of_questions["oaq"])
    oaq_cut = distribute_text_cuts(number_of_questions["oaq"], len(text_cuts))

    final_questions_list = []

    for cut in text_cuts:
        if mcq_record >= mcq_cut and mcq_cut != 0:
            final_questions_list.extend(gpt_engine(multi_choice_prompt(cut), mcq_cut))
            mcq_record = mcq_record - mcq_cut
        elif mcq_record < mcq_cut and mcq_record != 0:
            final_questions_list.extend(gpt_engine(multi_choice_prompt(cut), mcq_record))
            mcq_record = 0

        if msq_record >= msq_cut and msq_cut != 0:
            final_questions_list.extend(gpt_engine(multi_selection_prompt(cut), msq_cut))
            msq_record = msq_record - msq_cut
        elif msq_record < msq_cut and msq_record != 0:
            final_questions_list.extend(gpt_engine(multi_selection_prompt(cut), msq_record))
            msq_record = 0

        if oaq_record >= oaq_cut and oaq_cut != 0:
            final_questions_list.extend(gpt_engine(open_answer_prompt(cut), oaq_cut))
            oaq_record = oaq_record - oaq_cut
        elif oaq_record < oaq_cut and oaq_record != 0:
            final_questions_list.extend(gpt_engine(open_answer_prompt(cut), oaq_record))
            oaq_record = 0
    json_questions_list = {}
    for final_question in range(len(final_questions_list)):
        lines = final_questions_list[final_question]["question"].splitlines()
        json_questions_list[f"q{final_question + 1}"] = {}
        json_questions_list[f"q{final_question + 1}"]["type"] = final_questions_list[final_question]["type"]
        json_questions_list[f"q{final_question + 1}"] = process_lines(json_questions_list[f"q{final_question + 1}"],
                                                                      lines)

    b = time.time()
    print(f"TIME: {b-a}")
    print(total_tokens)
    return json_questions_list


def distribute_text_cuts(questions, cuts):
    # Calculate the number of apples to be placed in each bucket
    if questions % cuts > 0:
        return questions // cuts + 1
    else:
        return questions // cuts


#TODO Gives list of text_cut strings. Add check where if the word is longer than 15 characters we count it as more than one word for every 15 characters
def split_into_parts(paragraph, max_words=400):
    # Split the paragraph into sentences using a regular expression
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph)

    # Initialize variables to keep track of the current word count and the accumulated sentences
    current_word_count = 0
    accumulated_sentences = []
    sentences_list = []

    for sentence in sentences:
        # Count the words in the current sentence
        words_in_sentence = len(re.findall(r'\b\w+\b', sentence))

        # If adding the current sentence would exceed the word limit, print the accumulated sentences
        if current_word_count + words_in_sentence > max_words:
            current_cut = " ".join(accumulated_sentences)
            sentences_list.append(current_cut)

            # Reset the variables for the next part
            current_word_count = 0
            accumulated_sentences = []

        # Accumulate the current sentence
        accumulated_sentences.append(sentence)
        current_word_count += words_in_sentence

    # Print any remaining sentences that haven't reached the word limit
    if accumulated_sentences:
        current_cut = " ".join(accumulated_sentences)
        sentences_list.append(current_cut)
    return sentences_list


exception_chars = []
for i in range(37):
    exception_chars.append(str(i))
    exception_chars.append(roman.toRoman(i))

def process_lines(json_question, lines):
    # Iterate over the lines in the input file
    for line in lines:
        s = copy(line)
        line = line.strip()
        if "*" in line[:5] or line.startswith(tuple(exception_chars)):
            json_question['question'] = line[line.find('*') + 1:]
            for other_lines in lines[lines.index(s) + 1:]:
                other_lines = other_lines.strip()
                if other_lines.startswith("~") or other_lines.startswith("|"):
                    break
                json_question['question'] = json_question['question'] + "\n" + other_lines
            json_question['answers'] = []
            json_question['correct_answer'] = []
            json_question['explanation'] = ''
        elif line.startswith('~'):
            # This line is an answer option
            option = line[3:]
            json_question['answers'].append(option)
        elif line.startswith('&'):
            # This line is the correct answer
            json_question['correct_answer'] = [int(char) for char in line if char.isdigit()]
        elif line.startswith('|'):
            # This line is the explanation
            json_question['explanation'] = line[1:]

    return json_question