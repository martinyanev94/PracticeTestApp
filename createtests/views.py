import json
import string
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from mytests.views import my_tests
from payment.models import UserMembership
from payment.signals import create_initial_membership
from payment.views import manage_membership
from .chat_gpt import generate_header, generate_subtitle, \
    generate_footer_info, generate_questions
from .messages import languages
from .models import UserTest

# Create your views here.

@login_required(login_url='/authentication/login')
def choose_create_speed(request):
    # You can make this global form the middleware on practicetests/custom_middleware
    manage_membership(request)

    user_membership = UserMembership.objects.filter(user=request.user).first()
    context = {
        'values': request.POST,
        'user_membership': user_membership.membership,
    }

    return render(request, 'createtests/choose-create-speed.html', context)


@login_required(login_url='/authentication/login')
def quick_test(request):
    user_membership = UserMembership.objects.filter(user=request.user).first()
    one_month_ago = timezone.now() - timedelta(days=30)
    user_test_count_last_month = UserTest.objects.filter(owner=request.user, created_at__gte=one_month_ago).count()

    context = {
        'values': request.POST,
        'user_membership': user_membership.membership,
        'user_test_count_last_month': user_test_count_last_month,
        'languages': languages,
    }

    if request.method == 'GET':
        return render(request, 'createtests/quick-test.html', context)

    if request.method == 'POST':
        teaching_material = request.POST['teaching_material']
        language = request.POST['language']

        header = generate_header(teaching_material, language)

#===================BACKEND CHECKS========================================
        if not header or header.isspace():
            messages.error(request, 'Header is required')
            return render(request, 'createtests/quick-test.html', context)

        if not teaching_material or teaching_material.isspace():
            messages.error(request, 'Please provide teaching material')
            return render(request, 'createtests/quick-test.html', context)
# ===================BACKEND CHECKS========================================

        subtitle = generate_subtitle(header, language)
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

        total_questions = mcq + msq + oaq

# ===================BACKEND CHECKS========================================
        if user_test_count_last_month > user_membership.membership.allowed_tests:
            messages.error(request, f'Total Test more {user_membership.membership.allowed_tests} allowed monthly')
            return render(request, 'createtests/quick-test.html', context)

        if total_questions > user_membership.membership.allowed_question:
            messages.error(request, f'Total Questions more {user_membership.membership.allowed_question}')
            return render(request, 'createtests/quick-test.html', context)

        if total_questions < 1:
            messages.error(request, 'Total questions are 0. Please add more questions')
            return render(request, 'createtests/quick-test.html', context)
# ===================BACKEND CHECKS========================================

        # Will use the generate_questions function
        question_data, usage = generate_questions(teaching_material, question_types, language)

        # Update tokens
        user_membership.used_tokens = usage[0] + user_membership.used_tokens
        user_membership.cost = usage[1] + user_membership.cost

        user_membership.save()

        footer = generate_footer_info(header)

        user_test = UserTest.objects.create(owner=request.user, header=header, subtitle=subtitle,
                                            institution=institution,
                                            add_header_info=add_header_info,
                                            grades=grades, question_types=question_types, questions=question_data,
                                            footer=footer, notes=tag)

        return redirect(my_tests)


@login_required(login_url='/authentication/login')
def advanced_test(request):
    user_membership = UserMembership.objects.filter(user=request.user).first()
    one_month_ago = timezone.now() - timedelta(days=30)
    user_test_count_last_month = UserTest.objects.filter(owner=request.user, created_at__gte=one_month_ago).count()

    context = {
        'values': request.POST,
        'user_membership': user_membership.membership,
        'user_test_count_last_month': user_test_count_last_month,
        'languages': languages,
    }

    if request.method == 'GET':
        return render(request, 'createtests/advanced-test.html', context)

    if request.method == 'POST':
        teaching_material = request.POST['teaching_material']
        header = request.POST['header']
        language = request.POST['language']


# ===================BACKEND CHECKS========================================
        if not header or header.isspace():
            messages.error(request, 'Header is required')
            return render(request, 'createtests/advanced-test.html', context)
        # disable for now for testing purposes
        if not teaching_material or teaching_material.isspace():
            messages.error(request, 'Please provide teaching material')
            return render(request, 'createtests/advanced-test.html', context)
