from rest_framework.authtoken.models import Token

def get_user(request):
    try:
        token = request.COOKIES["token"]
        user = Token.objects.get(key=token).user
    except:
        return None
    return user