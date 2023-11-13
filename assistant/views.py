# importing render and redirect
from django.shortcuts import render, redirect
from django.http import HttpResponse

# importing the libraries
import os
import json
import requests
import ast
import time

name = ""
phone = ""
email = ""
instagram = ""
propertyaddress = ""
cityaddress = ""
listprice = ""
description = ""


def generate(request):
    # Get the information from the user input
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    instagram = request.POST.get('instagram')
    propertyaddress = request.POST.get('propertyaddress')
    cityaddress = request.POST.get('cityaddress')
    listprice = request.POST.get('listprice')
    description = request.POST.get('description')

    context = {
        'name': name,
        'phone': phone,
        'email': email,
        'instagram': instagram,
        'propertyaddress': propertyaddress,
        'cityaddress': cityaddress,
        'listprice': listprice,
        'description': description,
        'errors': {},
        'res_urls': []
    }

    # Send address to zillow.com and get zpid.
    url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"

    querystring = {"location": str(propertyaddress)}

    headers = {
        "X-RapidAPI-Key": "0229d73864msh521a5aee8b7afe1p1969ecjsna56ec50c4faf",
        "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    temp = response.json()
    print('----------------')
    print(temp)
    print('----------------')
    if temp.get('zpid') is None:
        context['errors']['propertyaddress'] = 'Property Address is required'
        return render(request, 'assistant/home.html', context)
    zpid = temp['zpid']

    # Based on zpid get the images about the property.
    url = "https://zillow-com1.p.rapidapi.com/images"

    querystring = {"zpid": str(zpid)}

    headers = {
        "X-RapidAPI-Key": "0229d73864msh521a5aee8b7afe1p1969ecjsna56ec50c4faf",
        "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    temp = response.json()
    temp = temp['images']
    imgurl_list = ast.literal_eval(str(temp))
    if len(imgurl_list) < 4:
        while len(imgurl_list) < 4:
            imgurl_list.append(imgurl_list[0])
    # Send images and descriptions to bannerbear to create real estate flyers.
    url = "https://api.bannerbear.com/v2/collections"
    payload = json.dumps({
        # "template_set": "V17MYjrN2evrR5eZGv",
        "template_set": "YpJ2mlgY5pjgMXLjnb",
        "modifications": [
            {
                "name": "background",
                "color": None
            },
            {
                "name": "photo_container",
                "image_url": imgurl_list[0]
            },
            {
                "name": "logo_container",
                "image_url": imgurl_list[0]
            },
            {
                "name": "title",
                "text": None,
                "color": None,
                "background": None
            },
            {
                "name": "rectangle_background",
                "color": None
            },
            {
                "name": "description",
                "text": description,
                "color": None,
                "background": None
            },
            {
                "name": "price_label",
                "text": listprice,
                "color": None,
                "background": None
            },
            {
                "name": "contact_details",
                "text": name+"  "+phone+"  \n"+email+" "+propertyaddress,
                "color": None,
                "background": None
            },
            {
                "name": "features_list",
                "text": None,
                "color": None,
                "background": None
            },
            {
                "name": "rectangle_border",
                "color": None
            },
            {
                "name": "image_container1",
                "image_url": imgurl_list[0]
            },
            {
                "name": "image_container2",
                "image_url": imgurl_list[1]
            },
            {
                "name": "image_container3",
                "image_url": imgurl_list[2]
            },
            {
                "name": "image_container4",
                "image_url": imgurl_list[3]
            },
            {
                "name": "border",
                "color": None
            },
            {
                "name": "description_title",
                "text": None,
                "color": None,
                "background": None
            },
            {
                "name": "description_text",
                "text": description,
                "color": None,
                "background": None
            },
            {
                "name": "price_text",
                "text": listprice,
                "color": None,
                "background": None
            },
            {
                "name": "propertyfeatures_title",
                "text": None,
                "color": None,
                "background": None
            },
            {
                "name": "propertyfeatures_list",
                "text": None,
                "color": None,
                "background": None
            },
            {
                "name": "photo",
                "image_url": imgurl_list[0]
            },
            {
                "name": "rectangle_1",
                "color": None
            },
            {
                "name": "avatar",
                "image_url": imgurl_list[0]
            },
            {
                "name": "details",
                "text": None,
                "color": None,
                "background": None
            },
            {
                "name": "contact",
                "text": name+"  "+phone+"  \n"+email+" "+propertyaddress,
                "color": None,
                "background": None
            }
        ],
        "webhook_url": None,
        "metadata": None
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer bb_pr_bbd8d0bffd822b82aaa4c22f4d1eaa'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    string = response.json()
    img_uid = string["uid"]
    print(img_uid)
    time.sleep(5)
    url = "https://api.bannerbear.com/v2/collections/"+str(img_uid)

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer bb_pr_bbd8d0bffd822b82aaa4c22f4d1eaa'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    string = response.json()
    res_urls = list(string["image_urls"].values())
    context['res_urls'] = res_urls
    return render(request, 'assistant/home.html', context)


def home(request):
    try:
        return render(request, 'assistant/home.html')
    except Exception as e:
        print(e)
        # if there is an error, redirect to the error handler
        return redirect('error_handler')


def new_chat(request):
    global index
    # clear the messages list
    request.session.pop('prompts', None)
    request.session.pop('messages', None)
    index = 0
    return redirect('home')


# this is the view for handling errors
def error_handler(request):
    return render(request, 'assistant/404.html')
