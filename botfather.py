from slackclient import SlackClient
import re
from wordFilter import WordFilter
import language_check


class BotFather:
    def __init__(self, slack_bot_token, bot_id):
        self.slackBotToken = slack_bot_token
        self.botID = bot_id
        self.slackClient = SlackClient(slack_bot_token)
        self.usernames = self.slackClient.api_call("users.list")
        self.atBot = "<@" + bot_id + ">"
        self.wordFilter = WordFilter()
        self.learned_words = {key: [] for key in self.usernames}
        # Init language check
        self.language = language_check.LanguageTool('it-IT')

    def post(self, text, channel):
        return self.slackClient.api_call("chat.postMessage", channel=channel, text=text, as_user=True)

    def get_channel_name(self, channel_id):
        info = self.slackClient.api_call("groups.info", channel=channel_id)
        if info and 'group' in info:
            return info['group']['name']
        
        return 'Untitled Document 1'

    def parse_slack_output(self, slack_rtm_output):
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                # act upon messages that are not its own
                if output and 'text' in output and 'user' in output and output['user'] != self.botID:
                    user, self.n_learned = self.learning_progress(output['user'], output['text'])
                    self.post(self.kernel.respond(output['text']), output['channel'])
                    self.learning_progress(output['user'], output['text'])

                    # Language check
                    correction = self.check_language(output['text'])
                    if correction is not None:
                        self.post(correction, output['channel'])

                    # Find myname-othername channels
                    channel = self.get_channel_name(output['channel'])
                    match = re.search(r"([A-Za-z0-9]+)-([A-Za-z0-9]+)", channel)
                    if match:
                        self.direct_message(output['text'], match.group(1), match.group(2))

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

    def check_language(self, text):
        txt = text.title()
        matches = self.language.check(txt)
        if len(matches) > 0:
            correction = language_check.correct(txt, matches)
            for match in matches:
                if len(match.replacements) > 0:
                    return "Did you mean '" + correction + "'?"
            return "Unclear what you mean by that."
        return None

    def direct_message(self, text, from_user, to_user):
        filtered = self.wordFilter.filter_text(text)
        if filtered is None:
            # if all words are allowed, pass the message along to other user
            channel = to_user + '-' + from_user
            self.post(from_user + ": " + text, channel)
            channel2 = from_user + '-' + to_user
            self.post("You have learned {} words so far!".format(
                self.n_learned), channel2)
        else:
            # if disallowed words present, notify the sender
            channel = from_user + '-' + to_user
            text = "Cannot use the word '" + filtered + "'."
            self.post(text, channel)

    def connect(self):
        return self.slackClient.rtm_connect()

    def perform(self):
        self.parse_slack_output(self.slackClient.rtm_read())
