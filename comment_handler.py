# Self-note: the comments should be made in a more standard format


from flask import Flask, config
from flask import request

import json
import facebook
import helper
import requests

app = Flask(__name__)

config = helper.get_configuration()


def verfication():
    hub_challenge = request.args.get('hub.challenge', '')
    hub_verify_token = request.args.get('hub.verify_token', '')
    if hub_verify_token == config['verify_token']:
        return hub_challenge
    else:
        return None

def bot_answer_this(comment_msg):
    # This function should fetch the reponse from NLU module
    bot_response = "This is bot response for " + comment_msg
    return bot_response

def auto_reply(comment_id, bot_response):
    # This function will send the reply to facebook
    url = 'https://graph.facebook.com/v12.0/' + comment_id + '/comments'
    payload = {
        'message': bot_response
    }
    reponse = requests.post(url, json=payload)
    print(reponse)
    return

def is_new_comments(change):
    # 'change' param should contain info regarding the change made (element in changes list)
    value = change.get('value')
    if value.get('item', False) == 'comment' and value.get('verb', False) == 'add' and value.get('comment_id', False):
        return True
    else:
        return False

def is_new_live_comments():
    return

@app.route("/webhooks", methods=["GET", "POST"])
def webhooks():
    if request.method == "GET":
        if request.args.get('hub.challenge', '') and request.args.get('hub.verify_token', ''):
            raw_response = verfication()
            return raw_response
        else:
            return None
    elif request.method == "POST":
        # Facebook webhooks send events in batch, the 'entry' field is a list of interest objects that webhooks are configured to send notifications for
        events = request.get_json()['entry']
        # field 'changes' contains list of changes made on the page: comments, posts, etc
        for event in events:
            data = dict(event)
            changes = data.get('changes', [])
            for change in changes:
                # the 'changes' <list> parameter is expected to contain infomation about the changes made: feed or message
                if change.get('field') == 'feed': 
                    if is_new_comments(change):
                        value = change.get('value')
                        comment_id = value.get('comment_id')
                        comment_msg = value.get('message')

                        bot_response = bot_answer_this(comment_msg)
                        auto_reply(comment_id, bot_response)
                    else:
                        pass

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

# The following session is for testing only
@app.route("/comments_handler")
def comments_handler():
    payload = {"msg": "The monkey is having his fun :)"}
    return json.dumps(payload)


def test_facebook():
    print('Hello world')
    print(facebook.__version__)



