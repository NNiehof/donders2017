import os
from flask import Flask, request
from slackclient import SlackClient

# Never do this in real life please
# alwasy host your data off of a coded repository
client_id = '66907352454.277487803284'
client_secret = 'e9adbe50a901ab7f1d52bf0c317ff9c4'
token = '4RFAStXyHjShkcS1rtHzQGaIcd'

oauth_scope = 'chat:write:bot'

app = Flask(__name__)

@app.route("/begin_auth", methods=["GET"])
def pre_install():
  return '''
      <a href="https://slack.com/oauth/authorize?scope={0}&client_id={1}">
          Add to Slack
      </a>
  '''.format(oauth_scope, client_id)


@app.route("/finish_auth", methods=["GET", "POST"])
def post_install():
    # Retrieve the auth code from the request params
    auth_code = request.args['code']

    # An empty string is a valid token for this request
    sc = SlackClient("")

    # Request the auth tokens from Slack
    auth_response = sc.api_call(
    "oauth.access",
    client_id=client_id,
    client_secret=client_secret,
    code=auth_code
    )

    # Save the bot token to an environmental variable or to your data store
    # for later use
    os.environ["SLACK_USER_TOKEN"] = auth_response['access_token']
    os.environ["SLACK_BOT_TOKEN"] = auth_response['bot']['bot_access_token']

    # Don't forget to let the user know that auth has succeeded!
    return "Auth complete!"

def __main__():
    print(pre_install())
    code = input("Just press enter")
    print(post_install())