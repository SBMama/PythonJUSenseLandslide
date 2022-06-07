import http
import json
import os

from flask import Flask, make_response, request
from flask_cors import CORS

from app.models.Final_landslide import ClassifyImage
from app.models.crowd_source_images import CrowdSource
from app.models.process_news_articles import ProcessArticles
from app.models.process_tweets import ProcessTweet

app = Flask(__name__)
CORS(app)


@app.route('/v1/get_tweets', methods=['GET'])
def get_tweets():
    filename = "./app/data/tweets.json"
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
    folder = "./app/data/articles"
    params = request.args.to_dict()
    news_obj = ProcessArticles(folder)
    result = news_obj.process_articles()
    response = make_response(json.dumps(result), http.HTTPStatus.OK)
    response.headers = {'Content-Type': 'application/json'}
    return response


@app.route('/v1/image_upload', methods=['POST'])
def upload_image():
    try:
        payload = request.form.to_dict()
        file = request.files
        obj = CrowdSource()
        imagefile = obj.save_image(file, request)
        obj.save_metadata(payload, imagefile, request)
        result = {"Status": "Uploaded Successfully"}
        response = make_response(json.dumps(result), http.HTTPStatus.OK)
        response.headers = {'Content-Type': 'application/json'}
        return response
    except Exception as e:
        result = {"Status": "Uploaded Failed"}
        response = make_response(json.dumps(result), http.HTTPStatus.OK)
        response.headers = {'Content-Type': 'application/json'}
        return response


@app.route('/v1/fetch_metadata', methods=['GET'])
def fetch_image():
    image_folder = "./app/data/images_uploaded"
    data_folder = "./app/data/crowd_source_data"
    obj = CrowdSource()
    result = obj.fetch_metadata(data_folder, image_folder)
    response = make_response(json.dumps(result), http.HTTPStatus.OK)
    response.headers = {'Content-Type': 'application/json'}
    return response


@app.route('/v1/image_classification', methods=['POST'])
def classify_image():
    try:
        image_folder = "./app/data/"
        file = request.files
        obj = ClassifyImage()
        status = obj.classify(file, image_folder)
        result = {"Status": status}
        response = make_response(json.dumps(result), http.HTTPStatus.OK)
        response.headers = {'Content-Type': 'application/json'}
        return response
    except Exception as e:
        result = {"Status": f"Classification Failed {str(e)}"}
        response = make_response(json.dumps(result), http.HTTPStatus.INTERNAL_SERVER_ERROR)
        response.headers = {'Content-Type': 'application/json'}
        return response