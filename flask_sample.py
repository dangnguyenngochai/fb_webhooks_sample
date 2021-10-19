from flask import Flask
import json

app = Flask(__name__)

@app.route("/comments_handler")
def comment_handler():
    payload = {"msg": "The monkey is having his fun"}
    return json.dumps(payload)
