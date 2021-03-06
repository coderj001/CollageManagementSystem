from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import (
    AdminHOD,
    Courses,
    CustomUser,
    SessionYearModel,
    Staffs,
    Students,
)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:

        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(
                admin=instance,
                course_id=Courses.objects.get(id=1),
                session_year_id=SessionYearModel.objects.get(id=1),
                address="",
                profile_pic="",
                gender="",
            )


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()
