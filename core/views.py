from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from core.forms import CommentForm, LessonForm, ReplyForm
from core.models import Comment, Lesson, Standard, Subject, TimeSlots, WorkingDays

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


class StandardListView(ListView):
    context_object_name = "standards"
    model = Standard
    template_name = "curriculum/standard_list_view.html"


class SubjectListView(DetailView):
    context_object_name = "standards"
    extra_context = {"slots": TimeSlots.objects.all()}
    model = Standard
    template_name = "curriculum/subject_list_view.html"


class LessonListView(DetailView):
    context_object_name = "subjects"
    model = Subject
    template_name = "curriculum/lesson_list_view.html"


class LessonDetailView(DetailView, FormView):
    context_object_name = "lessons"
    model = Lesson
    template_name = "curriculum/lesson_detail_view.html"
    form_class = CommentForm
    second_form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        if "form" not in context:
            context["form"] = self.form_class(request=self.request)
        if "form2" not in context:
            context["form2"] = self.second_form_class(request=self.request)
        # context['comments'] = Comment.objects.filter(id=self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if "form" in request.POST:
            form_class = self.get_form_class()
            form_name = "form"
        else:
            form_class = self.second_form_class
            form_name = "form2"

        form = self.get_form(form_class)

        if form_name == "form" and form.is_valid():
            print("comment form is returned")
            return self.form_valid(form)
        elif form_name == "form2" and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.Standard
        subject = self.object.subject
        return reverse_lazy(
            "curriculum:lesson_detail",
            kwargs={
                "standard": standard.slug,
                "subject": subject.slug,
                "slug": self.object.slug,
            },
        )

    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.comments.name
        fm.lesson_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get("comment.id")
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


class LessonCreateView(CreateView):
    # fields = ('lesson_id','name','position','image','video','ppt','Notes')
    form_class = LessonForm
    context_object_name = "subject"
    model = Subject
    template_name = "curriculum/lesson_create.html"

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
        return reverse_lazy(
            "curriculum:lesson_list",
            kwargs={"standard": standard.slug, "slug": self.object.slug},
        )

    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.Standard = self.object.standard
        fm.subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


class LessonUpdateView(UpdateView):
    fields = ("name", "position", "video", "ppt", "Notes")
    model = Lesson
    template_name = "curriculum/lesson_update.html"
    context_object_name = "lessons"


class LessonDeleteView(DeleteView):
    model = Lesson
    context_object_name = "lessons"
    template_name = "curriculum/lesson_delete.html"

    def get_success_url(self):
        print(self.object)
        standard = self.object.Standard
        subject = self.object.subject
        return reverse_lazy(
            "curriculum:lesson_list",
            kwargs={"standard": standard.slug, "slug": subject.slug},
        )
