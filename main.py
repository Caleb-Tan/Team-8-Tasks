from flask import Flask, render_template, request
from firebase_interactor import Firebase_Interactor
import slack_interactor as slack
from apscheduler.scheduler import Scheduler 
import datetime
import json
import ast


app = Flask(__name__) # flask app
fb = Firebase_Interactor() # firebase initialization
sched = Scheduler() # scheduler initialization

"""
shows every subteam
"""
@app.route('/')
def list_subteams():
    subteam_list = ['Design', 'Build', 'Business', 'Art']
    management_list = {'Lab':'Vyomika Gupta', 'Pit':'Lawrence Chang', 'Treasury':'Amy Lin', 'Competition':'Jeffery Yu'}
    specops_list = ['Drive Team', 'Strategy and Scouting', 'Zero Robotics', 'VEX']
    admin_list = {'Team Captain': 'Devin Ardeshna', 'Assistant Captain': 'Annalee Soohoo', 'Project Manager': 'Eli Zucker', 'Strategic Director': 'Simran Pujji'}
    
    return render_template('home.html', subteams=subteam_list, management=management_list, spec_ops=specops_list, admin=admin_list, date=datetime.date.today().strftime("%m/%d"))

"""
called upon clicking on a subteam, displays tasks
"""
@app.route('/<name>')
def display_subteam(name):
    ret_data = fb.display_list(name, False) 
    
    return render_template('subteam.html', subteam=name, data=ret_data, date=datetime.date.today().strftime("%m/%d"))

"""
adds a task
"""
@app.route('/<name>/add_task', methods=['POST'])
def add_task(name):
    if request.method == 'POST':
        task = request.form
        fb.add_task(name, task) 
    
    ret_data = fb.display_list(name, False)
    return render_template('subteam.html', subteam=name, data=ret_data, date=datetime.date.today().strftime("%m/%d"))
    
"""
updates individual task
"""
@app.route('/<name>/update_task/<status>/<id_task>', methods=['POST'])
def update_task(name, status, id_task):
    if request.method == 'POST':
        task = ast.literal_eval(json.dumps(request.form))
        fb.update_task(name, status, id_task, task) 
    else: 
        fb.update_task(name, status, id_task) 

    ret_data = fb.display_list(name, False) 
    return render_template('subteam.html', subteam=name, data=ret_data, date=datetime.date.today().strftime("%m/%d"))

"""
returns the edit task page with the data of the task to be edited
"""
@app.route('/<name>/edit_task/<id_task>')
def edit_task(name, id_task):
    
    ret_data = fb.display_list(name, True)
    task = filter(lambda x: x[0] == id_task, ret_data)[0]  # extracts data for the specific task to edit  

    return render_template('edit_task.html', subteam=name, task=task, date=datetime.date.today().strftime("%m/%d"))

    
"""
deletes individual task
"""
@app.route('/<name>/delete_task/<id_task>')
def delete_task(name, id_task):  
     fb.delete_task(name, id_task)
     ret_data = fb.display_list(name, False) 
     
     return render_template('subteam.html', subteam=name, data=ret_data, date=datetime.date.today().strftime("%m/%d"))

"""
clears every task of that status: completed/overdue
"""
@app.route('/<name>/clear_all/<status>')
def clear_all(name, status):
    ret_data = fb.display_list(name, False)  # get current data
    if status == 'overdue':
        for task in ret_data:
            if task[3] == 2:
                fb.delete_task(name, task[0])
    elif status == 'completed':
        for task in ret_data:
            if task[3] == 1:
                fb.delete_task(name, task[0])
    
    updated_ret_data = fb.display_list(name, False) # get updated data
    return render_template('subteam.html', subteam=name, data=updated_ret_data, date=datetime.date.today().strftime("%m/%d"))

"""
slack interaction methods
"""
@app.route('/tasks', methods=['POST'])
def display_slack_tasks():
    text = ast.literal_eval(json.dumps(request.form)).get('text')
    if text == 'show':
        post_tasks('Business', 'visible')
        return 'Success! Tasks shared to channel.'
    else:
        payload = post_tasks('Business', 'ephemeral')
        return payload

def post_tasks(name, visibility):
    ret_data = fb.display_list(name, False)
    return slack.post_tasks(ret_data, visibility)

"""
scheduling, checks every new day if there are overdue tasks
"""
@sched.cron_schedule(hour=0)
def check_overdue():
    fb.check_overdue()

if __name__ == "__main__":
    sched.add_cron_job(lambda: post_tasks('Business', 'visible'), hour=7)
    sched.start()
    app.run(debug=True)

    
    
