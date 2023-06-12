from django.shortcuts import redirect, render
from django.template import RequestContext

from userauths.forms import UserRegisterForm
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your views here.

def register_view(request):

    if request.method == "POST":
         form = UserRegisterForm(request.POST or None)
         if form.is_valid():
             new_user = form.save()
             username = form.cleaned_data.get("username")
             messages.success(request, f"Hey {username}, Your account was created successfully.")
             new_user = authenticate(username=form.cleaned_data['email'],
                                     password=form.cleaned_data['password1'])
             login(request, new_user)
             return redirect("MyApp:index")
             

    else: 
        form = UserRegisterForm()

    
    context = {
        'form' : form,
    }
    return render(request, "userauths/sign-up.html", context)
# j'ai un probleme au niveau de cette fonction
def login_view(request):
    if request.user.is_authenticated:
        return redirect("MyApp:index")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.warning(request, f" User with {email} does not exist")

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in")
                return redirect("MyApp:index")
            else:
                messages.warning(request, "You should crete account")
                return redirect("MyApp:index")

    else:
        context = {}
        return render(request, "userauths/sign-in.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "You are logged Out")

    return redirect("userauths:sign-in")
    # return redirect("userauths:sign-in")