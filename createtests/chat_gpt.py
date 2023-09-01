import pdb
import random
import time
from copy import copy, deepcopy
import roman
import openai
import time
import re
import concurrent.futures
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

from practicetests.settings import OPENAI_API_KEY
from .messages import preparation_prompt, multi_choice_prompt, multi_selection_prompt, open_answer_prompt

openai.api_key = OPENAI_API_KEY


# Retry function in case we reach open ai rate limits. stop_after_attempt can be increased

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    print("RATE LIMIT")
    return openai.ChatCompletion.create(**kwargs)


total_tokens = 0


def gpt_engine(prompt, n=1, max_tokens=200):
    global total_tokens
    gpt_35_turbo = {"type": "gpt-3.5-turbo", "prompt_cost": 0.0015, "completion_cost": 0.002}
    gpt_35_turbo_16k = {"type": "gpt-3.5-turbo-16k", "prompt_cost": 0.003, "completion_cost": 0.004}
    model = gpt_35_turbo
    response = completion_with_backoff(
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
    # # PROMPT DEBUG LINES
    # print("============================")
    # print(prompt[1])
    # print("****************************")
    # print(response)
    # print("============================")
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
    response = completion_with_backoff(
        model=model['type'],
        n=n,
        max_tokens=max_tokens,
        temperature=0.7,
        messages=[
            {"role": "user", "content": f"I will ask you a question."},
            {"role": "assistant", "content": "Ok"},
            {"role": "user", "content": f" {prompt}"}
        ]
    )
    # print(response)
    total_tokens += response['usage']['total_tokens']
    response_text = [response["choices"][0]["message"]["content"]]

    return response_text


def generate_header(teaching_material):
    return gpt_headers(f"Generate a short title on the following text. Give me only the title without any quotes or "
                       f"additional explanation: \n {teaching_material[:500]}")[0]


def generate_subtitle(header):
    return gpt_headers(f"Generate a subtitle on the following text.  Give me only the subtitle without any quotes or "
                       f"additional explanation:: \n {header}")[0]


def generate_footer_info(header):
    return f"Congratulations on completing the {header} test! " \
           f"We hope you found this practice test to be " \
           f"both challenging and insightful. Remember, " \
           f"every question is an opportunity to learn and grow." \
           f" Your dedication to preparing for this exam will undoubtedly pay off in the long run."


# In Teaching material -> Out questions
def generate_questions(teaching_material, number_of_questions):
    desired_words_per_question = 100
    max_words_per_question = 2000
    sub_cut_words = 100
    a = time.time()
    total_questions_record = number_of_questions["mcq"] + number_of_questions["msq"] + number_of_questions["oaq"]
    number_of_words = len(teaching_material.split())
    WQRatio = number_of_words // total_questions_record

    if WQRatio < desired_words_per_question:
        max_words_per_cut = desired_words_per_question  # number of words used for each text cut
    elif WQRatio > max_words_per_question:
        max_words_per_cut = max_words_per_question
    else:
        max_words_per_cut = WQRatio

    text_cuts = split_into_parts(teaching_material, max_words=max_words_per_cut)

    # TODO maybe ask users if they want to shuffle
    random.shuffle(text_cuts)

    mcq_cut = distribute_text_cuts(number_of_questions["mcq"], len(text_cuts))

    msq_cut = distribute_text_cuts(number_of_questions["msq"], len(text_cuts))

    oaq_cut = distribute_text_cuts(number_of_questions["oaq"], len(text_cuts))

    final_questions_list = []

    def process_mcq(cut):
        if mcq_cut[cut] != 0:
            final_questions_list.extend(gpt_engine(multi_choice_prompt(text_cuts[cut]), mcq_cut[cut]))

    def process_msq(cut):
        if msq_cut[cut] != 0:
            final_questions_list.extend(gpt_engine(multi_selection_prompt(text_cuts[cut]), msq_cut[cut]))

    def process_oaq(cut):
        if oaq_cut[cut] != 0:
            final_questions_list.extend(gpt_engine(open_answer_prompt(text_cuts[cut]), oaq_cut[cut]))

    # Inner thread loop for each question type
    def process_cut(cut):
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            futures = []
            futures.append(executor.submit(process_mcq, cut))
            futures.append(executor.submit(process_msq, cut))
            futures.append(executor.submit(process_oaq, cut))

            for future in concurrent.futures.as_completed(futures):
                pass  # We don't need to do anything here, but this waits for all futures to complete

    # Outer main thread loop for each cut iteration
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as main_executor:
        futures = []
        for cut in range(len(text_cuts)):
            if len(text_cuts[cut].split()) > sub_cut_words:
                text_cuts[cut] = random_portion_of_words(text_cuts[cut], sub_cut_words)
                text_cuts[cut] = text_cuts[cut][:sub_cut_words*10]   # Make sure too long words does not increase tokens size
            else:

                text_cuts[cut] = text_cuts[cut][:max_words_per_cut*10]
            futures.append(main_executor.submit(process_cut, cut))

        for future in concurrent.futures.as_completed(futures):
            pass  # Wait for all cut processing to complete

    json_questions_list = {}
    for final_question in range(len(final_questions_list)):
        lines = final_questions_list[final_question]["question"].splitlines()
        json_questions_list[f"q{final_question + 1}"] = {}
        json_questions_list[f"q{final_question + 1}"]["type"] = final_questions_list[final_question]["type"]
        json_questions_list[f"q{final_question + 1}"] = process_lines(json_questions_list[f"q{final_question + 1}"],
                                                                      lines)

    for key, question in json_questions_list.items():
        # Check if 'correct_answer' or 'answers' is empty
        if not question.get('correct_answer') or not question.get('answers'):
            # Remove the keys 'correct_answer' and 'answers' if they are empty
            question.pop('correct_answer', None)
            question.pop('answers', None)

    b = time.time()
    print(f"TIME: {b - a}")
    print(total_tokens)
    return json_questions_list


def distribute_text_cuts(questions, num_elements):

    if num_elements == 0:
        return []

    # Calculate the equal portion of the input number for each element
    equal_portion = questions // num_elements

    # Distribute the equal portion to each element
    result = [equal_portion] * num_elements

    # Distribute any remaining part of the input number
    remaining = questions % num_elements
    for i in range(remaining):
        result[i] += 1
    random.shuffle(result)

    return result


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


def random_portion_of_words(input_string, num_words):
    words = input_string.split()

    if num_words >= len(words):
        return ' '.join(words)

    start_index = random.randint(0, len(words) - num_words)
    selected_words = words[start_index: start_index + num_words]

    return ' '.join(selected_words)
