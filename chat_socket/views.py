import json

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from dwebsocket.decorators import accept_websocket
from django.core import serializers

from users.models import Users
from chat_socket.models import ChatRecord
from chat.send import WebSocketHandler


@accept_websocket
def conn(request):
    WebSocketHandler().connect(request)


def index(request):
    person_list = []
    request.session['msg'] = None
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
        username = request.POST.get('nickname')
        text = request.POST.get('text')
        record = ChatRecord.objects.create(username=username, text=text)
        record.save()
        json_success = {'status': 'success'}
        return HttpResponse(json.dumps(json_success), content_type='application/json')
    except Exception as e:
        json_fail = {'status': 'fail', 'msg': str(e)}
        return HttpResponse(json.dumps(json_fail), content_type='application/json')


def load_record(request):
    try:
        records = ChatRecord.objects.all()[20:]
        records_tbd = serializers.serialize('json', records)
        json_success = {'status': 'success', 'text': records_tbd}
        return HttpResponse(json.dumps(json_success), content_type='application/json')
    except Exception as e:
        json_fail = {'status': 'fail', 'msg': str(e)}
        return HttpResponse(json.dumps(json_fail), content_type='application/json')