#!/usr/bin/python3
import requests
import base64
import json

# Function to get access and refresh tokens
def get_tokens(client_id, client_secret, code, redirect_uri):
    token_url = 'https://accounts.spotify.com/api/token'
    request_body = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }

    headers = {
        'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('utf-8')).decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(token_url, headers=headers, data=request_body)
    response_data = response.json()
    access_token = response_data['access_token']
    refresh_token = response_data['refresh_token']
    return access_token, refresh_token

def refresh_token(refresh_token):
    """ get new access_token in case the existing one expires """

    token_url = 'https://accounts.spotify.com/api/token'
    request_body = {
            'grant_type': 'refresh_token',
            'refresh_token': user.refresh_token
            }

    headers = {
            'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('utf-8')).decode('utf-8'),
            'Content-Type': 'application/x-www-form-urlencoded'
            }

    response = requests.post(token_url, headers=headers, data=request_body)
    response = response.json()

    access_token = response['access_token']

    return access_token


def get_user_info(access_token):
    url = 'https://api.spotify.com/v1/me'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)
    response_data = response.json()
    

    return response_data

def get_track_info(access_token):
    url = 'https://api.spotify.com/v1/me/tracks?limit=50&offset=0'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)
    response_data = response.json()


    return response_data


def get_album_info(access_token):
    url = 'https://api.spotify.com/v1/me/albums?limit=50&offset=0'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)
    response_data = response.json()


    return response_data

def get_playlist_info(access_token):
    url = 'https://api.spotify.com/v1/me/playlists?limit=50&offset=0'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)
    response_data = response.json()


    return response_data

def get_top_track_info(access_token):
    url = 'https://api.spotify.com/v1/me/top/tracks'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)
    response_data = response.json()


    return response_data
