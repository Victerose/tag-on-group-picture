import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import json

# set up congnitive_face
KEY = 'df1f5ec6fd2f417486df8372b4f3fa1b'  
CF.Key.set(KEY)

BASE_URL = 'https://southcentralus.api.cognitive.microsoft.com/face/v1.0/'  
CF.BaseUrl.set(BASE_URL)

# set up the url of th e group picture
group_img_url = 'https://scontent-tpe1-1.xx.fbcdn.net/v/t1.0-9/21231822_1426449027450252_8407870731039537619_n.jpg?oh=1da059fd8453ea18fa3764b5d90090bf&oe=5B18E601'
#group_img_url = 'https://i.imgur.com/4UvEUGk.jpg'


faces = CF.face.detect(group_img_url)
#print(faces)
#print(json.dumps(faces, sort_keys=True, indent=2))


#Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))
        
#Download the image from the url
response = requests.get(group_img_url)
group_img = Image.open(BytesIO(response.content))

#For each face returned use the face rectangle and draw a red box.
draw = ImageDraw.Draw(group_img)
for face in faces:
    draw.rectangle(getRectangle(face), outline='red')
    #print(getRectangle(face))

#Display the image in the users default image browser.
group_img.show()