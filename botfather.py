from slackclient import SlackClient
import re
from wordFilter import WordFilter
import aiml.Kernel


class BotFather:

    def __init__(self, slack_bot_token, bot_id):
        self.slackBotToken = slack_bot_token
        self.botID = bot_id
        self.slackClient = SlackClient(slack_bot_token)
        self.atBot = "<@" + bot_id + ">"
        self.wordFilter = WordFilter()
        self.learned_words = [key([]) for key in self.usernames]

        # Init AIML
        self.kernel = aiml.Kernel()
        self.kernel.learn('botfather.xml')

    def post(self, text, channel):
        return self.slackClient.api_call("chat.postMessage", channel=channel, text=text, as_user=True)

    def get_channel_name(self, channel_id):
        info = self.slackClient.api_call("groups.info", channel=channel_id)
        if info and 'group' in info:
            return info['group']['name']

        return ''

    def parse_slack_output(self, slack_rtm_output):
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                # act upon messages that are not its own
                if output and 'text' in output and 'user' in output and output['user'] != self.botID:
                    self.learning_progress(output['user'], output['text'])
                    self.post(self.kernel.respond(output['text']), output['channel'])

                    # Find myname-othername channels
                    channel = self.get_channel_name(output['channel'])
                    match = re.search(r"([A-Za-z0-9]+)-([A-Za-z0-9]+)", channel)
                    if match:
                        self.direct_message(output['text'], match.group(1), match.group(2))
        return None, None

    def learning_progress(self, user, text):
        """Add user text input to that user's list of learned words,
        if the words are unique and correct
        """
        if WordFilter.filter_text(text) is None:
            for word in text:
                if word not in self.learned_words[user]:
                    self.learned_words[user].append(word)
        n_learned = len(self.learned_words[user])
        return user, n_learned

    def direct_message(self, text, from_user, to_user):
        filtered = self.wordFilter.filter_text(text)
        if filtered is None:
            channel = to_user + '-' + from_user
            self.post(from_user + ": " + text, channel)
        else:
            channel = from_user + '-' + to_user
            text = "Cannot use the word '" + filtered + "'."
            self.post(text, channel)

    def connect(self):
        return self.slackClient.rtm_connect()

    def perform(self):
        self.parse_slack_output(self.slackClient.rtm_read())
