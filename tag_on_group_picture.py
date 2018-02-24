import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import json

# set up congnitive_face
KEY = 'you own key'  
CF.Key.set(KEY)

BASE_URL = 'your azure face api url'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

# set up the url of th e group picture
group_img_url = 'url of your own group picture'
#group_img_url = 'url of your own group picture'


faces = CF.face.detect(group_img_url)
#print('faces:')
#print(faces)
#print(json.dumps(faces, sort_keys=True, indent=2))


# convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))
        
# download the image from the url
response = requests.get(group_img_url)
group_img = Image.open(BytesIO(response.content))

# for each face returned use the face rectangle and draw a red box.
draw = ImageDraw.Draw(group_img)
for face in faces:
    draw.rectangle(getRectangle(face), outline='red')
    #print('location of the face: ')
    #print(getRectangle(face))

# display the image in the users default image browser.
#group_img.show()


######################################################

# set dataset
img_url = list()
for i in range(2):
	img_url.append('')
img_url[0] = {'picture_url': 'url of your friend picture', 'name': 'friend name'} 
img_url[1] = {'picture_url': 'url of your friend picture', 'name': 'friend name'} 

# use CF to get the faceID of dataset
dataset_detect = list()
for i in range(len(img_url)):
    id = (CF.face.detect(img_url[i]['picture_url']))
    dataset_detect.append({'faceId': id[0]["faceId"], 'name': img_url[i]['name']})

#print('dataset_detect:')
#print(dataset_detect)	

######################################################

# get the faceIDs of the group picture

group_faces_id = [faces[i]['faceId'] for i in range(len(faces))]
#print('group_faces_id: ')
#print(group_faces_id)

######################################################
# combine faceIds of dataset and group picture

dataset_list = list()
for i in range(2):
    dataset_list.append(dataset_detect[i]['faceId'])
allfaceIDs = dataset_list + group_faces_id
#print('allfaceIDs: ')
#print(allfaceIDs)

######################################################
# use face API's group

body = {"faceIds":allfaceIDs}

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': KEY,
}

# Request parameters.
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

response = requests.request('POST', BASE_URL + 'group', json=body, data=None, headers=headers, params=params)

parsed = json.loads(response.text)
#print ('result after grouping:')
#print (json.dumps(parsed, sort_keys=True, indent=2))

######################################################

match_id = list()
for i in range(len(parsed['groups'])):
    match_id.append(parsed['groups'][i])

# compare match_id to faces to get location of face
# compare match_id to dataset_detect to get name of face

def writename(match_id, faceDictionary, dataset_detect):
    showname = 'temp_name'

    for id in match_id:
        find_match_location = 0
        find_match_name = 0

        # find the name
        for data in dataset_detect:
            if (id[0] == data['faceId']) or (id[1] == data['faceId']):
                showname = data['name']
                find_match_name = 1
        
        # find the location
        for face in faceDictionary:
            if (id[0] == face['faceId']) or (id[1] == face['faceId']):
                rect = face['faceRectangle']
                left = rect['left']
                top = rect['top']
                find_match_location = 1

        # if find the location and name
        if (find_match_location == 1) and (find_match_name == 1):
        	# set font
            largefont = ImageFont.truetype("calibri.ttf",30)
            draw = ImageDraw.Draw( group_img )
            draw.text( (left-15, top-30), showname, font = largefont, fill=(255,0,0,255))

writename(match_id, faces, dataset_detect)

group_img.show()
