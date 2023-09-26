from flask import Flask, render_template, redirect, url_for, request
import requests

app = Flask(__name__)

# Update the backend URL to use the service name 'backend'
backend_url = "http://backend-service:3001"  

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        task_text = request.form['task_text']
        response = requests.post(f"{backend_url}/add", json={'task_text': task_text})

        # Check for a successful response (HTTP status code 201)
        if response.status_code == 201:
            return redirect(url_for('add_task'))
        else:
            return "Failed to add task."

    return render_template('add_task.html')

@app.route('/tasks')
def task_list():
    response = requests.get(f"{backend_url}/tasks")

    # Check for a successful response (HTTP status code 200)
    if response.status_code == 200:
        tasks = response.json()
        return render_template('task_list.html', tasks=tasks)
    else:
        return "Failed to fetch tasks."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

