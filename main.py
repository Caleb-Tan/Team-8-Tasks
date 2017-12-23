from flask import Flask, render_template, request
from firebase_interactor import Firebase_Interactor
import slack_interactor as slack
from apscheduler.scheduler import Scheduler 
import datetime

app = Flask(__name__) # flask app
fb = Firebase_Interactor() # firebase initialization
sched = Scheduler()

@app.route('/')
def list_subteams():
    subteam_list = ['Design', 'Build', 'Business', 'Art']
    management_list = {'Lab':'Vyomika Gupta', 'Pit':'Lawrence Chang', 'Treasury':'Amy Lin', 'Competition':'Jeffery Yu'}
    specops_list = ['Drive Team', 'Strategy and Scouting', 'Zero Robotics', 'VEX']
    admin_list = {'Team Captain': 'Devin Ardeshna', 'Assistant Captain': 'Annalee Soohoo', 'Project Manager': 'Eli Zucker', 'Strategic Director': 'Simran Pujji'}
    
    return render_template('home.html', subteams=subteam_list, management=management_list, spec_ops=specops_list, admin=admin_list, date=datetime.date.today().strftime("%m/%d"))

@app.route('/<name>')
def display_subteam(name):
    ret_data = fb.display_list(name) # updates data
    
    return render_template('subteam.html', subteam=name, data=ret_data, date=datetime.date.today().strftime("%m/%d"))

@app.route('/<name>/add_task', methods=['POST'])
def add_task(name):
    if request.method == 'POST':
        task = request.form
        fb.add_task(name, task) # calls firebase interactor's add task method
    
    ret_data = fb.display_list(name)
    return render_template('subteam.html', subteam=name, data=ret_data, date=datetime.date.today().strftime("%m/%d"))
    
@app.route('/<name>/update_task/<status>/<id_task>')
def update_task(name, status, id_task):
    fb.update_task(name, status, id_task) 
    ret_data = fb.display_list(name) # gets data
    
    return render_template('subteam.html', subteam=name, data=ret_data, date=datetime.date.today().strftime("%m/%d"))

@app.route('/<name>/delete_task/<id_task>')
def delete_task(name, id_task):
     fb.delete_task(name, id_task)
     ret_data = fb.display_list(name) # gets data
     
     return render_template('subteam.html', subteam=name, data=ret_data, date=datetime.date.today().strftime("%m/%d"))

@sched.cron_schedule(hour=0)
def check_overdue():
    fb.check_overdue()

def post_tasks(name):
    ret_data = fb.display_list(name)
    slack.post_tasks(ret_data)

if __name__ == "__main__":
    sched.add_cron_job(lambda: post_tasks('Business'), hour=7)
    sched.start()
    app.run(debug=True)

    
    
