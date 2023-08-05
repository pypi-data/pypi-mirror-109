import requests
import json
import sys

def incomingWebhook(url, message):
	try:
		data = {
				'blocks': [
				{
					'type': "section",
					'text': {
						'type': 'mrkdwn',
						'text': message
					}
				},
				{
                        'type': 'divider'
                }
			]
		}

		requests.post(url, headers={ 'Content-type': 'application/json' }, data=json.dumps(data))
	except Exception as e:
        print(e)
