# -*- coding: utf-8 -*-

import os
import sys
import json
import time

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
                        #response_text = "Super, danke! Ich werde jetzt mal auswerten, was Dir zusteht... "
                        time.sleep(5)
                        response_text = "Also Manfred, noch einmal vielen Dank! Du bekommst laut aktuellen Stand eine Altersrente von EUR 1.185,58. Wusstest Du, dass bei Deinem geplanten Altersrenteneintritt 2032 bei einer Inflationsrate von 2 % nur noch einem heutigen Wert von EUR 523,74 entspricht? Möchtest Du mehr wissen?"

                    elif checkJson(messaging_event) == "text":

                        sender_id = messaging_event["sender"]["id"]        
                        recipient_id = messaging_event["recipient"]["id"]
                        incoming_text = messaging_event["message"]["text"]

                        if incoming_text.lower().startswith('hallo') or incoming_text.lower().startswith('hi'):
                            response_text = "Hi! Ich bin der Allianz Renten- scanner! Schick mir Deine Rentenbescheinigung!"
                        elif incoming_text.lower().startswith('ja'):
                            response_text = "OK, gerne. In den von den offiziellen Stellen verschickten Renteninformationen fehlen die Angaben zum realen Geldwert der erreichbaren Rente. Darauf solltest Du immer achten, wenn Du diese Dokumente liest. Willst Du mehr zum Thema Inflation wissen? Oder soll ich Dich mit einem Berater verknüpfen?"
                        elif incoming_text.lower().startswith('berater') or incoming_text.lower().startswith('ein berater'):
                            response_text = "Super, willst Du einen Vertreter in Deiner Nähe kennenlernen oder direkt von uns betreut werden?"
                        elif incoming_text.lower().startswith('vertreter') or incoming_text.lower().startswith('ein vertreter'):
                            response_text = "Hier sind zwei Agenturen in Deiner Nähe. Wir leiten Deine Kontaktdaten weiter, Sie melden sich bei Dir zur Terminvereinbarung!"
                        elif incoming_text.lower().startswith('nein'):
                            response_text = "OK"

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
