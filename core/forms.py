from django import forms

from core.models import Assigment, Courses, SessionYearModel


class DateInput(forms.DateInput):
    input_type = "date"


def course_list():
    # For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        print("here")
        course_list = []
    return course_list


def session_year_list():
    # For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (
                session_year.id,
                str(session_year.session_start_year)
                + " to "
                + str(session_year.session_end_year),
            )
            session_year_list.append(single_session_year)

    except:
        session_year_list = []

    return session_year_list


class AddStudentForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=50,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Password",
        max_length=50,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    username = forms.CharField(
        label="Username",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    address = forms.CharField(
        label="Address",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    gender_list = (("Male", "Male"), ("Female", "Female"))

    course_id = forms.ChoiceField(
        label="Course",
        choices=course_list,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    gender = forms.ChoiceField(
        label="Gender",
        choices=gender_list,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    session_year_id = forms.ChoiceField(
        label="Session Year",
        choices=session_year_list(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    profile_pic = forms.FileField(
        label="Profile Pic",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )


class EditStudentForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=50,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    username = forms.CharField(
        label="Username",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    address = forms.CharField(
        label="Address",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    gender_list = (("Male", "Male"), ("Female", "Female"))

    course_id = forms.ChoiceField(
        label="Course",
        choices=course_list(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    gender = forms.ChoiceField(
        label="Gender",
        choices=gender_list,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    session_year_id = forms.ChoiceField(
        label="Session Year",
        choices=session_year_list(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    profile_pic = forms.FileField(
        label="Profile Pic",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )


class AssigmentForm(forms.ModelForm):
    name = forms.CharField(
        label="Name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    question_paper = forms.FileField(
        label="Question Paper",
        required=True,
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )
    description = forms.CharField(
        label="Description",
        max_length=50,
        widget=forms.Textarea(attrs={"cols": 80, "rows": 5}),
    )

    class Meta:
        model = Assigment
        fields = ["name", "question_paper", "description"]
