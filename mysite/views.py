
from django.db import connection, connections, transaction
from django.contrib.sessions.models import Session
from django.http import HttpResponse, StreamingHttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.cache import cache
from django.shortcuts import render
from mysite.basics import ME
from mysite.basics import login_exempt
import random, time, logging
log = logging.getLogger('log')

@login_exempt
def api_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return {'id': user.id, 'name': user.username, 'sessionid': request.session.session_key}
        #api登入 请求头带上 Cookie: sessionid=xxx
    else:
        raise ME(ME.login)

def api_logout(request):
    logout(request)
    return 1

@login_exempt
def index(request):
    return render(request, 'index.html')




