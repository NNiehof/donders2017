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

intro = ["Benvenuti allo Starlight Casinò! Stasera abbiamo con noi il miglior sosia di Elvis di Las Vegas. Godetevi lo spettacolo.",
    "Appena lo spettacolo inizia, si sente un forte sparo. Il sipario di alza, ed Elvis cade. La porta del casinò sbatte.",
    "Tutti i presenti sono ora sospettati dell'omicidio del sosia di Elvis. Parlate tra di voi, e aiutatemi a capire chi è l'assassino.",
    "Dopo 15 minuti, vi chiederò chi pensate sia l'assassino. Se hai bisogno di aiuto, scrivi @botfather help",
    "Cerca di capire 1) CHI è l'assassino/a, 2) PERCHE' ha ucciso e 3) COME ha commesso l'omicidio."]

lang_tips = ["Try asking who has been to the casino before: 'Sei stato al casinò prima d'ora?'",
    "Try to find out who is married: 'Sei sposato?'",
    "Find out who has a gun: 'Hai pistole?'"]

tips = ["Solo pochi tra noi sono quello che sembrano. -Agatha Christie",
    "Una volta che hai eliminato l'impossibile, quel che rimane, per quanto improbabile, dev'essere la verità. -Sherlock Holmes",
    "Un buon consiglio sarà quasi certamente ignorato, ma non c'è motivo di non darlo. -Agatha Christie",
    "Proprio quando pensavo di esserne fuori, mi tirano di nuovo in mezzo.",
    "Gli farò una proposta che non può rifiutare.",
    "La vendetta è un piatto da servire freddo."]

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
    "gunnut": ["Possiedi diverse pistole.",
        "Tu e tua moglie siete grandi fan di Elvis.",
        "Ma tu hai visto questo sosia di Elvis e pensi che sia pessimo.",
        "Hai assistito ad altri suoi spettacoli e hai manifestato l'hai fischiato mentre era sul palco e a spettacolo finito.",
        "NON sei l'assassino.",
        "Indizio: Hai perso la tua pistola al casinò la scorsa settimana."],
    "escort": ["Intrattieni alcuni tra i più stimati ospiti del Starlight Casino.", 
        "Sei orgogliosa di essere una di alto bordo, e non ti mischieresti mai alle battone.",
        "Indizio: una volta Elvis ha portato la Escort a un matrimonio, e lei dopo ci aveva provato con lui, ma lui non era interessato."],
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
    active_uids = []
    for u in users["members"]: 
        print u["id"]
        if not u["is_bot"]:
            uids.append(u["id"])
    for u in uids:
        status = slack_client.api_call("users.getPresence", user=u, channel=channel, as_user=True)
        if status["presence"]=="active":
            active_uids.append(u)
    return active_uids

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
            players = get_active_users(channel)
            print players # need 5...
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