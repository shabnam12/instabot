import requests
import requests, urllib
import uuid
import matplotlib
import time
from termcolor import colored
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from graph import plotgraph

APP_ACCESS_TOKEN = '5703461132.e1ef995.dc620dfcff1541cd81f42f9b91217e85'
BASE_URL = 'https://api.instagram.com/v1/'
tag_list=[]
'''
Function declaration to get your own info
'''
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'
    time.sleep(5)

'''
Function declaration to get the ID of a user by username
'''

def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()
    time.sleep(5)
'''
Function declaration to get the info of a user by username
'''

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'
    time.sleep(5)

'''
Function declaration to get your own post
'''

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'
    time.sleep(5)

'''
Function declaration to get the recent post of a user by username
'''


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'
    time.sleep(5)
'''
Function declaration to get the ID of the recent post of a user by username
'''

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
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
    time.sleep(5)
'''
Fuction declaration to get the like list of the post
'''

def get_like_list(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    image_name = user_media['data'][0]['id']
    like = "https://api.instagram.com/v1/media/"+ image_name + "/likes?access_token="+ APP_ACCESS_TOKEN
    list1=requests.get(like).json()
    index=0
    for names in list1['data']:
        print list1['data'][index]['username']
        index = index + 1
    time.sleep(5)


'''
Function declaration to make a comment on the recent post of the user................
'''

def post_a_comment(insta_username):         #     Defining the function ......
    media_id = get_post_id(insta_username)    #   Getting media id by calling the get post id function....
    comment_text = raw_input(colored("Please Write Your comment: ",'blue'))
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print colored('POST request url : %s\n','blue') % (request_url)

    post_comment = requests.post(request_url, payload).json()    #   Fetching json data ...
    if post_comment['meta']['code'] == 200:             #      checking status code ......
        print colored("Successfully added a new comment!\n",'brown')
    else:
        print colored("Unable to add comment.Please Try again!!\n",'red')
    time.sleep(5)


'''
Function declaration to like the recent post of a user
'''


def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'
    time.sleep(5)

    '''
 Function declaration to Get the lists of comments on  the recent post of a user.........
    '''

def get_comment_list(insta_username):  # Defining the Function ............
    media_id = get_post_id(insta_username)  # Getting post id by passing the username .......
    request_url = BASE_URL + 'media/%s/comments?access_token=%s' % (media_id, APP_ACCESS_TOKEN)   #    passing the end points and media id along with access token ..
    print colored('GET request url : %s\n', 'blue') % (request_url)
    comment_list = requests.get(request_url).json()

    if comment_list['meta']['code'] == 200:  # checking the status code .....
        if len(comment_list['data']):
            position = 1
            print colored("List of people who commented on Your Recent post", 'blue')
            for _ in range(len(comment_list['data'])):
                if comment_list['data'][position-1]['text']:
                    print colored(comment_list['data'][position-1]['from']['username'],'magenta') +colored( ' said: ','magenta') + colored(comment_list['data'][position-1]['text'],'blue')      #    Json Parsing ..printing the comments ..
                    position = position+1
                else:
                    print colored('No one had commented on Your post!\n', 'red')
        else:
            print colored("There is no Comments on User's Recent post.\n", 'red')
    else:
        print colored('Status code other than 200 recieved.\n', 'red')
    time.sleep(5)
'''
Function declaration to Get the like lists on the recent post of a user.........
'''
def get_like_list(insta_username):            # Defining the Function ............
    media_id = get_post_id(insta_username)  # Getting post id by passing the username .......
    request_url = BASE_URL + 'media/%s/likes?access_token=%s' % (media_id, APP_ACCESS_TOKEN)    #    passing the end points and media id along with access token ..
    print colored('GET request url : %s\n', 'blue') % (request_url)
    like_list = requests.get(request_url).json()

    if like_list['meta']['code'] == 200:  # checking the status code .....
        if len(like_list['data']):
            position = 1
            print colored("List of people who Liked Your Recent post", 'blue')
            for users in like_list['data']:
                if users['username']!= None:
                    print position, colored(users['username'],'green')
                    position = position + 1
                else:
                    print colored('No one had liked Your post!\n', 'red')
        else:
            print colored("User Does not have any post.\n",'red')
    else:
        print colored('Status code other than 200 recieved.\n', 'red')
    time.sleep(5)

'''
Function Declaration For List Of Comments 
'''

def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id,APP_ACCESS_TOKEN)
    comment_list = requests.get(request_url).json()
    if comment_list['meta']['code']==200:
        if comment_list['data']:
            for x in range(0,len(comment_list['data'])):
                comments=comment_list['data'][x]['text']
                print comments
        else:
            print 'comments doesn\'t exist'
    else:
        print'status code other then 200 recieved'
    time.sleep(5)
'''
Function declaration to make a comment on the recent post of the user
'''


def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"
    time.sleep(5)
'''
Function declaration to make delete negative comments from the recent post
'''

def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'
    time.sleep(5)
'''
 Function declaration to get a post by caption.
'''
def get_post_by_caption(insta_username):
    caption = raw_input("Enter caption : ")
    user_id = get_user_id(insta_username)
    if user_id == None:
      request_url = BASE_URL + 'users/' + user_id + '/media/recent/?access_token=' + APP_ACCESS_TOKEN
    print('GET request url :', request_url)
    try:
        user_media = requests.get(request_url).json()
    except requests.exceptions.ConnectionError:
            item = 1
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            flag = False
            for post in user_media['data']:
                for anish in post['tags']:
                    if anish == caption:
                        flag = True
            if (flag):
                print "found"
            else:
                print " not found"
        else:
                print(colored('Status code other than 200 received!\n', 'red'))
    time.sleep(5)
'''
  A user's interests based on hashtag analysis of recent posts and plotted using matplotlib.
 '''
def get_tag_list(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    #tag_list=[]
    if user_media['meta']['code'] == 200:
        i=0
        rang=len(user_media['data'])
        for i in range(rang):
            list=[]
            if user_media['data'][i]['tags']!=None:


                tag_list.append(user_media['data'][i]['tags'])


        i+=1
    else:
        print'status code other then 200 recieved'
    print tag_list
    for temp in tag_list:
        list+=temp
    print list
    plotgraph(list)
    time.sleep(5)


def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Get a list of people who have liked the recent post of a user\n"
        print "f.Like the recent post of a user\n"
        print "g.Get a list of comments on the recent post of a user\n"
        print "h.Make a comment on the recent post of a user\n"
        print "i.Delete negative comments from the recent post of a user\n"
        print "j.Declaration to get a post by caption \n"
        print "l.Plot a graph of the tags of the user "
        print "k.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "e":
            insta_username = raw_input("Enter the username of the user: ")
            get_like_list(insta_username)
        elif choice == "f":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice == "g":
            insta_username = raw_input("Enter the username of the user: ")
            get_comment_list(insta_username)
        elif choice == "h":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice == "i":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
        elif choice == "j":
            insta_username = raw_input("Enter the username of the user:")
            get_post_by_caption(insta_username)
        #elif choice=='l':
         #   insta_username = raw_input("Enter the username of the user:")
          #  get_tag_list(insta_username)
           # generate_words()
        elif choice == "k":
            exit()
    else:
        print "wrong choice"
start_bot()