import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect

from createtests.models import UserTest
from django.contrib import messages
import docx
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt
from django.http import HttpResponse


from django.shortcuts import render
from django.http import HttpResponse
from docx.shared import Pt
import docx

def download_teacher_view(request, id):
    user_tests = UserTest.objects.get(pk=id)

    # Function to create the Word document for teacher view
    def create_teacher_view_docx(user_tests):
        doc = docx.Document()
        heading = doc.add_heading(user_tests.header, level=1)
        heading.paragraph_format.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER

        subtitle = doc.add_heading(user_tests.subtitle, level=3)
        subtitle.paragraph_format.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER

        institution = doc.add_heading(user_tests.institution, level=3)
        institution.paragraph_format.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER

        add_header_info = doc.add_heading(user_tests.add_header_info, level=3)
        add_header_info.paragraph_format.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER


        for question_id, question_data in user_tests.questions.items():
            doc.add_heading(f"Question {question_id[1:]}:", level=2)
            doc.add_paragraph(question_data['question'])

            if 'answers' in question_data:
                for index, answer in enumerate(question_data['answers'], start=1):
                    doc.add_paragraph(f"{index}. {answer}")

            if 'correct_answer' in question_data:
                doc.add_heading("Correct Answer:", level=3)
                correct_answer_list = question_data['correct_answer']  # Assuming correct_answer is a list
                doc.add_paragraph(", ".join(str(answer) for answer in correct_answer_list))

            if question_data['explanation']:
                doc.add_heading("Explanation:", level=3)
                doc.add_paragraph(question_data['explanation'])

            doc.add_paragraph("")  # Adding a blank line between questions
        doc.add_heading(user_tests.footer, level=3)

        return doc

    # Create the Word document for teacher view
    doc = create_teacher_view_docx(user_tests)

    # Create a response with the Word document as a downloadable file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename=teacher_view_{user_tests.id}.docx'

    # Save the document to the response
    doc.save(response)

    return response


def download_student_view(request, id):
    user_tests = UserTest.objects.get(pk=id)
    header = user_tests.header

    # Function to create the Word document
    def create_student_view_docx(user_tests):
        doc = docx.Document()
        heading = doc.add_heading(user_tests.header, level=1)
        heading.paragraph_format.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER

        subtitle = doc.add_heading(user_tests.subtitle, level=3)
        subtitle.paragraph_format.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER

        institution = doc.add_heading(user_tests.institution, level=3)
        institution.paragraph_format.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER

        add_header_info = doc.add_heading(user_tests.add_header_info, level=3)
        add_header_info.paragraph_format.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER


        for question_id, question_data in user_tests.questions.items():
            print(question_data)
            doc.add_heading(f"Question {question_id[1:]}:", level=2)
            doc.add_paragraph(question_data['question'])

            if 'answers' in question_data:
                for index, answer in enumerate(question_data['answers'], start=1):
                    doc.add_paragraph(f"{index}. {answer}")

            doc.add_paragraph("")  # Adding a blank line between questions

        doc.add_heading(user_tests.footer, level=3)

        return doc

    # Create the Word document
    doc = create_student_view_docx(user_tests)

    # Create a response with the Word document as a downloadable file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename=student_view_{user_tests.id}.docx'

    # Save the document to the response
    doc.save(response)

    return response

#-----------------END DOWNLOAD VIEWS----------------------



def search_tests(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        user_tests = UserTest.objects.filter(
            header__istartswith=search_str, owner=request.user) | UserTest.objects.filter(
            notes__istartswith=search_str, owner=request.user) | UserTest.objects.filter(
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
def home_view(request, id):
    user_tests = UserTest.objects.get(pk=id)
    context = {
        'user_tests': user_tests,
        'values': user_tests,
    }
    if request.method == 'GET':
        return render(request, 'mytests/home-view.html', context)
    if request.method == 'POST':
        header = request.POST['header']



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
        #TODO do the same for the answers field to be in a list
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