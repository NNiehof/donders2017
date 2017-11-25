from botfather import BotFather
import time

# Hackathon-style tokens and IDs!
SLACK_BOT_TOKEN = 'xoxb-277615982901-7g14MbeJ71m1t3joJuOfnRJl'
BOT_ID = "U85J3UWSH"

READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose

# ..and so began the reign of the Botfather.
botFather = BotFather(SLACK_BOT_TOKEN, BOT_ID)

if botFather.connect():
	print("StarterBot connected and running!")
	while True:
		botFather.perform()
		time.sleep(READ_WEBSOCKET_DELAY)
else:
	print("Connection failed. Invalid Slack token or bot ID?")