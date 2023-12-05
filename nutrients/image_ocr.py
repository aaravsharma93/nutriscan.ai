#!/usr/bin/env python
# coding: utf-8

# In[1]:

from __future__ import print_function
import cv2
import glob
import os
import numpy as np
from PIL import Image
import io
import proto

import re
# os.chdir('C:\Users\Administrator\Desktop\Nutrition_OCR\nutriscan\nutrients')

from django.conf import settings
from google.cloud import vision
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"C:\Users\Administrator\Desktop\Nutrition_OCR\nutriscan\nutrients\credentials.json"


# In[3]:


def ocr(image_file):
    data = {}

    # image = cv2.imread('sample labels/IMG_20210126_182640.jpg')
    image = cv2.imread(image_file)
    print('image', image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


    # In[5]:


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 30, 500)


    # In[6]:


    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    print(laplacian_var)
    if laplacian_var < 75:
        return {"Error":"Image blurry! Select another image"}


    # In[118]:


    # blur = cv2.GaussianBlur(gray, (1,1), 0)
    # thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 5)
    blur = cv2.GaussianBlur(gray, (1, 1), 0)
    thresh = cv2.threshold(blur, 0, 245, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


    # In[122]:


    gray2 = thresh.copy()
    gray2.shape


    # In[125]:


    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(gray2, -25, sharpen_kernel)


    # In[126]:


    de_sharpen = cv2.fastNlMeansDenoising(sharpen)


    # In[129]:


    cv2.imwrite(os.path.join(settings.MEDIA_ROOT, image_file), de_sharpen)


    # In[130]:


    def getSkewAngle(cvImage) -> float:
        # Prep image, copy, convert to gray scale, blur, and threshold
        newImage = cv2.imread(cvImage)
        gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Apply dilate to merge text into meaningful lines/paragraphs.
        # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
        # But use smaller kernel on Y axis to separate between different blocks of text
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
        dilate = cv2.dilate(thresh, kernel, iterations=5)

        # Find all contours
        contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)

        # Find largest contour and surround in min area box
        largestContour = contours[0]
        minAreaRect = cv2.minAreaRect(largestContour)

        # Determine the angle. Convert it to the value that was originally used to obtain skewed image
        angle = minAreaRect[-1]
        if angle < -45:
            angle = 90 + angle
        return -1.0 * angle


    # In[131]:


    # Rotate the image around its center
    def rotateImage(cvImage, angle: float):
        newImage = cv2.imread(cvImage)
        (h, w) = newImage.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        cv2.imwrite(cvImage, newImage)


    # In[132]:


    # Deskew image
    def deskew(cvImage):
        angle = getSkewAngle(cvImage)
        return rotateImage(cvImage, -1.0 * angle)


    # In[133]:


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
        # print("Area of Polygon: ", area)
        return area


    # In[134]:


    # gcp_credentials_string = r"C:\Users\mradul\PycharmProjects\Nutrition_OCR\nutrition-ocr-303906-48e94a8fb64d.json"
    # gcp_json_credentials_dict = json.loads(gcp_credentials_string)
    # credentials = service_account.Credentials.from_service_account_info(gcp_json_credentials_dict)

    image_uri = os.path.join(settings.MEDIA_ROOT, image_file)
    image_shape = cv2.imread(image_uri).shape
    image_area = image_shape[0]*image_shape[1]

    # angle = getSkewAngle(image_uri)
    # print(angle)
    # deskew(image_uri) if angle else None

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
        vertices = [(v.x, v.y) for v in text.bounding_poly.vertices]
        center = {'x': (int(vertices[0][0]) + int(vertices[1][0]) + int(vertices[2][0]) + int(vertices[3][0]))/4,
                'y': (int(vertices[0][1]) + int(vertices[1][1]) + int(vertices[2][1]) + int(vertices[3][1]))/4,
                'area': poly_area(vertices)}
        boxes.append(center)


    # In[135]:


    serializable_tags = [proto.Message.to_dict(tag) for tag in response.text_annotations]
    zipped = zip(boxes, serializable_tags)


    # In[136]:


    sorted_zipped = sorted(zip(boxes, serializable_tags), key=lambda z: (z[0]['y']))


    # In[137]:


    box, res = zip(*sorted_zipped)


    # In[138]:


    pivot = 0
    p = 1

    grouped = []
    while p < len(sorted_zipped):
        if abs(sorted_zipped[p][0]['y'] - sorted_zipped[pivot][0]['y']) < image_shape[1]*0.04:
            p += 1
        else:
            grouped.append(list(sorted_zipped[pivot:p]))
            pivot = p
    grouped.append(list(sorted_zipped[pivot:p]))


    # In[139]:


    final_list = []
    for group in grouped:
        text = []
        group = sorted(group, key=lambda z: (z[0]['x']))
        for item in group:
            if item[0]['area']/image_area < 0.7:
                text.append(item[1]['description'])
        # print(' '.join(text), '\n')
        final_list.append(' '.join(text))


    # In[141]:


    patterns = {
        'Calories': r'Calories|Calorie|Calori|Calor|Calo',
        'Cholesterol': r'Cholesterol|Cholestero|Cholester|Cholest|Choles',
        'Potassium': r'Potassium|Potassiu|Potassi|Potass|Potas|Pota|Pot',
        'Sodium': r'Sodium|Sodiu|Sodi|Secl|Sedi|Sedium',
        'Calcium': r'Calcium|Calciu|Calci|Calc|Calcwm|Calcum|Calcim',
        'Fat Trans': r'Trans Fat|TransFat|TranFat|Trans Fa|Tran Fat|Trans|Tran|Trans Phat|Trans Pat|Trans At|Tran Pat|Tran At',
        'Fat Saturated': r'Sat. Fat|Sat.Fat|SatFat|Sat Fa|Sa. Fat|Saturated|Sat|Saturated Fat|SaturatedFat',
        'Fat Total': r'Total Fat|TotalFat|Tatal Fat|Total Pat|TotalPat',
        'Carbohydrates': r'Carbohydrate|Carbohydrat|Carbohydra|Carb',
        'Protein': r'Protein|Protei|Prote',
        'Dietary Fiber': r'Fiber|Fibr|Fibe',
        'Vitamin': r'Vitamin\s?[A-Z]([0-9]{1,2})?|vitamin\s?[A-Z]([0-9]{1,2})?|vitamn\s?[A-Z]([0-9]{1,2})?|vitmn\s?[A-Z]([0-9]{1,2})?',
        'Iron': r'iron|iro|irn|Iron|Irn|Iro',
        'Sugar': r'Total Sugar|total sugar|Total Suga|totalsuga',
        'Magnesium': r'Magnesium|Magnesum|Magnesiim|Mognesium|Mognesum|Mognesiim',
        'Zinc': r'Zinc|Zin|Zimc|Zine|Zime|Zim',
        'Iodine': r'Iodine|Iodin|Iodi',
        'Copper': r'Copper|Coppe|Coppcr',
        'Chloride': r'Chloride|Chloridc|Chioride|Chioridc|Chlorid',
        'Chromium': r'Chromium|Chromiun|Chromim|Chronium|Chroniun|Chromiim|Chroniim|Chronium|Chromiun|Chronin|Chromiwm',
        'Phosphorus': r'Phosphorus|Phosphor',
        'Molybdenum': r'Molybdenum|Molybdemum|Molybdenun|Molybdenim|Molybdcnum|Molybde',
        'Manganese': r'Manganese|Manganesc|Mangancse|Mangancsc|Mangane|Mangan',
        'Selenium': r'Selenium|Seleniun|Selemium|Selemum|Seleniim|Seleniwm|Selen',
        'Vitamin B12 (Cobalamin)': r'Cyanocobalamin|Cobalamin|cobalamin|Cobalamn|cobalamn',
        'Vitamin B1 (Thiamin)': r'Thiamin|thiamin|Thiamn|thiamn',
        'Vitamin B2 (Riboflavin)': r'Riboflavin|riboflavin',
        'Vitamin B3 (Niacin)': r'Niacin|niacin',
        'Vitamin B5 (Pantothenic acid)': r'Pantothenic acid|pantothenic acid',
        'Vitamin B6 (Pyridoxin)': r'Pyridoxin|pyridoxin',
        'Vitamin B7 (Biotin)': r'Biotin|biotin',
        'Vitamin B9 (Folic Acid)': r'Folic Acid|Folic|folic acid|folic Acid|Folic acid'
    }


    # In[166]:


    for nutrient, pattern in patterns.items():
        # print('\n', nutrient)
        for i, line in enumerate(final_list):
            sub_data = {}
            find = re.search(pattern, line, flags=re.IGNORECASE)
            if find:
                value = re.search(r'(\d+(\.\d+)?)(\s)?(\w*)', line[find.end():], flags=re.IGNORECASE)
                # print(i, line, '\n', value)
                if nutrient == 'Vitamin':
                    nutrient = find.group()
                if value and value.start() < 50:
                    # print(value.groups())
                    sub_data['value'] = value.groups()[0]
                    sub_data['value_unit'] = value.groups()[3]
                    
                    if sub_data['value']:
                        data[nutrient] = sub_data


    # ### **API: http://45.138.27.162:8000/nutrients_file/api/?age=25&gender=M&nutrientName=Cholesterol**

    # In[116]:


    nutrients = [
        'Choline',
        'Lutein and zeaxanthin',
        'Lycopene',
        'Vitamin A',
        'Vitamin B1 (Thiamin)', 
        'Vitamin B12 (Cobalamin)', 
        'Vitamin B2 (Riboflavin)', 
        'Vitamin B3 (Niacin)', 
        'Vitamin B5 (Pantothenic acid)', 
        'Vitamin B6 (Pyridoxin)', 
        'Vitamin B7 (Biotin)', 
        'Vitamin B9 (Folic Acid)', 
        'Vitamin C',
        'Vitamin D',
        'Vitamin E',
        'Vitamín K',
        'Calcium',
        'Chloride',
        'Chromium',
        'Copper',
        'Fluoride',
        'Iodine',
        'Iron',
        'Magnesium',
        'Manganese',
        'Molybdenum',
        'Phosphorus',
        'Potassium',
        'Selenium',
        'Sodium',
        'Zinc',
        'Protein',
        '- Cystine',
        '- Histidine',
        '- Isoleucine',
        '- Leucine',
        '- Lysine',
        '- Methionine',
        '- Phenylalanine',
        '- Threonine',
        '- Tryptophan',
        '- Valine',
        'Cholesterol',
        'Sugar',
        'Calories',
        '- ALA',
        '- EPA',
        '- DHA',
        '- DPA',
        'Fat Saturated',
        'Fat Total',
        'Carbohydrates',
        'Dietary Fiber',
        'Water'
    ]


    return data





