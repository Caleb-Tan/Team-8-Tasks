from slackclient import SlackClient
from firebase_interactor import Firebase_Interactor
from pyee import EventEmitter
import requests
import json
import time


# header
header = {'content-type': 'application/json'}
# tokens 
SLACK_BOT_TOKEN = 'xoxb-295366353890-BS36I6qZm2QI77ZOt166AhGl'
sc = SlackClient(SLACK_BOT_TOKEN)
fb = Firebase_Interactor()

def handle_event(event_data):
    """
    handle_event() handles dm messages that are sent to the bot
    """
    # define variable of data
    message = event_data.get('event')
    channel = message.get('channel')
    msg = message.get('text')
    userid = message.get('user')
    username = convert_unicode(sc.api_call('users.info', user=userid)).get('user').get('name')
    text = None

    if "tasks" in msg or "task" in msg:
        text = "These are your tasks:"
        ret_data = fb.display_list('Business', False)
        filtered_ret_data = return_tasks(filter(lambda x:x[2]==username, ret_data))
        text = filtered_ret_data
    elif "hello" in msg or "hi" in msg or "hey" in msg:
        text = "Hello <@" + userid + ">! What's up?"
    else:
        text = 'Sorry I do not know what that command means. Try "tasks" to list your tasks.'

    sc.api_call('chat.postMessage', channel=channel, text=text, as_user=True)

def return_tasks(data):
    """
    post_tasks() returns a payload of text that is then returned as an ephemeral message
    """
    ongoing = "*Ongoing:*\n"
    overdue = "*Overdue:*\n"
    completed = "*Completed:*\n"
    ongoing_counter = 0
    overdue_counter = 0
    completed_counter = 0

    """
    task[3] - status
    task[2] - text
    task[1] - date
    """
    for task in data:   
        if task[3] == 0:
            ongoing += task[1] + " | " + task[2] + " - " + task[4] + "\n"
            ongoing_counter += 1
        if task[3] == 1:
            completed += task[1] + " | " + task[2] + " - " + task[4] + "\n"
            completed_counter += 1
        if task[3] == 2:
            overdue += task[1] + " | " + task[2] + " - " + task[4] + "\n"
            overdue_counter += 1
        
    if ongoing_counter == 0:
        ongoing += "You have no ongoing tasks.\n"
    if overdue_counter == 0:
        overdue += "You have no overdue tasks.\n"
    if completed_counter == 0:
        completed += "You have no completed tasks.\n"

    text = ongoing + overdue + completed + "\nAs always, the task app website can be found <http://server.palyrobotics.com:7000|here>."

    return text

def convert_unicode(input):
    if isinstance(input, dict):
        return {convert_unicode(key): convert_unicode(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert_unicode(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input