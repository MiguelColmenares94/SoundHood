<h1 align="center"> Soundhood </h1>

![Soundhood](./example/login.jpeg)

## Introduction

Soundhood is a web application that leverages [Spotify's API](https://developer.spotify.com/documentation/web-api) to collect data from users, such as the songs they like the most, the most played songs, the albums they like the most, and much more. It analyzes this data and provides personalized recommendations to users based on their music preferences. Soundhood identifies other users who share similar musical tastes and suggests possible musical matches.

- Read this [Article](https://www.linkedin.com/pulse/we-sound-better-together-introducing-soundhood-app-music-miguel%3FtrackingId=bx0TVu3tTmOImmOkAk6FHQ%253D%253D/?trackingId=bx0TVu3tTmOImmOkAk6FHQ%3D%3D) to know more about our app. 
- You can see a video demonstration of Soundhood [here](https://youtu.be/0flNVK7fxNc)
## Features

- User Authentication
- Data Gathering
- Similarity Analysis
- Compatibility Scores
- Matching Recommendations
- Detailed Profiles

## Installation
![Python](https://logos-world.net/wp-content/uploads/2021/10/Python-Logo.png)

This installation guide is oriented to Ubuntu 22.04.2 for compatibility problems check your OS documentation.

1. Make sure you have python3 installed, the app was created using python 3.10.6.

2. Create a virtual environment with Python's [venv module](https://docs.python.org/3/library/venv.html)

```
python3 -m venv .venv
```

3. Activate the virtual environment

```
. .venv/bin/activate
```

3. Install all the required dependencies with pip

```
pip install -r requirements.txt
```

4. Install mysql-server

```
sudo apt install mysql-server
```

5. Start the MySQL service

```
sudo systemctl start mysql
```

6. Load all environment variables

```
source env.txt
```
NOTE: if you want to close the virtual environment just type ```deactivate``` in your CLI

## Usage

To run the web app just write in your CLI

```
flask run
```

After that the web server will start running, by default it runs in ```http://127.0.0.1:5000/```

## Configuration

In order for the app to work properly you need to [create an app](https://developer.spotify.com/documentation/web-api/concepts/apps) in spotify developer dashboard and set some environment variables:

1. Create a file named env.txt

```
vim env.txt
```

2. Then add all these lines into env.txt

```
export FLASK_APP=run.py
export CLIENT_ID=[client id given by spotify after created the app]
export CLIENT_SECRET=[client secret given by spotify after created the app]
export RESPONSE_TYPE='code'
export REDIRECT_URL='http://127.0.0.1:5000/callback' [you can use your own URL here]
export SCOPE='user-read-email user-library-read user-read-recently-played user-top-read user-read-private'
export USER_DB=[your mysql user]
export PASS_DB=[your mysql password]
export HOST_DB=[your host]
export NAME_DB=[your DB name]
export POOL_NAME=[your pool connection name]
export POOL_SIZE=5 (you can modify the value)
```


## Contribute

We are open to contributions, team work is the key to success, just write us (links in credit section)

## License

MIT License

## Credits

- [Miguel Colmenares](https://www.linkedin.com/in/miguel-colmenaresp/)
- [Marcelo Vizcarra](https://www.linkedin.com/in/marcelo-vizcarra-7459841b1/)

## Roadmap

During the first phase the main thing is to finish the basic functionalities of the app, to make sure that each page of recommendations gives good results to the user and is user friendly.

In the second phase we will start with the development of the app for mobile phones.
