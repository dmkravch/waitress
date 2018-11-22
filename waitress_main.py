from flask import Flask, request, render_template
import sys, json, requests
import datetime
import time
import requests
from ciscosparkapi import CiscoSparkAPI, Webhook
import string
import random

app = Flask(__name__)

at = "Y2Q5NGNjOTctN2I3Yi00YjhmLWJmYTYtYzIyY2U0NzIwNGE1NjU3ZDAzNGItZTMy"
spark_api = CiscoSparkAPI(at)
accesstoken = "Bearer " + at
bot_id = "Y2lzY29zcGFyazovL3VzL1BFT1BMRS8yYWZjYzc2Ny1iOGZmLTQ4YTgtOWExYy0yNGYxMDFmZTA5Zjc"
webhook_id = "Y2lzY29zcGFyazovL3VzL1dFQkhPT0svZWZlNjdhOWItZTA2OS00MDg5LWJhN2UtZGU1MzA2ODBkYmIz"
headers = {
    'Authorization': accesstoken,
    'Content-Type': "application/json; charset=utf-8",
    'Cache-Control': "no-cache"
}

hello_message = "Hello!"


# functions:

def get_message(msgid, accesstoken):
    url = "https://api.ciscospark.com/v1/messages/" + msgid
    headers = {
        'Authorization': accesstoken}
    obtained = requests.get(url, headers=headers)
    # print(obtained)
    dict = json.loads(obtained.text)
    dict['statuscode'] = str(obtained.status_code)
    return dict


def remove_bots_display_name(message, accesstoken):
    # get display name of the bot
    url = "https://api.ciscospark.com/v1/people/me"
    headers = {
        'Authorization': accesstoken}
    obtained = requests.get(url, headers=headers)
    dict = json.loads(obtained.text)
    name = dict['displayName']
    # check if message starts with the display name, and remove display name
    if (message.startswith(name) == True):
        message = (message[(len(name) + 1):])
    return message


@app.route("/", methods=['POST'])
def handle_message():
    data = request.get_json()
    personid = data["data"]["personId"]
    if personid == bot_id:
        return 'OK'
    else:
        if data["id"] != webhook_id:
            return 'ok'
        else:
            msgid = data["data"]["id"]
            roomId = data["data"]["roomId"]
            txt = get_message(msgid, accesstoken)
            message = txt['text']
            user_email = data["data"]["personEmail"]
            message = remove_bots_display_name(message, accesstoken)
            if message == message == "hello" or message == "hi" or message == "hi!":
                spark_api.messages.create(roomId, text=hello_message, markdown=hello_message)
            else:
                spark_api.messages.create(roomId,
                                          text='Sorry, the space that you would like to join is no longer active or does not exist.')


# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='ec2-52.28.189.59.eu-west-1.compute.amazonaws.com', port=8080)

