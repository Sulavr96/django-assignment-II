from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from .forms import LoginForm, SignUpForm
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
USER = get_user_model()


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['email'],
                                password=form.cleaned_data['password'])
            if user:
                print("a user is found", user)
                login(request, user)
                return redirect('/user/profile')

            else:
                print("Credentials doesnt match")
                return redirect('/user/login')


class SignUpView(View):
    template_name = 'signup.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            user = USER(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],

            )
            user.save()
            user.set_password(form.cleaned_data['password'])
            user.save()

            logout(request)

            return redirect('/user/login')


class ProfileView(View):
    @method_decorator(login_required(login_url='/user/login/'))
    def get(self, request):
        return render(request, 'profile.html')

    def logout_view(request):
        logout(request)
        return redirect('/user/login/')