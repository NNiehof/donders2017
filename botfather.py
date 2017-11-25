from slackclient import SlackClient


class BotFather:

	def __init__(self, slack_bot_token, bot_id):
		self.slackBotToken = slack_bot_token
		self.botID = bot_id
		print(bot_id)
		self.slackClient = SlackClient(slack_bot_token)
		self.atBot = "<@" + bot_id + ">"

	def handle_command(self, command, channel):
		self.slack_client.api_call("chat.postMessage", channel=channel, text="Well I don't give a shit.", as_user=True)

	def parse_slack_output(self, slack_rtm_output):
		output_list = slack_rtm_output
		print(output_list)
		if output_list and len(output_list) > 0:
			for output in output_list:
				if output and 'text' in output and self.atBot in output['text']:
					# return text after the @ mention, whitespace removed
					return output['text'].split(self.atBot)[1].strip().lower(), output['channel']
		return None, None

	def connect(self):
		return self.slackClient.rtm_connect()

	def perform(self):
		command, channel = self.parse_slack_output(self.slackClient.rtm_read())
		if command and channel:
			self.handle_command(command, channel)