import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()

    class Meta:
        verbose_name = _("SessionYearModel")
        verbose_name_plural = _("SessionYearModels")
        db_table = "session_year"


class CustomUser(AbstractUser):
    HOD = "1"
    STAFF = "2"
    STUDENT = "3"

    EMAIL_TO_USER_TYPE_MAP = {"hod": HOD, "staff": STAFF, "student": STUDENT}

    user_type_data = ((HOD, "HOD"), (STAFF, "Staff"), (STUDENT, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

    class Meta:
        verbose_name = _("CustomUser")
        verbose_name_plural = _("CustomUsers")
        db_table = "custom_user"


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _("AdminHOD")
        verbose_name_plural = _("AdminHOD")
        db_table = "admin_hod"


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _("Staff")
        verbose_name_plural = _("Staffs")
        db_table = "staff"


class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _("Courses")
        verbose_name_plural = _("Courses")
        db_table = "course"


class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)

    # need to give default course
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        db_table = "subject"


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default=1)
    session_year_id = models.ForeignKey(
        SessionYearModel, null=True, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")
        db_table = "student"


class Attendance(models.Model):

    # Subject Attendance
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")
        db_table = "attendance"


class AttendanceReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _("AttendanceReport")
        verbose_name_plural = _("AttendancesReports")
        db_table = "attendance_report"


class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _("LeaveReportStudent")
        verbose_name_plural = _("LeaveReportsStudent")
        db_table = "leave_report_student"


class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _("LeaveReportStaff")
        verbose_name_plural = _("LeaveReportsStaff")
        db_table = "leave_report_staff"


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _("FeedBackStudent")
        verbose_name_plural = _("FeedBackStudents")
        db_table = "feed_back_student"


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _("FeedBackStaff")
        verbose_name_plural = _("FeedBackStaffs")
        db_table = "feed_back_staff"


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _("NotificationStudent")
        verbose_name_plural = _("NotificationsStudent")
        db_table = "notification_student"


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    stafff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _("NotificationStaff")
        verbose_name_plural = _("NotificationsStaff")
        db_table = "notification_staff"


class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE, default=1)
    subject_exam_marks = models.FloatField(default=0)
    subject_assignment_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _("StudentResult")
        verbose_name_plural = _("StudentResults")
        db_table = "student_result"


# Create your models here.
class Standard(SessionYearModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def save_subject_image(instance, filename):
    upload_to = "Images/"
    ext = filename.split(".")[-1]
    # get filename
    if instance.subject_id:
        filename = "Subject_Pictures/{}.{}".format(instance.subject_id, ext)
    return os.path.join(upload_to, filename)


class Subject(Subjects):
    subject_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    standard = models.ForeignKey(
        Standard, on_delete=models.CASCADE, related_name="subjects"
    )
    image = models.ImageField(
        upload_to=save_subject_image, blank=True, verbose_name="Subject Image"
    )
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args, **kwargs)


def save_lesson_files(instance, filename):
    upload_to = "Images/"
    ext = filename.split(".")[-1]
    # get filename
    if instance.lesson_id:
        filename = "lesson_files/{}/{}.{}".format(
            instance.lesson_id, instance.lesson_id, ext
        )
        if os.path.exists(filename):
            new_name = str(instance.lesson_id) + str("1")
            filename = "lesson_images/{}/{}.{}".format(
                instance.lesson_id, new_name, ext
            )
    return os.path.join(upload_to, filename)


class Lesson(models.Model):
    lesson_id = models.CharField(max_length=100, unique=True)
    Standard = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(
        Subjects, on_delete=models.CASCADE, related_name="lessons"
    )
    name = models.CharField(max_length=250)
    position = models.PositiveSmallIntegerField(verbose_name="Chapter no.")
    slug = models.SlugField(null=True, blank=True)
    video = models.FileField(
        upload_to=save_lesson_files, verbose_name="Video", blank=True, null=True
    )
    ppt = models.FileField(
        upload_to=save_lesson_files, verbose_name="Presentations", blank=True
    )
    Notes = models.FileField(
        upload_to=save_lesson_files, verbose_name="Notes", blank=True
    )

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "curriculum:lesson_list",
            kwargs={"slug": self.subject.slug, "standard": self.Standard.slug},
        )


class WorkingDays(models.Model):
    standard = models.ForeignKey(
        SessionYearModel, on_delete=models.CASCADE, related_name="standard_days"
    )
    day = models.CharField(max_length=100)

    def __str__(self):
        return self.day


class TimeSlots(models.Model):
    standard = models.ForeignKey(
        SessionYearModel, on_delete=models.CASCADE, related_name="standard_time_slots"
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return str(self.start_time) + " - " + str(self.end_time)


class SlotSubject(models.Model):
    standard = models.ForeignKey(
        SessionYearModel, on_delete=models.CASCADE, related_name="standard_slots"
    )
    day = models.ForeignKey(
        WorkingDays, on_delete=models.CASCADE, related_name="standard_slots_days"
    )
    slot = models.ForeignKey(
        TimeSlots, on_delete=models.CASCADE, related_name="standard_slots_time"
    )
    slot_subject = models.ForeignKey(
        Subjects, on_delete=models.CASCADE, related_name="standard_slots_subject"
    )

    def __str__(self):
        return (
            str(self.standard)
            + " - "
            + str(self.day)
            + " - "
            + str(self.slot)
            + " - "
            + str(self.slot_subject)
        )


class Comment(models.Model):
    lesson_name = models.ForeignKey(
        Lesson, null=True, on_delete=models.CASCADE, related_name="comments"
    )
    comm_name = models.CharField(max_length=100, blank=True)
    # reply = models.ForeignKey("Comment", null=True, blank=True, on_delete=models.CASCADE,related_name='replies')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.comm_name = slugify(
            "comment by" + "-" + str(self.author) + str(self.date_added)
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ["-date_added"]


class Reply(models.Model):
    comment_name = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies"
    )
    reply_body = models.TextField(max_length=500)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "reply to " + str(self.comment_name.comm_name)
