#!/usr/bin/python3

class User:

    def __init__(self, user_id, spotify_user_id, email,
                 username, profile_photo, birthday, gender,
                 created_at, modified_at, country, refresh_token):
        self.user_id = user_id
        self.spotify_user_id = spotify_user_id
        self.email = email
        self.username = username
        self.profile_photo = profile_photo
        self.birthday = birthday
        self.gender = gender
        self.created_at = created_at
        self.modified_at = modified_at
        self.country = country
        self.refresh_token = refresh_token

    @property
    def user_id(self):
        """The user_id property."""
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def email(self):
        """The email property."""
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def username(self):
        """The username property."""
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def profile_photo(self):
        """The profile_photo property."""
        return self._profile_photo

    @profile_photo.setter
    def profile_photo(self, value):
        self._profile_photo = value

    @property
    def birthday(self):
        """The birthday property."""
        return self._birthday

    @birthday.setter
    def birthday(self, value):
        self._birthday = value

    @property
    def gender(self):
        """The gender property."""
        return self._gender

    @gender.setter
    def gender(self, value):
        self._gender = value

    @property
    def created_at(self):
        """The created_at property."""
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = value

    @property
    def modified_at(self):
        """The modified_at property."""
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value):
        self._modified_at = value

    @property
    def country(self):
        """The country property."""
        return self._country

    @country.setter
    def country(self, value):
        self._country = value

    @property
    def refresh_token(self):
        """The refresh_token property."""
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, value):
        self._refresh_token = value
