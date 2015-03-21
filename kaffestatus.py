# coding=utf8
import json
import urllib2
import datetime
import random


class EtaCan:
	"""
	Wrapper class for ETA CAN HTTP API

	"""

	_url = ''
	def __init__(self, url = 'http://user01.eta.lan/infosoffa/1/can.php'):
		self._url = url

	def getResponse(self):
		"""
		Fetch data from CAN API

		"""
		response = urllib2.urlopen(self._url)
		data = json.load(response)
		response.close()
		return data


class CoffeeAnswer:
	"""
	Generate an appropriate response for a given coffee state

	"""

        # for better pythonness this should be represented as an objects with attributes instead
	STATE_BREWING=0
	STATE_AVAILABLE=1
        STATE_MAYBE=2
	STATE_OLD=3

	_BrewingAnswer = [
			'Det bryggs kaffe för fullt!',
			'Snart finns det svart guld i cisternen.',
			'Räddningen är nära, kaffet är på gång!',
			'Det är fritt fram att titta förbi, ty kaffet är snart klart.'
			]
	_CoffieAnswer =  [
			'Visst finns det kaffe! Senast bryggdes det %(antal)s koppar och det var %(tid)ssedan.',
			'Är du sugen på kaffe så kanske det finns något kvar om du har tur, det bryggdes %(antal)s koppar för %(tid)ssedan.',
			'Någon fantastisk människa har bryggt %(antal)s koppar för %(tid)ssedan!'
			]

	_OldCoffieAnswer = [
			'Det var allt ett tag sedan det bryggdes, det finns nog inte kvar och skulle det mot förmodan göra det så gör du nog bättre i att brygga nytt då det är %(tid)s gammalt...',
			'Troligtvis inte.',
			'Om det mot förmodan skulle finnas något kaffe, så gör du nog bäst i att provsmaka först... En ålder på %(tid)sbådar inte gott.',
			'Se: http://www.youtube.com/watch?v=InsspuvAmBs'
			]

        _MaybeAnswer = [
                'Med en stor gnutta tur kan du hinna sno åt dig den sista slurken svart guld',
                'Mjo, mycket möjligt att det finns kaffe'
                ]

	def getAnswer(self, state):
		"""
		Return an answer string containing formatting markup:

		%(antal)s - Number of cups
		%(tid)s - Time since last brewing.

		Parameters:
		state -- state to generate answer for

		Returns:
		string with answer and markup

		"""

		answer = ""
		if state == self.STATE_BREWING:
			answer = random.choice(self._BrewingAnswer)
		elif state == self.STATE_AVAILABLE:
			answer = random.choice(self._CoffieAnswer)
                elif state == self.STATE_MAYBE:
                        answer = random.choice(self._MaybeAnswer)
		elif state == self.STATE_OLD:
			answer = random.choice(self._OldCoffieAnswer)
		else:
			answer = "Bananaaaa"

		return answer

        def guessState(self, timediff, cups, status):
                """
                Return a state based on the time since and number of cups brewed
                and brewing status

                Parameters:
                timediff -- timedelta since last brewed pot
                cups     -- number of cups brewed in last pot
                status   -- status code from coffee pot

                Returns:
                one of STATE_BREWING, STATE_AVAILABLE, STATE_MAYBE, STATE_OLD

                """

                # Status 2 = brewing
                if status == 2: # Coffie is brewing.
                        state = self.STATE_BREWING
                elif cups < 12 and timediff.seconds <= 5400: # Age is less than 1.5 h
                        if timediff.seconds <= 1800:         # Age is less than 0.5 h
                                state = self.STATE_AVAILABLE
                        else:
                                state = self.STATE_MAYBE
                else: # Coffie is most probably old.
                        state = self.STATE_OLD
                return state



if __name__ == '__main__':
        eta_can = EtaCan()
        coffee_data = eta_can.getResponse()
        last_update = datetime.datetime.strptime(coffee_data['coffie_nCups']['last_update'], '%Y-%m-%d %H:%M:%S')

        now = datetime.datetime.now()
        diff =  now-last_update
        diff_hours = diff.seconds / 3600
        diff_mins = (diff.seconds / 60) % 60
        timestr = ""
        if (diff_hours > 0):
        	timestr = timestr + str(diff_hours) + "h "
        if (diff_mins > 0):
        	timestr = timestr + str(diff_mins) + "min "

        coffee_answer = CoffeeAnswer()
        state = coffee_answer.guessState(diff,
                                         coffee_data['coffie_nCups']['value'],
                                         coffee_data['coffie_status']['value'])
        answer = coffee_answer.getAnswer(state)
       	answer = answer % {'antal' : coffee_data['coffie_nCups']['value'], 'tid': timestr}
        print answer
