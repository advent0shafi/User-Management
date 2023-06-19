from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import cache_control

# Create your views here.

def signup(request):

    if request.method == 'POST':
        username = request.POST.get("username" )
        fname = request.POST.get("fname" )
        lname = request.POST.get("lname" )
        email = request.POST.get('email')
        pass1 = request.POST.get("pass1" )
        pass2 = request.POST.get("pass2")

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist..!!")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request," Email already registered..!!")
            return redirect('signup')
        
        if len(username)>10:
            messages.error(request, "User name must be under 10 characters")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request,"Passwords didn't match !")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric")
            return redirect('signup')
        
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
       

        myuser.save()

        messages.success(request, "Your account has been succesfully created")

        return redirect('signin')


    return render(request, 'authentication/signup.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
          username = request.POST["username"] 
          pass1 = request.POST["pass1" ]

          user = authenticate(username = username, password = pass1)

          if user is not None:
              login(request, user)
              
             
              return redirect('home')
            
          else:
              messages.error(request, "Hey !!! username or password incorrect")  
              return redirect('signin')

    return render(request, 'authentication/signin.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.user.is_authenticated:
        fname = request.user.first_name
        return render(request, 'authentication/index.html',{'fname':fname}) 
        
    return render(request, 'authentication/index.html')       
    

def signout(request):
    if request.user.is_authenticated:
        logout(request)
  
    messages.success(request,"logged Out Successfully")
    return redirect('home')

