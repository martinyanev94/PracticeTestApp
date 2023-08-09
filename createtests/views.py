import json
import pdb

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from mytests.views import my_tests
from .chat_gpt import gpt_engine, generate_header, generate_subtitle, \
    generate_footer_info, generate_questions
from .models import UserTest


# Create your views here.

@login_required(login_url='/authentication/login')
def choose_create_speed(request):
    return render(request, 'createtests/choose-create-speed.html')

@login_required(login_url='/authentication/login')
def quick_test(request):
    context = {
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'createtests/quick-test.html')

    if request.method == 'POST':
        teaching_material = request.POST['teaching_material']

        header = generate_header(teaching_material)

        if not header or header.isspace():
            messages.error(request, 'Header is required')
            return render(request, 'createtests/quick-test.html', context)
        if not teaching_material or teaching_material.isspace():
            messages.error(request, 'Please provide teaching material')
            return render(request, 'createtests/quick-test.html', context)
        if len(teaching_material) < 100:
            messages.error(request, "Please provide teaching material longer than 100 characters.")
            return render(request, 'createtests/quick-test.html', context)

        subtitle = generate_subtitle(header)
        institution = " "
        tag = request.POST['tag']

        add_header_info = " "

        grades = [
                {
                    "percentage": 49,
                    "grade": "F"
                },
                {
                    "percentage": 65,
                    "grade": "C"
                },
                {
                    "percentage": 75,
                    "grade": "B"
                },
                {
                    "percentage": 100,
                    "grade": "A"
                }
            ]


        # Questions Data
        mcq = request.POST['mcq']
        if mcq != "":
            mcq = int(mcq)
        else:
            mcq = 0

        msq = request.POST['msq']
        if msq != "":
            msq = int(msq)
        else:
            msq = 0

        oaq = request.POST['oaq']
        if oaq != "":
            oaq = int(oaq)
        else:
            oaq = 0
        question_types = {"mcq": mcq, "msq": msq, "oaq": oaq}

        total_questions = msq + msq + oaq
        if total_questions > 120:
            messages.error(request, 'Total Questions more than 120')
            return render(request, 'createtests/quick-test.html', context)

        if total_questions < 1:
            messages.error(request, 'Total questions are 0. Please add more questions')
            return render(request, 'createtests/quick-test.html', context)

        # Will use the generate_questions function
        question_data = generate_questions(teaching_material, question_types)
        footer = generate_footer_info(header)


        print(question_data)



        user_test = UserTest.objects.create(owner=request.user, header=header, subtitle=subtitle,
                                            institution=institution,
                                            add_header_info=add_header_info,
                                            grades=grades, question_types=question_types, questions=question_data,
                                            footer=footer, notes=tag)

        return redirect(my_tests)

@login_required(login_url='/authentication/login')
def advanced_test(request):
    context = {
        'values': request.POST
    }
    max_tokens_per_teaching_material = 14000
    max_characters = max_tokens_per_teaching_material*4
    min_characters = 100
    max_words = 14000*.75

    if request.method == 'GET':
        return render(request, 'createtests/advanced-test.html')

    if request.method == 'POST':
        teaching_material = request.POST['teaching_material']
        header = request.POST['header']

        if not header or header.isspace():
            messages.error(request, 'Header is required')
            return render(request, 'createtests/advanced-test.html', context)
        # disable for now for testing purposes
        if not teaching_material or teaching_material.isspace():
            messages.error(request, 'Please provide teaching material')
            return render(request, 'createtests/advanced-test.html', context)
        print(len(teaching_material))
        if len(teaching_material) < min_characters:
            messages.error(request, f"Please provide teaching material longer than {min_characters} characters.")
            return render(request, 'createtests/advanced-test.html', context)
        if len(teaching_material) > max_characters:
            messages.error(request, f"Please provide teaching material shorter than {max_characters} characters.")
            return render(request, 'createtests/advanced-test.html', context)

        subtitle = request.POST['subtitle']

        institution = request.POST['institution']
        add_header_info = request.POST['add_header_info']

        tag = request.POST['tag']

        # Access grades data
        grades_data_json = request.POST['grades_data']
        grades_data = json.loads(grades_data_json)
        # Use the grades_data as needed
        grades = grades_data['grades']

        # Questions Data
        mcq = request.POST['mcq']
        if mcq != "":
            mcq = int(mcq)
        else:
            mcq = 0

        msq = request.POST['msq']
        if msq != "":
            msq = int(msq)
        else:
            msq = 0

        oaq = request.POST['oaq']
        if oaq != "":
            oaq = int(oaq)
        else:
            oaq = 0
        question_types = {"mcq": mcq, "msq": msq, "oaq": oaq}

        total_questions = mcq + msq + oaq
        if total_questions > 120:
            messages.error(request, 'Total Questions more than 120')
            return render(request, 'createtests/advanced-test.html', context)

        if total_questions < 1:
            messages.error(request, 'Total questions are 0. Please add more questions')
            return render(request, 'createtests/advanced-test.html', context)

        # Will be question_data = generate_questions(request.POST['teaching_materail']) in->text out->json
        question_data = generate_questions(teaching_material, question_types)
        footer = request.POST['footer']

        print(question_data)


        user_test = UserTest.objects.create(owner=request.user, header=header, subtitle=subtitle,
                                            institution=institution,
                                            add_header_info=add_header_info,
                                            grades=grades, question_types=question_types, questions=question_data,
                                            footer=footer, notes=tag)


        return redirect(my_tests)
