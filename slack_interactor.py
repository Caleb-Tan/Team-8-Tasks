import requests
import json

# urls and header
webhook_url = 'https://hooks.slack.com/services/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' # private test dm
webhook_url_business = 'https://hooks.slack.com/services/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' # business channel
header = {'content-type': 'application/json'}

def post_tasks(data, visibility):
    ongoing = "*Ongoing:*\n"
    overdue = "*Overdue:*\n"
    completed = "*Completed:*\n"
    ongoing_counter = 0
    overdue_counter = 0
    completed_counter = 0

    for task in data:
        if task[3] == 0:
            ongoing += task[1] + " | " + task[2] + "\n"
            ongoing_counter += 1
        if task[3] == 1:
            completed += task[1] + " | " + task[2] + "\n"
            completed_counter += 1
        if task[3] == 2:
            overdue += task[1] + " | " + task[2] + "\n"
            overdue_counter += 1
        
    if ongoing_counter == 0:
        ongoing += "You have no ongoing tasks.\n"
    if overdue_counter == 0:
        overdue += "You have no overdue tasks.\n"
    if completed_counter == 0:
        completed += "You have no completed tasks.\n"

    text = ongoing + overdue + completed
    if visibility == 'visible':
        payload = {'text' : text}
        results = requests.post(webhook_url_business, json.dumps(payload), headers=header)
    elif visibility == 'ephemeral':
        return text

