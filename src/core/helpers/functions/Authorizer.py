import os
import jwt

from src.core.helpers.http.http import Unauthorized


class Authorizer:
    def __init__(self):
        self.secret = os.environ.get("JWT_SECRET")

    def authorize(self, token: str):
        """
        Authorizes the request by validating the JWT token.
        """
        try:

            # Decode the token
            decoded = jwt.decode(token, self.secret, algorithms=["HS256"])

            return decoded

        except Exception as e:
            return Unauthorized("Unauthorized", str(e)).to_dict()
