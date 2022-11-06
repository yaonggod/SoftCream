from ast import Pass

from django.http import JsonResponse
from .models import Profile, User
from articles.models import Articles
from django.shortcuts import render, redirect

from accounts.forms import SignupForm, UpdateForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    users = User.objects.all()
    context = {
        "users": users,
    }
    return render(request, "accounts/index.html", context)


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        profile = Profile()
        if form.is_valid():
            user = form.save()
            profile.user = user
            profile.save()
            return redirect("articles:index")
    else:
        form = SignupForm()
    context = {"form": form}
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get("next") or "articles:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


def logout(request):
    auth_logout(request)
    return redirect("articles:index")


@login_required
def update(request):
    if request.method == "POST":
        form = UpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("articles:index")
    else:
        form = UpdateForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)


@login_required
def password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("accounts:update")
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/password.html", context)


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect("articles:index")


def mypage(request, pk):
    user = get_user_model().objects.get(pk=pk)
    articles = Articles.objects.filter(user=user)
    context = {
        "user": user,
        "articles": articles,
    }
    return render(request, "accounts/mypage.html", context)


def profile(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {
        "user": user,
    }
    return render(request, "accounts/profile.html", context)


@login_required
def pupdate(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile", request.user.pk)
    else:
        form = ProfileForm(instance=request.user.profile)
    context = {
        "form": form,
    }
    return render(request, "accounts/pupdate.html", context)


@login_required
def follow(request, pk):
    if request.user.is_authenticated:
        me = request.user
        user = get_user_model().objects.get(pk=pk)
        if me != user:
            if me in user.followers.all():
                user.followers.remove(me)
                is_followed = False
            else:
                user.followers.add(me)
                is_followed = True
            context = {
                "is_followed": is_followed,
                "followersC": user.followers.count(),
                "followingsC": user.followings.count(),
            }
            return JsonResponse(context)
        return redirect("accounts:mypage", pk)
    return redirect("accounts:login")
