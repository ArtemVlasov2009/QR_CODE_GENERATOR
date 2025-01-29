from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.utils import IntegrityError 
from django.contrib.auth import authenticate, login, logout

def render_home(request):
    return render(request=request, template_name='base.html')

def render_registration(request):
    show_text_passwords_dont_match = False
    show_text_not_unique_name = False

    if request.method == "POST":
        username = request.POST.get("name")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            show_text_passwords_dont_match = True
        else:
            try:
                User.objects.create_user(username=username, password=password)
                return redirect("authorization")
            except IntegrityError:
                show_text_not_unique_name = True

    return render(
        request=request,
        template_name="registration.html",
        context={
            "show_text_passwords_dont_match": show_text_passwords_dont_match,
            "show_text_not_unique_name": show_text_not_unique_name
        }
    )

def render_authorization(request):
    user = True
    if request.method == "POST":
        username = request.POST.get("name")
        password = request.POST.get("password")

        print(f"Debug: Username: {username}, Password: {password}")

        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            print(f"Debug: Username: {username}, Password: {password}")
            return redirect('generator')

    return render(request, "authorization.html", {"user": user})

def render_contacts(request):
    return render(request=request, template_name='contacts.html')

def render_generator(request):
    if request.user.is_authenticated:
        return render(request, "generator.html")
    else:
        return redirect("registration")
    

def render_history_gen(request):
    return render(request=request, template_name='history_gen.html')

def logout_user(request):
    logout(request)
    return redirect('authorization')