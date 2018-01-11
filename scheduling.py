import main as main
import slack_interactor as slack
import schedule
import time
import sys
import datetime

sys.dont_write_bytecode = True

fb = Firebase_Interactor()


def remind_tasks():
    now = datetime.datetime.now()
    if now.day % 2 == 0:
        slack.remind_tasks()
    
def check_overdue():
    main.check_overdue()
    
schedule.every().day.at("0:00").do(check_overdue)
schedule.every().day.at("8:00").do(remind_tasks)

while 1:
    schedule.run_pending()
    time.sleep(1)
