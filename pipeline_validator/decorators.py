import jwt


def nexus_token_is_valid(function):
    """
    Decorator to check whether the nexus token is valid
    :param function:
    :return:
    """

    def wrapper(self):
        try:
            jwt.decode(self.token, options={"verify_signature": False})
            return function(self)
        except jwt.ExpiredSignatureError:
            raise ValueError("Access token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Access token is invalid")

    return wrapper
