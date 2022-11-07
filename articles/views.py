from django.shortcuts import render, redirect
from .models import Articles
from .models import Articles, Category, Comment, Image
from .forms import ArticleForm, CommentForm, ImageForm
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction

import json

from django.db.models import Q


# Create your views here.
def index(request):
    articles = Articles.objects.order_by("-pk")
    image = Image.objects.order_by("-pk")
    form = CommentForm()
    context = {
        "articles": articles,
        "image": image,
        "form": form,
    }
    return render(request, "articles/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        article_forms = ArticleForm(request.POST, request.FILES)
        image_form = ImageForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")
        if article_forms.is_valid() and image_form.is_valid():
            article_form = article_forms.save(commit=False)
            article_form.user = request.user
            if len(images):
                for image in images:
                    image_instance = Image(articles=article_form, image=image)
                    article_form.save()
                    image_instance.save()
            else:
                article_form.save()
            return redirect("articles:index")
    else:
        article_form = ArticleForm()
        image_form = ImageForm()
    context = {
        "article_form": article_form,
        "image_form": image_form,
    }
    return render(request, "articles/create.html", context)


def detail(request, pk):
    article = Articles.objects.get(pk=pk)
    form = CommentForm()
    context = {
        "article": article,
        "form": form,
    }
    return render(request, "articles/detail.html", context)


@require_http_methods(["GET", "POST"])
def update(request, pk):
    article = Articles.objects.get(pk=pk)
    # image = Image.objects.get(pk=pk)
    if request.method == "POST":
        article_forms = ArticleForm(request.POST, request.FILES, instance=article)
        image_form = ImageForm(request.POST, request.FILES, instance=article)
        images = request.FILES.getlist("image")
        if article_forms.is_valid() and image_form.is_valid():
            article = article_forms.save(commit=False)
            # image_form = article_forms.save(commit=False)
            if len(images):
                for image in images:
                    image_instance = Image(articles=article, image=image)
                    article.save()
                    image_instance.save()
            else:
                article_form.save()
            return redirect("articles:detail", article.pk)
    else:
        article_form = ArticleForm(instance=article)
        image_form = ImageForm(instance=article)
    context = {
        "article_form": article_form,
        "image_form": image_form,
    }
    return render(request, "articles/update.html", context)


def delete(request, pk):
    article = Articles.objects.get(pk=pk)
    article.delete()
    return redirect("articles:index")


def category(request, category_pk):
    category = Category.objects.get(pk=category_pk)
    category_articles = Articles.objects.filter(category=category)
    context = {"category": category, "category_articles": category_articles}
    return render(request, "articles/category.html", context)


@login_required
def category_follow(request, category_pk):
    category = Category.objects.get(pk=category_pk)
    if request.user in category.category_followers.all():
        category.category_followers.remove(request.user)
        category_follow = False
    else:
        category.category_followers.add(request.user)
        category_follow = True
    return JsonResponse(
        {
            "categoryFollow": category_follow,
            "followCount": category.category_followers.count(),
        }
    )


@login_required
def like(request, pk):
    article = Articles.objects.get(pk=pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
        is_liked = False
    else:
        article.like_users.add(request.user)
        is_liked = True
    return JsonResponse({"isLiked": is_liked, "likeCount": article.like_users.count()})


def comment(request, pk):
    article = Articles.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.articles = article
        comment.user = request.user
        comment.save()
        context = {
            "content": comment.content,
            "userName": comment.user.username,
            "userImgUrl": comment.user.profile.image.url,
            "created": comment.create_at,
            "comment_count": article.comment_set.count(),
            "user": comment.user.pk,
        }
        return JsonResponse(context)
    return redirect("articles:detail", article.pk)


def comment_d(request):
    jsonObject = json.loads(request.body)
    context = {"result": "no"}
    reply = Comment.objects.filter(id=jsonObject.get("replyId"))

    if reply is not None:
        reply.delete()
        context = {
            "result": "ok",
        }
        return JsonResponse(context)
    return JsonResponse(context)


def search(request):
    searched = request.GET.get("searched", False)
    field = request.GET.get("field")
    if field == "1":
        articles = Articles.objects.filter(
            Q(title__contains=searched)
            | Q(content__contains=searched)
            | Q(user__username__contains=searched)
        ).order_by("-pk")
    elif field == "2":
        articles = Articles.objects.filter(Q(title__contains=searched)).order_by("-pk")
    elif field == "3":
        articles = Articles.objects.filter(Q(content__contains=searched)).order_by(
            "-pk"
        )
    elif field == "4":
        articles = Articles.objects.filter(
            Q(user__username__contains=searched)
        ).order_by("-pk")
    if not searched:
        articles = []
        text = "검색어를 입력하세요."
    elif len(articles) == 0:
        text = "검색 결과가 없습니다."
    else:
        text = ""
    context = {
        "articles": articles,
        "text": text,
    }
    return render(request, "articles/search.html", context)
