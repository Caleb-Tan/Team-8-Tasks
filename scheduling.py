import main as main
import schedule
import time


def post_tasks():
    main.post_tasks('Business', 'public')

def check_overdue():
    main.check_overdue()
    
schedule.every().day.at("0:00").do(check_overdue)

while 1:
    schedule.run_pending()
    time.sleep(1)
