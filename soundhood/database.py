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


def create_tables():
    connection = create_connection()
    if connection is None:
        print('can\'t connect with DB')
        return
    
    cursor = connection.cursor()
    
    # Check if the tables exists
    cursor.execute("SHOW TABLES LIKE 'User'")
    result = cursor.fetchone()
    if result:
        print("Tables already exists :)")
        return

    # SQL statements to create tables
    create_users_table = '''
    CREATE TABLE IF NOT EXISTS User (
     user_id INT AUTO_INCREMENT PRIMARY KEY,
     spotify_user_id VARCHAR(255),
     email VARCHAR(255) NOT NULL,
     user_name VARCHAR(255),
     profile_photo VARCHAR(255),
     birthday DATE,
     gender VARCHAR(255),
     created_at DATETIME,
     modified_at DATETIME,
     country VARCHAR(255),
     refresh_token VARCHAR(255)
);
    '''
    
    create_album_table = '''
    CREATE TABLE IF NOT EXISTS Album (
     album_id INT AUTO_INCREMENT PRIMARY KEY,
     spotify_album_id VARCHAR(255),
     album_name VARCHAR(255),
     cover_image VARCHAR(255),
     spotify_url VARCHAR(255)
    );
    '''

    create_track_table = '''
    CREATE TABLE IF NOT EXISTS Track (
     track_id INT AUTO_INCREMENT PRIMARY KEY,
     spotify_track_id VARCHAR(255),
     spotify_album_id VARCHAR(255),
     track_name VARCHAR(255),
     spotify_url VARCHAR(255),
     cover_image VARCHAR(255)
    );
    '''
   
    create_playlist_table = '''
    CREATE TABLE IF NOT EXISTS Playlist (
     playlist_id INT AUTO_INCREMENT PRIMARY KEY,
     spotify_playlist_id VARCHAR(255),
     owner_id INT,
     spotify_url VARCHAR(255),
     cover_image VARCHAR(255)
    );
    '''

    create_user_album_table = '''
    CREATE TABLE IF NOT EXISTS User_Album (
        user_id INT,
        album_id INT,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (album_id) REFERENCES Album(album_id),
        PRIMARY KEY (user_id, album_id)
        );
        '''

    create_user_track_table = '''
    CREATE TABLE IF NOT EXISTS User_Track (
        user_id INT,
        track_id INT,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (track_id) REFERENCES Track(track_id),
        PRIMARY KEY (user_id, track_id)
        );
        '''

    create_user_playlist_table = '''
    CREATE TABLE IF NOT EXISTS User_Playlist (
        user_id INT,
        playlist_id INT,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id),
        PRIMARY KEY (user_id, playlist_id)
        );
        '''

    create_user_top_track_table = '''
    CREATE TABLE IF NOT EXISTS User_TopTrack (
        user_id INT,
        track_id INT,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (track_id) REFERENCES Track(track_id),
        PRIMARY KEY (user_id, track_id)
         );
        '''

    

    # Execute table creation statements
    try:
        cursor.execute(create_users_table)
        cursor.execute(create_album_table)
        cursor.execute(create_track_table)
        cursor.execute(create_playlist_table)
        cursor.execute(create_user_album_table)
        cursor.execute(create_user_track_table)
        cursor.execute(create_user_playlist_table)
        cursor.execute(create_user_top_track_table)
        connection.commit()
        print('Tables created successfully')
    except mysql.connector.Error as err:
        print('Error creating tables:', err)
        connection.rollback()
    
    # Close the cursor and connection
    cursor.close()
    connection.close()
    return

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

def get_user_db(cursor):

    query = "SELECT user_name, profile_photo, country FROM User WHERE spotify_user_id = %s"

    cursor.execute(query, (session['user_id'],))

    user = cursor.fetchone()
    
    if user:
        keys = ('user_name', 'profile_photo', 'country')
        user = dict(zip(keys, user))
        return user
    else:
        return('User not in DB')

def get_other_users_db(cursor):
    query = "SELECT user_id, user_name, profile_photo, country FROM User WHERE spotify_user_id <> %s"
    cursor.execute(query, (session['user_id'],))

    users_data = []
    row = cursor.fetchone()
    while row is not None:
        users_data.append(row)
        row = cursor.fetchone()

    users_dict = {}
    for user_id, user_name, profile_photo, country in users_data:
        users_dict[user_id] = {
                "name": user_name,
                "profile_photo": profile_photo,
                "country": country
        }

    print (users_dict)
    return (users_dict)

def get_top_tracks_db(cursor):
    
    query = "SELECT user_id FROM User WHERE spotify_user_id = %s"
    cursor.execute(query, (session['user_id'],))
    user_id = cursor.fetchone()

    query = "SELECT track_id FROM User_TopTrack WHERE user_id = %s"
    cursor.execute(query, user_id)
    top_tracks = cursor.fetchall()

    if top_tracks:
        return top_tracks
    else:
        return ('There are no Top Tracks')

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