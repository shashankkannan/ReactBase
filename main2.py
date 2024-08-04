import os
from tkinter import Tk
from tkinter.filedialog import askdirectory

def create_file(path, filename, content):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, filename), 'w') as file:
        file.write(content)

def setup_flask_firebase_app():
    root = Tk()
    root.withdraw()
    folder_path = askdirectory(title='Select the folder to create the Flask app')

    if not folder_path:
        print("No folder selected. Exiting...")
        return

    app_name = input("Enter the name of your Flask app: ").strip()
    if not app_name:
        print("App name cannot be empty. Please run again")
        return

    app_path = os.path.join(folder_path, app_name)

    os.makedirs(app_path, exist_ok=True)
    os.chdir(app_path)

    os.system('python -m venv venv')
    os.system('venv\\Scripts\\pip install flask firebase-admin')

    app_py_content = """
from flask import Flask, render_template, request, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

cred = credentials.Certificate('path/to/your/firebase/credentials.json')
firebase_admin.initialize_app(cred)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user(email=email, password=password)
            flash('Signup successful. Please verify your email.', 'success')
            return redirect(url_for('signin'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.get_user_by_email(email)
            if user:
                # Password validation should be handled differently in real applications
                flash('Sign in successful', 'success')
                return redirect(url_for('home'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)
"""
    create_file(app_path, 'app.py', app_py_content)

    signup_html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="form-container">
        <h1>Sign Up</h1>
        <form method="post" class="form-box">
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Sign Up</button>
        </form>
    </div>
</body>
</html>
"""
    create_file(os.path.join(app_path, 'templates'), 'signup.html', signup_html_content)

    signin_html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign In</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="form-container">
        <h1>Sign In</h1>
        <form method="post" class="form-box">
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Sign In</button>
        </form>
    </div>
</body>
</html>
"""
    create_file(os.path.join(app_path, 'templates'), 'signin.html', signin_html_content)

    home_html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>Welcome Home!</h1>
    </div>
</body>
</html>
"""
    create_file(os.path.join(app_path, 'templates'), 'home.html', home_html_content)

    style_css_content = """
body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
}

.container, .form-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.form-box {
    display: flex;
    flex-direction: column;
    padding: 20px;
    border: 1px solid #ccc;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    background-color: #fff;
}

.form-box input {
    margin-bottom: 10px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.form-box button {
    padding: 10px;
    border: none;
    border-radius: 4px;
    background-color: #28a745;
    color: white;
    cursor: pointer;
}

.form-box button:hover {
    background-color: #218838;
}
"""
    create_file(os.path.join(app_path, 'static'), 'style.css', style_css_content)

    print(f"Setup complete. Navigate to {app_path}, activate the virtual environment with 'venv\\Scripts\\activate', and start the app with 'python app.py'.")

if __name__ == "__main__":
    setup_flask_firebase_app()
