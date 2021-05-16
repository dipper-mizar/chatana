import json

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from dwebsocket.decorators import accept_websocket

from users.models import Users
from chat.send import WebSocketHandler


@accept_websocket
def conn(request):
    WebSocketHandler().connect(request)


def index(request):
    person_list = []
    obj = Users.objects.filter(status=True)
    for active_person in obj:
        person_list.append(active_person.name)
    nickname = request.session.get('nickname')
    if Users.objects.filter(name=nickname, status=True):
        return render(request, 'chat.html', {'person_list': person_list})
    return render(request, 'login.html')


@csrf_exempt
def save(request):
    try:
        text = request.POST.get('text')
        name = request.POST.get('nickname')
        with open('static/record/record.txt', 'a+', encoding='utf-8') as record:
            record.write(name + ' ' + text + '\n')
        json_success = {'status': 'success'}
        return HttpResponse(json.dumps(json_success), content_type='application/json')
    except Exception as e:
        json_fail = {'status': 'fail', 'msg': str(e)}
        return HttpResponse(json.dumps(json_fail), content_type='application/json')
