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



















