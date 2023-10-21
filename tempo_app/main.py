# https://www.youtube.com/watch?v=WAmEZBEeNmg&t=838s
# Youtube tutorial was used to:
#   1. Understand how to get access token using client id and client secret
#   2. How to use the token to search for an artist
#   3. How to use token and artist id to search for songs
# The tutorial was basically used to understand how spotify api works
#   and to get ideas on how to display information on our app

# pip install  python-dotenv
# pip install requests
# pip install python-env
# pip install dotenv
# You need a .env file
#       file has CLIENT_ID=""
#           AND  CLIENT_SECRET=""
from dotenv import load_dotenv
import os
# Base64 imported because the concatenated string of clientId and client secret
#   needs to be encoded with base 64, then it can be sent to receive a token
import base64
# https://docs.python.org/3/library/hashlib.html#hashlib.sha256
import hashlib
# https://pypi.org/project/localStoragePy/
from localStoragePy import localStoragePy
import random
from requests import post, get, put
import json

# Will only load if there is a .env file created
load_dotenv()

localStorage = localStoragePy('tempo', 'text')

# Note: Research what os is
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

def get_token():
# Steps to get token
    # First concatenate client id and client secret(important to have ":")
    auth_string = client_id + ":" + client_secret

    # Encode the concatenated string
    auth_bytes = auth_string.encode("utf-8")

    # Encode using base 64
    #   base64... returns a base64 object and then it's converted into a string
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    # Steps to send request to accounts service api

    # Write out url we want to send request to
    url = "https://accounts.spotify.com/api/token"

    # headers associated with the request, 
    # we'll be sending a post request to the url
    headers = {
        "Authorization":"Basic "+ auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Gather data(basically the body of the request)
    data = {"grant_type": "client_credentials"}

    # Sending post request
    result = post(url, headers=headers, data=data)

    # JSON data is returned in a field known as .content from the result object
    # Convert the JSON data into a python dictionary so the information can be accessed
    # loads is load s, which is load from string
    json_result = json.loads(result.content)

    # Parse the token(saved in a field known as "access_token")
    token = json_result["access_token"]

    return token
# function for convience, will contruct the header we need using the token
#   for any requests
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# Write a function that allows us to search for an artist
def search_for_artist(token, artist_name):
    # endpoint url to search for an artist
    url = "https://api.spotify.com/v1/search"

    # construct header using header function
    headers = get_auth_header(token)

    # artist_name is the text value of whatever we're searching for
    #   type is a comma serparated list of items to search across, in this case only artist
    #   after type - we can pass optional arguments, such as limit so you only get
    #   the top search for an artist name(in the case multiple have the same name)
    query = f"?q={artist_name}&type=artist&limit=1"

    # now combine them all together for a query url
    query_url = url + query

    # now submit a get request(import get at the top with post)
    #   pass in query_url and headers
    result = get(query_url, headers=headers)

    # parse json result(loads is load s, for load from string)
    # json_result = json.loads(result.content)
    # parse using above json, but get items list inside artists dictionary
    # artists is inside result.content dictionary
    json_result = json.loads(result.content)["artists"]["items"]

    # conditional to check if an artist was returned
    if len(json_result)== 0:
        print("No Artist with this name exists...")
        return None
    # otherwise, return the first result(only one would exist since we set limit to 1 above)
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    # endpoint url to get top tracks for a specifi artist
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_user_top_items(token):
    url = 'https://api.spotify.com/v1/me/top/artists'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_track(track_id):
    url=f"https://api.spotify.com/v1/tracks/{track_id}"
    token = get_token()
    headers=get_auth_header(token)
    result = get(url=url,headers=headers)
    json_result = json.loads(result.content)
    return json_result


def pause_song(token):
    url = "https://api.spotify.com/v1/me/player/pause"
    headers = get_auth_header(token)
    put(url=url,headers=headers)


def play_song(token, track_id):
    print(track_id)
    track_id = f"spotify:track:{track_id}"
    url = "https://api.spotify.com/v1/me/player/play"
    headers = {
        "Authorization":"Bearer "+token,
        "Content-Type": "application/json"
    }
    data = {
    "uris": [
        track_id
        ],
    "position_ms": 0
    }
    # The request body needs to be in json format
    data = json.dumps(data)
    print(data)
    result = put(url=url, headers=headers, data=data)
    # pause_song(token)
    return result.json()

# https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow
def generateRandomString(length):
    text = ''
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    for i in range(length):
        text+=possible[random.randint(0,len(possible)-1)]
    return text

def generateCodeChallenge(codeVerifier):

    # https://docs.python.org/3/library/hashlib.html#hashlib.sha256
    h = hashlib.new('sha256')
    h.update(codeVerifier.encode('utf8'))
    digest = h.digest()
    digest = str(base64.b64encode(digest, altchars=b'-_'),"utf-8")
    digest = digest.replace('=','')
    # digest = base64.b64encode(digest, altchars=b'-:')

    return digest

# # This token will be used in future headers when requests to the api are sent
# #   requests such as trying to get artist info or album info
# token = get_token()

# # call search for artist using token
# result = search_for_artist(token, "ACDC")
# # print(result)
# # print(result["name"])
# # now that we only have the artist info we need, we can gather the artist id for further use
# artist_id = result["id"] # can be used to look up songs for an artist

# songs = get_songs_by_artist(token, artist_id)
# # print(songs) # shows that songs is a list of the top songs

# # printing each song name
# for idx, song in enumerate(songs):
#     print(f"{idx+1}. {song['name']}")