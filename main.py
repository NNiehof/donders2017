from slackclient import SlackClient
import time

# Hackathon-style tokens!
SLACK_BOT_TOKEN = 'xoxb-277615982901-7g14MbeJ71m1t3joJuOfnRJl'
BOT_NAME = 'botfather'

# Hackathon style!
BOT_ID = "U85J3UWSH"

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

slack_client = SlackClient(SLACK_BOT_TOKEN)

slack_client.api_call("chat.postMessage", channel='#general', text="Hello Cruel World!", as_user=True)

def handle_command(command, channel):
	"""
		Receives commands directed at the bot and determines if they
		are valid commands. If so, then acts on the commands. If not,
		returns back what it needs for clarification.
	"""
	response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + "* command with numbers, delimited by spaces."
	if command.startswith(EXAMPLE_COMMAND):
		response = "Sure...write some more code then I can do that!"
	print(command)
	slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
	"""
		The Slack Real Time Messaging API is an events firehose.
		this parsing function returns None unless a message is
		directed at the Bot, based on its ID.
	"""
	output_list = slack_rtm_output
	if output_list and len(output_list) > 0:
		for output in output_list:
			if output and 'text' in output and AT_BOT in output['text']:
				# return text after the @ mention, whitespace removed
				return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
	return None, None

READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
if slack_client.rtm_connect():
	print("StarterBot connected and running!")
	while True:
		command, channel = parse_slack_output(slack_client.rtm_read())
		if command and channel:
			handle_command(command, channel)
		time.sleep(READ_WEBSOCKET_DELAY)
else:
	print("Connection failed. Invalid Slack token or bot ID?")