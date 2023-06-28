#!usr/bin/python3
""" Module for all the routes managed by the app """

from flask import request, redirect, session, url_for, render_template
from soundhood import app
from soundhood.api_call import get_tokens, get_user_info, get_track_info, get_album_info, get_playlist_info, get_top_track_info
from soundhood.database import create_connection, save_user_info, get_user_db, get_top_tracks_db, get_top_tracks_from_other_users, get_user_track_db, get_tracks_from_other_users, get_other_users_db
from soundhood.recommendation_system import jaccard_similarity, jaccard_distance, not_common_items
import base64
import json
import requests
from os import getenv


client_id = getenv('CLIENT_ID')
client_secret = getenv('CLIENT_SECRET')
response_type = getenv('RESPONSE_TYPE')
redirect_url = getenv('REDIRECT_URL')
scope = getenv('SCOPE')
auth_url = f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type={response_type}&redirect_uri={redirect_url}&scope={scope}'


@app.route("/", methods=['GET', 'POST'])
@app.route("/login/", methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('index.html', authorization=auth_url)

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    code = request.args.get('code')
    access_token, refresh_token = get_tokens(client_id, client_secret, code, redirect_url)
    user_info = get_user_info(access_token)
    session['user_id'] = user_info['id']
    print(session['user_id'])
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM User Where spotify_user_id = %s", (session['user_id'],))
    result = cursor.fetchone()
    
    #if already in DB redirect to home
    if result:
        return redirect(url_for('home'))
    
    track_info = get_track_info(access_token)
    album_info = get_album_info(access_token)
    playlist_info = get_playlist_info(access_token)
    top_track = get_top_track_info(access_token)
    #if no in DB save all the info to the DB
    save_user_info(connection, refresh_token, user_info, track_info, album_info, playlist_info, top_track)
    return redirect(url_for('home'))


@app.route("/home/")
def home():
    if not 'user_id' in session:
        return redirect(url_for('login'))

    # query user data from DB
    connection = create_connection()
    cursor = connection.cursor()
    #user for template
    user_data = get_user_db(cursor)
    if user_data['profile_photo'] is None:
        user_data['profile_photo'] = 'https://www.coachhousevets.com/wp-content/uploads/2023/04/no-photo-icon-22.png'
    others_data = get_other_users_db(cursor)
    user_tt = get_top_tracks_db(cursor)
    others_tt = get_top_tracks_from_other_users(cursor)
    jaccard_scores = jaccard_similarity(user_tt, others_tt)
    jaccard_dist = jaccard_distance(jaccard_scores)
    not_common = not_common_items(user_tt, others_tt)
    cursor.close()
    connection.close()
    return render_template('home.html', user=user_data, others=others_data, matches=jaccard_scores, not_match=jaccard_dist, not_common=not_common)

@app.route("/tracks")
def tracks():
    if not 'user_id' in session:
        return redirect(url_for('login'))
    connection = create_connection()
    cursor = connection.cursor()
    #tracks user likes
    user_t = get_user_track_db(cursor)
    #tracks all other users likes
    others_t = get_tracks_from_other_users(cursor)
    #other users personal info
    others_data = get_other_users_db(cursor)
    #match percentage
    jaccard_scores = jaccard_similarity(user_t, others_t)
    #not match percentage
    jaccard_dist = jaccard_distance(jaccard_scores)
    #songs that other users like but not the logged user
    not_common = not_common_items(user_t, others_t)
    cursor.close()
    connection.close()
    return render_template('tracks.html', others=others_data, matches=jaccard_scores, not_match=jaccard_dist, not_common=not_common)

@app.route("/soundmates/")
def sound_mates():
    return render_template('soundmates.html')

@app.route("/user-profile/")
def user_profile():
    return render_template('user-profile.html')

@app.route("/logout/")
def logout():
    session.clear()
    return redirect('https://www.spotify.com/us/account/apps/')
