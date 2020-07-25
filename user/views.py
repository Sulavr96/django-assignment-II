from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from .forms import LoginForm, SignUpForm, UpdateForm
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from blog.models import Blog
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


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
                logout(request)
                print("a user is found", user)
                login(request, user)
                return redirect('/users/profile/')

            else:
                print("Credentials doesnt match")
                messages.error(request, 'Login failed (Please Check your email/password)')
                return redirect('/users/login/')


class SignUpView(View):
    template_name = 'signup.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            custom_username = form.cleaned_data['email'].split('@')[0]
            user = USER(
                email=form.cleaned_data['email'],
                username=custom_username,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                is_staff=True,
                is_active=False,
                profile_image=form.cleaned_data['profile_image'],
            )
            user.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            mail_subject = 'Activate your account.'
            message = render_to_string('mail_body.html', {
                    'user': user.get_full_name,
                    'domain': request.get_host(),
                    'user_id': user.id,
            })
            to_email = user.email

            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            messages.success(request, 'User created successfully!! please check your email and verify your account ')
            logout(request)
            return redirect('/users/signup/')
        else:
            messages.error(request, 'Please check your credentials')
            return redirect('/users/signup/')
            

class ProfileView(View):

    @method_decorator(login_required(login_url='/users/login/'))
    def get(self, request):
        user_blog = Blog.objects.filter(user__pk=request.user.id)
        context = {'blogs': user_blog}
        if request.user.is_active:
            return render(request, 'profile.html', context=context)
        else:
            return render(request, 'activate.html')

    @staticmethod
    def logout_view(request):
        logout(request)
        return redirect('/users/login/')


class UserView(View):
    def get(self, request):
        users = USER.objects.all()
        context = {'users': users}
        return render(request, 'users.html', context=context)

class AccountActivate(View):
    template_name = 'activate.html'

    def get(self, request):
        uid = request.GET.get('user_id')
        user = USER.objects.get(pk=int(uid))

        user.is_active = True
        user.save()

        return redirect('/users/login')

class UserUpdate(View):
    template_name = 'userupdate.html'

    @method_decorator(login_required(login_url='/users/login/'))
    def get(self, request):
        user_object = get_object_or_404(USER, id = request.user.id) 
        form = SignUpForm(instance=user_object)
        return render(request, 'userupdate.html', {'form': form})

    @method_decorator(login_required(login_url='/users/login/'))
    def post(self, request):
        user_object = get_object_or_404(USER, id = request.user.id) 
        form = UpdateForm(request.POST, request.FILES, instance=user_object)

        if form.is_valid():
            user_object.set_password(form.cleaned_data['password'])
            form.save()
            messages.success(request, 'User updated successfully')

            return redirect('/users/update')
        else:
            print("Error")
            messages.error(request, "Something went wrong")

            return redirect('/users/update')


class UserDelete(View):

    @method_decorator(login_required(login_url='/users/login/'))
    def get(self, request):
        user_object = get_object_or_404(USER, id=request.user.id)
        USER.objects.get(pk=request.user.id).blog_set.all().delete()
        user_object.delete()
        messages.success(request, 'User deleted successfully')
        return redirect('/users/login')
