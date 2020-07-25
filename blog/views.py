from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from django.contrib.auth import get_user_model
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import CreateBlogForm
from django.contrib import messages

User = get_user_model()

# Create your views here.
def home(request):
    return render(request, 'home.html')

def user_blog(request, user_id):

    user_blogs = Blog.objects.filter(user__pk=user_id)
    user_name = User.objects.get(pk=user_id)

    context = {'blogs': user_blogs,
               'user_name': user_name
               }

    return render(request, 'user_blogs.html', context=context)

def blog(request):
    blogs = Blog.objects.all()
    context = {
                'blogs': blogs
            }
    
    return render(request, 'blogs.html', context=context)

class CreateBlog(View):

    @method_decorator(login_required(login_url='/users/login/'))
    def get(self, request):
        form = CreateBlogForm()
        return render(request, 'createblog.html', {'form': form})

    @method_decorator(login_required(login_url='/users/login/'))
    def post(self, request):
        form = CreateBlogForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            blog = Blog(
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                user_id=request.user.id
            )

            blog.save()
            messages.success(request, 'Blog Created')

            return redirect('/users/profile/')
        else:   
            messages.error(request, 'Something went wrong')
            return redirect('/blogs/create/')

class EditBlog(View):

    @method_decorator(login_required(login_url='/users/login/'))
    def get(self, request, blog_id):
        blog_obj = get_object_or_404(Blog, id=blog_id)
        form = CreateBlogForm(instance=blog_obj)

        return render(request, 'editblog.html', {'form': form})

    @method_decorator(login_required(login_url='/users/login/'))
    def post(self, request, blog_id):
        blog_obj = get_object_or_404(Blog, id=blog_id)
        form = CreateBlogForm(request.POST, instance=blog_obj)

        if form.is_valid():
            form.save()
            messages.success(request, "Updated successfully")

            return redirect(f'/blogs/{blog_id}/edit')
        else:
            messages.error(request,"Something went wrong")
            
            return redirect(f'/blogs/{blog_id}/edit')


class DeleteBlog(View):

    @method_decorator(login_required(login_url='/users/login/'))
    def get(self, request, blog_id):
        blog_object = get_object_or_404(Blog, id=blog_id)
        blog_object.delete()
        messages.success(request, 'Blog deleted successfully')
        return redirect('/users/profile')
    