from datetime import timezone
from timeit import reindent
from django.utils.crypto import get_random_string
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

from Malign import settings
from blog.forms import CustomUserForm, CreatorForm
from blog.models import Podcast, Creator, Comment, CustomUser


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def podcasts(request):
    podcasts = Podcast.objects.all()
    return render(request, 'podcasts.html', {'posts': podcasts})

def home(request):
    podcasts = Podcast.objects.all()
    return render(request, 'podcasts.html', {'posts': podcasts})
def nothing(request):
    return redirect('/home/')

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


        CustomUser = get_user_model()


        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken!')
            return redirect('creator_signup')


        user = CustomUser.objects.create_user(username=username, email=email, password=password)




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
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')

def dashboard_view(request):
    if request.user.is_authenticated:

        print("I am being redirected to the dashboard.")
        creator_profile = getattr(request.user, 'creator_profile', None)
        if creator_profile:
            return render(request, 'creator_dashboard.html', {'creator': creator_profile})
        else:
            print("I am entering the if!")
            return render(request, 'user_dashboard.html', {'user': request.user})
    else:
        return redirect('/blog/podcasts')
def custom_logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def upload_podcast(request):

    if hasattr(request.user, 'creator_profile'):
        creator = request.user.creator_profile

        if request.method == 'POST':
            try:

                title = request.POST.get('title')
                description = request.POST.get('description')
                pub_date = request.POST.get('pub_date')
                link = request.POST.get('link')
                image = request.FILES.get('image')


                if not all([title, description, pub_date, link, image]):
                    messages.error(request, 'All fields are required.')
                    return redirect('dashboard')


                try:
                    pub_date = datetime.fromisoformat(pub_date)
                except ValueError:
                    messages.error(request, 'Invalid date format. Use YYYY-MM-DDTHH:MM.')
                    return redirect('dashboard')


                if not link.startswith(('http://', 'https://')):
                    messages.error(request, 'Invalid URL format.')
                    return redirect('dashboard')


                podcast = Podcast.objects.create(
                    title=title,
                    creator=creator,
                    description=description,
                    pub_date=pub_date,
                    link=link,
                    image=image
                )
                print("MEDIA_ROOT:", settings.MEDIA_ROOT)
                print("Uploaded File Path:", podcast.image.path)
                print("Uploaded File URL:", podcast.image.url)
                podcast.save()

                messages.success(request, 'Podcast uploaded successfully!')
                return redirect('dashboard')
            except Exception as e:
                print("Error Creating Podcast:", e)
                messages.error(request, f"An error occurred: {e}")
                return redirect('dashboard')


        return render(request, 'creator_dashboard.html', {'creator': creator})
    else:

        messages.error(request, 'Only creators can upload podcasts.')
        return redirect('home')

def podcast_detail(request, podcast_id):

    podcast = get_object_or_404(Podcast, id=podcast_id)

    comments = Comment.objects.filter(post=podcast)

    return render(request, 'podcast_detail.html', {'podcast': podcast, 'comments': comments})


@login_required(login_url='login')
def add_comment(request, podcast_id):
    podcast = get_object_or_404(Podcast, id=podcast_id)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()

        if not content:
            return redirect('podcast_detail', podcast_id=podcast_id)

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
        form = CustomUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CustomUserForm(instance=request.user)

    return render(request, 'update_user_info.html', {'form': form})


@login_required
def update_creator_info(request):
    if not hasattr(request.user, 'creator_profile'):
        return redirect('dashboard')  # Redirect if not a creator

    creator = request.user.creator_profile  # Access the related Creator instance

    if request.method == 'POST':
        form = CreatorForm(request.POST, request.FILES, instance=creator, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CreatorForm(instance=creator, user=request.user)

    return render(request, 'update_creator_info.html', {'form': form})

def visit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if hasattr(user, 'creator_profile'):
        return render(request, 'visit_creator.html', {'creator': user})
    else:
        return render(request, 'visit_user.html', {'user': user})

def visit_creator(request, user_id):
    user = get_object_or_404(Creator, id=user_id)

    return render(request, 'visit_creator.html', {'creator': user})


def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        if not username or not email:
            messages.error(request, "Both username and email are required.")
            return redirect('forgot_password')

        try:
            user = CustomUser.objects.get(username=username, email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "No user found with the provided username and email.")
            return redirect('forgot_password')
        token = get_random_string(32)
        reset_link = request.build_absolute_uri(f'/reset_password/{token}/')
        print(f"Reset link for {user.username}: {reset_link}")
        messages.success(request, "A password reset link has been sent to your email (simulated in console).")
        return redirect('login')

    return render(request, 'forgot_password.html')

def reset_password(request, token):
    print(f"Token received: {token}")

    messages.success(request, "Password reset successful (simulated).")
    return redirect('dashboard')
