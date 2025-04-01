from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import os
from agent import process_message
from jobs import job_manager
import threading
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session management

# Hardcoded credentials for testing
TEST_USERNAME = "admin"
TEST_PASSWORD = "password123"

def job_execution_callback(job_id: str, execution_time: datetime) -> None:
    """Callback function to handle job executions."""
    print(f"\n[Job Execution] Job {job_id} executed at {execution_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')}\n")

def start_job_manager():
    """Start the job manager in a separate thread."""
    job_manager.set_execution_callback(job_execution_callback)
    job_manager.start()

# Start the job manager in a separate thread when the app is created
job_thread = threading.Thread(target=start_job_manager, daemon=True)
job_thread.start()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == os.environ.get('USERNAME') and password == os.environ.get('PASSWORD'):
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', username=session['username'])

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    message = request.form.get('message')
    response = process_message(message)
    return {"response": response}

if __name__ == '__main__':
    app.run(debug=True)
