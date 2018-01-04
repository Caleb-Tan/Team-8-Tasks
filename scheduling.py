import main as main
import schedule
import time


def post_tasks():
    main.post_tasks('Business', 'public')

schedule.every().day.at("19:18").do(post_tasks)

while 1:
    schedule.run_pending()
    time.sleep(1)
