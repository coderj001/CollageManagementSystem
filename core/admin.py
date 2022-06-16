# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import (
    AdminHOD,
    Attendance,
    AttendanceReport,
    Comment,
    Courses,
    CustomUser,
    FeedBackStaffs,
    FeedBackStudent,
    LeaveReportStaff,
    LeaveReportStudent,
    Lesson,
    NotificationStaffs,
    NotificationStudent,
    Reply,
    SlotSubject,
    Staffs,
    Students,
    Subjects,
    TimeSlots,
    WorkingDays,
    Subject,
    Standard
)


# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)

admin.site.register(AdminHOD)
admin.site.register(Staffs)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(Students)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportStudent)
admin.site.register(LeaveReportStaff)
admin.site.register(FeedBackStudent)
admin.site.register(FeedBackStaffs)
admin.site.register(NotificationStudent)
admin.site.register(NotificationStaffs)
admin.site.register(Lesson)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(WorkingDays)
admin.site.register(TimeSlots)
admin.site.register(SlotSubject)
admin.site.register(Standard)
admin.site.register(Subject)
