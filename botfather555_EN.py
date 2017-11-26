import os
import time, random
from slackclient import SlackClient
from itertools import combinations


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

roles = ["reporter","tutor","gunnut","escort","gladiator"] # shuffle
roles_assigned = {}

private_msg = {
    "reporter": ["You are the reporter, a bad boy with a reputation for using dirty tricks to get the latest news.",
        "Your methods are not always legal..but that only matters if you get caught, right?", 
        "You have never been to the casino before.",
        "Clue: You have been following Elvis for a story and you know that he was in a relationship with someone who was married."],
    "tutor": ["tutors gotta tute"],
    "gunnut": ["You own several guns, as a true American.",
        "You and your wife are big Elvis fans.",
        "But you saw this this Elvis impersonator before, and think he is terrible.",
        "You have been to several of his other shows and heckle him on and off stage.",
        "You are NOT the murderer.",
        "Clue: You lost your gun at the casino bar last week."],
    "escort": ["You are an escort hired by many of the Starlight Casino's most famous guests.", 
        "You are proud to be high-class, and would never mix with street prostitutes.",
        "Clue: Elvis once brought the Escort to a wedding, and she tried to fool around with him afterwards but he was not interested."],
    "gladiator" : ["You are a recently-fired gladiator, and used to be best friends with Elvis.", 
        "You were previously employed by the casino to entertain the gamblers.", 
        "Elvis revealed to the owner that you were drinking on the job.",
        "One night, very drunk, you told the dancer that planned to stab Elvis in the back (like Brutus stabbed Caesar)."]
}

# instantiate Slack & Twilio clients
#slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
slack_client = SlackClient('xoxb-277472522770-EfeEaV59j5YciorxivClwLeu')

players = []

def get_active_users(channel):
    # check for 5 active users, assign to roles, and send personal messages..
    users = slack_client.api_call("users.list", channel=channel, as_user=True)
    uids = []
    unames = []
    active_uids = []
    active_unames = []
    for u in users["members"]: 
        print(u["id"])
        if not u["is_bot"]:
            uids.append(u["id"])
            unames.append(u["real_name"])
    for u, u_name in zip(uids, unames):
        status = slack_client.api_call("users.getPresence", user=u, channel=channel, as_user=True)
        if status["presence"]=="active":
            active_uids.append(u)
            active_unames.append(u_name)
    return active_uids, active_unames

def assign_active_users(players, channel):
    global roles_assigned
    # send messages to specific user (only works for active users)
    for i, uid in enumerate(players):
        roles_assigned[roles[i]] = uid
        for msg in private_msg[roles[i]]:
            slack_client.api_call("chat.postEphemeral", channel=channel, text=msg, user=uid, as_user=True)
            time.sleep(2)

def handle_command(command, channel):
    """Receives commands directed at the bot and determines if they are
    valid commands. If so, then acts on the commands. If not, asks for clarification.
    """
    global GAME_STARTED, lang_tips_ind, tips_ind, players
    if not GAME_STARTED:
        if command.startswith(START_GAME):
            players, playernames = get_active_users(channel)
            print(players) # need 5...
            assign_active_users(players, channel)

            for i in intro:
                slack_client.api_call("chat.postMessage", channel=channel, text=i, as_user=True)
                time.sleep(5)
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
