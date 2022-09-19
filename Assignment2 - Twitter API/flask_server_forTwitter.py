#import flask
from requests_oauthlib import OAuth1Session
import json
from flask import Flask, request
import configparser


# read configs
config = configparser.ConfigParser()
config.read('config.ini')


consumer_key = config['twitter']['consumer_key']
consumer_secret = config['twitter']['consumer_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/createTweet', methods=['GET', 'POST'])
def createTweet():
    tweet_text = request.args.get('tweet_text')
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json={"text": f"{tweet_text}"},
    )
    return str(response.status_code)

@app.route('/searchTweet', methods=['GET'])
def searchTweet():
    keyword = request.args.get('keyword')
    response = oauth.get(
        "https://api.twitter.com/2/tweets/search/recent?query="+keyword
        )
    return response.json()['data']

@app.route('/deleteTweet', methods=['GET', 'POST'])
def deleteTweet():
    id = request.args.get('id')
    response = oauth.delete(
        "https://api.twitter.com/2/tweets/{}".format(id)
        )
    return str(response.status_code)

app.run(port=80)
