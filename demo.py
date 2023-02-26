import json
from todoist.api import TodoistAPI
from matplotlib import pyplot as plt

with open("context.json") as json_file:
    creds = json.load(json_file)

api = TodoistAPI(creds['token'])
api.sync()

for project in api.state['projects']:
    print(project['name'])

events = api.activity.sync()["events"]

event_dict = {}
for e in events:
    if e['event_type'] == 'completed':
        date_strip = e['event_date'].split('T')[0]
        value = event_dict.get(date_strip)
        if value == None:
            event_dict.update({date_strip: 1})
        else:
            event_dict.update({date_strip: value + 1})

plt.plot(event_dict.values())
plt.show()
