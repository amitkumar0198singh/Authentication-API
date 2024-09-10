from api.models import User


# Create you authentication functions here.
def authenticate(username: str, password: str) -> User:
    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        return user
    return None