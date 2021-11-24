import requests
import json
import os
from PIL import Image
import socket

API_APOD_COUNT = 25

def get_data(api_key):
    raw_response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}').text
    response = json.loads(raw_response)
    return response

def get_data_by_date(api_key,date):
    raw_response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date}').text
    response = json.loads(raw_response)
    return response

def get_data_array(api_key):
    raw_responses = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}&count={API_APOD_COUNT}').text
    responses = json.loads(raw_responses)
    return responses

def get_date(response):
    date = response['date']
    return date


def get_explaination(response):
    explaination = response['explanation']
    return explaination


def get_hdurl(response):
    hdurl = response['hdurl']
    return hdurl


def get_media_type(response):
    media_type = response['media_type']
    return media_type


def get_service_version(response): 
    service_version = response['service_version']
    return service_version


def get_title(response):
    service_version = response['title']
    return service_version

def get_url(response):
    url = response['url']
    return url

def get_thumbnail_url(response):
    thumbnail_url = response['thumbnail_url']
    return thumbnail_url

def download_image(url, date):
    apod_dir_path = getProperDirectoryPath()
    
    complete_file_path = os.path.join(apod_dir_path, f'{date}.png')
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
    }

    if os.path.isfile(complete_file_path) == False:
        raw_image = requests.get(url, headers).content
        with open(complete_file_path, 'wb') as file:
            file.write(raw_image)
    return complete_file_path
            
        
def getProperDirectoryPath():
    base_path = os.path.expanduser("~\\Pictures\\")
    directory = "NasaApod"
    apod_dir_path = os.path.join(base_path, directory)
    if not os.path.isdir(apod_dir_path):
        os.makedirs(apod_dir_path)
    return os.path.abspath(apod_dir_path)

def convert_image(image_path):
    path_to_image = os.path.normpath(image_path)

    basename = os.path.basename(path_to_image)

    filename_no_extension = basename.split(".")[0]

    base_directory = os.path.dirname(path_to_image)

    image = Image.open(path_to_image)
    image.save(f"{base_directory}/{filename_no_extension}.png")

def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False