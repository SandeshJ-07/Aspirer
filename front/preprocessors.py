from django.conf import settings
from .models import *

def follow_requests(request):
    if(request.user.is_authenticated):
        Request_Users = []
        CUser = Profile.objects.filter(user = request.user)[0]
        for i in CUser.follow_request:
            user = User.objects.filter(id = i)[0]
            P = Profile.objects.filter(user = user)[0]
            Request_Users.append({"P":P,"U":user})
        return {
            "Requests": CUser.follow_request,
            "Request_Users": Request_Users,
            "footer": True,
            "navbar" : True,
        }    
    return {"Requests": [], "footer":True, "navbar":True}