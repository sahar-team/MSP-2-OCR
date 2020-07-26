import helper
import requests
from flask import Flask, request, Response, render_template, redirect 
import json
import time
from requests import get, post
import urllib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO
import os
import random
import string
import glob
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/')
def hello_world():
    # url_image = "https://help.aronium.com/hc/user_images/clTArYEKfNByoZgk4a5o0w.png"
    # headers = {"Ocp-Apim-Subscription-Key": '81fb31af7aa046f6b7bb0cd162b3ff09', 'Content-type': 'application/json'}
    # url = 'https://westeurope.api.cognitive.microsoft.com/formrecognizer/v2.0/prebuilt/receipt/analyze'
    # data = {"source": url_image}
    # response = requests.post(url, headers=headers, data=data)
    # print(response.text)
    return render_template('index.html')

@app.route('/comment/new', methods=['POST'])
def add_comment():
    # Get comment from the POST body
    if request.method == "POST":
        
        req = request.form.to_dict()
        comment = req["comment"]
        #text = get_text_from_url(comment)
        files = glob.glob('./static/output/*')
        for f in files:
            os.remove(f)
        plt, texte = get_image_from_url(comment)
        file_name = get_random_string(8)
        plt.savefig('./static/output/{}.jpeg'.format(file_name), bbox_inches='tight') 
        return render_template("resultats.html", text_result=texte, filename = '/output/' + file_name + '.jpeg')
        # return render_template("/index.html")

    
    req_data = request.get_json()
    comment = req_data['comment']

    # Add comment to the list
    res_data = helper.add_to_list(comment)

    # Return error if comment not added
    if res_data is None:
        response = Response("{'error': 'comment not added - " + comment + "'}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return render_template("index.html")

def get_text_from_url(url_image):
    
    url_image = url_image
    subscription_key = os.getenv("COMPUTER_VISION_SUBSCRIPTION_KEY")
    endpoint = os.getenv("COMPUTER_VISION_ENDPOINT")
    ocr_url = endpoint + "vision/v3.0/ocr"
    
    headers = {"Ocp-Apim-Subscription-Key": subscription_key,
               'Content-type': 'application/json'}
    #params = {"includeTextDetails": True}
    
    data = {"url" : url_image}
    response = requests.post(url=ocr_url,
                             headers=headers,
                             json=data,
                             #params = params
                             )
    

    texte = ''
    for index, line in enumerate(response.json()['regions'][0]['lines']):
        for num in range(len(line['words'])):
            texte += ' ' + str(line['words'][num]['text'])
            
    return texte

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
    
def get_image_from_url(url_image):
    subscription_key = os.getenv("COMPUTER_VISION_SUBSCRIPTION_KEY")
    endpoint = os.getenv("COMPUTER_VISION_ENDPOINT")
    text_recognition_url = endpoint + "vision/v3.0/read/analyze"
    # Set image_url to the URL of an image that you want to recognize.
    image_url = url_image
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    data = {"url": image_url}
    response = requests.post(
        url = text_recognition_url, headers=headers, json=data)
    
    #Deuxieme commande get pour obtenir les resultats.
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
        time.sleep(1)
        if ("analyzeResult" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'failed'):
            poll = False
    
    texte = ''
    for index, line in enumerate(analysis['analyzeResult']['readResults'][0]['lines']):
        for num in range(len(line['words'])):
            texte += ' ' + str(line['words'][num]['text'])

    polygons = []
    if ("analyzeResult" in analysis):
        # Extract the recognized text, with bounding boxes.
        polygons = [(line["boundingBox"], line["text"])
                    for line in analysis["analyzeResult"]["readResults"][0]["lines"]]
        
    image = Image.open(BytesIO(requests.get(image_url).content))
    fig = plt.figure()
    ax = plt.imshow(image)
    for polygon in polygons:
        vertices = [(polygon[0][i], polygon[0][i+1])
                    for i in range(0, len(polygon[0]), 2)]
        text = polygon[1]
        patch = Polygon(vertices, closed=True, fill=False, linewidth=2, color='y')
        ax.axes.add_patch(patch)
        plt.text(vertices[0][0]+image.size[0], vertices[0][1], text, fontsize=20, va="top")
    return fig, texte