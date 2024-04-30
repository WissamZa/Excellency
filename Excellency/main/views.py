from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from main.models import Contactus, Post, Like, Bookmark
from service.models import Service
from account.models import User, Specialty, LawyerProfile
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def index_view(request: HttpRequest):
    order_num = Service.objects.all().count()
    lawyers_num = User.objects.filter(role="Lawyer").count()
    customar_num = User.objects.filter(role="Customar").count()
    return render(request, "main/index.html", {"order_num": order_num,
                                               "lawyers_num": lawyers_num,
                                               "customar_num": customar_num})


def contactus_view(request: HttpRequest):
    msg = None
    try:
        if request.method == "POST":
            Contactus.objects.create(full_name=request.POST.get('full_name'),
                                     email=request.POST.get('email'),
                                     subject=request.POST.get('subject'),
                                     message=request.POST.get('message'),
                                     )
            msg = "تم ارسال رسالتك بنجاح"
            return redirect("main:contact_success")
    except Exception as e:
        msg = e
    return render(request, "main/contactus.html", {'msg': msg})


# def check_lawyer_has_specialty(lawyer: User, specialty):
#     if specialty in lawyer.lawyer_profile.specialty.all():
#         return True
#     return False


def lawyers_view(request: HttpRequest):
    try:
        lawyers = User.objects.filter(
            role="Lawyer", lawyer_profile__certified=True).order_by("id")
        spcialities = Specialty.objects.all()

        if "lawyer_name" in request.GET:
            lawyers = lawyers.filter(
                full_name__contains=request.GET.get("lawyer_name")
            )
        if "spcialties" in request.GET:
            spcialities_filter = request.GET.getlist("spcialties")
            lawyers = lawyers.filter(
                lawyer_profile__specialty__in=spcialities_filter).annotate(Count("id"))
        if "sort" in request.GET:
            if request.GET.get("sort") == "user_name_a_z":
                lawyers = lawyers.order_by("full_name")
            if request.GET.get("sort") == "user_name_z-a":
                lawyers = lawyers.order_by("-full_name")
            if request.GET.get("sort") == "rating_top":
                pass
    except Exception as e:
        print(e)
    return render(request, "main/lawyers.html", {"lawyers": lawyers, "specialities": spcialities})


@login_required(login_url='/account/login')
def contact_messages(request: HttpRequest):
    if not (request.user.is_staff or request.user.is_superuser):
        return render(request, "no_permission.html")
    messages = Contactus.objects.all()

    return render(request, 'main/contact_messages.html', {'messages': messages})


@login_required(login_url='/account/login')
def admin_view(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return render(request, "no_permission.html")
    lawyer_profiles = LawyerProfile.objects.all()
    return render(request, 'main/admin.html', {'lawyer_profiles': lawyer_profiles})


def lawyer_details_view(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'main/lawyer_details.html', {"user": user})


@login_required(login_url='/account/login')
def verification(request: HttpRequest, user_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return render(request, "no_permission.html")
    user = User.objects.get(id=user_id)
    user.lawyer_profile.certified = True
    user.lawyer_profile.save()
    return redirect("main:admin_view")


def post_list(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        return render(request, 'main/post_lawyers.html', {'posts': posts})
    else:
        return redirect('account:login_view')


def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    if user.is_authenticated:
        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            like.delete()
    return redirect(reverse('main:post_list'))


def bookmark_post(request: HttpRequest, post_id):

    if not request.user.is_authenticated:
        return redirect("account:login_view")

    try:
        post = Post.objects.get(pk=post_id)

        bookmarked_post = Bookmark.objects.filter(user=request.user, post=post).first()

        if not bookmarked_post:

            bookmark = Bookmark(user=request.user, post=post)
            bookmark.save()
        else:

            bookmarked_post.delete()

    except Exception as e:
        print(e)

    return redirect("main:post_list")


def contact_success(request):
    return render(request, 'main/contact_success.html')
