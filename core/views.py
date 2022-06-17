from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, render

from .models import AdminHOD, CustomUser, Staffs, Students


def home(request):
    return render(request, "home.html")


def contact(request):
    return render(request, "contact.html")


def loginUser(request):
    return render(request, "login_page.html")


def doLogin(request):
    if request.method == "POST":
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        if not (email and password):
            messages.error(request, "Please provide all the details!!")
            return render(request, "login_page.html")

        try:
            u = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            u = None
        if u:
            user = authenticate(username=u.username, password=password)
            if not user:
                messages.error(request, "Invalid Login Credentials!!")
                return render(request, "login_page.html")
        else:
            messages.error(request, "Invalid Login Email Id!!")
            return render(request, "login_page.html")

        login(request, user)

        if user.user_type == CustomUser.STUDENT:
            return redirect("student_home/")
        elif user.user_type == CustomUser.STAFF:
            return redirect("staff_home/")
        elif user.user_type == CustomUser.HOD:
            return redirect("admin_home/")

    return render(request, "home.html")


def registration(request):
    return render(request, "registration.html")


def doRegistration(request):
    first_name = request.GET.get("first_name")
    last_name = request.GET.get("last_name")
    email_id = request.GET.get("email")
    password = request.GET.get("password")
    confirm_password = request.GET.get("confirmPassword")

    print(email_id)
    print(password)
    print(confirm_password)
    print(first_name)
    print(last_name)
    if not (email_id and password and confirm_password):
        messages.error(request, "Please provide all the details!!")
        return render(request, "registration.html")

    if password != confirm_password:
        messages.error(request, "Both passwords should match!!")
        return render(request, "registration.html")

    is_user_exists = CustomUser.objects.filter(email=email_id).exists()

    if is_user_exists:
        messages.error(
            request, "User with this email id already exists. Please proceed to login!!"
        )
        return render(request, "registration.html")

    user_type = get_user_type_from_email(email_id)

    if user_type is None:
        messages.error(
            request,
            "Please use valid format for the email id: '<username>.<staff|student|hod>@<college_domain>'",
        )
        return render(request, "registration.html")

    username = email_id.split("@")[0].split(".")[0]

    if CustomUser.objects.filter(username=username).exists():
        messages.error(
            request,
            "User with this username already exists. Please use different username",
        )
        return render(request, "registration.html")

    user = CustomUser()
    user.username = username
    user.email = email_id
    user.password = password
    user.user_type = user_type
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    if user_type == CustomUser.STAFF:
        Staffs.objects.create(admin=user)
    elif user_type == CustomUser.STUDENT:
        Students.objects.create(admin=user)
    elif user_type == CustomUser.HOD:
        AdminHOD.objects.create(admin=user)
    return render(request, "login_page.html")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def get_user_type_from_email(email_id):
    """
    Returns CustomUser.user_type corresponding to the given email address
    email_id should be in following format:
    '<username>.<staff|student|hod>@<college_domain>'
    eg.: 'abhishek.staff@jecrc.com'
    """

    try:
        email_id = email_id.split("@")[0]
        email_user_type = email_id.split(".")[1]
        return CustomUser.EMAIL_TO_USER_TYPE_MAP[email_user_type]
    except:
        return None
