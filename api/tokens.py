import jwt
import datetime
from django.conf import settings


# Create your tokens here.
def generate_token(username: str, type: str, minutes=0, days=0):
    payload = {
        'username': username,
        'type': type,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes, days=days),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def verify_token(token: str, type: str) -> bool:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        if payload['type'] == type:
            return True
        return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    except Exception:
        return False
    

def get_username_from_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None