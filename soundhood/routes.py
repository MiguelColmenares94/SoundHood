#!usr/bin/python3
""" Module for all the routes managed by the app """

from flask import request, redirect, session, url_for, render_template
from soundhood import *
from soundhood.models import *
import base64
import json
import requests


client_id = 
client_secret = 
response_type = 'code'
redirect_url = 'http://127.0.0.1:5000/callback'
scope = 'user-read-email user-library-read user-read-recently-played user-top-read user-read-private'
auth_url = f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type={response_type}&redirect_uri={redirect_url}&scope={scope}'


@app.route("/")
def test():
    return render_template('home.html', login=auth_url)

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    code = request.args.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    request_body = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_url
            }

    headers = {
            'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('utf-8')).decode('utf-8'),
            'Content-Type': 'application/x-www-form-urlencoded'
            }

    response = requests.post(token_url, headers=headers, data=request_body)
    response = response.json()
    access_token = response['access_token']
    refresh_token = response['refresh_token']

    if not access_token:
        new_token()
    
    # URL para hacer el llamado a la api
    url = 'https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=50&offset=0'
    headers = {
            'Authorization': 'Bearer ' + access_token
            }

    result = requests.get(url, headers=headers)
    result = result.json()
    
    # test para guardar informacion obtenida con la api a BD (completado)
    """
    user1 = User(user_name=user_data['display_name'], email=user_data['email'])
    db.session.add(user1)
    db.session.commit()
    """
    return render_template('test.html', result=result)



def new_token():
    """ obtener un nuevo access token en caso de que expire """

    token_url = 'https://accounts.spotify.com/api/token'
    request_body = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
            }

    headers = {
            'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('utf-8')).decode('utf-8'),
            'Content-Type': 'application/x-www-form-urlencoded'
            }

    response = requests.post(token_url, headers=headers, data=request_body)
    response = response.json()
    
    access_token = response['access_token']

    return access_token
