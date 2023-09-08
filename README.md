# PracticeTestApp

## How to run the project


###Install python

###Create virtual environment in /PracticeTestApp
>python -m venv venv_name
> 
> source venv/bin/activate    Mac
> 
> or
> 
> ./venv/Scripts/activate     Windows

###Install the requirements
>pip install -r requirements.txt

###Migrate the project
>python manage.py makemigrations
> 
> python manage.py migrate

###Run the project
>python manage.py runserver

###Make pricing models:
####Go to createtests/views.py and comment out line
> create_initial_membership()
####Go to the http://127.0.0.1:8000/create-tests/
####Go to createtests/views.py and comment in line
> create_initial_membership()


##Text processing

1. The text is divided to a list[str]. Each str has predefined number of words(50)
["bla bla", "bla bla", "bla bla", "bla bla"]
2. We create a list of number of questions per question type mcqList[num]. 
The number specifies the number of questions and the index specifies the ext cut we will use. 
[0, 1, 0, 2]
3. A function will automatically choose only one question type per text cut, so they are no repetitions
