# ===================BACKEND CHECKS========================================


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

        # ===================BACKEND CHECKS========================================
        if user_test_count_last_month > user_membership.membership.allowed_tests:
            messages.error(request, f'Total Test more {user_membership.membership.allowed_tests} allowed monthly')
            return render(request, 'createtests/quick-test.html', context)

        if total_questions > user_membership.membership.allowed_question:
            messages.error(request, f'Total Questions more {user_membership.membership.allowed_question}')
            return render(request, 'createtests/quick-test.html', context)

        if total_questions < 1:
            messages.error(request, 'Total questions are 0. Please add more questions')
            return render(request, 'createtests/quick-test.html', context)
        # ===================BACKEND CHECKS========================================

        # Will use the generate_questions function
        question_data, usage = generate_questions(teaching_material, question_types, language)

        # Update tokens
        user_membership.used_tokens = usage[0] + user_membership.used_tokens
        user_membership.cost = usage[1] + user_membership.cost

        user_membership.save()

        footer = request.POST['footer']

        user_test = UserTest.objects.create(owner=request.user, header=header, subtitle=subtitle,
                                            institution=institution,
                                            add_header_info=add_header_info,
                                            grades=grades, question_types=question_types, questions=question_data,
                                            footer=footer, notes=tag)

        return redirect(my_tests)




def demo_test(request):
    submission_count = request.session.get('submission_count', 0)

    if submission_count >= 3:
        # User has reached the submission limit, show an error message or redirect
        messages.success(request, 'Sign Up to TestBox AI to continue building FREE exams. Advanced features such as Exam Downloads and Management included')
        return redirect('register')  # Redirect to another view or page

    mcq = 3
    context = {
        'values': request.POST,
        'languages': languages,
        'mcq': mcq
    }

    if request.method == 'GET':
        return render(request, 'createtests/demo.html', context)

    if request.method == 'POST':
        # Increment the submission count and store it in the session
        submission_count += 1
        request.session['submission_count'] = submission_count

        teaching_material = request.POST['teaching_material']
        language = request.POST['language']

        header = generate_header(teaching_material, language)

#===================BACKEND CHECKS========================================
        if not header or header.isspace():
            messages.error(request, 'Header is required')
            return render(request, 'createtests/demo.html', context)

        if not teaching_material or teaching_material.isspace():
            messages.error(request, 'Please provide teaching material')
            return render(request, 'createtests/demo.html', context)

        if len(teaching_material.split()) > 3000:
            messages.error(request, 'Text is longer than 3000 words. Please reduce the words or login for unlimited words for FREE')
            return render(request, 'createtests/demo.html', context)

        if len(teaching_material.split()) < 50:
            messages.error(request, 'Text is shorter than 50 words. Please more context')
            return render(request, 'createtests/demo.html', context)


# ===================BACKEND CHECKS========================================

        subtitle = generate_subtitle(header, language)

        # Questions Data
        if mcq != "":
            mcq = int(mcq)
        else:
            mcq = 0
        if mcq < 1:
            messages.error(request, 'Total questions are 0. Please add more questions')
            return render(request, 'createtests/demo-test.html', context)

        question_types = {"mcq": mcq, "msq": 0, "oaq": 0}

        question_data, usage = generate_questions(teaching_material, question_types, language)

        alphabet = string.ascii_uppercase
        for key, question in question_data.items():
            if 'answers' in question:
                updated_answers = [f"{alphabet[i]}. {answer}" for i, answer in enumerate(question['answers'])]
                question['answers'] = updated_answers

            if 'correct_answer' in question:
                updated_correct_answer = [alphabet[i - 1] for i in question['correct_answer']]
                question['correct_answer'] = updated_correct_answer


        context = {
            'header': header,
            'subtitle': subtitle,
            'questions': question_data,
            'alphabet': alphabet,
            'values': request.POST,
            'languages': languages,
            'mcq':mcq,

        }
        return render(request, 'createtests/demo-home.html', context)



