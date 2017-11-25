import os
import time, random
from slackclient import SlackClient


# starterbot's ID as an environment variable
#BOT_ID = os.environ.get("BOT_ID")
BOT_ID = "U85DWFCNN"

# constants
AT_BOT = "<@" + BOT_ID + ">"
HELP_LANGUAGE = "help language"
HELP_OTHER = "help detect"
START_GAME = "start"
# accuse?

GAME_STARTED = False

intro = ["Welcome to the Starlight Casino bar! Tonight we have the best Elvis impersonator in Las Vegas. Please enjoy the show.",
    "As the show starts--BANG!--a loud gun shot is heard. The curtain comes up, and Elvis falls over. The casino's bar doors slam shut.]",
    "Everyone here is now a suspect to the murder of the Elvis impersonator. Please talk to everyone, and help me find out who the murderer is.",
    "After 15 minutes, I will ask who you think is the murderer. If you want help, please type @Botfather help language",
    "Try to find out 1) WHO is the murderer, 2) WHY did she/he commit the murder, and 3) HOW did they commit the murder."]

lang_tips = ["Try asking who has been to the casino before: 'Have you been to the casino before?'",
    "Try to find out who is married: 'Are you married?'",
    "Find out who has a gun: 'Do you have guns?'"]

tips = ["Very few of us are what we seem. -Agatha Christie",
    "When you have eliminated the impossible, whatever remains, however improbable, must be the truth. -Sherlock Holmes",
    "Good advice is always certain to be ignored, but that's no reason not to give it. -Agatha Christie",
    "Just when I thought I was out, they pull me back in.",
    "I'm going to make him an offer he can't refuse.",
    "Revenge is a dish best served cold."]

lang_tips_ind = 0
tips_ind = 0

# instantiate Slack & Twilio clients
#slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
slack_client = SlackClient('xoxb-277472522770-EfeEaV59j5YciorxivClwLeu')

def handle_command(command, channel):
    """Receives commands directed at the bot and determines if they are
    valid commands. If so, then acts on the commands. If not, asks for clarification.
    """
    global GAME_STARTED, lang_tips_ind, tips_ind
    if not GAME_STARTED:
        if command.startswith(START_GAME):
            # check for 5 active users, assign to roles, and send personal messages..
            for i in intro:
                slack_client.api_call("chat.postMessage", channel=channel, text=i, as_user=True)
                time.sleep(7)
            GAME_STARTED = True
        else:
            response = "Sorry? Try starting a game ('start game')."
            slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
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
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Starlight Casino (botfather555) connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")