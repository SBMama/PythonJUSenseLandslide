import http
import json
import os

from flask import Flask, make_response, request
from flask_cors import CORS

from app.models.crowd_source_images import CrowdSource
from app.models.process_news_articles import ProcessArticles
from app.models.process_tweets import ProcessTweet

app = Flask(__name__)
CORS(app)


@app.route('/v1/get_tweets', methods=['GET'])
def get_tweets():
    filename = os.path.join("..","data","tweets.json")
    params = request.args.to_dict()
    tweet_obj = ProcessTweet(filename)
    result = tweet_obj.map_tweets_from_json()
    if "text" in params or "date" in params:
        text = params.get("text", None)
        date = params.get("date", None)
        result = tweet_obj.filter_tweets(result, text, date)
    response = make_response(json.dumps(result), http.HTTPStatus.OK)
    response.headers = {'Content-Type': 'application/json'}
    return response


@app.route('/v1/get_news', methods=['GET'])
def get_news():
    folder = os.path.join("..","data","articles")
    params = request.args.to_dict()
    news_obj = ProcessArticles(folder)
    result = news_obj.process_articles()
    response = make_response(json.dumps(result), http.HTTPStatus.OK)
    response.headers = {'Content-Type': 'application/json'}
    return response


@app.route('/v1/image_upload', methods=['POST'])
def upload_image():
    image_folder = os.path.join("..","data","images_uploaded")
    data_folder = os.path.join("..","data","crowd_source_data")
    payload = request.form.to_dict()
    file = request.files
    obj = CrowdSource()
    obj.save_image(file, image_folder)
    obj.save_metadata(payload, file, data_folder)
    result = {"Status": "Ok"}
    response = make_response(json.dumps(result), http.HTTPStatus.OK)
    response.headers = {'Content-Type': 'application/json'}
    return response


