from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.utils import IntegrityError 
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
import qrcode
from io import BytesIO
from home.models import qr_code

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
        if request.method == "POST":
            qr_link = request.POST.get("link_or_text")

            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=4
            )
            qr.add_data(qr_link)
            qr.make(fit=True)
        
            img = qr.make_image(fill_color="black", back_color="white")

            image_io = BytesIO()
            img.save(image_io, format="PNG")

            # Создаем объект модели
            qr_code1 = qr_code()

            # Сбрасываем указатель потока в начало
            image_io.seek(0)

            # Сохраняем изображение в модель без tuple
            qr_code1.image.save(f"qr_code.png", ContentFile(image_io.getvalue()), save=True)
        
            return render(request, "generator.html")
        return render(request, "generator.html")
    else:
        return redirect("registration")
    

def render_history_gen(request):
    return render(request=request, template_name='history_gen.html')

def logout_user(request):
    logout(request)
    return redirect('authorization')







