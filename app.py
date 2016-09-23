import os
import sys
import json

import requests
from flask import Flask, request

VERIFY_TOKEN = '1122332211'
PAGE_ACCESS_TOKEN = 'EAACsJddva3cBAHBDXTvYuHnMPBRZBZCdqsx8AbskK1LUK2G3t3nNCibShZAiZBPaeHTKunmZCySycmrnoVIBtOr1jQzAkaW58lIbl0xVqTbsm2yKwgUhbLEcgTIdViEbaGgUCo3n2c8nsZAfrq0kTfqCrwOyO4rUyGXOqShwsUkgZDZD'


app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():

    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    data = request.get_json()

    response_text = "initial dummy text"

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  

                    # print '+++++++++++++++++'
                    # print 'NEW MESSAGE!!!!!!!'
                    # print '+++++++++++++++++'
                    # print messaging_event
                    # print '+++++++++++++++++'
                    
                    if checkJson(messaging_event) == "image":

                        sender_id = messaging_event["sender"]["id"]        
                        recipient_id = messaging_event["recipient"]["id"]
                        image_url = messaging_event["message"]["attachments"][0]["payload"]["url"]
                        response_text = "got an image: " + image_url

                    elif checkJson(messaging_event) == "text":

                        sender_id = messaging_event["sender"]["id"]        
                        recipient_id = messaging_event["recipient"]["id"]
                        incoming_text = messaging_event["message"]["text"]

                        response_text = "got a text:" + incoming_text

                    send_message(sender_id, response_text)

                if messaging_event.get("delivery"):  
                    pass

                if messaging_event.get("optin"):  
                    pass

                if messaging_event.get("postback"):  
                    pass

    return "ok", 200


def checkJson(jsonContents):
    msg_type = 'image' if "attachments" in jsonContents["message"] and jsonContents["message"]["attachments"][0]["type"] == "image" else 'text'
    return msg_type

def send_message(recipient_id, message_text):
    params = {
    "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

if __name__ == '__main__':
    app.run(debug=True)
