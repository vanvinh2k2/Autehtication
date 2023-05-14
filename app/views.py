from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile
import uuid
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .hepper import send_forget_password_mail

# Create your views here.
def Init(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            re_password = request.POST.get('re_password')

            if password != re_password: 
                return HttpResponse("Error!")
            else:
                my_user = User.objects.create_user(username, email, password);
                my_user.save()

                profile = Profile.objects.create(user=my_user)
                my_user.save()
                return redirect('login')
        return render(request, 'app/signup.html')

def Login(request):
        if request.method == 'POST':
            name = request.POST.get('name')
            pass1 = request.POST.get('password')
            auth = authenticate(request, username=name, password=pass1)
            if auth is not None:
                  login(request,auth)
                  return redirect('home')
            else: return HttpResponse("Error!")
        return render(request, 'app/login.html')

@login_required(login_url='login')
def Home(request):
        return render(request, 'app/home.html')

def Logout(request):
        logout(request)
        return redirect('login')

def ChangePassword(request, token):
      profile_obj = Profile.objects.filter(forget_password_token=token).first()
      content = {'user_id': profile_obj.user.id}
      if request.method == 'POST':
            new_password = request.POST.get('password')
            renew_password = request.POST.get('re_password')
            used_id = request.POST.get('user_id')

            if used_id is None:
                  return redirect(f'/change-password/{token}/')
            if new_password != renew_password:
                  return redirect(f'/change-password/{token}/')
            
            user_obj = User.objects.get(id=used_id)
            user_obj.set_password(new_password);
            user_obj.save()
            return redirect('login')

      return render(request, 'app/change_password.html', content)

def ForgetPassword(request):
      if request.method == 'POST':
            user_name = request.POST.get('username')
            if not User.objects.filter(username=user_name).first():
                  return HttpResponse("Not find user")
            
            user_obj = User.objects.get(username=user_name)
            token = str(uuid.uuid4())
            send_forget_password_mail(user_obj, token)

            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            return redirect('forget-password')
      return render(request, 'app/forget_password.html')