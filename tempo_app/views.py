from django.shortcuts import render, redirect
from .seed_artist import Artists, Merchs
from .models import Artist
from .main import *
from .main import get_token, search_for_artist
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Merch
import requests

# https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/#
# imported these for login, used to create a random 16 character string
import string
import random
# https://docs.python.org/3/library/urllib.request.html#urllib-examples
# to convert an object into a query string
import urllib.request
import urllib.parse


class StoredInfo:
    redirect_uri='https://tempo-clone-test-aaeef8af869b.herokuapp.com/callback'
    # redirect_uri='http://localhost:8000/callback'
    access_token = ''
    refresh_token = ''

class MerchCreate(CreateView):
    model = Merch
    fields = '__all__'

class MerchUpdate(UpdateView):
  model = Merch
  fields = '__all__'

class MerchDelete(DeleteView):
  model = Merch
  success_url = '/store'



def home(request):
    return redirect('login')

def landing(request):
    return render(request, 'tempo_app/landing.html')

def player(request, track_id):
    result = get_track(track_id)
    track={
        "img":result["album"]["images"][0]["url"],
        "artist_name":result["artists"][0]["name"],
        "track_name":result["name"],
        "track_id": track_id,
    }
    return render(request, 'tempo_app/player.html',{
        # 'access_token':StoredInfo.access_token,
        'access_token':localStorage.getItem('access_token'),
        'track':track,
    })

def merch(request):
    merchs = Merch.objects.all()
    return render(request, 'merch/merch.html', {'merchs': merchs})

def merch_detail(request, merch_id):
    merch = Merch.objects.get( id=merch_id )
    return render(request, 'merch/merch_detail.html', { 'merch': merch })

# Artist Detail
def artist(request, artist_name):
    c = Artist.objects.get(name=artist_name)
    merchs = c.merch_set.all()
    # merch_list=[]
    # for merch in merchs:
    #     merch_list.append({
    #         "item":merch.item,
    #         "description":merch.description,
    #         "price":merch.price,
    #         "image":merch.image
    #     })
    # use main.py functions(funtions to use spotify api)
    token = get_token()
    result = search_for_artist(token, artist_name)

    # Getting artist Id, necessary to get artist details
    artist_id = result["id"]

    # Getting artist top tracks using api
    songs = get_songs_by_artist(token, artist_id)

    # Putting all the song names into a list
    song_list = []
    for song in songs:
        song_list.append({
            'name':song['name'],
            'id':song["id"]
        })
    # Getting artist picture
    image_url = result["images"][0]["url"]
    return render(request, 'tempo_app/artist.html',{
        'artist': artist_name,
        'songs': song_list,
        'image_url': image_url,
        # 'merch_list':merch_list,
        'merchs':merchs,
    })


# Seed Artists(localhost:PORT/seed_artists/)
def seed_artists(request):
    for artist in Artists:
        c = Artist(name=artist['name'])
        c.save()
    seed_merch()
    return redirect('landing')

def seed_merch():
    for merch in Merchs:
        c = Artist.objects.get(name=merch['name'])
        c.merch_set.create(
            item=merch['item'],
            description=merch['description'],
            price=merch['price'],
            image=merch['image'],
            artist=merch['name']
            )
    return

def artist_api(request):
    artists = Artist.objects.all()
    artist_data = []
    token = get_token()
    for artist in artists:
        result = search_for_artist(token, artist.name)
        if result:
            artist_name = result["name"]
            image_url = result["images"][0]["url"]
            spotify_id = result["id"]
            existing_artist, created = Artist.objects.get_or_create(name=artist_name)
            existing_artist.spotify_id = spotify_id
            existing_artist.image_url = image_url
            existing_artist.save()
            artist_data.append({
                "name": artist_name,
                "image_url": image_url,
                "spotify_id": spotify_id
            })

    return render(request, 'tempo_app/artist_api.html', {'artist_data': artist_data})


