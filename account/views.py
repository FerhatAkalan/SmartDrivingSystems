from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserSettingsForm
from django.http import JsonResponse
from .models import UserSettings 

# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return redirect("upload_file")

    if request.method =="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user= authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,"account/login.html",{"error":"username ya da password yanlıs"})
    else:
        return render(request,"account/login.html")

def user_register(request):
    if request.method=="POST":
        username=request.POST["username"]
        email=request.POST["email"]
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        password=request.POST["password"]
        repassword=request.POST["repassword"]
    
        if password != repassword:
            return render(request, "account/register.html",
            {
                "error":"password eslesmiyor",
                "username": username,
                "email": email 
            }) 

        if User.objects.filter(username= username).exists():
            return render(request, "account/register.html",
            {   "error":"username kullaniliyor",
                "username": username,
                "email": email
            })
             
        if User.objects.filter(email=email).exists():
            return render(request, "account/register.html",
            {
                "error":"email kullaniliyor",
                "username": username,
                "email": email 
            })
                
        user = User.objects.create_user(username=username,first_name=first_name, last_name=last_name,email=email,password=password)
        user.save()
        user_settings = UserSettings.objects.create(user=user)
        user_settings.save()    
        return redirect("user_login")
        
            
    else:
        return render(request,"account/register.html")

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def user_profile(request):
    # Burada kullanıcının profiline özgü verileri alabilirsiniz
    user = request.user
    context = {
        'user': user,
        # Eğer kullanıcının profiline özgü başka veriler varsa, context içerisine ekleyebilirsiniz
    }
    return render(request, 'account/profile.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})  # Başarı durumunda JSON yanıtı döndür
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)  # Hata durumunda JSON yanıtı döndür
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

@login_required
def settings(request):
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=request.user.usersettings)
        if form.is_valid():
            form.clean()
            form.save()
            return JsonResponse({'success': True}) 
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = UserSettingsForm(instance=request.user.usersettings)
    return render(request, 'account/settings.html', {'form': form})