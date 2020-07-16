import requests​
url_image = "https://www.accede-web.com/wp-content/uploads/2015/06/justification-01.jpg"
endpoint = "https://quentin-computervision.cognitiveservices.azure.com/"
subscription_key = '3878ef99c82a42c184eb1a2ef7c3773b'
endpoint = "https://quentin-computervision.cognitiveservices.azure.com/"
ocr_url = endpoint + "vision/v3.0/ocr"
​
headers = {"Ocp-Apim-Subscription-Key": '3878ef99c82a42c184eb1a2ef7c3773b',
           'Content-type': 'application/json'}
#params = {"includeTextDetails": True}
​
data = {"url" : url_image}
response = requests.post(url=ocr_url,
                         headers=headers,
                         json=data,
                         #params = params
                         )
​
print(response.text)
​
print(response.json()['regions'])
​
for index, line in enumerate(response.json()['regions'][0]['lines']):
    print(line['words'])
    for word in range(len(line['words'])):
        print(word)
        
for index, line in enumerate(response.json()['regions'][0]['lines']):
    print(line['words'])
    for word in range(len(line['words'])):
        print(word)        
​
