from django.shortcuts import render
from . import models

# -*- coding:utf-8 -*-

# Create your views here.
def index(request):
    postData = request.POST
    getData = request.GET
    fill_dict = {
        'username': None,
        'fName': None,
        'lName': None,
        'gender': None,
        'birY': None,
        'birM': None,
        'birD': None,
        'hobbies': None,
        'repeatUName': 0,
        'noMatchUName': 0,
        'wrongPwd': 0,
        'successLogin': 0,
        'openLogin': 1
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
        fill_dict['fName'] = targetUser.fName
        fill_dict['lName'] = targetUser.lName
        fill_dict['gender'] = targetUser.gender
        fill_dict['birY'] = targetUser.birthdayY
        fill_dict['birM'] = targetUser.birthdayM
        fill_dict['birD'] = targetUser.birthdayD
        fill_dict['hobbies'] = targetUser.hobbies

        fill_dict['openLogin'] = 0
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

    # Handle editProfile procedure
    if 'username_e' in postData:
        username_e = postData['username_e']
        fName = postData['fName']
        lName = postData['lName']
        gender = postData['gender']
        birthday = str(postData['birthday']).split('-')
        if len(birthday) < 3:
            birD = birM = birY = 0
        else:
            birY = birthday[0]
            birM = birthday[1]
            birD = birthday[2]
        hobbies = postData['hobbies']

        targetUser = models.APPUser.objects.get(username=username_e)
        targetUser.fName = fName
        targetUser.lName = lName
        targetUser.gender = gender
        targetUser.birthdayY = birY
        targetUser.birthdayM = birM
        targetUser.birthdayD = birD
        targetUser.hobbies = hobbies

        targetUser.save()
        # Make sure the user is still logging in after editing the profile
        fill_dict['successLogin'] = 1
        # And the info are properly set
        fill_dict['username'] = targetUser.username
        fill_dict['fName'] = targetUser.fName
        fill_dict['lName'] = targetUser.lName
        fill_dict['gender'] = targetUser.gender
        fill_dict['birY'] = targetUser.birthdayY
        fill_dict['birM'] = targetUser.birthdayM
        fill_dict['birD'] = targetUser.birthdayD
        fill_dict['hobbies'] = targetUser.hobbies

        fill_dict['openLogin'] = 0

        return render(request, 'index.html', fill_dict)

    if 'login' in getData:
        username = getData['usn']

        targetUser = models.APPUser.objects.get(username=username)

        # Make sure the user is still logging in after editing the profile
        fill_dict['successLogin'] = 1
        # And the info are properly set
        fill_dict['username'] = targetUser.username
        fill_dict['fName'] = targetUser.fName
        fill_dict['lName'] = targetUser.lName
        fill_dict['gender'] = targetUser.gender
        fill_dict['birY'] = targetUser.birthdayY
        fill_dict['birM'] = targetUser.birthdayM
        fill_dict['birD'] = targetUser.birthdayD
        fill_dict['hobbies'] = targetUser.hobbies

        fill_dict['openLogin'] = 0
        return render(request, 'index.html', fill_dict)

    return render(request, 'index.html', fill_dict)

def diary(request):
    getData = request.GET
    postData = request.POST

    fill_dict = {
        'username': getData['usn'],
        'noticeSubmit': 0,
        'diaries': None,
        'hideInputs': 0,
    }

    if 'all' in getData:
        username = getData['usn']
        targetUser = models.APPUser.objects.get(username=username)
        diaries = targetUser.diaries.all()
        diaries_list = []
        for d in diaries:
            diaries_list.append({'title':d.title, 'content': d.content})
        fill_dict['diaries'] = diaries_list
        fill_dict['hideInputs'] = 1

    if 'author' in postData:
        author = postData['author']
        diaryTitle = postData['title']
        diaryContent = postData['content']

        diary = models.Diary.objects.create(
            title=diaryTitle,
            content=diaryContent,
            author=models.APPUser.objects.get(username=author)
        )
        diary.save()

        fill_dict['noticeSubmit'] = 1
        return render(request, 'diary.html', fill_dict)

    return render(request, 'diary.html', fill_dict)
