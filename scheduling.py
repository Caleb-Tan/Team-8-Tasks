import main as main
from firebase_interactor import Firebase_Interactor
import slack_interactor as slack
import schedule
import time
import pprint

fb = Firebase_Interactor()

def remind_tasks():
    ret_data = fb.display_list('Business', False)
    pprint ret_data
def check_overdue():
    main.check_overdue()
    
schedule.every().day.at("0:00").do(check_overdue)

while 1:
    schedule.run_pending()
    time.sleep(1)
