#!/usr/bin/env python
# coding: utf-8

# In[1]:

from __future__ import print_function
import pytesseract as pt
import cv2
import glob
import re
import os
import numpy as np

import matplotlib.pyplot as plt
# plt.figure(num=None, figsize=(8, 6), dpi=200)
plt.figure(figsize=(100,100))


# In[2]:


pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# In[3]:


image = cv2.imread('IMG_20210126_182640.jpg')
image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)


# In[4]:


# print(pt.image_to_string(image).replace('\n\n', ''))


# In[5]:


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(gray, 30, 500)


# In[6]:


# contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# cv2.drawContours(image, contours, -1, (0, 255, 0), 3)


# In[7]:


# cv2.namedWindow('Gray', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Gray', 800,900)
# cv2.imshow('Gray', gray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# In[8]:


# cv2.namedWindow('Canny Edges After Contouring', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Canny Edges After Contouring', 800,900)
# cv2.imshow('Canny Edges After Contouring', edged)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# # plt.imshow(edged)


# In[9]:


# cv2.namedWindow('Contours', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Contours', 800,900)
# cv2.imshow('Contours', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# # plt.imshow(image)


# In[ ]:





# In[10]:


"""# Load image, grayscale, Gaussian blur, adaptive threshold
image = cv2.imread('sample labels/IMG_20210126_182959.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (1,1), 0)
thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 13)

# Dilate to combine adjacent text contours
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
dilate = cv2.dilate(thresh, kernel, iterations=4)

# Find contours, highlight text areas, and extract ROIs
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

ROI_number = 0
for c in cnts:
    area = cv2.contourArea(c)
    if area > 10000:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
        # ROI = image[y:y+h, x:x+w]
        # cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
        # ROI_number += 1

cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
cv2.resizeWindow('thresh', 650,750)
cv2.imshow('thresh', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.namedWindow('dilate', cv2.WINDOW_NORMAL)
cv2.resizeWindow('dilate', 650,750)
cv2.imshow('dilate', dilate)
cv2.waitKey(0)
cv2.destroyAllWindows()

mid = cv2.bitwise_and(gray, dilate)
cv2.namedWindow('mid_image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('mid_image', 650,750)
cv2.imshow('mid_image', mid)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 600,700)
cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()"""


# In[11]:


# pt.image_to_string(image)


# In[12]:


gray2 = gray.copy()
gray2.shape


# In[13]:


for i in range(gray2.shape[0]):
    for j in range(gray2.shape[1]):
        if gray2[i][j] < 125:
            gray2[i][j] = 240
        else:
            gray2[i][j] = 35


# In[14]:


# cv2.namedWindow('gray2', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('gray2', 650,750)
# cv2.imshow('gray2', gray2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# In[15]:


sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(gray2, -1, sharpen_kernel)


# In[16]:


de_sharpen = cv2.fastNlMeansDenoising(sharpen)


# In[17]:


# cv2.namedWindow('sharpen', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('sharpen', 650,750)
# cv2.imshow('sharpen', de_sharpen)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# In[18]:


# print(pt.image_to_string(sharpen).replace('\n\n', ' '))


# In[19]:


cv2.imwrite('sharpen1.jpg', sharpen)


# In[20]:


#cv2.imwrite('gray.jpg', gray2)


# In[21]:


def poly_area(vertices):
    x_cords = []
    y_cords = []
    for k in vertices:
        x_cords.append(k[0])
        y_cords.append(k[1])
    area = 0
    for x in range(len(vertices)-2):
        v1,v2,v3 = 0,x+1,x+2
        tr_area = abs(0.5*(x_cords[v1]*(y_cords[v2]-y_cords[v3])+
                       x_cords[v2]*(y_cords[v3]-y_cords[v1])+
                       x_cords[v3]*(y_cords[v1]-y_cords[v2])))
        area += tr_area
    print("Area of Polygon: ", area)
    return area


# In[22]:


from PIL import Image
import io
import proto

from google.cloud import vision
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"C:\Users\Administrator\Desktop\Nutrition_OCR\nutriscan\nutrition-ocr-303908-e56c789f74d0.json"

# gcp_credentials_string = r"C:\Users\mradul\PycharmProjects\Nutrition_OCR\nutrition-ocr-303906-48e94a8fb64d.json"
# gcp_json_credentials_dict = json.loads(gcp_credentials_string)
# credentials = service_account.Credentials.from_service_account_info(gcp_json_credentials_dict)

image_uri = 'sharpen1.jpg'

