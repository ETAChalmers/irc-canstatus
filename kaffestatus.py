# coding=utf8
import json
import urllib2
import datetime
import random

url = 'http://localhost/can.php'
response = urllib2.urlopen(url)
data = json.load(response)
response.close()

answer = ""

BrewingAnswer = [
		'Det bryggs kaffe för fullt!',
		'Snart finns det svart guld i cisternen.', 
		'Räddningen är nära, kaffet är på gång!', 
		'Det är fritt fram att titta förbi, ty kaffet är snart klart.'
		]
CoffieAnswer =  [
		'Visst finns det kaffe! Senast bryggdes det %(antal)s koppar och det var %(tid)ssedan.',
		'Är du sugen på kaffe så kanske det finns något kvar om du har tur, det bryggdes %(antal)s koppar för %(tid)ssedan.'
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
if data['coffie_status']['value'] == 2:
	answer = random.choice(BrewingAnswer)
elif data['coffie_nCups']['value'] < 12:
	answer = random.choice(CoffieAnswer) % {'antal' : data['coffie_nCups']['value'],
						'tid': timestr
						}
print answer
