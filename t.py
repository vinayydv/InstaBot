import requests

ACCESS_TOKEN = '5730266253.4e4a94a.cb49a51cb3f44aada44057d7eadee522'
BASE_URL = 'https://api.instagram.com/v1/'

def self_info():
    request_url = BASE_URL + "users/self/?access_token=%s"%ACCESS_TOKEN
    user_info = requests.get(request_url).json()
    return user_info


print self_info()
