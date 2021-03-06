# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request

from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

slack_token = ""
slack_client_id = ""
slack_client_secret = ""
slack_verification = ""
sc = SlackClient(slack_token)


url = "https://us.soccerway.com/national/england/premier-league/20182019/regular-season/r48730/?ICID=SN_01_01"
soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

teams = []
rank = 1
for a in soup.find_all("table", class_="leaguetable sortable table detailed-table"):
    for col in a.find_all("tbody"):
        for tr in col.find_all("tr"):

            team = []
            team.append(rank)
            for data in tr.find_all("td", "text team large-link"):
                team.append(data.get_text())
            for data in tr.find_all("td", "number total mp"):
                team.append(data.get_text())
            for data in tr.find_all("td", "number total won total_won"):
                team.append(data.get_text())
            for data in tr.find_all("td", "number total drawn total_drawn"):
                team.append(data.get_text())
            for data in tr.find_all("td", "number total lost total_lost"):
                team.append(data.get_text())
            for data in tr.find_all("td", "number total gf total_gf"):
                team.append(data.get_text())
            for data in tr.find_all("td", "number total ga total_ga"):
                team.append(data.get_text())
            for data in tr.find_all("td", "number points"):
                team.append(data.get_text())
            teams.append(team)
            rank += 1

key = [a[0] for a in teams]


# 크롤링 함수 구현하기
def _crawl_naver_keywords(text):
    keywords = []
    # 여기에 함수를 구현해봅시다.
    for a in teams:
        keywords.append("순위 : " + str(a[0]) + "   팀 이름 : " + a[1] + "   MP: " + a[2] + "   W: " + a[3] + "   D: " + a[
            4] + "   L: " + a[5] + "   G: " + a[6] + "   GF: " + a[7] + "   P: " + a[8])

    # 한글 지원을 위해 앞에 unicode u를 붙혀준다.
    return u'\n'.join(keywords)


# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        keywords = _crawl_naver_keywords(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )

        return make_response("App mention message has been sent", 200, )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/r", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)