from botfather import BotFather
from botfather_commander import BotfatherCommander
import time

# Hackathon-style tokens and IDs!
SLACK_BOT_TOKEN = 'xoxb-277615982901-QpYOuR6ck9co1gled5dIjpIm'
BOT_ID = "U85J3UWSH"

READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose

# ..and so began the reign of the Botfather.
botFather = BotFather(SLACK_BOT_TOKEN, BOT_ID)
botFatherCmd = BotfatherCommander(SLACK_BOT_TOKEN, BOT_ID)

if botFather.connect() and botFatherCmd.connect():
    while True:
        botFather.perform()
        botFatherCmd.perform()
        time.sleep(READ_WEBSOCKET_DELAY)
else:
    print("Connection failed. Invalid Slack token or bot ID?")
