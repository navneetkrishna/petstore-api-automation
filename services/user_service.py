from .base_service import BaseService


class UserClient(BaseService):
    """API client for the /user domain.

    Endpoint reference:
        POST   /user                     — Create a new user
        POST   /user/createWithArray     — Create users from an array
        POST   /user/createWithList      — Create users from a list
        GET    /user/login               — Log user into the system
        GET    /user/logout              — Log out current user
        GET    /user/{username}          — Get user by username
        PUT    /user/{username}          — Update user
        DELETE /user/{username}          — Delete user
    """

    USER_WITH_LIST_ENDPOINT = "/user/createWithList"
    USER_ENDPOINT           = "/user"
    USERNAME_ENDPOINT       = "/user{username}"
    LOGIN_ENDPOINT          = "/user/login"
    LOGOUT_ENDPOINT         = "/user/logout"




    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    def create_user(self, payload):
        """POST /user — Create a single user."""
        return self.post(self.USER_ENDPOINT, payload)

    def create_users_with_list(self, payloads):
        """POST /user/createWithList — Create multiple users at once."""
        return self.post(self.USER_WITH_LIST_ENDPOINT, payloads)

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def login(self, username, password):
        """GET /user/login — Log in and receive a session token."""
        return self.get(self.LOGIN_ENDPOINT, params={
            "username": username,
            "password": password
        })

    def logout(self):
        """GET /user/logout — Log out the current session."""
        return self.get(self.LOGOUT_ENDPOINT)

    # ------------------------------------------------------------------
    # Read / Update / Delete
    # ------------------------------------------------------------------

    def get_user(self, username):
        """GET /user/{username} — Retrieve a user by username."""
        return self.get(self.USERNAME_ENDPOINT)

    def update_user(self, username, payload):
        """PUT /user/{username} — Update a user's details."""
        return self.put(self.USERNAME_ENDPOINT, payload)

    def delete_user(self, username):
        """DELETE /user/{username} — Delete a user."""
        return self.delete(self.USERNAME_ENDPOINT)
