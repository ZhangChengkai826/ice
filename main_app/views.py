from django.shortcuts import render
from . import models
import re

# -*- coding:utf-8 -*-

def checkMobile(request):
    """
    demo :
        @app.route('/m')
        def is_from_mobile():
            if checkMobile(request):
                return 'mobile'
            else:
                return 'pc'
    :param request:
    :return:
    """
    userAgent = request.META.get('HTTP_USER_AGENT', None)
    # userAgent = env.get('HTTP_USER_AGENT')

    _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
    _long_matches = re.compile(_long_matches, re.IGNORECASE)
    _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'
    _short_matches = re.compile(_short_matches, re.IGNORECASE)

    if _long_matches.search(userAgent) != None:
        return True
    user_agent = userAgent[0:4]
    if _short_matches.search(user_agent) != None:
        return True
    return False

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
            if checkMobile(request):
                return render(request, 'index_mobile.html', fill_dict)
            else:
                return render(request, 'index.html', fill_dict)

        pwd = postData['pwd']
        targetUser = models.APPUser.objects.get(username=username)
        # Test whether the password is right
        if pwd != targetUser.password:
            fill_dict['wrongPwd'] = 1
            if checkMobile(request):
                return render(request, 'index_mobile.html', fill_dict)
            else:
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
        if checkMobile(request):
            return render(request, 'index_mobile.html', fill_dict)
        else:
            return render(request, 'index.html', fill_dict)

    # Handle sign up procedure
    if 'username_s' in postData:
        username_s = postData['username_s']
        # Test whether the username has been registered
        if models.APPUser.objects.filter(username=username_s):
            fill_dict['repeatUName'] = 1
            if checkMobile(request):
                return render(request, 'index_mobile.html', fill_dict)
            else:
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
        if checkMobile(request):
            return render(request, 'index_mobile.html', fill_dict)
        else:
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

        if checkMobile(request):
            return render(request, 'index_mobile.html', fill_dict)
        else:
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
        if checkMobile(request):
            return render(request, 'index_mobile.html', fill_dict)
        else:
            return render(request, 'index.html', fill_dict)

    if checkMobile(request):
        return render(request, 'index_mobile.html', fill_dict)
    else:
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

def photo(request):
    getData = request.GET;
    fill_dict = {
        'username': getData['usn'],
    }
    return render(request, 'photo.html', fill_dict)
