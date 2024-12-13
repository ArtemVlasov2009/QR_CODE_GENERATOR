from django.shortcuts import render

# Create your views here.
def render_home(request):
    return render(request=request, template_name='base.html')

def render_registration(request):
    return render(request=request, template_name='registration.html')

def render_authorization(request):
    return render(request=request, template_name='authorization.html')

def render_contacts(request):
    return render(request=request, template_name='contacts.html')

def render_generator(request):
    return render(request=request, template_name='generator.html')

def render_history_gen(request):
    return render(request=request, template_name='history_gen.html')
