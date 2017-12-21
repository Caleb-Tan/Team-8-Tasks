from flask import Flask, render_template, request
from firebase_interactor import Firebase_Interactor
from firebase import firebase
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__) # flask app
fb = Firebase_Interactor() # firebase initialization
scheduler = BackgroundScheduler() # background task scheduler


@app.route('/')
def list_subteams():
    subteam_list = ['Design', 'Build', 'Business', 'Art']
    management_list = {'Lab':'Vyomika Gupta', 'Pit':'Lawrence Chang', 'Treasury':'Amy Lin', 'Competition':'Jeffery Yu'}
    specops_list = ['Drive Team', 'Strategy and Scouting', 'Zero Robotics', 'VEX']
    admin_list = {'Team Captain': 'Devin Ardeshna', 'Assistant Captain': 'Annalee Soohoo', 'Project Manager': 'Eli Zucker', 'Strategic Director': 'Simran Pujji'}
    
    return render_template('home.html', subteams=subteam_list, management=management_list, spec_ops=specops_list, admin=admin_list)

@app.route('/<name>')
def display_subteam(name):
    ret_data = fb.display_list(name) # updates data
    
    return render_template('subteam.html', subteam=name, data=ret_data)

@app.route('/<name>/add_task', methods=['POST'])
def add_task(name):
    if request.method == 'POST':
        task = request.form
        fb.add_task(name, task) # calls firebase interactor's add task method
    
    ret_data = fb.display_list(name)
    return render_template('subteam.html', subteam=name, data=ret_data)
    
@app.route('/<name>/update_task/<status>/<id_task>')
def update_task(name, status, id_task):
    fb.update_task(name, status, id_task) 
    ret_data = fb.display_list(name) # updates data
    
    return render_template('subteam.html', subteam=name, data=ret_data)

@app.route('/<name>/delete_task/<id_task>')
def delete_task(name, id_task):
     fb.delete_task(name, id_task)
     ret_data = fb.display_list(name) # updates data
     
     return render_template('subteam.html', subteam=name, data=ret_data)

@scheduler.scheduled_job('cron', hour=7)
def check_overdue():
    fb.check_overdue

scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
    
    