client = vision.ImageAnnotatorClient()
# image = vision.Image()
# image.source.image_uri = image_uri

with io.open(image_uri, 'rb') as image_file:
    content = image_file.read()
        
image = vision.Image(content=content)
response = client.text_detection(image=image)
response.full_text_annotation

boxes = []
for text in response.text_annotations:
    print('=' * 30)
    print(text.description)
    vertices = [(v.x, v.y) for v in text.bounding_poly.vertices]
    center = {'x': (int(vertices[0][0]) + int(vertices[1][0]) + int(vertices[2][0]) + int(vertices[3][0]))/4,
              'y': (int(vertices[0][1]) + int(vertices[1][1]) + int(vertices[2][1]) + int(vertices[3][1]))/4,
             'area': poly_area(vertices)}
    boxes.append(center)


# In[23]:


serializable_tags = [proto.Message.to_dict(tag) for tag in response.text_annotations]
zipped = zip(boxes, serializable_tags)


# In[24]:


sorted_zipped = sorted(zip(boxes, serializable_tags), key=lambda z: (z[0]['y']))


# In[25]:


box, res = zip(*sorted_zipped)


# In[26]:


pivot = 0
p = 1

grouped = []
while p < len(sorted_zipped):
    if abs(sorted_zipped[p][0]['y'] - sorted_zipped[pivot][0]['y']) < 50:
        p += 1
    else:
        grouped.append(list(sorted_zipped[pivot:p]))
        pivot = p
grouped.append(list(sorted_zipped[pivot:p]))


# In[27]:

final_list = []
for group in grouped:
    text = []
    group = sorted(group, key=lambda z: (z[0]['x']))
    for item in group:
        if item[0]['area'] < 1000000.0:
            text.append(item[1]['description'])
    print(' '.join(text), '\n')
    final_list.append(' '.join(text))

list_text = '\n'.join(final_list)

# In[30]:


calories_pattern = r'[Calories|Calorie|Calori|Calor|Calo|Cal]'
cholesterol_pattern = r'[Cholesterol|Cholestero|Cholester|Cholest|Choles]'
iron_pattern = r'[iron|iro]'
potassium_pattern = r'[Potassium|Potassiu|Potassi|Potass|Potas|Pota|Pot]'
sodium_patern = r'[Sodium|Sodiu|Sodi|Sod]'
trans_fat_pattern = r'[Trans Fat|TransFat|TranFat|Trans Fa|Tran Fat|Trans|Tran]'
calcium_pattern = r'[Calcium|Calciu||Calci||Calc|Calcwm|Calcum|Calcim]'
saturated_fat_pattern = r'[Sat. Fat|Sat.Fat|SatFat|Sat Fa|Sa. Fat|Saturated|Sat|Saturated Fat|SaturatedFat]'
carb_pattern = r'[Carbohydrate|Carbohydrat|Carbohydra|Carb]'
protein_pattern = r'[Protein|Protei|Prote]'
fibre_pattern = r'[Fibre|Fibr]'
vitamin_pattern = r'Vitamin\s[A-Z]'


# In[ ]:
if re.search(pattern=calories_pattern, string=list_text, flags=re.IGNORECASE):
    name = "Calories"
elif re.search(pattern=vitamin_pattern, string=list_text, flags=re.IGNORECASE):
    pass
elif re.search(pattern=carb_pattern, string=list_text, flags=re.IGNORECASE):
    name = "Carbohydrates"
elif re.search(pattern=calcium_pattern, string=list_text, flags=re.IGNORECASE):
    name = "Calcium"
elif re.search(pattern=potassium_pattern, string=list_text, flags=re.IGNORECASE):
    name = "Potassium"
elif re.search(pattern=sodium_patern, string=list_text, flags=re.IGNORECASE):
    name = "Sodium"
elif re.search(pattern=saturated_fat_pattern, string=list_text, flags=re.IGNORECASE):
    name = "Saturated Fat"
elif re.search(pattern=trans_fat_pattern, string=list_text, flags=re.IGNORECASE):
    name = "Trans Fat"
elif re.search(pattern=protein_pattern, string=list_text, flags=re.IGNORECASE):
    name = "Protein"
elif re.search(pattern=iron_pattern, string=list_text, flags=re.IGNORECASE):
    name = "Iron"
elif re.search(pattern=cholesterol_pattern, string=list_text, flags=re.IGNORECASE):
    name = "Cholesterol"
elif re.search(pattern=fibre_pattern, string=list_text, flags=re.IGNORECASE):
    pass
