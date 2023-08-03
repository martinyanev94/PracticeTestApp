import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use,choose another one '}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use,choose another one '}, status=409)
        return JsonResponse({'username_valid': True})


# Your email configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
username = 'mpyanev@gmail.com'
password = 'zzntmppswidndcyv'
# password = 'arggrupobdqxwpez'
sender_email = 'mpyanev@gmail.com'


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_body = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    }

    link = reverse('activate', kwargs={
        'uidb64': email_body['uid'], 'token': email_body['token']})

    email_subject = 'Activate your account'
    activate_url = 'http://' + current_site.domain + link

    email_body_text = f'Hi {user.username}, Please click the link below to activate your account: {activate_url}'

    message = MIMEMultipart("alternative")
    message["Subject"] = 'Activate your account'
    message["From"] = sender_email
    message["To"] = user.email

    text = f"""\
    Hi {user.username}, Please click the link below to activate your account: {activate_url}
    
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(username, password)
            server.sendmail(from_addr=sender_email, to_addrs=user.email, msg=message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", str(e))


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):

        context = {
            'values': request.POST
        }

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():

            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)
                try:
                    user = User.objects.create_user(username=username, email=email)
                    user.set_password(password)
                    user.is_active = False
                    user.save()
                    send_activation_email(user, request)
                    messages.success(request, f"Account successfully created. Now you need to verify your email. "
                                              f"We've send you a verification message on {user.email}.")
                    return render(request, 'authentication/login.html')
                except:
                    messages.error(request, "Please provide a username")

        return render(request, 'authentication/register.html', context)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login' + '?message=' + 'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +
                                     user.username + ' you are now logged in')
                    return redirect('choose-create-speed')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'authentication/login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')


# function to create reset password
class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset_password.html')

    def post(self, request):
        email = request.POST['email']

        context = {
            'values': request.POST
        }
        if not validate_email(email):
            messages.error(request, "Please supply a valid email")

        # Skipped because gmail gives ssl certificate error.
        current_site = get_current_site(request)

        #Will fail for invalid email no matter what fails in the block below
        try:
            user = User.objects.get(email__exact=email)
            email_contents = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': PasswordResetTokenGenerator().make_token(user),
            }

            link = reverse('reset-user-password', kwargs={
                'uidb64': email_contents['uid'], 'token': email_contents['token']})

            email_subject = 'Reset Password Instructions'

            reset_url = 'http://' + current_site.domain + link

            message = MIMEMultipart("alternative")
            message["Subject"] = email_subject
            message["From"] = sender_email
            message["To"] = user.email

            text = f"""\
            Hi {user.username}, Please click the link below to reset your password: {reset_url}
    
            """
            print(reset_url)

            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")

            message.attach(part1)
            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.ehlo()
                    server.starttls()
                    server.login(username, password)
                    server.sendmail(from_addr=sender_email, to_addrs=user.email, msg=message.as_string())
                    print("Email sent successfully!")
            except Exception as e:
                print("Error sending email:", str(e))

            messages.success(request, "We have sent you and email to reset your password")
            return render(request, 'authentication/reset_password.html')
        except:
            messages.error(request, "Please supply a valid email")
            return render(request, 'authentication/reset_password.html')



class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(
                    request, "Password link is invalid. Please request a new one.")
                return render(request, 'authentication/reset_password.html')
        except Exception as identifier:
            pass

        return render(request, 'authentication/set_new_password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            messages.error(request, "Passwords do not match")
            return render(request, 'authentication/set_new_password.html', context)

        if len(password) < 6:
            messages.error(request, "Password too short")
            return render(request, 'authentication/set_new_password.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(
                request, "Password reset succesfully, you can login with your new password")
            return redirect('login')
        except Exception as identifier:
            messages.info(
                request, 'Something went wrong, try again')
            return render(request, 'authentication/set_new_password.html', context)


