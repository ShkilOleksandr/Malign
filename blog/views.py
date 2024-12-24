from datetime import timezone
from timeit import reindent

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from datetime import datetime
from django import forms
# Create your views here.


from django.http import HttpResponse
from django.utils.functional import SimpleLazyObject

from blog.forms import CustomUserUpdateForm, CreatorUpdateForm
from blog.models import Podcast, Creator, Comment, CustomUser


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def podcasts(request):
    podcasts = Podcast.objects.all()
    return render(request, 'podcasts.html', {'posts': podcasts})

def home(request):
    return redirect('/blog/podcasts')
def nothing(request):
    return redirect('/blog/podcasts')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('user_signup')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken!')
            return redirect('user_signup')

        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'User account created successfully. Please log in.')
        return redirect('login')

    return render(request, 'user_signup.html')


def creator_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('creator_signup')

        # Get the custom user model
        CustomUser = get_user_model()

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken!')
            return redirect('creator_signup')

        # Create the user
        user = CustomUser.objects.create_user(username=username, email=email, password=password)

        # Create a linked Creator profile
        Creator.objects.create(user=user)

        messages.success(request, 'Creator account created successfully. Please log in.')
        return redirect('login')

    return render(request, 'creator_signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to a common dashboard
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')

def dashboard_view(request):
    if hasattr(request.user, 'creator'):
        # User is a Creator
        return render(request, 'creator_dashboard.html', {'creator': request.user.creator})
    elif hasattr(request.user, 'is_authenticated') and request.user.is_authenticated:
        # User is a regular User (not a Creator)
        return render(request, 'user_dashboard.html', {'user': request.user})
    else:
        # Handle the case where the user is neither a Creator nor a recognized User
        return redirect('/blog/podcasts')

def custom_logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def upload_podcast(request):
    if hasattr(request.user, 'creator'):
        creator = request.user.creator

        if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            pub_date = request.POST['pub_date']
            link = request.POST['link']
            image = request.FILES['image']  # Handle uploaded file

            # Create the podcast instance
            podcast = Podcast.objects.create(
                title=title,
                creator=creator,
                description=description,
                pub_date=pub_date,
                link=link,
                image=image
            )
            podcast.save()
            messages.success(request, 'Podcast uploaded successfully!')
            return redirect('dashboard')  # Redirect back to the dashboard

        return render(request, 'creator_dashboard.html', {'creator': creator})
    else:
        messages.error(request, 'Only creators can upload podcasts.')
        return redirect('home')

def podcast_detail(request, podcast_id):
    # Fetch the podcast by ID
    podcast = get_object_or_404(Podcast, id=podcast_id)
    # Fetch comments for the podcast
    comments = Comment.objects.filter(post=podcast)

    return render(request, 'podcast_detail.html', {'podcast': podcast, 'comments': comments})


@login_required(login_url='login')  # Ensure the user is authenticated
def add_comment(request, podcast_id):
    podcast = get_object_or_404(Podcast, id=podcast_id)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()

        # Ensure content is not empty
        if not content:
            return redirect('podcast_detail', podcast_id=podcast_id)

        # Create the comment with the logged-in user as the author
        Comment.objects.create(
            post=podcast,
            content=content,
            author=request.user,
            pub_date=datetime.now(timezone.utc),
        )

    return redirect('podcast_detail', podcast_id=podcast_id)

@login_required
def update_user_info(request):
    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('dashboard')
    else:
        user_form = CustomUserUpdateForm(instance=request.user)

    return render(request, 'update_user_info.html', {'user_form': user_form})


@login_required
def update_creator_info(request):
    if not hasattr(request.user, 'creator'):
        return redirect('dashboard')  # Redirect non-creators to the user dashboard

    if request.method == 'POST':
        creator_form = CreatorUpdateForm(request.POST, request.FILES, instance=request.user.creator)
        if creator_form.is_valid():
            creator_form.save()
            return redirect('dashboard')
    else:
        creator_form = CreatorUpdateForm(instance=request.user.creator)

    return render(request, 'update_creator_info.html', {'creator_form': creator_form})