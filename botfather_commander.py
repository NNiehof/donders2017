import time
from slackclient import SlackClient

from story_it import intro, lang_tips, tips, roles, private_msg

# constants
HELP_LANGUAGE = "help language"
HELP_OTHER = "help detect"
START_GAME = "start"

GAME_STARTED = False


class BotfatherCommander:

    lang_tips_ind = 0
    tips_ind = 0
    roles_assigned = {}

    def __init__(self, slack_api_key, bot_id):
        self.botID = bot_id
        self.atBot = "<@" + bot_id + ">"
        self.slack_client = SlackClient(slack_api_key)

    players = []

    def get_active_users(self, channel):
        users = self.slack_client.api_call("users.list", channel=channel, as_user=True)
        uids = []
        active_uids = []
        for u in users["members"]:
            if not u["is_bot"]:
                uids.append(u["id"])
        for u in uids:
            status = self.slack_client.api_call("users.getPresence", user=u, channel=channel, as_user=True)
            if status["presence"]=="active":
                active_uids.append(u)
        return active_uids

    def assign_active_users(self, players, channel):
        # send messages to specific user (only works for active users)
        for i, uid in enumerate(players):
            self.roles_assigned[roles[i]] = uid
            for msg in private_msg[roles[i]]:
                self.slack_client.api_call("chat.postEphemeral", channel=channel, text=msg, user=uid, as_user=True)

    def handle_command(self, command, channel):
        """Receives commands directed at the bot and determines if they are
        valid commands. If so, then acts on the commands. If not, asks for clarification.
        """
        global GAME_STARTED, lang_tips_ind, tips_ind, players
        if not GAME_STARTED:
            if command.startswith(START_GAME):
                players = self.get_active_users(channel)
                self.assign_active_users(players, channel)

                for i in intro:
                    self.slack_client.api_call("chat.postMessage", channel=channel, text=i, as_user=True)
                    time.sleep(5)
                GAME_STARTED = True
            else:
                response = "Sorry? Try starting a game ('start game')."
                self.slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        else:
            if command.startswith(HELP_LANGUAGE):
                response = lang_tips[lang_tips_ind]
                if lang_tips_ind < len(lang_tips):
                    lang_tips_ind += 1
            elif command.startswith(HELP_OTHER):
                response = tips[tips_ind]
                if tips_ind < len(tips):
                    tips_ind +=1
            else:
                response = "Sorry, I don't understand. Try '" + HELP_LANGUAGE + "' or '" + HELP_OTHER # or accuse?
            self.slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    def parse_slack_output(self, slack_rtm_output):
        """
            The Slack Real Time Messaging API is an events firehose.
            this parsing function returns None unless a message is
            directed at the Bot, based on its ID.
        """
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and self.atBot in output['text']:
                    # return text after the @ mention, whitespace removed
                    return output['text'].split(self.atBot)[1].strip().lower(), \
                           output['channel']
        return None, None

    def perform(self):
        command, channel = self.parse_slack_output(self.slack_client.rtm_read())
        if command and channel:
            self.handle_command(command, channel)

    def connect(self):
        if self.slack_client.rtm_connect():
            print("Starlight Casino (botfather555) connected and running!")
            return True
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
            return False
