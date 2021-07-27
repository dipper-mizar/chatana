from django.shortcuts import redirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _

from users.models import Users


@csrf_exempt
def login(request):
    if request.method == "GET":
        request.session['msg'] = None
        return render(request, 'login.html')
    elif request.method == "POST":
        try:
            user = Users.objects.get(name=request.POST.get('nickname'))
            if user.password != request.POST.get('password'):
                request.session['msg'] = 'Invalid username or password!'
                return render(request, 'login.html')
        except Exception as e:
            request.session['msg'] = 'Invalid username or password!'
        request.session['nickname'] = request.POST.get('nickname')
        Users.objects.filter(name=request.POST.get('nickname')).update(status=True)
        return redirect('/chat/')
    return HttpResponse('Unsupported method!')


def logout(request):
    nickname = request.GET.get('nickname')
    if nickname:
        try:
            request.session.flush()
            Users.objects.filter(name=nickname).update(status=False)
        except Exception as e:
            return redirect('/user/login/')
    return redirect('/user/login/')


@csrf_exempt
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        name = request.POST.get('nickname')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if name and password1 and password2:
            if Users.objects.filter(name=name):
                request.session['msg'] = 'User already exist.'
                return render(request, 'register.html')
            if password1 != password2:
                request.session['msg'] = 'Two passwords do not match up.'
                return render(request, 'register.html')
            user = Users.objects.create(name=name, password=password1)
            user.save()
            request.session.flush()
            return redirect('/user/login/')
        request.session['msg'] = 'Exist null parameter(s).'
        return render(request, 'register.html')