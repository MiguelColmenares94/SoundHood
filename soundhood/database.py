from flask import session
import mysql.connector
from mysql.connector import pooling

def create_connection():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'database': 'soundhood',
        'pool_name': 'soundhood_pool',
        'pool_size': 5
        
    }
    
    try:
        pool = mysql.connector.pooling.MySQLConnectionPool(**config)
        connection = pool.get_connection()
        print('Successfully connected to the MySQL database')
        return connection
    except mysql.connector.Error as err:
        print('Error connecting to the MySQL database:', err)
        return None


def save_user_info(connection, refresh_token, user_info, track_info, album_info, playlist_info, top_track):
    
    """ Save all user info in DB """
    #data to save into user table
    email = user_info.get('email')
    spotify_user_id = user_info.get('id')
    user_name = user_info.get('display_name')
    profile_photo = user_info.get('images')[0].get('url') if user_info.get('images') else None
    country = user_info.get('country')
    refresh_token = refresh_token

    query_user = "INSERT IGNORE  INTO User (email, spotify_user_id, user_name, profile_photo, country, refresh_token) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (email, spotify_user_id, user_name, profile_photo, country, refresh_token)
    
    cursor = connection.cursor()
    cursor.execute(query_user, values)
    cursor.close()

    #data to save into album table
    items = album_info.get("items")

    for item in items:
        spotify_album_id = item.get('album').get('id')
        album_name = item.get('album').get('name')
        cover_image = item.get('album').get('images')[0].get('url')
        spotify_url = item.get('album').get('external_urls').get('spotify')

        query_album = "INSERT IGNORE INTO Album (album_name, cover_image, spotify_url) VALUES (%s, %s, %s)"
        values = (spotify_album_id, album_name, cover_image, spotify_url)
        
        cursor = connection.cursor()
        cursor.execute(query_album, values)
        cursor.close()

        
    #data to save in track table
    items = track_info.get("items")

    for item in items:

        spotify_track_id = item.get('track').get('id')
        track_name = item.get('track').get('name')
        spotify_url = item.get('track').get('external_urls').get('spotify')
        cover_image = item.get('track').get('album').get('images')[0].get('url')

        query_track = "INSERT IGNORE INTO Track (spotify_track_id, track_name, spotify_url, cover_image) VALUES (%s, %s, %s, %s)"
        values = (spotify_track_id, track_name, spotify_url, cover_image)
        
        cursor = connection.cursor()
        cursor.execute(query_track, values)
        cursor.close()

    #data to save in playlist table
    items = playlist_info.get('items')
    
    for item in items:
        spotify_playlist_id = item.get('id')
        owner_id = int(item.get('owner').get('id')) if item.get('owner') else None
        spotify_url = item.get('external_urls').get('spotify') if item.get('external_urls') else None
        cover_image = item.get('images')[0].get('url')

        query_playlist = "INSERT IGNORE INTO Playlist (spotify_playlist_id, owner_id, spotify_url, cover_image) VALUES (%s, %s, %s, %s)"
        values = (spotify_playlist_id, owner_id, spotify_url, cover_image)
        
        cursor = connection.cursor()
        cursor.execute(query_playlist, values)
        cursor.close()


    #data to save in user_top_track table
    item = top_track.get('items')

    for item in items:
        query = "SELECT user_id  FROM User WHERE spotify_user_id = %s"
        cursor = connection.cursor()
        cursor.execute(query, (session['user_id'],))
        user_id = cursor.fetchone()
        cursor.close()

        query = "SELECT track_id FROM Track WHERE spotify_track_id = %s"
        value = (item.get('id'), )
        cursor = connection.cursor()
        cursor.execute(query, value)

        track_id = cursor.fetchone()
        cursor.close()

        query_top_track = "INSERT IGNORE INTO User_TopTrack (user_id, track_id) VALUES (%s, %s)"

        values = (user_id, track_id)
        
        cursor = connection.cursor()
        cursor.execute(query_top_track, values)
        cursor.close()

    #data to save in User_Album table
    item = album_info.get('items')

    for item in items:
        query = "SELECT user_id  FROM User WHERE spotify_user_id = %s"
        cursor = connection.cursor()
        cursor.execute(query, (session['user_id'],))
        user_id = cursor.fetchone()
        cursor.close()

        query = "SELECT album_id FROM Album WHERE spotify_album_id = %s"
        value = (item.get('album').get('id'),)
        cursor = connection.cursor()
        cursor.execute(query, value)

        album_id = cursor.fetchone()
        cursor.close()

        query_user_album = "INSERT IGNORE INTO User_Album (user_id, album_id) VALUES (%s, %s)"
        values = (user_id, album_id,)
        
        cursor = connection.cursor()
        cursor.execute(query_user_album, values)
        cursor.close()
    
    #data to save in User_Track
    items = track_info.get('items')

    for item in items:
        query = "SELECT user_id  FROM User WHERE spotify_user_id = %s"
        cursor = connection.cursor()
        cursor.execute(query, (session['user_id'],))
        user_id = cursor.fetchall()
        cursor.close()
        if user_id:
            user_id = user_id[0][0]  #get first element of the tuple
            print(user_id)

        query = "SELECT track_id FROM Track WHERE spotify_track_id = %s"
        value = (item.get('track').get('id'),)
        cursor = connection.cursor()
        cursor.execute(query, value)
        track_id = cursor.fetchall()
        cursor.close()
        if track_id:
            track_id = track_id[0][0] #get first element of the tuple
            print(track_id)

        query_user_track = "INSERT IGNORE INTO User_Track (user_id, track_id) VALUES (%s, %s)"
        values = (user_id, track_id,) if user_id and track_id else (None, None)

        cursor = connection.cursor()
        cursor.execute(query_user_track, values)
        cursor.close()

    #data to save in User_Playlist
    items = playlist_info.get('items')

    for item in items:
        query = "SELECT user_id  FROM User WHERE spotify_user_id = %s"
        cursor.execute(query, (session['user_id'],))
        user_id = cursor.fetchone()

        query = "SELECT playlist_id FROM Playlist WHERE spotify_playlist_id = %s"
        value = (item.get('id'),)
        cursor.execute(query, value)

        playlist_id = cursor.fetchone()


        query_user_playlist = "INSERT IGNORE INTO User_Playlist (user_id, playlist_id) VALUES (%s, %s)"
        values = (user_id, playlist_id)

        cursor.execute(query_user_playlist, values)


    connection.commit()
    cursor.close()
    connection.close()
    return

