import os
import subprocess

def create_django_project():
    project_name = "my_django_project"
    app_name = "accounts"

    subprocess.run(["django-admin", "startproject", project_name])
    os.chdir(project_name)
    subprocess.run(["python", "manage.py", "startapp", app_name])
    create_django_files(app_name)
    subprocess.run(["python", "manage.py", "makemigrations"])
    subprocess.run(["python", "manage.py", "migrate"])
    subprocess.run(["python", "manage.py", "createsuperuser"])

def create_django_files(app_name):
    project_name = "my_django_project"
    models_content = '''
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass
    '''

    views_content = '''
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')
    '''

    urls_content = f'''
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
]
    '''

    register_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Register</title>
</head>
<body>
    <h2>Register</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Register</button>
    </form>
</body>
</html>
    '''

    login_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <form method="post">
        {% csrf_token %}
        <label for="username">Username:</label>
        <input type="text" name="username" id="username" required><br>
        <label for="password">Password:</label>
        <input type="password" name="password" id="password" required><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
    '''

    with open(f"{app_name}/models.py", "w") as file:
        file.write(models_content)

    with open(f"{app_name}/views.py", "w") as file:
        file.write(views_content)

    with open(f"{app_name}/urls.py", "w") as file:
        file.write(urls_content)

    os.makedirs(f"{app_name}/templates", exist_ok=True)
    with open(f"{app_name}/templates/register.html", "w") as file:
        file.write(register_template)

    with open(f"{app_name}/templates/login.html", "w") as file:
        file.write(login_template)

    settings_file = f"{project_name}/settings.py"
    with open(settings_file, "a") as file:
        file.write(f"\nINSTALLED_APPS += ['{app_name}']")
        file.write(f"\nAUTH_USER_MODEL = '{app_name}.CustomUser'")

    project_urls_file = f"{project_name}/urls.py"
    with open(project_urls_file, "a") as file:
        file.write(f"\nfrom {app_name} import urls as {app_name}_urls")
        file.write(f"\nurlpatterns += [path('', {app_name}_urls)]")

if __name__ == "__main__":
    create_django_project()
