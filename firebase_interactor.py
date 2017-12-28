from firebase import firebase
from operator import itemgetter
import ast
import json
import datetime

class Firebase_Interactor:
    fb = firebase.FirebaseApplication('https://inventory-cade0.firebaseio.com', None)

    def add_task(self, subteam, raw_task):
        task = {}
        for key in raw_task:
            x = key.encode("ascii")
            y = raw_task[key].encode("ascii")
            task[x] = y
        task["completed"] = 0
        task["date-added"] = datetime.date.today()
        result = Firebase_Interactor.fb.post('/'+subteam, task)

    """
    update_task() changes the status of a current task (completed or ongoing)
    the data parameter is optional and is only used for editing a task
    """
    def update_task(self, subteam, status, id_task, data=None):
        if status == "completed":
            Firebase_Interactor.fb.put('/'+subteam+'/'+id_task, 'completed', 1)
        elif status == "ongoing":
            Firebase_Interactor.fb.put('/'+subteam+'/'+id_task, 'completed', 0)
        elif status == "edited":
            Firebase_Interactor.fb.put('/'+subteam+'/'+id_task, 'date', data.get('date'))
            Firebase_Interactor.fb.put('/'+subteam+'/'+id_task, 'text', data.get('text'))
    
    """
    edit_task() updates the information of a task
    """
    def edit_task(self, subteam, id_task, raw_task):
        Firebase_Interactor.fb.put('/'+subteam+'/'+id_task, {})

    def delete_task(self, subteam, id_task):
        Firebase_Interactor.fb.delete('/'+subteam, id_task)

    """
    displaay_list() returns the entire list for the subteam and is called in every app route.
    The boolean has_year is used to add a year to the date (used for checking overdue and
    updating task) or return the data without the year.
    """
    def display_list(self, subteam, has_year):
        raw_ret_data = Firebase_Interactor.fb.get('/'+subteam, None) 
        ret_data = []
        task_ongoing = False

        for id_task, data in raw_ret_data.iteritems():
            temp = []
            temp.append(id_task)
            for value in data.values():
                temp.append(value)
                if value == 0:
                    task_ongoing = True
            ret_data.append(temp)

        if len(ret_data) > 1 and task_ongoing: # removes default message if there is at least one task present, and a task ongoing
            ret_data = filter(lambda x:x[0]!='x',ret_data)

        ret_data = sorted(ret_data, key=itemgetter(1)) # sort by date
        
        if has_year == False:
            for datalist in ret_data:
                datalist[1] = datalist[1][5:] # remove year if necessary

        return ast.literal_eval(json.dumps(ret_data))

    def check_overdue(self):
        all_ret_data = Firebase_Interactor.fb.get('/', None)
        yesterday_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")        

        for key in all_ret_data.keys():
            ret_data = self.display_list(key, True)
            for datalist in ret_data:
                if yesterday_date >= datalist[1] and datalist[3] == 0:   # if due date is equal to yesterday's date, mark as overdue (2)
                    Firebase_Interactor.fb.put('/'+key+'/'+datalist[0], 'completed', 2)
                
