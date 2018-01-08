from slackclient import SlackClient
from pyee import EventEmitter
import requests
import json
import time


# header
header = {'content-type': 'application/json'}
# tokens
SLACK_VERIFICATION_TOKEN = 'RubANxonQSPFjp0u125Clrzi'
SLACK_BOT_TOKEN = 'xoxb-295366353890-BS36I6qZm2QI77ZOt166AhGl'
slack_client = SlackClient(SLACK_BOT_TOKEN)

"""
post_tasks() returns a payload of text that is then returned as an ephemeral message
"""
def post_tasks(data):
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
        print task
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



"""
handle_message() handles dm messages that are sent to the bot
"""
