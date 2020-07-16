import helper
import requests
from flask import Flask, request, Response, render_template, redirect 
import json
import time
from requests import get, post
import urllib

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
        text = get_text_from_url(comment)
        return Response("<p>" + text + "</p>") 
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
    subscription_key = '3878ef99c82a42c184eb1a2ef7c3773b'
    endpoint = "https://quentin-computervision.cognitiveservices.azure.com/"
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
    
