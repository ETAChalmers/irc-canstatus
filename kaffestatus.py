# coding=utf8
import json
import urllib2
import datetime
import random

url = 'http://user01.eta.lan/infosoffa/1/can.php'
response = urllib2.urlopen(url)
data = json.load(response)
response.close()

answer = ""

# Format reference:
#   %(antal)s - Number of cups
#   %(tid)s - Time since last brewing.

BrewingAnswer = [
    'Det bryggs kaffe för fullt!',
    'Snart finns det svart guld i cisternen.', 
    'Räddningen är nära, kaffet är på gång!', 
    'Det är fritt fram att titta förbi, ty kaffet är snart klart.'
]

CoffieAnswer =  [
    'Visst finns det kaffe! Senast bryggdes det %(antal)s koppar och det var %(tid)ssedan.',
    'Är du sugen på kaffe så kanske det finns något kvar om du har tur, det bryggdes %(antal)s koppar för %(tid)ssedan.',
    'Någon fantastisk människa har bryggt %(antal)s koppar för %(tid)ssedan!'
]

OldCoffieAnswer = [
    'Det var allt ett tag sedan det bryggdes, det finns nog inte kvar och skulle det mot förmodan göra det så gör du nog bättre i att brygga nytt då det är %(tid)s gammalt...',
    'Troligtvis inte.',
    'Om det mot förmodan skulle finnas något kaffe, så gör du nog bäst i att provsmaka först... En ålder på %(tid)sbådar inte gott.',
    'Se: http://www.youtube.com/watch?v=InsspuvAmBs'
]

last_update = datetime.datetime.strptime(data['coffie_nCups']['last_update'], '%Y-%m-%d %H:%M:%S')
now = datetime.datetime.now()
diff =  now-last_update
diff_hours = diff.seconds / 3600
diff_mins = (diff.seconds / 60) % 60
timestr = ""

if (diff_hours > 0):
    timestr = timestr + str(diff_hours) + "h "
if (diff_mins > 0):
    timestr = timestr + str(diff_mins) + "min "

# Status 2 = brewing
if data['coffie_status']['value'] == 2: # Coffie is brewing.
    answer = random.choice(BrewingAnswer)
elif data['coffie_nCups']['value'] < 12 and diff.seconds <= 5400: # Age is less than 1.5h.
    answer = random.choice(CoffieAnswer) % {
        'antal' : data['coffie_nCups']['value'],
        'tid': timestr
        }
else: # Coffie is most probably old.
    answer = random.choice(OldCoffieAnswer) % {
        'antal' : data['coffie_nCups']['value'],
        'tid': timestr
        }

print answer