# Login(basically just authorizing spotify)
# https://developer.spotify.com/documentation/web-api/tutorials/code-flow
# the documentation is in JS and uses express
# converting the code was a major challenge
# def login(request):
#     # var to specify how many characters the random string should be
#     N = 16
#     # state is a optional param which provides added security
#     # This provides protection against attacks such as cross-site request forgery
#     state = ''.join(random.choices(string.ascii_uppercase +
#                              string.digits, k=N))
#     # Scope are the permissions we want the user to authorize(can add more)
#     # https://developer.spotify.com/documentation/web-api/concepts/scopes
#     scope = 'user-read-private user-read-email user-top-read user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming user-read-playback-position';
#     # convert an object to url query form and save it
#     query_string = urllib.parse.urlencode({
#         'response_type': 'code',
#         'client_id': client_id,
#         'scope':scope,
#         'redirect_uri':StoredInfo.redirect_uri,
#         'state':state,
#     })
#     # redirect to the page that asks the user to authorize
#     # once authorized(or cancelled), redirects to redirect uri(stored here, but also saved on spotify app dashboard)
#     return redirect('https://accounts.spotify.com/authorize?'+query_string)

def login(request):
    codeVerifier = generateRandomString(128)
    # codeVerifier = 'tTipOAamz8fcpEgKTRZk3L5Ps6aMqgQv1CV8mYMxvL0Zxajoh0v0ImqOwJpHGRuPyt5qZocKsi1IlIwTyXQJSjILvYnsxzwj3bWQHYzrvHENGcSDWbadYhN8vkiN4Upb'
    # print('Code Verifier: '+ codeVerifier)
    codeChallenge = generateCodeChallenge(codeVerifier=codeVerifier)
    # print("Code Challenge: "+codeChallenge)
    state = generateRandomString(16)
    scope = 'user-read-private user-read-email user-top-read user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming user-read-playback-position';
    localStorage.setItem('code_verifier', codeVerifier)
    query_string = urllib.parse.urlencode({
        'response_type':'code',
        'client_id': client_id,
        'scope':scope,
        'redirect_uri':StoredInfo.redirect_uri,
        'state':state,
        'code_challenge_method':'S256',
        'code_challenge':codeChallenge
    })
    # print('Code Challenge: '+codeChallenge)
    # print('Code Verifier: '+codeVerifier)
    # print('Args: ' + query_string)
    return redirect('https://accounts.spotify.com/authorize?'+query_string)

def callback(request):
    code = request.GET['code']
    codeVerifier = localStorage.getItem('code_verifier')
    # print('Local Code Verifier: '+ codeVerifier)

    body = {
        'grant_type': 'authorization_code',
        'code':code,
        'redirect_uri':StoredInfo.redirect_uri,
        'client_id':client_id,
        'code_verifier':codeVerifier
    }
    headers={
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    url = 'https://accounts.spotify.com/api/token'

    result = post(url=url, headers=headers, data=body)
    json_result = json.loads(result.content)
    localStorage.setItem('access_token',json_result['access_token'])
    # StoredInfo.access_token = json_result['access_token']
    # StoredInfo.refresh_token = json_result['refresh_token']

    return redirect('landing')
# # https://developer.spotify.com/documentation/web-api/tutorials/code-flow
# def callback(request):
#     code = request.GET['code']
#     state = request.GET['state']

#     # First concatenate client id and client secret(important to have ":")
#     auth_string = client_id + ":" + client_secret

#     # Encode the concatenated string
#     auth_bytes = auth_string.encode("utf-8")

#     # Encode using base 64
#     #   base64... returns a base64 object and then it's converted into a string
#     auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

#     if state==None:
#         return redirect('login'+urllib.parse.urlencode({'error':'state_mismatch'}))
#     else:
#         url='https://accounts.spotify.com/api/token'
#         form = {
#             'code':code,
#             'redirect_uri':StoredInfo.redirect_uri,
#             'grant_type':'authorization_code',
#             }
#         headers = {
#             "Authorization":"Basic "+ auth_base64,
#             "Content-Type": "application/x-www-form-urlencoded"
#         }
#         result = post(url, headers=headers, data=form)
#         json_result = json.loads(result.content)
#         StoredInfo.access_token = json_result['access_token']
#         StoredInfo.refresh_token = json_result['refresh_token']
#     return redirect('landing')


def artist_search(request):
    artist_name = None
    songs = []
    image_url = None
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            token = get_token()  
            result = search_for_artist(token, query)  

            if result:
                artist_name = result["name"]
                image_url = result["images"][0]["url"]
                spotify_id = result["id"]
                songs = get_songs_by_artist(token, spotify_id)
                artist, created = Artist.objects.get_or_create(name=artist_name)
                artist.spotify_id = spotify_id
                artist.image_url = image_url
                artist.save()
    if artist_name is None:
        return render(request, 'tempo_app/artist_search.html')  

    return render(request, 'tempo_app/artist.html', {
        'artist': artist_name,
        'songs': songs,
        'image_url': image_url,
    })