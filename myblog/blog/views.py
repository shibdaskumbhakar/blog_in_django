from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Blog, Like, Comment
from django.views.generic import DetailView, UpdateView, DeleteView
from django.http import Http404
from django.http import HttpResponse


def index(request):
    blog = Blog.objects.all().order_by('-views')

    context = {
        'blog': blog,

    }
    return render(request, "blog/index.html", context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('blog:myaccount')
        else:
            messages.info(request, 'invalid credentials')
            return render(request, "blog/login.html", {})
    else:

        return render(request, "blog/login.html", {})


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']

        password = request.POST['password']
        password2 = request.POST['re_password']

        if password == password2:

            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email Already Register !')
                return redirect('blog:register')
            else:
                user = User.objects.create_user(
                    first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                user.save()

                messages.success(
                    request, 'Your Succesfully Register !  Login To Continue')
                return redirect('blog:login')

        else:
            messages.warning(request, 'Your Password Not Match !')
            return redirect('blog:register')

    else:
        return render(request, "blog/register.html", {})


@login_required
def myaccount(request):
    user = request.user
    myblog = Blog.objects.filter(user=user)
    context = {
        'user': user,
        'myblog': myblog
    }
    return render(request, "blog/myaccount.html", context)

# blog details


class blogtDetailSlugViews(DetailView):

    queryset = Blog.objects.all()
    template_name = "blog/details.html"

    def get_context_data(self, *args, **kwargs):
        context = super(blogtDetailSlugViews,
                        self).get_context_data(*args, **kwargs)
        request = self.request

        user = request.user
        slug = self.kwargs.get('slug')
        blogobj = Blog.objects.get(slug=slug)
        Dislike = ''
        liked = ''
        if request.user.is_authenticated:

            liked = Like.objects.filter(user=user, blog=blogobj, likes=True)
            Dislike = Like.objects.filter(
                user=user, blog=blogobj, likes=False, dislikes=True)

        likecount = Like.objects.filter(blog=blogobj, likes=True).count()
        dislikecount = Like.objects.filter(
            blog=blogobj, dislikes=True).count()

        comment = Comment.objects.filter(blog=blogobj)

        context['likecount'] = likecount
        context['dislikecount'] = dislikecount
        context['Dislike'] = Dislike
        context['liked'] = liked
        context['comment'] = comment

        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        try:
            instance = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            raise Http404("Not Fund..")
        except Blog.MultipleObjectsRequest:
            qs = Blog.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Error")
        obj = Blog.objects.get(slug=slug)
        obj.views += 1
        obj.save()
        return instance

# post update views


class BlogUpdateView(UpdateView):
    model = Blog
    template_name = "blog/update.html"
    fields = [
        "title",
        "description",
        "image"
    ]
    success_url = "/myaccount"

# post delete


class BlogDeleteView(DeleteView):

    model = Blog
    template_name = "blog/delete.html"

    success_url = "/myaccount"

# add new post


def addblog(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']

        title = request.POST['title']

        description = request.POST['description']

        blog = Blog.objects.create(
            title=title, description=description, image=image)
        blog.user = request.user
        blog.save()
        return redirect('blog:myaccount')

    else:
        return render(request, "blog/myaccount.html", {})

# post like


def like(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blogid')
        title = request.POST.get('title')

        user = request.user
        blog = Blog.objects.get(id=blog_id)

        if Like.objects.filter(user=user, blog=blog, blog_title=title, likes=True).exists():
            obj = Like.objects.filter(
                user=user, blog=blog, blog_title=title).update(dislikes=True, likes=False)

        else:
            if Like.objects.filter(user=user, blog=blog, blog_title=title).exists():
                obj = Like.objects.filter(user=user, blog=blog, blog_title=title).update(
                    likes=True, dislikes=False)

            else:

                obj = Like.objects.create(
                    user=user, blog=blog, blog_title=title)
                obj.likes = True
                obj.save()
    return HttpResponse("Success!")

# post dislike


def Dislike(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blogid')
        title = request.POST.get('title')

        user = request.user
        blog = Blog.objects.get(id=blog_id)

        if Like.objects.filter(user=user, blog=blog, blog_title=title, dislikes=True).exists():
            obj = Like.objects.filter(
                user=user, blog=blog, blog_title=title).update(likes=True, dislikes=False)

        else:
            if Like.objects.filter(user=user, blog=blog, blog_title=title).exists():
                obj = Like.objects.filter(user=user, blog=blog, blog_title=title).update(
                    likes=False, dislikes=True)

            else:
                obj = Like.objects.create(
                    user=user, blog=blog, blog_title=title)

                obj.dislikes = True
                obj.save()
    return HttpResponse("Success!")

# post comment


def comment(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blogid')
        comment = request.POST.get('comment')
        blog = Blog.objects.get(id=blog_id)
        user = request.user
        addcomment = Comment.objects.create(
            user=user, blog=blog, comment=comment)
        addcomment.save()

    return HttpResponse("Success!")
