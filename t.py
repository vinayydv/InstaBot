import requests


ACCESS_TOKEN = '5730266253.4e4a94a.cb49a51cb3f44aada44057d7eadee522'
BASE_URL = 'https://api.instagram.com/v1/'



#Fucntion to get self info
def self_info():
    '''
    Make request url
    Get data through get
     Read json data through url
     return json data
    '''
    request_url = BASE_URL + "users/self/?access_token=%s" % ACCESS_TOKEN
    user_info = requests.get(request_url)
    user_info = user_info.json()

    '''
    if status code is 200
        if data is not empty
            print required info   
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

#Fucntion to get user id
def get_user_id(insta_username):
    '''
    Make request url
    Get data through get
     Read json data through url
     return json data
    '''
    request_url = BASE_URL + "users/search?q=%s&access_token=%s" %(insta_username, ACCESS_TOKEN)
    print 'Request url is' + request_url
    user_info = requests.get(request_url)
    user_info = user_info.json()

    '''
    if status code is 200
        if data is not empty
            print required info   
    '''
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
           return user_info['data'][0]['id']
        else:
            print "No user found"
    else:
        print "Status code other than 200"
        exit()
    return user_id


#function to get user info
def get_user_info(insta_username):
    '''
    get user id
    check if it exists and if not then exit
    '''
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exists'
        exit()
    '''
    get request url
    print required info
    '''
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id,ACCESS_TOKEN)
    print 'Request usrl is' + request_url
    user_info = requests.get(request_url).json()
    '''
        if status code is 200
            if data is not empty
                print required info   
        '''

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username is: %s' % (user_info['data']['username'])
            print 'No. of user followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people user is following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'

    return user_info