def get_user_db(cursor, u_id=None):
    if not u_id:

        query = "SELECT user_id, spotify_user_id, email, user_name, profile_photo, birthday, gender, created_at, country FROM User WHERE spotify_user_id = %s"

        cursor.execute(query, (session['user_id'],))

        user = cursor.fetchone()
    
        if user:
            keys = ('user_id', 'spotify_user_id', 'email', 'user_name', 'profile_photo', 'birthday', 'gender',
                'created_at', 'country')
            user = dict(zip(keys, user))
            return user
        else:
            return('User not in DB')

    if u_id:
        query = "SELECT user_name, profile_photo, birthday, gender, country FROM User WHERE user_id = %s"

        cursor.execute(query, (u_id,))

        user = cursor.fetchone()

        if user:
            keys = ('user_name', 'profile_photo', 'birthday', 'gender', 'country')
            user = dict(zip(keys, user))
            return user
        else:
            return('User not in DB')

def get_other_users_db(cursor):
    query = "SELECT user_id, user_name, profile_photo, birthday, gender, country FROM User WHERE spotify_user_id <> %s"
    cursor.execute(query, (session['user_id'],))

    users_data = []
    row = cursor.fetchone()
    while row is not None:
        users_data.append(row)
        row = cursor.fetchone()

    users_dict = {}
    for user_id, user_name, profile_photo, birthday, gender, country in users_data:
        users_dict[user_id] = {
                "id": user_id,
                "name": user_name,
                "profile_photo": profile_photo,
                "birthday": birthday,
                "gender": gender,
                "country": country
        }

    print (users_dict)
    return (users_dict)

