from slackclient import SlackClient
from firebase_interactor import Firebase_Interactor
from pyee import EventEmitter
import requests
import json
import time
import sys

sys.dont_write_bytecode = True


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
    msg = message.get('text').lower()
    userid = message.get('user')
    username = convert_unicode(sc.api_call('users.info', user=userid)).get('user').get('profile').get('display_name')
    text = None

    if "tasks" in msg or "task" in msg:
        ret_data = fb.display_list('Business', False)
        ret_data = return_tasks(filter(lambda x:username in [names.strip() for names in x[2].split(',')], ret_data))
        text = ret_data
    elif "hello" in msg or "hi" in msg or "hey" in msg:
        text = "Hello <@" + userid + ">! What's up?"
    elif "no u" in msg:
        text = "no u"
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
            ongoing += task[1] + " | " + task[4] + " - " + task[2] + "\n"
            ongoing_counter = 1
        if task[3] == 1:
            completed += task[1] + " | " + task[4] + " - " + task[2] + "\n"
            completed_counter = 1
        if task[3] == 2:
            overdue += task[1] + " | " + task[4] + " - " + task[2] + "\n"
            overdue_counter = 1
        
    if ongoing_counter == 0:
        ongoing += "You have no ongoing tasks.\n"
    if overdue_counter == 0:
        overdue += "You have no overdue tasks.\n"
    if completed_counter == 0:
        completed += "You have no completed tasks.\n"

    text = ongoing + overdue + completed + "\nAs always, the task app website can be found <http://server.palyrobotics.com:7000|here>."

    return text

def remind_tasks(subteam):
    ret_data = fb.display_list(subteam, False)
    members = convert_unicode(sc.api_call('users.list')).get('members')
    users = []
    for task in ret_data:
        users.extend([names.strip() for names in task[2].split(',')])
    
    for user in set(users):
        for member in members:
            if member.get('profile').get('display_name') == user:
                users_tasks = return_tasks(filter(lambda x:user in [names.strip() for names in x[2].split(',')], ret_data))
                dm_id = convert_unicode(sc.api_call('im.open', user=member.get('id'), return_im=True)).get('channel').get('id')
                text = "Hi! Here are your tasks for today:\n" + users_tasks
                sc.api_call('chat.postMessage', channel=dm_id, text=text, as_user=True)
    

def convert_unicode(input):
    if isinstance(input, dict):
        return {convert_unicode(key): convert_unicode(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert_unicode(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

