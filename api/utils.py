from rest_framework.authtoken.models import Token

def get_user(request):
    try:
        token = request.META.get("HTTP_AUTHORIZATION").split()[-1]
        user = Token.objects.get(key=token).user
    except:
        return None
    return user