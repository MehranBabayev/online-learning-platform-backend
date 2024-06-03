from django.db import models
from apps.users.models import CustomUser
from ckeditor.fields import RichTextField

class Category(models.Model):
    CATEGORY_TYPES = (
        ('CREATE', 'Create'),
        ('BUILD', 'Build'),
        ('THRIVE', 'Thrive'),
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category_type = models.CharField(max_length=50, choices=CATEGORY_TYPES)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_instructor': True}, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(CustomUser, related_name='enrolled_courses', blank=True, limit_choices_to={'is_student': True})

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = RichTextField(null=True)
    video_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title