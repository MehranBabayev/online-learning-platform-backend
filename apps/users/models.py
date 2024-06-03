from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    name = models.CharField(_('Name'), max_length=100)
    surname = models.CharField(_('Surname'), max_length=100)
    email = models.EmailField(_('Email Address'), unique=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    is_student = models.BooleanField(_('Student'), default=False)
    is_instructor = models.BooleanField(_('Instructor'), default=False)
    is_active = models.BooleanField(_('active'), default=False)
    username = models.CharField(max_length=150, blank=True, null=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f'{self.name} {self.surname}'

class BaseProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(_('Profile Image'), upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(_('Bio'), blank=True)
    interests = models.TextField(_('Interests'), blank=True)

    class Meta:
        abstract = True
        verbose_name = _('Base Profile')
        verbose_name_plural = _('Base Profiles')

    def __str__(self):
        return str(self.user)

class StudentProfile(BaseProfile):
    class Meta:
        verbose_name = _('Student Profile')
        verbose_name_plural = _('Student Profiles')

class InstructorProfile(BaseProfile):
    headline = models.CharField(_('Headline'), max_length=100, blank=True)
    qualifications = models.TextField(_('Qualifications'), blank=True)

    class Meta:
        verbose_name = _('Instructor Profile')
        verbose_name_plural = _('Instructor Profiles')

