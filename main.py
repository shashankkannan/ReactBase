import os
from tkinter import Tk
from tkinter.filedialog import askdirectory


def create_file(path, filename, content):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, filename), 'w') as file:
        file.write(content)


def setup_react_firebase_app():
    root = Tk()
    root.withdraw()
    folder_path = askdirectory(title='Select the folder to create the React app')

    if not folder_path:
        print("No folder selected. Exiting...")
        return

    app_name = input("Enter the name of your React app: ").strip()
    if not app_name:
        print("App name cannot be empty. Please run again")
        return

    app_path = os.path.join(folder_path, app_name)

    os.system(f'npx create-react-app {app_path}')
    os.chdir(app_path)
    os.system('npm install firebase react-router-dom')
    firebase_js_content = """
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getDatabase } from "firebase/database";

const firebaseConfig = {
    apiKey: "",
    authDomain: "",
    databaseURL: "",
    projectId: "",
    storageBucket: "",
    messagingSenderId: "",
    appId: "",
    measurementId: ""
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const database = getDatabase(app);

export { app, auth, database };
"""
    create_file('src/components', 'firebase.js', firebase_js_content)

    # auth.js file
    auth_js_content = """
import { auth } from "./firebase";
import { createUserWithEmailAndPassword, sendEmailVerification, sendPasswordResetEmail, signInWithEmailAndPassword } from "firebase/auth";

export const doCreateUserWithEmailAndPassword = async (email, password) => {
    return createUserWithEmailAndPassword(auth, email, password);
};

export const doSignInWithEmailAndPassword = async (email, password) => {
    return signInWithEmailAndPassword(auth, email, password);
};

export const doSignOut = () => {
    return auth.signOut();
};

export const doPasswordReset = (email) => {
    return sendPasswordResetEmail(auth, email);
};
"""
    create_file('src/components', 'auth.js', auth_js_content)

    # Signup component
    signup_js_content = """
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { doCreateUserWithEmailAndPassword } from './auth';
import { sendEmailVerification } from 'firebase/auth';
import './Form.css';

export const Signup = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [reenterPassword, setReenterPassword] = useState('');
    const navigate = useNavigate();

    const handleSignup = async (e) => {
        e.preventDefault();
        if (password === reenterPassword) {
            try {
                const userCredential = await doCreateUserWithEmailAndPassword(email, password);
                await sendEmailVerification(userCredential.user);
                alert('Verification email sent!');
                navigate('/signin');
            } catch (error) {
                alert(error.message);
            }
        } else {
            alert('Passwords do not match');
        }
    };

    return (
        <div className="form-container">
            <h1>Sign Up</h1>
            <form onSubmit={handleSignup} className="form-box">
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
                <input type="password" value={reenterPassword} onChange={(e) => setReenterPassword(e.target.value)} placeholder="Reenter Password" required />
                <button type="submit">Sign Up</button>
            </form>
        </div>
    );
};

export default Signup;
"""
    create_file('src/components', 'Signup.js', signup_js_content)

    # Signin component
    signin_js_content = """
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { doSignInWithEmailAndPassword } from './auth';
import './Form.css';

export const Signin = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSignin = async (e) => {
        e.preventDefault();
        try {
            const userCredential = await doSignInWithEmailAndPassword(email, password);
            if (userCredential.user.emailVerified) {
                alert('Sign in successful');
                navigate('/home');
            } else {
                alert('Please verify your email before signing in');
            }
        } catch (error) {
            alert(error.message);
        }
    };

    return (
        <div className="form-container">
            <h1>Sign In</h1>
            <form onSubmit={handleSignin} className="form-box">
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
                <button type="submit">Sign In</button>
            </form>
        </div>
    );
};

export default Signin;
"""
    create_file('src/components', 'Signin.js', signin_js_content)

    # Home component
    home_js_content = """
import React from 'react';

export const Home = () => {
    return (
        <div>
            <h1>Welcome Home!</h1>
        </div>
    );
};

export default Home;
"""
    create_file('src/components', 'Home.js', home_js_content)

    # App.js file
    app_js_content = """
import logo from './logo.svg';
import './App.css';
import Signin from './components/Signin';
import Signup from './components/Signup';
import Home from './components/Home'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Signup />} />
          <Route path="/signin" element={<Signin />} />
          <Route path="/home" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
"""
    create_file('src', 'App.js', app_js_content)

    # Form.css for styling forms
    form_css_content = """
.form-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f5f5f5;
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
    create_file('src/components', 'Form.css', form_css_content)

    print(f"Setup complete. Navigate to {app_path} and start the app with 'npm start'.")


if __name__ == "__main__":
    setup_react_firebase_app()
