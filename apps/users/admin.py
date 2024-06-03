from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, StudentProfile, InstructorProfile

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'surname', 'is_active', 'is_staff', 'is_student', 'is_instructor', 'created_at')
    list_filter = ('is_staff', 'is_active', 'is_student', 'is_instructor')
    search_fields = ('email', 'name', 'surname')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'surname')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_student', 'is_instructor', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'surname', 'password1', 'password2', 'is_active', 'is_staff', 'is_student', 'is_instructor')}
        ),
    )
    readonly_fields = ('created_at', 'last_login', 'date_joined')

    def get_inlines(self, request, obj=None):
        if obj and obj.is_student:
            return [StudentProfileInline]
        elif obj and obj.is_instructor:
            return [InstructorProfileInline]
        return []

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = _('Student Profile')
    
    def has_add_permission(self, request, obj=None):
        if obj and obj.is_instructor:
            return False
        return True

class InstructorProfileInline(admin.StackedInline):
    model = InstructorProfile
    can_delete = False
    verbose_name_plural = _('Instructor Profile')

    def has_add_permission(self, request, obj=None):
        if obj and obj.is_student:
            return False
        return True

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'interests')
    search_fields = ('user__email', 'user__name', 'user__surname')

    def has_add_permission(self, request):
        return False

class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'headline', 'qualifications')
    search_fields = ('user__email', 'user__name', 'user__surname')

    def has_add_permission(self, request):
        return False


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(InstructorProfile, InstructorProfileAdmin)