def get_top_tracks_db(cursor, u_id=None):
    
    if not u_id:
        query = "SELECT user_id FROM User WHERE spotify_user_id = %s"
        cursor.execute(query, (session['user_id'],))
        user_id = cursor.fetchone()

        query = "SELECT track_id FROM User_TopTrack WHERE user_id = %s"
        cursor.execute(query, user_id)
        top_tracks = cursor.fetchall()

        if top_tracks:
            top_tracks = [item[0] for item in top_tracks]
            print(top_tracks)
            return top_tracks
        else:
            return ('There are no Top Tracks')

    if u_id:
        query = "SELECT t.track_name, t.album_name FROM Track AS t \
                 INNER JOIN User_TopTrack AS ut ON ut.track_id = t.track_id WHERE ut.user_id = %s"
        cursor.execute(query, (u_id,))
        rows = cursor.fetchall()
        
        if rows:
            tracks_album_list = []
            for row in rows:
                track_name, album_name = row
                if not track_name or not album_name:
                    continue
                tracks_album_list.append([track_name, album_name])

            print(tracks_album_list)
            return tracks_album_list
        else:
            return ('There are no Top Tracks')

def get_top_tracks_from_other_users(cursor):

    query = "SELECT user_id FROM User WHERE spotify_user_id = %s"
    cursor.execute(query, (session['user_id'],))
    user_id = cursor.fetchone()

    query = "SELECT ut.user_id, t.track_id FROM User_TopTrack ut INNER JOIN Track t \
             ON ut.track_id = t.track_id WHERE ut.user_id <> %s ORDER BY ut.user_id;"
    cursor.execute(query, user_id)
    other_users_top_track = cursor.fetchall()

    if other_users_top_track:
        users_top_tracks = {}

        for user, track in other_users_top_track:
            if user not in users_top_tracks:
                users_top_tracks[user] = []
            users_top_tracks[user].append(track)

        users_tracks_list = [{user: tracks} for user, tracks in users_top_tracks.items()]
        print(users_tracks_list)
        return (users_tracks_list)
    else:
        return print("Error retrieve all other users track")

def get_user_track_db(cursor):

    query = "SELECT user_id FROM User WHERE spotify_user_id = %s"
    cursor.execute(query, (session['user_id'],))
    user_id = cursor.fetchone()
    
    query = "SELECT track_id FROM User_Track WHERE user_id = %s"
    cursor.execute(query, user_id)
    tracks = cursor.fetchall()
    
    if tracks:
        tracks = [item[0] for item in tracks]
        print(tracks)
        return tracks
    else:
        return ('User have no track in Liked List')

def get_tracks_from_other_users(cursor):

    query = "SELECT user_id FROM User WHERE spotify_user_id = %s"
    cursor.execute(query, (session['user_id'],))
    user_id = cursor.fetchone()

    query = "SELECT ut.user_id, t.track_id FROM User_Track ut INNER JOIN Track t \
             ON ut.track_id = t.track_id WHERE ut.user_id <> %s ORDER BY ut.user_id;"
    cursor.execute(query, user_id)
    other_users_track = cursor.fetchall()

    if other_users_track:
        users_tracks = {}

        for user, track in other_users_track:
            if user not in users_tracks:
                users_tracks[user] = []
            users_tracks[user].append(track)

        users_tracks_list = [{user: tracks} for user, tracks in users_tracks.items()]
        print(users_tracks_list)
        return (users_tracks_list)
    else:
        return print("Error retrieve all other users track")

def filter_by_track(cursor, track_name):
    query = "SELECT track_id FROM Track WHERE track_name = %s;"
    cursor.execute(query, (track_name,))
    t_id = cursor.fetchone()

    query = "SELECT user_id FROM User_TopTrack WHERE track_id = %s;"
    cursor.execute(query, t_id)
    users = cursor.fetchall()

    users_list = []
    for user in users:
        query = "SELECT user_id, user_name, profile_photo, birthday, gender, country FROM User WHERE user_id = %s;"
        cursor.execute(query, user)
        user_data = cursor.fetchone()
        users_list.append(user_data)
    
    print(users_list)
    return users_list

