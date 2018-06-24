from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
import bcrypt
import re
from apps.thewall.models import *

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    if 'counter' not in request.session:
        request.session['counter'] = 0
        return render(request, 'thewall/index.html')

    request.session['counter'] += 1
    if request.session['counter'] ==1:
        request.session.flush()

    return render(request, 'thewall/index.html')

def register(request):
    errors = []
    request.session['error_msg'] = errors

    if len(request.POST['first_name']) < 1:
        errors.append("Your First Name is too short")
        request.session['first_name'] = request.POST['first_name']
    if len(request.POST['last_name']) < 1:
        errors.append("Your Last Name is too short")
    if len(request.POST['email']) < 1:
        errors.append("Your Email is too short")
    if not EMAIL_REGEX.match(request.POST['email']):
        errors.append("Invalid Email")
    if len(request.POST['password']) < 8:
        errors.append("Your Password is too short")
    if request.POST['confirm'] != request.POST['password']:
        errors.append("Your Passwords do not match")

    if len(errors) > 0:
        print('EEEEERRRRROOOOORRRRRRS', errors)
        return redirect('/', errors)

    else:
        request.session['logged_in'] = True

        firstname = request.POST['first_name']  #created variables to feed into table 
        lastname = request.POST['last_name']    #table input starts right below
        email = request.POST['email']
        password = request.POST['password']
        hashbrown = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        User.objects.create(first_name = firstname, last_name = lastname, email = email, password = hashbrown)

        success = []
        success.append("Successfully registered!!!!")
        request.session['success_msg'] = success
        request.session['first_name'] = request.POST['first_name']

        c = User.objects.get(first_name = request.POST['first_name'])
        id = c.id
        request.session['user_id'] = id
        print(id)

    return redirect('/success', success)

def login(request):

    a = User.objects.filter(email = request.POST['login_email'])
    a = a[0]


    if a and bcrypt.checkpw(request.POST['login_password'].encode(), a.password.encode()):
        print(a.first_name)
        request.session['first_name'] = a.first_name
        request.session['user_id'] = a.id
        print(request.session['user_id'])
        return redirect('/success')

    else:
        request.session['login_error'] = "Invalid Credential"
        return redirect('/')

def success(request):

    context = {
        'user':User.objects.all(),
        'message': Messages.objects.all(),
        'comment': Comments.objects.all()
    }
    return render(request, 'thewall/success.html', context)

def logoff(request):
    request.session.clear()
    return redirect('/')

def newmessage(request):
    wall_message = request.POST['newmessage']
    id = request.session['user_id']
    Messages.objects.create(
        message = wall_message,
        user_id_id = id
    )
    return redirect('/success')

def newcomment(request):
    msg_comment = request.POST['comment']
    msg_id = request.POST['msg_id']
    user_id = request.session['user_id']
    print("!!!!!!!!!!!!", request.POST['msg_id'])

    Comments.objects.create(
        message = msg_comment,
        comment_id_id = msg_id,
        user_id_id = user_id
    )
    return redirect('/success')

def deletemessage(request):
    
    i = Messages.objects.get(id = request.POST['message_id'])
    if i.id == request.session['user_id']:
        i.delete()
        return redirect('/success')
    else:
        return render(request, 'thewall/wrong.html')
    

def deletecomment(request):
    i = Comments.objects.get(id = request.POST['comment_id'])
    i.delete()
    return redirect('/success')
