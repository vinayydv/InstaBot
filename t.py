import requests, urllib, sys
from termcolor import colored
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


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
    print 'GET request url for my own info : %s' % request_url
    own_media = requests.get(request_url).json()
    if own_media['meta']['code'] == 200:
        if len(own_media['data']):

            '''
            If you want to download your own post
            '''

            own_post_id = own_media['data'][0]['id']
            print 'My own post id is %s' % own_post_id
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your recent post is downloaded.'


            '''
            If you want to download the post with most number of comments 
            '''

            question = raw_input("Do you want to know the post with most number of comments? (Y, N) ")
            if question.upper() == "Y":
                num_comments = 0
                '''
                loop to get the post with most number of comments
                '''
                for a in range(len(own_media['data'])):
                    if own_media['data'][a]['comments']['count'] >= num_comments:
                        num_comments = own_media['data'][a]['comments']['count']
                        number = a

                image_url = own_media['data'][number]['images']['standard_resolution']['url']
                print image_url
                post_id = own_media['data'][number]['id']
                print 'Post id of the post with most number of comments is %s ' % post_id

        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

    return own_post_id


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
            '''
             If you want to download your own post
            '''

            user_post_id = user_media['data'][0]['id']
            print 'User post id is %s' % user_post_id
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Image url for recent post is %s ' % image_url
            print 'User post is downloaded.'

            '''
             If you want to download the post with most number of comments 
            '''

            question = raw_input("Do you want to download the post with most number of likes? (Y, N) ")
            if question.upper() == "Y":
                num_likes = 0

                '''
                loop to get the post with most number of comments
                '''

                for a in range(len(user_media['data'])):
                    if user_media['data'][a]['likes']['count'] >= num_likes:
                        num_likes = user_media['data'][a]['likes']['count']
                        number = a

                image_url = user_media['data'][number]['images']['standard_resolution']['url']
                print image_url
                post_id = user_media['data'][number]['id']
                print 'Post id of the post with most number of comments is %s ' % post_id

        else:
            print "There is no recent post!"
    else:
        print "Status code other than 200 received!"
    return user_post_id


#Fucntion to get recent media liked by user


def get_recent_media():


    '''
    Make request url
    Get data through get
     Read json data through url
     return json data
    '''
    request_url = BASE_URL + "users/self/media/liked?access_token=%s" % ACCESS_TOKEN
    print 'Request url for recent media liked is ' + request_url
    user_info = requests.get(request_url)
    user_info = user_info.json()

    '''
    if status code is 200
        if data is not empty
            print required info   
    '''
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            image_url = user_info['data'][0]['images']['standard_resolution']['url']
            print 'Url of the media recently liked by the user is %s ' % image_url
            post_id = user_info['data'][0]['id']
            print 'Post id of the recently liked by the user is %s ' % post_id
            return post_id
            return user_info['data'][0]['id']

        else:
            print "No user found"
    else:
        print "Status code other than 200"
        exit()
    return user_info


#function to get the post id of a user's recent posts


def get_post_id(insta_username):

    '''
    Check if user exists or not
    '''

    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()

    '''
      Make request url
      Get data through get
      Read json data through url
      return json data
    '''

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


#function to get the recent comments on a media of a user

def get_media_comments(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, ACCESS_TOKEN)
    post_comments = requests.get(request_url).json()
    print 'Get request URL for recent comments is: %s ' % request_url

    if post_comments['meta']['code'] == 200:
        if len(post_comments['data']):
            b = 1
            for a in range(len(post_comments['data'])):
                print ' comment number %s : %s' % (b, post_comments['data'][a]['text'])
                b = b+1

        else:
            print "No comments found!"
        print '\n Comments fetched successfully!'
        exit()

    else:
        print "Status code other than 200 received"
        exit()

#Function to delete negative comments


def delete_negative_comment(insta_username):
    #get media id
    media_id = get_post_id(insta_username)
    '''
    make request url
    get json data
    '''

    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            # Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())

                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % comment_text
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, ACCESS_TOKEN)
                    print 'DELETE request url : %s' % delete_url
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % comment_text

        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'




#function to like the most recent post of a user

def like_a_post(insta_username):

    '''
    Get media id
    make post payload and url

    :param insta_username:
    :return:
    '''

    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % media_id
    payload = {"access_token": ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()

    '''
    Check if like was succesful or not
    '''

    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

    '''
    Function declaration to make a comment on the recent post of the user
    '''

def post_a_comment(insta_username):
    '''
    get media id
    '''
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Enter the comment : ")
    payload = {"access_token": ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % media_id
    print 'POST request url : %s' % request_url

    make_comment = requests.post(request_url, payload).json()
    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


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
        print colored('5. Get recent media liked byt the user', 'yellow')
        print colored('6. Like the recent post of a  user', 'yellow')
        print colored('7. Comment on the recent post of a  user', 'yellow')
        print colored('8. Get recent comments on a post of a user', 'yellow')
        print colored('9. Delete negative comments from a user post', 'yellow')

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

        elif choice == '5':
            get_recent_media()
            print '\n'

        elif choice == '6':
            insta_username = raw_input('Enter the username whose recent post you want to like : ')
            like_a_post(insta_username)
            print '\n'

        elif choice == '7':
            insta_username = raw_input('Enter the username whose recent post you want to comment on : ')
            post_a_comment(insta_username)
            print '\n'

        elif choice == '8':
            insta_username = raw_input('Enter the username whose  post comments you want to see : ')
            get_media_comments(insta_username)
            print '\n'

        elif choice == "9":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)

        elif choice == 'e':
            exit()

        else:
            print 'Wrong choice'


start_bot()