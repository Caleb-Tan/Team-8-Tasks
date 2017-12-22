from firebase import firebase
import time
from datetime import datetime
from operator import itemgetter

class Firebase_Interactor:
    fb = firebase.FirebaseApplication('https://inventory-cade0.firebaseio.com', None)

    def add_task(self, subteam, raw_task):
        task = {}
        for key in raw_task:
            x = key.encode("ascii")
            y = raw_task[key].encode("ascii")
            task[x] = y
        task["completed"] = 0
        task["date-added"] = datetime.now().strftime('%m-%d')
        result = Firebase_Interactor.fb.post('/'+subteam, task)

    def update_task(self, subteam, status, id_task):
        if status == "completed":
            Firebase_Interactor.fb.put('/'+subteam+'/'+id_task, 'completed', 1)
        elif status == "ongoing":
            Firebase_Interactor.fb.put('/'+subteam+'/'+id_task, 'completed', 0)

    def delete_task(self, subteam, id_task):
        Firebase_Interactor.fb.delete('/'+subteam, id_task)

    
    # this function updates the list. It is called in every approute
    def display_list(self, subteam):
        raw_ret_data = Firebase_Interactor.fb.get('/'+subteam, None) 
        ret_data = []

        all_completed = True 
        for datadict in raw_ret_data.values():
            if 0 in datadict.values():
                all_completed = False

        if len(raw_ret_data) != 1 and not all_completed:
            raw_ret_data.pop('x') # removes "You're all caught up!" if necessary

        for id_task, data in raw_ret_data.iteritems():
            temp = []
            temp.append(id_task)
            for value in data.values():
                temp.append(value)
            ret_data.append(temp)

        ret_data = sorted(ret_data, key=itemgetter(1)) # sort by date

        for datalist in ret_data:
            datalist[1] = datalist[1][5:] # remove year

        return ret_data

    def check_overdue(self):
        for 
        self.display_list('Business')
