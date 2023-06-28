-- Go to DB
USE soundhood;

-- Users table
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

-- Album table
CREATE TABLE IF NOT EXISTS Album (
     album_id INT AUTO_INCREMENT PRIMARY KEY,
     spotify_album_id VARCHAR(255),
     album_name VARCHAR(255),
     cover_image VARCHAR(255),
     spotify_url VARCHAR(255)
    );

-- Track table
CREATE TABLE IF NOT EXISTS Track (
     track_id INT AUTO_INCREMENT PRIMARY KEY,
     spotify_track_id VARCHAR(255),
     spotify_album_id VARCHAR(255),
     track_name VARCHAR(255),
     spotify_url VARCHAR(255),
     cover_image VARCHAR(255)
    );

-- Playlist table
CREATE TABLE IF NOT EXISTS Playlist (
     playlist_id INT AUTO_INCREMENT PRIMARY KEY,
     spotify_playlist_id VARCHAR(255),
     owner_id INT,
     spotify_url VARCHAR(255),
     cover_image VARCHAR(255)
    );

-- User_Album table
CREATE TABLE IF NOT EXISTS User_Album (
        user_id INT,
        album_id INT,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (album_id) REFERENCES Album(album_id),
        PRIMARY KEY (user_id, album_id)
        );

-- User_Track table
CREATE TABLE IF NOT EXISTS User_Track (
        user_id INT,
        track_id INT,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (track_id) REFERENCES Track(track_id),
        PRIMARY KEY (user_id, track_id)
        );

-- User_Playlist table
CREATE TABLE IF NOT EXISTS User_Playlist (
        user_id INT,
        playlist_id INT,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id),
        PRIMARY KEY (user_id, playlist_id)
        );

-- User_TopTrack table
CREATE TABLE IF NOT EXISTS User_TopTrack (
        user_id INT,
        track_id INT,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (track_id) REFERENCES Track(track_id),
        PRIMARY KEY (user_id, track_id)
        );
