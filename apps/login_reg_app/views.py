from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from .models import User
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request,'login_reg_app/index.html')

def process(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        if 'fname' not in request.session:
            request.session['fname'] = ""
        input_pass = request.POST['pass']
        hash1 = bcrypt.hashpw(input_pass.encode(), bcrypt.gensalt())
        print "password is.....{}....{}".format(input_pass,hash1)
        User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hash1)
        request.session['fname'] = request.POST['first_name']
        return redirect('/success')
def login_process(request):
    errors1 = User.objects.login_validator(request.POST)
    if len(errors1):
        for tag, error in errors1.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        if 'fname' not in request.session:
            request.session['fname'] = ""
        u = []
        u = User.objects.filter(email = request.POST['login_email'])
        request.session['fname'] = u[0].first_name
        
        return redirect('/success')
    # return redirect('/')

def success(request):
    
    return render(request,'login_reg_app/success.html')
