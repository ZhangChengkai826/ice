from django.shortcuts import render
from . import models

# -*- coding:utf-8 -*-

# Create your views here.
def index(request):
    postData = request.POST
    fill_dict = {
        'username': None,
        'repeatUName': 0,
        'noMatchUName': 0,
        'wrongPwd': 0,
        'successLogin': 0,
    }

    # Handle log in procedure
    if 'username' in postData:
        username = postData['username']
        # Test whether the username is in the Database
        if not models.APPUser.objects.filter(username=username):
            fill_dict['noMatchUName'] = 1
            return render(request, 'index.html', fill_dict)

        pwd = postData['pwd']
        targetUser = models.APPUser.objects.get(username=username)
        # Test whether the password is right
        if pwd != targetUser.password:
            fill_dict['wrongPwd'] = 1
            return render(request, 'index.html', fill_dict)

        # Successfully log in
        fill_dict['successLogin'] = 1
        fill_dict['username'] = targetUser.username
        return render(request, 'index.html', fill_dict)

    # Handle sign up procedure
    if 'username_s' in postData:
        username_s = postData['username_s']
        # Test whether the username has been registered
        if models.APPUser.objects.filter(username=username_s):
            fill_dict['repeatUName'] = 1
            return render(request, 'index.html', fill_dict)
        pwd_s = postData['pwd_s']
        appUser = models.APPUser.objects.create(
            username=username_s,
            password=pwd_s,
            fName=u"某",
            lName=u"人",
            gender="SECRET",
            birthdayY=0,
            birthdayM=0,
            birthdayD=0,
            hobbies="N/A"
        )
        appUser.save()

    return render(request, 'index.html', fill_dict)