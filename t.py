import requests, urllib
from termcolor import colored

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
    print 'Request url for user id is ' + request_url
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
    print 'Request url for user info is ' + request_url
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


#fuction to get own posts
def get_own_post():
    '''
    get reqeust url
    get json data
    print required posts
    :return:
    '''
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % ACCESS_TOKEN
    print 'GET request url : %s' % request_url
    own_media = requests.get(request_url).json()
    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            own_post_id = own_media['data'][0]['id']
            print 'My own post id is %s' % own_post_id
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your post is downloaded.'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'



#function to get other users post
def get_users_post(insta_username):
    '''
    get user id
    '''
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()

    '''
    get reqeust url
    get json data
    print required posts
    :return:
    '''
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request for user recent post : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            user_post_id = user_media['data'][0]['id']
            print 'User post id is %s' % user_post_id
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'User post is downloaded.'
        else:
            print "There is no recent post!"
    else:
        print "Status code other than 200 received!"
    return None


#function to start insta_bot
def start_bot():

    '''
    show menu
    take input
    run following function
    '''

    while True:
        print colored("Hello Dear", "green")
        print colored("Welcome to InstaBot!", "red"), colored("\nPlease select what do you want me to do !", "red")
        print colored('1. Get your own info', 'yellow')
        print colored('2. Get details of a user using username', 'yellow')
        print colored('3. Get details of a own recent posts', 'yellow')
        print colored('4. Get details of a user recent posts using username', 'yellow')
        print colored('e. Exit\n', 'yellow')
        choice = raw_input(colored('Please select from above options : ', 'green'))
        if choice == '1':
            self_info()

        elif choice == '2':
            insta_username = raw_input('Enter the username you want to search : ')
            get_user_info(insta_username)
            print '\n'

        elif choice == '3':
            get_own_post()
            print '\n'

        elif choice == '4':
            insta_username = raw_input('Enter the username you want to search : ')
            get_users_post(insta_username)
            print '\n'

        elif choice == 'e':
            exit()

        else:
            print 'Wrong choice'


start_bot()