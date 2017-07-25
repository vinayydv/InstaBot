import requests

ACCESS_TOKEN = '5730266253.4e4a94a.cb49a51cb3f44aada44057d7eadee522'
BASE_URL = 'https://api.instagram.com/v1/'

def self_info():
    '''
    Make reuest url
    Get data through get
     Read json data through url
     return json data
    '''
    request_url = BASE_URL + "users/self/?access_token=%s"%ACCESS_TOKEN
    user_info = requests.get(request_url)
    user_info = user_info.json()

    '''
    if status code is 200
        if data is not empty
            print username
            print No of followers
            print No of people following
            Print number of media files    
    '''
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print "My username is %s" % user_info['data']['username']
            print "My number of followers is %s" % user_info['data']['counts']['followed_by']
            print "I am following %s persons" % user_info['data']['counts']['follows']
            print "I have made %s posts" % user_info['data']['counts']['media']
            print "Successfully fetched"
        else:
            print "No user found"
    else:
        print "Status code other than 200"
    return user_info


print self_info()

