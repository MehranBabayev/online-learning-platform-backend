from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, StudentProfile, InstructorProfile

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            StudentProfile.objects.create(user=instance)
        elif instance.is_instructor:
            InstructorProfile.objects.create(user=instance)
    else:
        if instance.is_student:
            StudentProfile.objects.get_or_create(user=instance)
            InstructorProfile.objects.filter(user=instance).delete()
        elif instance.is_instructor:
            InstructorProfile.objects.get_or_create(user=instance)
            StudentProfile.objects.filter(user=instance).delete()

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_student and hasattr(instance, 'studentprofile'):
        instance.studentprofile.save()
    elif instance.is_instructor and hasattr(instance, 'instructorprofile'):
        instance.instructorprofile.save()
