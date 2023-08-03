import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect

from createtests.models import UserTest
from django.contrib import messages




def search_tests(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        user_tests = UserTest.objects.filter(
            header__istartswith=search_str, owner=request.user) | UserTest.objects.filter(
            notes__istartswith=search_str, owner=request.user) | UserTest.objects.filter(
            num_questions__icontains=search_str, owner=request.user) | UserTest.objects.filter(
            created_at__icontains=search_str, owner=request.user)
        data = user_tests.values()
        return JsonResponse(list(data), safe=False)

# Create your views here.
@login_required(login_url='/authentication/login')
def my_tests(request):
    user_tests = UserTest.objects.filter(owner=request.user)
    paginator = Paginator(user_tests, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'user_tests': user_tests,
        'page_obj': page_obj,
    }
    return render(request, 'mytests/index.html', context)



@login_required(login_url='/authentication/login')
def edit_pt(request, id):
    user_tests = UserTest.objects.get(pk=id)
    context = {
        'user_tests': user_tests,
        'values': user_tests,
    }
    if request.method == 'GET':
        return render(request, 'mytests/edit_pt.html', context)
    if request.method == 'POST':
        header = request.POST['header']

        if not header:
            messages.error(request, 'Header is required')
            return render(request, 'mytests/edit_pt.html', context)

        subtitle = request.POST['subtitle']
        institution = request.POST['institution']
        add_header_info = request.POST['add_header_info']

        tag = request.POST['notes']
        footer = request.POST['footer']
        grades = []
        print(user_tests.grades)
        for i in range(1, 20):  # Assuming there are four grades (you can adjust the range based on your actual data)
            grade_key = f'grade_{i}_grade'
            percentage_key = f'grade_{i}_percentage'
            grade = request.POST.get(grade_key)
            percentage = request.POST.get(percentage_key)

            if grade and percentage:
                grades.append({
                    'grade': grade,
                    'percentage': int(percentage),  # Convert percentage to an integer if required
                })

        # Update main fields
        user_tests.header = header
        user_tests.subtitle = subtitle
        user_tests.institution = institution
        user_tests.add_header_info = add_header_info
        user_tests.grades = grades
        user_tests.notes = tag
        user_tests.footer = footer


        # Update question fields
        questions = {}
        for key, value in request.POST.items():
            if key.startswith('questions_'):
                parts = key.split('_')
                question_id = parts[1]
                field_name = parts[2]

                if question_id not in questions:
                    questions[question_id] = {}

                # If it's an answer field, create a list and append the values
                if field_name == 'answers':
                    if 'answers' not in questions[question_id]:
                        questions[question_id]['answers'] = []
                    questions[question_id]['answers'].append(value)
                else:
                    questions[question_id][field_name] = value

        user_tests.questions = questions

        user_tests.save()
        messages.success(request, f'Practice test {header} updated successfully')

        return redirect('my-tests')




def delete_pt(request, id):
    user_test = UserTest.objects.get(pk=id)
    header = user_test.header
    user_test.delete()
    messages.success(request, f'Test {header} removed')
    return redirect('my-tests')