# importing render and redirect
import asyncio
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

# importing the libraries
import os
import json
import requests
import ast
import time

from datetime import datetime
from .forms import UploadFileForm, FileUploadForm
from .models import UploadModel

name = ""
phone = ""
email = ""
instagram = ""
propertyaddress = ""
cityaddress = ""
listprice = ""
description = ""

def upload_image(request):
    if request.method == "POST":
        print(request.FILES)
        uploadModel = UploadModel()
        _, file = request.FILES.popitem()
        file = file[0]
        print(file)
        uploadModel.file = file
        uploadModel.save()
        print(uploadModel.file)
        return JsonResponse({'thumb_url': str(uploadModel.file)}, status=200)

def generateImage(payload):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer bb_pr_bbd8d0bffd822b82aaa4c22f4d1eaa'
    }
    response = requests.request("POST", "https://api.bannerbear.com/v2/images", headers=headers, data=payload)
    string = response.json()

    img_uid = string["uid"]

    print(img_uid)
    limit = 5
    while limit > 0:
        time.sleep(1)
        response = requests.request("GET", "https://api.bannerbear.com/v2/images/"+str(img_uid), headers=headers, data="")
        string = response.json()
        if string["image_url"] is not None:
            return string["image_url"]
        limit -= 1
    return None

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
    thumb_url = request.POST.get('thumb_url')
    print('-----------')
    print(thumb_url)

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
        'thumb_url': thumb_url,
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
    print(type(temp))
    if isinstance(type(temp), list):
        temp = temp[0]
    if temp.get('zpid') is None:
        if temp.get('status') is not None:
            context['errors']['propertyaddress'] = 'Property Address is required'
        else:
            context['errors']['res_urls'] = 'No Result'
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
    payloads = []
    payloads.append(json.dumps({        # template 1
        "template": "BAQGWyDLM6LMbgmENL",
        "modifications": [
            {
                "name": "hero-image",
                "image_url": thumb_url
            },
            {
                "name": "BG",
                "color": None
            },
            {
                "name": "heading",
                "text": name,
                "color": None,
                "background": None
            },
            {
                "name": "list",         # 1
                "text": description,
                "color": None,
                "background": None
            },
            {
                "name": "bg-price",
                "color": None
            },
            {
                "name": "price",        # 1
                "text": listprice,
                "color": None,
                "background": None
            },
            {
                "name": "address",      # 1
                "text": propertyaddress + '\n' + cityaddress,
                "color": None,
                "background": None
            },
            {
                "name": "Contact Us-Heading",   # 1
                "text": "Contact Us:",
                "color": None,
                "background": None
            },
            {
                "name": "contact info",         # 1
                "text": phone + '\n' + email + '\n' + instagram,
                "color": None,
                "background": None
            }
        ],
        "webhook_url": None,
        "metadata": None
    }))
    payloads.append(json.dumps({        # template 2
        "template": "k4qoBVDy1KOzDzN0gj",
        "modifications": [
            {
                "name": "hero-image",
                "image_url": thumb_url
            },
            {
                "name": "bg-main",
                "color": None
            },
            {
                "name": "BG-heading",
                "color": None
            },
            {
                "name": "corp name",
                "text": "You can change this text",
                "color": None,
                "background": None
            },
            {
                "name": "heading",
                "text": name,
                "color": None,
                "background": None
            },
            {
                "name": "list",
                "text": description,
                "color": None,
                "background": None
            },
            {
                "name": "bg-price",
                "color": None
            },
            {
                "name": "price",
                "text": listprice,
                "color": None,
                "background": None
            },
            {
                "name": "address",
                "text": propertyaddress + '\n' + cityaddress,
                "color": None,
                "background": None
            },
            {
                "name": "contact info - phone",
                "text": phone,
                "color": None,
                "background": None
            },
            {
                "name": "contact info - email",
                "text": email,
                "color": None,
                "background": None
            },
            {
                "name": "title-1",
                "text": "Overview",
                "color": None,
                "background": None
            },
            {
                "name": "title-2",
                "text": "You can change this text",
                "color": None,
                "background": None
            },
            {
                "name": "line",
                "color": None,
                "hide": True
            },
            {
                "name": "title-3",
                "text": "",
                "color": None,
                "background": None,
                "hide": True
            },
            {
                "name": "text-feature-1",
                "text": "",
                "color": None,
                "background": None,
                "hide": True
            },
            {
                "name": "text-feature-2",
                "text": "",
                "color": None,
                "background": None,
                "hide": True
            },
            {
                "name": "text-feature-3",
                "text": "",
                "color": None,
                "background": None,
                "hide": True
            },
            {
                "name": "title-4",
                "text": "Contact Details",
                "color": None,
                "background": None
            },
            {
                "name": "contact info - website",  # 2
                "text": instagram,
                "color": None,
                "background": None
            },
        ],
        "webhook_url": None,
        "metadata": None
    }))
    payloads.append(json.dumps({        # template 3
        "template": "V4WN6JDx01vVD3Gqjk",
        "modifications": [
            {
                "name": "big-img-mask",
                "image_url": thumb_url
            },
            {
                "name": "BG",
                "color": None
            },
            {
                "name": "heading",
                "text": name,
                "color": None,
                "background": None
            },
            {
                "name": "address",
                "text": propertyaddress + '\n' + cityaddress,
                "color": None,
                "background": None
            },
            {
                "name": "contact info - phone",
                "text": phone,
                "color": None,
                "background": None
            },
            {
                "name": "contact info - email",
                "text": email,
                "color": None,
                "background": None
            },
            {
                "name": "title-footer",
                "text": "Address",
                "color": None,
                "background": None
            },
            {
                "name": "text-feature-1",
                "text": "",
                "color": None,
                "background": None,
                "hide": True
            },
            {
                "name": "text-feature-2",
                "text": "",
                "color": None,
                "background": None,
                "hide": True
            },
            {
                "name": "text-feature-3",
                "text": "",
                "color": None,
                "background": None,
                "hide": True
            },
            {
                "name": "name",
                "text": "Contact Details",
                "color": None,
                "background": None
            },
            {
                "name": "bg-price",
                "color": None
            },
            {
                "name": "title-1",
                "text": listprice,
                "color": None,
                "background": None
            },
        ],
        "webhook_url": None,
        "metadata": None
    }))
    payloads.append(json.dumps({        # template 4
        "template": "RnxGpW5lj8PQbEXrJ1",
        "modifications": [
            {
                "name": "head",
                "image_url": thumb_url
            },
            {
                "name": "heading",
                "text": name,
                "color": None,
                "background": None
            },
            {
                "name": "title-1",
                "text": "For Sale",
                "color": None,
                "background": None
            },
            {
                "name": "contact info - phone",
                "text": phone,
                "color": None,
                "background": None
            },
            {
                "name": "contact info - email",
                "text": email,
                "color": None,
                "background": None
            },
            {
                "name": "sub text",
                "text": description,
                "color": None,
                "background": None
            },
            {
                "name": "website",
                "text": instagram,
                "color": None,
                "background": None
            }
        ],
        "webhook_url": None,
        "metadata": None
    }))
    payloads.append(json.dumps({        # template 5
        "template": "w0kdleZGl7oL5orWxN",
        "modifications": [
            {
                "name": "hero-image",
                "image_url": thumb_url
            },
            {
                "name": "bg-shape",
                "color": None
            },
            {
                "name": "heading",
                "text": name,
                "color": None,
                "background": None
            },
            {
                "name": "title-1",
                "text": "Where Dreams Come True",
                "color": None,
                "background": None
            },
            {
                "name": "contact info - phone",
                "text": phone,
                "color": None,
                "background": None
            },
            {
                "name": "contact info - email",
                "text": email,
                "color": None,
                "background": None
            },
            {
                "name": "sub text",
                "text": description,
                "color": None,
                "background": None
            },
            {
                "name": "website",
                "text": instagram,
                "color": None,
                "background": None
            },
            {
                "name": "rectangle_16",
                "color": None
            },
            {
                "name": "price-text",
                "text": "Price",
                "color": None,
                "background": None
            },
            {
                "name": "price-number",
                "text": listprice,
                "color": None,
                "background": None
            },
            {
                "name": "website Duplicate 17",
                "text": "Aenean tristique pulvinar commodo",
                "color": None,
                "background": None,
                "hide": True
            },
            {
                "name": "list",
                "text": "Vivamus ullamcorper odio felis in finibus",
                "color": None,
                "background": None,
                "hide": True
            },
            {
                "name": "contact info - phone Duplicate 19",
                "text": "Book Now",
                "color": None,
                "background": None
            }
        ],
        "webhook_url": None,
        "metadata": None
    }))
    res_urls = []
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer bb_pr_bbd8d0bffd822b82aaa4c22f4d1eaa'
    }
    res_urls.append(generateImage(payloads[0]))
    res_urls.append(generateImage(payloads[1]))
    res_urls.append(generateImage(payloads[2]))
    res_urls.append(generateImage(payloads[3]))
    res_urls.append(generateImage(payloads[4]))
    # for payload in payloads:
    #     response = requests.request("POST", "https://api.bannerbear.com/v2/images", headers=headers, data=payload)
    #     string = response.json()

    #     img_uid = string["uid"]

    #     print(img_uid)
    #     time.sleep(5)

    #     response = requests.request("GET", "https://api.bannerbear.com/v2/images/"+str(img_uid), headers=headers, data="")
    #     string = response.json()
    #     res_urls.append(string["image_url"])
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
