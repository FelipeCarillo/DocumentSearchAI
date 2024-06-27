import os
import jwt

from src.core.helpers.http.http_codes import Unauthorized
from src.core.helpers.exeptions.exceptions import UnauthorizedAccess


class Authorizer:
    def __init__(self):
        self.secret = os.environ.get("JWT_SECRET")

    def authorize(self, token: str) -> bytes:
        """
        Authorizes the request by validating the JWT token.
        args:
            token: str: JWT token
        return:
            bytes: decoded token
        """
        try:

            # Decode the token
            decoded = jwt.decode(token, self.secret, algorithms=["HS256"])

            return decoded

        except Exception as e:
            # Raise an exception if the token is invalid or expired
            raise UnauthorizedAccess("Token is invalid or expired.")
