from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from github import Github
# Create your views here.

def index(request):
    if request.user.is_anonymous:
        raise PermissionDenied("Anonymous user not allowed.")
    if not request.user.profile:
        raise PermissionDenied("User does not have a profile")
    if not request.user.profile.token:
        raise PermissionDenied("user profile does not have a token")
    
    g = Github(request.user.profile.token)
    
    return render(request, "index.html", {"github_user": g.get_user()})